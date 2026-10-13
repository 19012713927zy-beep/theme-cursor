# 来源与验证边界

本地流程从用户提供的烤妹儿 X 帖子及 kaomei/mouse-pointer-theme-maker v1.1.1 改编。
上游 commit：eea0c47790cdd19d54be5bb95a83efcd66fced30。
原帖：https://x.com/CrazyKaomei/status/2109523656942760036

真实先例为“英雄联盟 · 峡谷指尖小队”：
阿狸、拉克丝、金克丝、提莫、艾克、布里茨、亚索、娜美、艾希、蔚、锐雯、锤石。
12 张独立图稿，25 个主题 ID，加 4 个系统功能补充，共 29 个记录。
本机 Mousecape 1.2.0 实际应用后，逐条读回并核对尺寸、热点与可见像素；Empty 确认透明。
保留已有主题备份、用户的光标大小与登录启动设置。没有做注销/重登录测试。

这不是所有 macOS 版本兼容性的证明。每次运行仍检查 doctor 与真实系统。
此 Skill 的新通用脚本与初次手工制作代码不完全相同，独立回归结果记在 [validation-result.json](../validation-result.json) 中。通用脚本已复用十二张真实原稿完成构建、29 项真实部署、系统读回及 Mousecape 界面验收；八项回归通过。预览混用旧包、恢复不全和撤回后旧成功记录三个前向检查问题均已修正并复核。

维护脚本时可用一份已经校验的 cape 跑不写真实系统的回归：
```sh
<PY> <SKILL_DIR>/scripts/self_test.py --cape <已有成品.cape>
```
