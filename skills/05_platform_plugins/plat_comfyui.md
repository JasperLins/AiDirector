---
name: plat_comfyui
description: ComfyUI（Flux / Wan2.1 / ControlNet / LoRA）工作流提示词插件。当用户指定 ComfyUI 生图或生视频，或需要本地可控管线（PuLID/IP-Adapter/Redux、Wan 动态幅度）时触发。
when_to_use: 目标平台为 ComfyUI；锁脸批量出图、ControlNet 精控、模式B无声视频+后期对口型降本管线。
required_kbs: [KB_06_三视图与角色一致性, KB_09_错误修正与Negative_Prompt]
---

# ComfyUI 平台插件（PLAT-03）

## 平台语法特征（核实版）

1. **英文语义强**：生图 Prompt 建议中英双轨——中文版存档（人读），英文版喂模型（Flux/SD 系）；三视图用 KB_06 英文对照串。
2. **工作流即技法**（节点级参数，随 Prompt 一并交付）：
   - 生图：Flux + PuLID（0.6~0.8）/ IP-Adapter（0.5~0.7）/ Redux（参考重铺）；ControlNet Depth 0.5~0.7 / OpenPose 0.6~0.8 / Canny 0.5~0.7；LoRA 角色权重 0.6~0.85。
   - 生视频：Wan2.1 图生视频（首帧锚定）+ Fun Control 三分支（姿态/深度/边缘）官方工作流；动态幅度（Motion Strength）按镜头调——情绪戏 0.4~0.6、动作戏 0.7~0.9；Wan2.2-S2V 无限时长数字人。
3. **独立负向输入端**：挂 KB_09 三节标准负向包。
4. **模式B 标配**：Wan 生成无声视频 → LatentSync / 剪映对口型（基底闭嘴声明）。

## 输出格式（节点参数随行）

```
【工作流】Flux.1-dev + PuLID(flux) 0.7 + ControlNet-Depth 0.6
【正向（EN）】```prompt masterpiece, 1girl, ... ```
【正向（中文存档）】```prompt … ````
【负向】```prompt 多余手指, 六指, ... ```
【生视频附加】Motion Strength 0.5 ｜ 首帧=前置基准图 ｜ 无声输出（模式B，台词走 Fish Audio+LatentSync）
```

## 模板示例（B级降本镜头 · 模式B）

```prompt
A gentle mother in beige knit cardigan crouches smiling at her small son in blue bear-ear hoodie, dusk old street with food stall steam, soft warm golden light, over-shoulder shot, shallow depth of field -- 中文存档：米白开衫@李梅蹲身含笑望向天蓝卫衣@张三，黄昏@光大街边美食摊白雾，过肩景深虚化，嘴唇保持自然闭合或极轻微闭合微动（预留后期Lip-Sync口型合成干净基底），@画风锁+暖金橙主调
负向：多人张嘴, 口型开合, 手指畸形, 背景闪烁, 文字, 水印
节点：Flux.1-dev + IP-Adapter(@李梅立绘 0.6/@张三立绘 0.6) + Depth 0.6 ｜ 视频：Wan2.1 I2V，Motion 0.4（静态情绪），输出无声
```

## 正反例

✅ 正确：中英双轨 + 节点参数随行 + 负向包 + 模式B闭嘴声明。
❌ 错误：只给中文散文不给节点参数（ComfyUI 是工作流引擎，缺参数=无法复现）；模式B 忘写闭嘴基底（后期对口型重影，崩坏16）。
