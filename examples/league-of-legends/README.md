# 英雄联盟 · 峡谷指尖小队

12 位英雄、12 种动作；25 个主题映射及 4 个系统补充，共 29 条光标记录。

完整的图稿、热点、生成提示词和成品在 [v1.0.0 Release](https://github.com/19012713927zy-beep/theme-cursor/releases/tag/v1.0.0) 的 `league-of-legends-source.zip` 中。

下载并解压源码包后，在 macOS 和已安装依赖的 Python 环境中执行：

```sh
python skills/theme-cursor/scripts/cursor_theme.py build --brief /path/to/league-of-legends/brief.json
```

这里的 `brief.json` 使用相对路径，可与源码包中的 `source-art/` 一起搬到其他目录。每张图均保留实际生成提示词、源像素热点与目视验收结果。

演示视频展示预览页面中的英雄切换，不是系统鼠标操作录屏；成品曾在 Mousecape 1.2.0 中实际部署并通过逐条系统读回。
