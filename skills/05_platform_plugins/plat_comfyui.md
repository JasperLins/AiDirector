---
name: plat_comfyui
description: "WHAT：ComfyUI 专属插件——Flux 生图与 Wan2.1/2.2 生视频的工作流节点配置建议（PuLID/Redux 锁脸、ControlNet 预处理器与权重、LoRA 区间、采样器/步数/CFG）、结构化 Tag+自然语言混合语法与专属 Negative Prompt 模板。WHEN：用户指定 ComfyUI（Flux/Wan/SD系）生图或生视频，或需要本地可控管线、锁脸批量出图、模式B无声视频+后期对口型降本时触发。"
required_kbs: [KB_06_三视图与角色一致性, KB_09_错误修正与Negative_Prompt, KB_08_Prompt编译器]
input_schema: "输入：{VID-01/KB_08编译稿, 任务类型(生图/生视频I2V), 锁脸需求(单人多道具), ControlNet需求(姿态/景深/线稿), 显存预算, 口型模式(A禁用→B)}"
output_schema: "{工作流节点配置单(模型+锁脸+控制+采样段逐项参数), 正向EN(```prompt), 正向中文存档行, 负向模板(```prompt), 视频附加段(Motion/首帧/模式B闭嘴), 交付格式(双轨+参数随行)}"
---

# ComfyUI 平台插件（PLAT-03）· 工业级完整版

## 一、核心职责与工业级法则（6 条硬核铁律）

1. **中英双轨铁律**：Flux/SD/Wan 系英文语义强——交付必须双轨：`正向EN（喂模型）+ 中文存档行（人读与注册表对照）`；中文稿直接喂英文模型=语义损耗过半。
2. **节点参数随行铁律**：ComfyUI 是工作流引擎，Prompt 必须与节点配置单**同单交付**（锁脸节点+权重、ControlNet 预处理器+强度、LoRA 权重、采样器/步数/CFG、视频 Motion）——无参数的 Prompt 无法复现，等于没交付。
3. **负向独立铁律**：ComfyUI 保留独立负向输入端——负向模板必挂（4.4）；把负向内容写进正向自然语言（"不要六指"）反而注入概念激活。
4. **模式B闭嘴铁律**：Wan 生成对白镜一律无声输出+`嘴唇自然闭合或极轻微闭合微动（预留后期 Lip-Sync 干净基底）`；大嘴型+LatentSync=重影（崩坏16）。
5. **锁脸优先铁律**：已注册人物入画必挂锁脸件——角色 LoRA（0.6~0.85）> PuLID（0.6~0.8）> IP-Adapter（0.5~0.7，挂单人立绘/面部特写）；三视图整图禁止入参考位（多头怪）。
6. **显存预算铁律**：交付前核对显存档位（4.5 节降级链）；24G 满配、12G 降采样两段式、8G 以下建议转在线平台并在选型备注声明。

## 二、标准执行 SOP（Step-by-Step）

**Step 1 · 读入定件**：读编译稿+锁脸需求+ControlNet 需求+显存预算 → 按 IMG-01 路由结论确定节点件清单。

**Step 2 · 组配置单**：按 4.1/4.2 表逐项填节点参数（生图走 Flux 段，视频走 Wan 段），锁脸与控制件按铁律 5 与权重区间。

**Step 3 · 双轨编译**：正向 EN（Tag 前置+自然语言主体段，权重语法 `(tag:1.2)`）+ 中文存档行（@资产名保留原样——注册表对照用）。

**Step 4 · 挂负向**：按 4.4 模板裁剪（生图全量/视频全量+模式B条目）。

**Step 5 · 视频附加段**：首帧声明、Motion Strength 定档（情绪 0.4~0.6/常规 0.5~0.7/动作 0.7~0.9）、模式B闭嘴句、Wan2.2-S2V 特例（无限时长数字人）。

**Step 6 · 送检交付**：R7 评分（平台附加项：负向齐/双轨齐/参数齐）≥9.0 → 单据化交付。

## 三、结构化输入/输出契约模板

### 输入契约

| 字段 | 类型 | 必填 | 示例 |
|---|---|---|---|
| 编译稿 | text | 是 | KB_08/VID-01 |
| 任务类型 | enum | 是 | 生视频 I2V（模式B） |
| 锁脸/控制需求 | list | 是 | 双人锁脸+Depth |
| 显存预算 | enum | 是 | 24G |

### 输出契约（下游：用户载工作流 / R7）

```yaml
工作流节点配置单:
  生图段: {底模: "Flux.1-dev", 锁脸: "PuLID(flux) 0.7", 控制: "ControlNet-Depth 0.6(预处理器:MidasDepth)", LoRA: "角色LoRA×0(已有PuLID不双挂)", 采样: "euler + simple｜steps 24｜guidance 3.5", 分辨率: "1344×768(16:9)"}
  视频段: {模型: "Wan2.1-I2V-14B", 首帧: "前置基准图", Motion: "0.5(情绪戏)", 采样: "uni_pc｜steps 20｜cfg 5.0", 输出: "无声(模式B)"}
正向EN: "```prompt masterpiece, (1girl:1.2), beige knit cardigan …lips naturally closed …```"
中文存档: "-- 米白开衫@李梅过肩镜头…嘴唇自然闭合(模式B基底)…@画风锁"
负向模板: "```prompt …4.4裁剪版…```"
交付格式: "双轨+节点单同页；文件名含镜号与版本"
```

## 四、专项工具箱

### 4.1 Flux 生图工作流节点配置表（基线值）

| 节点段 | 推荐配置 | 参数区间 | 越界后果 |
|---|---|---|---|
| 底模 | Flux.1-dev（fp8 可省显存） | —— | —— |
| PuLID（锁脸） | PuLID(flux)，权重 0.7 | 0.6~0.8 | >0.8 表情锁死 |
| IP-Adapter | 面部特写参考 0.6 | 0.5~0.7 | >0.7 串风格 |
| Redux（参考重铺） | 参考图风格迁移 0.5 | 0.4~0.6 | >0.6 抄图 |
| ControlNet-OpenPose | 预处理器 DWPose，强度 0.7 | 0.6~0.8 | >0.8 肢体僵 |
| ControlNet-Depth | 预处理器 MidasDepth，0.6 | 0.5~0.7 | >0.7 画面糊 |
| ControlNet-Canny/Lineart | 预处理器 Canny，0.6 | 0.5~0.7 | >0.7 描边感 |
| LoRA | 角色专属 0.7 | 0.6~0.85 | >0.9 塑胶脸 |
| 采样器 | euler + simple | flux guidance 3.0~4.0 | guidance>5 过饱和 |
| 步数 | 24 | 20~28 | >30 边际极小 |
| SDXL 旧管线备选 | DPM++ 2M Karras，steps 28，CFG 6 | CFG 5~7 | CFG>7 油画感 |

### 4.2 Wan2.1/2.2 生视频节点配置表

| 节点段 | 推荐配置 | 区间 | 说明 |
|---|---|---|---|
| 模型 | Wan2.1-I2V-14B（首帧锚定） | —— | T2V 仅空镜用 |
| Fun Control 三分支 | 姿态/深度/边缘引导视频 | 单支起步 | 官方工作流，多支各×0.7 |
| Motion Strength | 情绪 0.5 | 0.4~0.6 | 静态表情戏 |
| Motion Strength | 常规 0.6 | 0.5~0.7 | 行走交互 |
| Motion Strength | 动作 0.8 | 0.7~0.9 | 打斗（配合首尾帧思路） |
| 采样 | uni_pc，steps 20，cfg 5.0 | steps 20~30 / cfg 5~6 | cfg>6 运动过冲 |
| 帧率/时长 | 16fps × 5s = 80 帧 | ≤5s/条 | 长镜走接力 |
| Wan2.2-S2V | 数字人无限时长口播 | —— | 模式B口播特化 |
| 输出 | 无声 + 闭嘴基底 | —— | 后期 LatentSync/剪映对口型 |

### 4.3 结构化 Tag + 自然语言混合语法

```text
正向EN结构 = [质量Tag: masterpiece, best quality, 8k] + [主体Tag(带权重): (1girl:1.2), black high ponytail] +
           [自然语言段: a young sword cultivator stands center of stone arena, robe hem lifted by wind…] +
           [光学/构图Tag: cinematic lighting, low angle] + [@画风锁中文行原样保留于存档行]
权重语法：(tag:1.2) 强化 / (tag:0.8) 弱化；Tag 在前抢注意力，自然语言在后管语义连贯。
```

### 4.4 专属 Negative Prompt 模板（裁剪用母版）

**生图母版**：
```prompt
多余手指, 六指, 手指粘连, 面部扭曲, 五官移位, 高光过曝, 硬阴影, 透视畸变, 双人融合, 三个相同人物, 复制人, 文字, 乱码, 水印, 签名, 低分辨率, 模糊, 噪点, 肢体比例错误, 畸形, 过饱和, 卡通辱画风
```
**生视频母版（+模式B条目）**：
```prompt
镜头切换, 机位跳切, 人物瞬移, 全员张嘴, 多人张嘴, 口型大开, 身份漂移, 肢体穿模, 手指畸形, 背景闪烁, 拖影, 鬼影, 色彩断层, 画面撕裂, 文字出现, 水印
```

## 五、常见错误示范 vs 满分工业级示范

### 对比组 1：无参数交付

❌ **Bad Case**：
> ComfyUI 提示词：一个穿黑衣服的长发剑客站在台子上，风吹起衣角，电影感，高清。（就这些，节点自己看着配）

**扣分点**：纯中文喂英文模型（语义损耗）；无节点配置单（无法复现）；无锁脸件（人物即兴）；无负向；"电影感高清"空洞——违反铁律 1/2/3/5。

✅ **Good Case**：
> 节点单：`Flux.1-dev + PuLID(flux)0.7(@林烬面部特写) + Depth 0.6(MidasDepth) ｜ euler+simple, steps 24, guidance 3.5 ｜ 1344×768`；正向EN：`masterpiece, (1boy:1.2), black outfit, high ponytail, a young sword cultivator stands center of stone arena, robe hem and loose strands lifted by wind force…`；负向母版全挂；中文存档行含 `@林烬…@画风锁`。——单据化可复现交付。

### 对比组 2：模式B口型

❌ **Bad Case**：
> Wan 视频：@李梅情绪饱满地大声说话，嘴型夸张开合，台词激昂，生成后我再用对口型软件配音。

**扣分点**：模式B写"嘴型夸张开合"——LatentSync 后期对口型与原视频大嘴型重影打架（崩坏16 一票否决）。

✅ **Good Case**：
> Wan 无声输出 + `lips naturally closed or near-closed micro movement (clean base for post lip-sync)`；微表情链保留（eye smile→gaze lowers→lash flutter）；台词按 NARR-03 控制符串由 Fish Audio 克隆 → LatentSync/剪映对口型 → 音画 ±2 帧微调。

## 六、边界情况处理（Edge Cases）

1. **显存不足（<16G）**：降级链——fp8 底模 → 分辨率降档（1024 级）→ Tiled VAE 分块解码 → 视频换 Wan2.1-1.3B 草稿迭代+单帧高清；8G 以下建议整任务转在线平台并备注。
2. **双参考打架（双人物锁脸失衡）**：双 IP-Adapter 各 0.6 起步；一人不像→该位换面部特写；仍打架→Depth 0.6 钉纵深+单 PuLID 只锁主角，配角靠分区句式。
3. **Wan 输出抖动（高频微震）**：Motion 降 0.1 档；fps 帧率补齐（16→24 补帧）；仍抖→剪辑段用剪映「智能补帧」+稳定（R8 流程）并复盘归档。
4. **批量出图（同角色多镜）**：固定种子区间+批量 Prompt 队列（JSON 清单）；每批抽 20% 人工抽检锁脸；注册表摘要词全程逐字复用。
5. **Flux guidance 过曝**：guidance 降到 3.0~3.5；高光区仍爆→正向加 `soft highlight rolloff`，负向加 `overexposed`。
6. **英文 Tag 与中文 @资产共存需求**：喂模型用 EN；@资产名只活在中文存档行与素材命名（文件名=镜号_@资产_版本）——保证批量脚本按名归档不错位。
