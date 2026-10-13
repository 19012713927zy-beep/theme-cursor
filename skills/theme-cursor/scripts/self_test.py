#!/usr/bin/env python3
"""Regression checks using an existing cape; all deployment effects are mocked."""
import argparse, copy, hashlib, json, plistlib, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import cursor_theme as m

FIXTURE=None
class PipelineChecks(unittest.TestCase):
    def setUp(self): self.cape=m.load_cape(FIXTURE)
    def test_visible_empty_rejected(self):
        broken=copy.deepcopy(self.cape)
        broken['Cursors'][m.EMPTY]=copy.deepcopy(broken['Cursors'][m.IDS['normal']])
        with self.assertRaisesRegex(ValueError,'Empty must be fully transparent'):m.validate_payload(broken)
    def test_hotspot_difference_detected(self):
        actual=copy.deepcopy(self.cape);actual['Cursors'][m.IDS['normal']]['HotSpotX']+=1
        with self.assertRaisesRegex(ValueError,'HotSpotX differs'):m.compare_capes(self.cape,actual)
    def test_visible_art_difference_detected(self):
        actual=copy.deepcopy(self.cape)
        actual['Cursors'][m.IDS['normal']]['Representations']=actual['Cursors'][m.IDS['text']]['Representations']
        with self.assertRaisesRegex(ValueError,'visible pixels differ'):m.compare_capes(self.cape,actual)
    def transaction_case(self,mode):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);library=root/'library';library.mkdir()
            wanted=copy.deepcopy(self.cape);wanted['Identifier']='local.cursor.regression'
            cape=root/'theme.cape';cape.write_bytes(plistlib.dumps(wanted))
            previous=copy.deepcopy(wanted);previous['Cursors'][m.IDS['normal']]['HotSpotX']+=1
            target=library/'local.cursor.regression.cape';old_bytes=plistlib.dumps(previous);target.write_bytes(old_bytes)
            initial={'MCAppliedCursor':'local.cursor.regression','lastAppliedCapeIdentifier':'local.cursor.regression',
              'capeListOrder':['local.cursor.older','local.cursor.regression'],'MCCursorScale':1.3,'launchAtLogin':True}
            prefs=copy.deepcopy(initial);active=copy.deepcopy(previous);live_scale=1.3;calls=[]
            def getprefs():return copy.deepcopy(prefs)
            def setpref(key,value):
                if value is None:prefs.pop(key,None)
                else:prefs[key]=copy.deepcopy(value)
            def fakecli(app,args,log):
                nonlocal active,live_scale
                calls.append([str(a) for a in args]);Path(log).parent.mkdir(parents=True,exist_ok=True)
                if args[0]=='scale':
                    if len(args)>1:live_scale=float(args[1]);prefs['MCCursorScale']=live_scale
                    message=str(live_scale)
                elif args[0]=='dump':
                    Path(args[1]).write_bytes(plistlib.dumps(active));message='dumped'
                elif Path(args[1]).name=='restore-system.cape':
                    active=m.load_cape(args[1]);prefs['MCAppliedCursor']=active['Identifier']
                    message=f"Successfully applied: {len(active['Cursors'])}\nFailed: 0"
                else:
                    if mode!='no-op':
                        active=copy.deepcopy(wanted);prefs['MCAppliedCursor']=wanted['Identifier']
                    if mode=='settings':
                        live_scale=2.0;prefs['MCCursorScale']=2.0;prefs['launchAtLogin']=False
                    message=f"Successfully applied: {len(wanted['Cursors'])}\nFailed: 0"
                Path(log).write_text(message);return message
            with patch.object(m,'LIBRARY',library),patch.object(m,'preferences',getprefs),patch.object(m,'set_preference',setpref),patch.object(m,'run_cli',fakecli),patch.object(m,'doctor',return_value={'platform':'Darwin','cli_available':True,'bundle_identifier':m.DOMAIN,'preferences':prefs}):
                if mode=='success':
                    deployed=m.deploy(cape);self.assertTrue(deployed['applied'])
                    m.restore_transaction(deployed['transaction'])
                    report=m.read_json(root/'deployment-verification.json')
                    self.assertFalse(report['applied']);self.assertTrue(report['rolled_back'])
                    m.write_json(root/'build-verification.json',{'preview_only':False,'cape_sha256':hashlib.sha256(cape.read_bytes()).hexdigest()})
                    (root/'preview.png').write_bytes(wanted['Cursors'][m.IDS['normal']]['Representations'][-1])
                    self.assertFalse(m.package(root)['applied_verified'])
                else:
                    with self.assertRaisesRegex(RuntimeError,'prior system snapshot was restored'):m.deploy(cape)
            self.assertEqual(target.read_bytes(),old_bytes);self.assertEqual(prefs,initial)
            self.assertEqual(active,previous);self.assertEqual(live_scale,1.3)
            transactions=list((root/'deployments').glob('*/transaction.json'));self.assertEqual(len(transactions),1)
            self.assertTrue(m.read_json(transactions[0])['rolled_back'])
            self.assertTrue(any(c[0]=='apply' and c[1].endswith('restore-system.cape') for c in calls))
    def test_false_success_triggers_verified_restore(self):self.transaction_case('no-op')
    def test_settings_and_runtime_scale_restored(self):self.transaction_case('settings')
    def test_success_then_rollback_invalidates_applied_status(self):self.transaction_case('success')
    def test_preview_only_rejects_stale_install_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);m.init_project('测试主题',root)
            self.assertEqual(len(m.read_json(root/'brief.json')['artworks']),12)
            with self.assertRaisesRegex(ValueError,'mark PASS first'):m.build(root/'brief.json',preview_only=True)
            self.assertFalse((root/'theme.cape').exists())
            (root/'theme.cape').write_bytes(plistlib.dumps(self.cape))
            m.write_json(root/'build-verification.json',{'preview_only':True})
            with self.assertRaisesRegex(ValueError,'preview-only'):m.package(root)
            with self.assertRaisesRegex(ValueError,'preview-only'):m.deploy(root/'theme.cape',dry_run=True)
    def test_changed_cape_requires_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'theme.cape').write_bytes(plistlib.dumps(self.cape))
            m.write_json(root/'build-verification.json',{'preview_only':False,'cape_sha256':'old hash'})
            with self.assertRaisesRegex(ValueError,'differs from latest build'):m.package(root)
            with self.assertRaisesRegex(ValueError,'differs from latest build'):m.deploy(root/'theme.cape',dry_run=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cape',type=Path,required=True);args=p.parse_args()
    FIXTURE=args.cape;m.validate_payload(m.load_cape(FIXTURE))
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PipelineChecks))
    raise SystemExit(0 if result.wasSuccessful() else 1)
