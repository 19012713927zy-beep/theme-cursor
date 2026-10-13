# brief.json

init 创建十二状态骨架。用户只需主题，agent 填写制作信息，无需用户手写 JSON。

```json
{
  "theme": {
    "name": "主题 · 指尖小队",
    "identifier": "local.cursor.theme-unique",
    "author": "自定义",
    "version": 1,
    "platform": "macos",
    "preview_style": "chibi-anime",
    "preview_title": "主题 · 指尖小队",
    "preview_subtitle": "十二种动作，把主题带到指尖。",
    "preview_footer": "主题预览 / 热点已校准"
  },
  "generation": {"provider": "built-in image_gen", "model": null},
  "artworks": {
    "normal": {
      "source": "source-art/normal.png",
      "source_hotspot": [108, 130],
      "character_name": "角色名",
      "prompt": "实际使用的生图提示词",
      "review": "PASS"
    }
  }
}
```

示例只有 normal；实际至少包含 normal、text、action、forbidden。默认含 12 种状态。可以通过 init --states 指定逗号分隔列表，或编辑 artworks。脚本只接受已定义的状态，不能用人名代替 state。

source 可为绝对路径，也可相对 brief.json。source_hotspot 是原始 PNG 像素坐标，不是最终 32px 坐标，不是画布中心的默认值。源图必须有真实透明通道，最短边至少 320px。

生成状态存在独立原稿、动作经过检查后再标 PASS。可额外记录 tool_output_path、repair_count、身份参考来源、版本等。模型未向工具公开时保持 model: null，不猜名称。

使用现有图稿重建时，保留真实提示词与来源；不要伪称此次重新生图。编译后的 artwork-manifest.json 是输出，不要把它当输入 brief。

build 自动生成：
- normalized 与 retina：标准化图稿和 4 档密度。
- preview.png 与 size-check.png：完整预览和深浅底真实尺寸。
- theme.cape：全部主题记录与补充系统记录（preview-only 不新建）。
- build-verification.json：原图哈希、边界、源热点和结果热点。
- system-fallbacks/source-record.json：本机系统 PDF / 透明图来源。

系统行为：
- 普通箭头、文本、链接、等待、准星、双向窗边与相应对角窗角可以复用。
- 不用横/竖图代替对角缩放；不把张手当闭手、相机、放大镜或帮助。
- Empty 总是全透明。
- copy、alias、move 未独立绘制时补入本机系统资源；已绘制时用指定角色图案。避免旧主题备份中的人物图残留。
