---
name: theme-cursor
description: 按主题、角色或参考图生成整套 macOS 鼠标皮肤，并直接部署到本机 Mousecape。用于“做一套某主题鼠标”“把某角色变成光标”“扩展这套鼠标角色”等请求；调用本 Skill 后只需给主题。包含独立透明生图、热点校准、Retina 打包、旧主题残留处理、系统读回验收与失败恢复。
metadata:
  short-description: 给一个主题，生成并部署可直接使用的鼠标皮肤
---

# 主题鼠标 · 生成并部署

交付能实际使用的系统鼠标皮肤，而非只有预览图。默认 macOS、Q 版二次元、12 种动作、完成后直接部署。用户明确说“只预览”“先让我确认”时遵守当次要求。

## 触发与默认决策

- 已调用本 Skill 或上下文已在制作鼠标时，单独一个主题就是完整输入。不要为平台、风格、角色名单重复发问。本机平台可检查；其他细节合理默认后简短说明。
- 不把无关对话里的角色名自动理解成切换系统主题。用户的当前指令优先。
- 多角色 IP 选 12 位有辨识度、适合动作的角色；单角色用同一角色的 12 种不同动作；抽象主题用统一视觉母题。用户给出数量、名单或风格时相应调整。
- 默认角色数不等于覆盖所有系统 ID；只复用语义等价的映射。需要更多角色时先增加具有独立功能的状态，见 [角色与状态](references/art-direction.md)。
- 当前脚本只实现 macOS。用户明确要 Windows 时说明需另做 Windows 适配，不把 .cape 当成 Windows 安装包。
- 不要求逐张确认，也不继承上游“必须确认预览后才能打包”的固定审批。这里的用户调用目标就是生成并部署；必要的系统授权仍按实际工具规则处理。

## 1. 检查能力与初始化

先读 [运行与部署](references/runtime.md)。用可用的 Python 运行：

```sh
<PY> <SKILL_DIR>/scripts/cursor_theme.py doctor
<PY> <SKILL_DIR>/scripts/cursor_theme.py init --theme "<主题>" --out "<输出目录>"
```

`<SKILL_DIR>` 是本文件所在目录；路径有空格时正确引用。输出放当前任务的 `outputs/` 下独立目录，不放进 Skill。检查真实 image_gen 工具、Mousecape CLI、Pillow 和 pypdfium2；缺少库优先使用 Codex 自带运行环境。缺少 Mousecape 时走官方安装路径，不打包第三方应用。

初始化产生 `brief.json`。按 [输入格式](references/manifest.md) 填角色、动作和实际生成记录。复用已经验收的状态，单独补画新增或失败状态；同一主题修订保留 identifier，不同主题用不同 identifier。

## 2. 分状态生成

读 [角色与状态](references/art-direction.md)，并遵守当前 imagegen Skill / 工具说明。

先生成 `normal`，检查实际图像后作为画风参考。其余状态一张一调用，保持角色与功能图案真实交互，不从一张拼图切片、不用代码画角色、不把人物头像贴到系统箭头旁。输出真正透明的高清 PNG。按工具能力顺序生成；不擅自并行。

每张检查角色、动作、方向、四边完整、透明度及缩小后的辨识度。精确找到源图上的功能热点，记录源像素坐标。将实际提示词、路径、角色名写入 brief；只有目视通过才写 `review: PASS`。最多两次针对性修图；仍不合格就明确失败状态，不部署半套或冒充完成。

## 3. 制作并检查成品

```sh
<PY> <SKILL_DIR>/scripts/cursor_theme.py build --brief "<输出目录>/brief.json"
```

脚本将透明原图对齐到 1024 画布，从高清源直接导出 32/64/160/320 px，生成热点预览、实际尺寸检查图和 `theme.cape`。它只清理极低 alpha 噪点、变换坐标和采样，不补画缺失身体或箭头。

用 `view_image` 查看 `preview.png` 和 `size-check.png`；大预览通过不代表小光标能看清。检查十字是否位于箭头尖、文字轴中心、指尖或功能符号中心。十字仅在预览图，不写入鼠标。方向或裁切有误时修该源图再构建。

仅预览模式使用 `build --preview-only`，不调用部署。正常模式展示预览并继续，无需等新的同意词。

## 4. 部署与验收

```sh
<PY> <SKILL_DIR>/scripts/cursor_theme.py deploy --cape "<输出目录>/theme.cape"
```

部署脚本：
- 保存当前主题选择、已有同 ID 文件和系统快照。
- 原子保存到 Mousecape 主题库，用官方 mousecloak 应用。
- 读回每一个系统光标，核对热点、尺寸、白底/黑底像素及 Empty 全透明。
- 保留大小与登录启动设置，保存持久选择；失败则尝试恢复快照，并报告恢复是否成功。

不要把 CLI 返回 0 或“已应用”提示单独当成完成。新版兼容问题读 [运行与部署](references/runtime.md)，不要临时编译私有 API 工具冒险清注册。

然后通过原生应用工具查看 Mousecape 中本主题的“已应用”及图案。CLI 写入后列表未刷新，按文档刷新应用。界面检查通过后，把真实结果记到 `deployment-verification.json` 的 `ui_verified` 与 `ui_evidence`，不得预填。有工具阻塞则报告“系统读回通过，界面未验收”。

## 5. 交付

仅预览模式直接交付 preview.png 与 size-check.png，跳过本节安装包命令。旧目录里可能还保留历史 cape，不能拿它配新预览交付。

```sh
<PY> <SKILL_DIR>/scripts/cursor_theme.py package --project "<输出目录>"
```

最终简短说明：已生成多少种动作、是否已应用、真实验收结果；给预览和安装包的绝对路径链接，以及切回原主题的方法。不要把“登录启动设置为开”说成已验证重登录；不要声称所有应用自绘鼠标也会被替换。

制作事实保存在输出目录：brief、原稿、Retina、预览、构建记录、部署记录和快照。只清理自己的无用临时文件，保留恢复所需文件。

## 来源

本 Skill 是从一次真实的英雄联盟 12 角色制作与部署中抽出的本地改进版。部分预览排版借鉴 [mouse-pointer-theme-maker](https://github.com/kaomei/mouse-pointer-theme-maker) 1.1.1，MIT 许可见 [LICENSE](LICENSE)。没有沿用上游 51 ID 无差别复用规则。设计与历史依据见 [验证记录](references/validation.md)。
