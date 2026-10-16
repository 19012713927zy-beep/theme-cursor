# Theme Cursor · 一句话做一套主题鼠标

给 Codex 一个主题，生成整套有角色、有动作、能直接使用的 **macOS 鼠标皮肤**。

从独立透明图稿、热点校准、Retina 输出，到 Mousecape 安装、系统读回和失败恢复，都整理成了一个可复用的 Skill。

## 主题预览

### 英雄联盟 · 峡谷指尖小队

![英雄联盟 · 峡谷指尖小队，12 位英雄对应 12 种光标动作](docs/preview.jpg)

[▶ 观看 25 秒效果演示](https://github.com/19012713927zy-beep/theme-cursor/releases/download/v1.0.0/league-of-legends-demo.mp4) · [下载英雄联盟成品](https://github.com/19012713927zy-beep/theme-cursor/releases/download/v1.0.0/league-of-legends-macos.zip) · [下载 Skill](https://github.com/19012713927zy-beep/theme-cursor/releases/download/v1.0.0/theme-cursor-skill-v1.0.0.zip)

### 瓦罗兰特 · 特工指尖小队

![瓦罗兰特 · 特工指尖小队，12 位特工对应 12 种光标动作](docs/valorant-preview.jpg)

### 三角洲行动 · 人气皮肤指尖小队

![三角洲行动 · 人气皮肤指尖小队，包含蜂医原皮、威龙凌霄戍卫、蝶原皮和蛊的女医皮肤](docs/delta-force-preview.jpg)

### 王者荣耀 · 人气女英雄皮肤小队

![王者荣耀 · 人气女英雄皮肤小队，12 位女英雄的精选皮肤对应 12 种光标动作](docs/honor-of-kings-preview.jpg)

## 直接用英雄联盟成品

1. 从 [Mousecape 官方项目](https://github.com/sdmj76/Mousecape-swiftUI/releases) 安装 Mousecape。
2. 下载上面的成品包，解压，在 Mousecape 中导入 `league-of-legends.cape` 并应用。
3. 想切回去时，在 Mousecape 中重新应用原来的主题或恢复默认。

成品包含阿狸、拉克丝、金克丝、提莫、艾克、布里茨、亚索、娜美、艾希、蔚、锐雯、锤石。涵盖普通选择、文本、链接、禁止、等待、抓取、精准选择以及四种缩放方向。

## 安装 Skill，以后只给主题

下载 Skill ZIP，把其中的 `theme-cursor` 文件夹放到 `~/.codex/skills/`，然后新开 Codex 对话。已有同名 Skill 时，先备份旧文件夹再替换。

也可以克隆本仓库：

```sh
git clone https://github.com/19012713927zy-beep/theme-cursor.git
cd theme-cursor
mkdir -p ~/.codex/skills
# 目标文件夹不存在时执行；已有安装请先备份。
cp -R skills/theme-cursor ~/.codex/skills/
```

在 Codex 中说：

```text
用 $theme-cursor 做一套宝可梦主题鼠标，生成后直接部署。
```

调用后，下一次可以直接给主题，例如：

```text
吉卜力森林风格
```

默认采用 Q 版风格和 12 种动作。多角色主题分配不同角色，单角色主题设计不同姿势；也可以指定角色或说“只生成预览”。需要 Codex 当前会话具有图像生成工具和本机操作能力；普通聊天界面不能仅靠这份文档完成安装。

## 环境与构建

- **macOS**；当前部署脚本适配 `com.sdmj76.Mousecape` 和其 `mousecloak` CLI。
- Python **3.10+**、Pillow、pypdfium2。
- Codex 中可用的 `image_gen` 用于生成透明图稿；构建脚本本身不调用图像生成 API。

手动准备 Python 环境：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python skills/theme-cursor/scripts/cursor_theme.py doctor
```

[完整流程](skills/theme-cursor/SKILL.md) · [部署与恢复](skills/theme-cursor/references/runtime.md) · [输入格式](skills/theme-cursor/references/manifest.md) · [角色与动作设计](skills/theme-cursor/references/art-direction.md)

英雄联盟示例的 [brief.json](examples/league-of-legends/brief.json) 保留了每张图的提示词、角色、原始热点和相对路径。[完整图稿与交互预览源码](https://github.com/19012713927zy-beep/theme-cursor/releases/download/v1.0.0/league-of-legends-source.zip) 单独下载，解压后可以重建成品。

## 做了哪些优化

- 每种状态独立生成透明 PNG，让角色真正参与点击、抓取或缩放动作。
- 从高清原稿直接输出 32 / 64 / 160 / 320 px，逐张检查热点与小尺寸辨识度。
- 按功能语义映射光标；英雄联盟示例含 25 个主题映射和 4 个系统补充，共 29 条记录。
- 部署前保存旧主题与设置，部署后逐条读回尺寸、热点和图像；失败时尝试恢复并报告结果。
- 安装选择持久保存，保留已有鼠标大小与登录启动设置。

## 验证与限制

英雄联盟成品已在一台 Mac 的 Mousecape 1.2.0 中实际应用，29 条光标通过系统读回，Mousecape 界面通过验收。通用脚本通过 8 项回归，覆盖图像不一致、热点错误、部署失败恢复及旧安装包误用等情况。

```sh
# 将下载成品解压后，使用其中的 cape；该回归不会改写真实系统设置。
python skills/theme-cursor/scripts/self_test.py --cape /path/to/league-of-legends.cape
```

当前仅实现 macOS；未验证所有系统版本，也未做注销后重新登录测试。应用自己绘制的光标不一定被替换。演示视频是预览页面的英雄切换展示，不是系统鼠标操作录屏。

## 来源与许可

灵感来自 [烤妹儿的演示帖](https://x.com/CrazyKaomei/status/2109523656942760036)，部分预览排版参考 [mouse-pointer-theme-maker](https://github.com/kaomei/mouse-pointer-theme-maker)。代码与文档采用 [MIT](LICENSE)，保留上游署名。

英雄联盟示例为 AI 生成的同人图稿，第三方角色、商标及系统原生素材不属于本项目 MIT 授权范围。详细来源见 [NOTICE.md](NOTICE.md)。
