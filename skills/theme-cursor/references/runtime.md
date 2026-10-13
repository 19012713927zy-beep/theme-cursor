# 运行、部署和恢复

## 运行环境

先执行 doctor，检查 Python、Pillow、pypdfium2、Mousecape 应用与 CLI。当前验证过的机器使用 Mousecape 1.2.0，bundle id 为 com.sdmj76.Mousecape；不要把这当成永远不变。

本机 Python 若缺库，调用 load_workspace_dependencies 获取 Codex 当前 bundled Python，再用返回的绝对路径运行 doctor。不要凭旧缓存路径认定可用，也不要为这一套流程污染系统 Python。若 bundled 环境也缺库，可在任务目录建立独立 venv 并安装必要的 Pillow / pypdfium2。

生图必须使用实际可用的 image_gen。没有工具就报告缺少能力，保留 brief 与已有资产，不用脚本画图或把生图提示词交付为图片。不要自行切换到需要密钥的付费提供商。

## Mousecape

默认应用 /Applications/Mousecape.app；CLI 在 Contents/MacOS/mousecloak。
doctor 为只读；deploy --dry-run 验证包和本地前提，不应用。

缺少应用时检查 [官方 Mousecape SwiftUI 发布页](https://github.com/sdmj76/Mousecape-swiftUI/releases) 的兼容版本，再按平台要求安装。不要从主题附件下载不明二进制，不把应用放入主题包。若要求同意条款、额外授权或系统阻止打开，说明具体屏幕/工具原因并遵守对应授权边界，不绕过安全拦截。

脚本通过 CLI 应用和读回，使用当前用户主题库：
~/Library/Application Support/Mousecape/capes/<identifier>.cape

通过当前用户 defaults 更新持久选择和列表顺序，不改大小或启动项。不要求管理员权限。app 版本变更造成路径、CLI、偏好域不一致时，应停在 doctor 并适配真实接口，不向未知位置写。

## 真实验收

mousecloak apply 有过“退出码 0 不等于所有记录成功”的表现。脚本同时检查可用的日志统计，并从系统 dump 后逐条验证：
- 标识存在；帧数、热点和逻辑尺寸匹配。
- 四种图像密度匹配。
- 合成到白底和黑底后，像素 RMS 均小于 3；避免透明 RGB 和导入编码的轻微差异造成误报。
- Empty alpha 的包围盒必须为空。

系统读回可能为 TIFF，安装包为 PNG；不要直接用编码哈希比较两种图。最终记录包含包哈希，改包后原部署记录失效。

还要在原生 Mousecape 界面看到目标主题“已应用”。只用当前允许的原生应用工具进行 UI 操作。若 CLI 新增的文件未刷新，可正常退出并重新打开 Mousecape，再检查；不要点击旧缓存记录重新覆盖新包。文件选择框先读状态，再给 PathTextField setValue 并读回，避免快速快捷键和粘贴竞态误选旧文件。

脚本不会伪造 UI 验收。确认后向输出记录增加：
```json
{"ui_verified": true, "ui_evidence": "Mousecape 界面显示目标主题名称及已应用"}
```
这只是事实记录，不是待确认的自动勾选项。

## 旧主题残留

本次历史观察：旧主题曾将 Empty 设为可见人物；reset 仍可能从已污染的备份恢复旧图。单看 GUI 成功会漏掉问题。流程现在显式提供透明 Empty，以及 copy / alias / move 的功能记录。没有自定义图稿时，从本机 HIServices 的 cursor.pdf 与 info.plist 读取图案和热点。

系统资源目录：
/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/HIServices.framework/Versions/A/Resources/cursors

这四项是针对本机 Mousecape 状态管理的兼容处理；不意味着所有操作系统或所有版本都有同样问题。不要复制整个旧 .cape 的非主题图案做 fallback，也不要编译私有 CGS 清除程序；跨进程清注册尝试曾返回 1000，未解决问题。

## 失败与恢复

deploy 在每次写入前保存：
- before-system.cape：此前实际系统记录；
- before_preferences：此前主题选择、顺序、大小、登录启动；
- previous-installed.cape：若目标 ID 原已存在，其原文件；
- apply/dump 日志。

保存位置在该项目 deployments/<时间与随机码>/。应用或验证失败时自动尝试回放快照、核对系统读回，再恢复保存的偏好和实际运行中的缩放，读回检查后才记为已恢复。恢复也失败时明确报告两个错误和路径，停止继续写入，不无限重试。

预览模式不会新建安装文件。历史 cape 可以保留，但最新构建是 preview-only 时 deploy/package 必须拒绝使用它。安装包和部署前都校验构建记录内的 cape 哈希。撤回会失效对应部署报告，历史成功不代表当前仍已应用。

用户以后要求撤回时：
```sh
<PY> <SKILL_DIR>/scripts/cursor_theme.py rollback --transaction "<部署事务目录>"
```
只为用户明确的恢复请求执行。创建 Skill 时，故障恢复测试用临时目录和模拟接口，不主动切换真实系统主题。

同名主题的修订不会删除原稿和恢复文件。只删除本轮确定无用的临时目录/编译物；保留活跃主题库和 deployments。
