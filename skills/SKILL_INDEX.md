# SKILL_INDEX.md — 全局技能插件路由索引表

> 本索引是 `skills/` 目录的唯一路由入口（仿 anthropics/skills 按需加载规范）。
> **使用规则**：总控（AGENTS.md）根据任务匹配下表 `WHEN 触发条件`，**只提取读取命中的 Skill 文件本体**，未命中的不读取，以节省上下文 Token。
> 平台插件（05 类）互斥加载：一次任务最多激活一个 `plat_*`；未指定平台时激活 `plat_00`。

---

## 01 叙事编剧类（narrative）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| NARR-01 市场钩子调研 | `01_narrative_skills/skill_market_hook_research.md` | KB_01 | 当需要分析目标市场受众、设计黄金前3秒钩子或情绪曲线时 |
| NARR-02 世界观与人物弧光 | `01_narrative_skills/skill_world_character_arc.md` | KB_01、KB_02 | 当需要构建世界观、人物立体小传、性格缺陷与潜台词时 |
| NARR-03 台词秒数精算 | `01_narrative_skills/skill_dialogue_second_calc.md` | KB_11 | 当台词需要按字数/语速精算镜头时长与重音节点（声画先行）时 |

## 02 导演美术场记类（visual_director）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| VIS-01 导演分镜拆解 | `02_visual_director_skills/skill_director_storyboard.md` | KB_07、KB_11 | 当需要拆解分镜、标注S/A/B算力分级、规划Cutaway缓冲镜时 |
| VIS-02 美术风格穿搭道具 | `02_visual_director_skills/skill_art_style_costume_prop.md` | KB_03、KB_04、KB_05 | 当需要确定画风、色彩脚本、人物穿搭、场景与道具视觉设定时 |
| VIS-03 纯中文零光影资产 | `02_visual_director_skills/skill_asset_pure_chinese_no_light.md` | KB_06、KB_08 | 当需要策划重要资产图并执行 @纯中文命名 与零高光阴影铁律时（核心） |
| VIS-04 连续性轴线守卫 | `02_visual_director_skills/skill_continuity_axis_guard.md` | KB_07 | 当需要校验180度轴线、左右站位、服装战损与跨集快照时 |

## 03 生图技法类（image_gen）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| IMG-01 生图技法路由器 | `03_image_gen_skills/skill_img_tech_router.md` | KB_06、KB_09 | 当需要为某个出图任务选择图生图/ControlNet/灰度图/LoRA/Inpainting策略时 |
| IMG-02 前置资源策划 | `03_image_gen_skills/skill_img_pre_resource_planner.md` | KB_06、KB_07 | 当需要为视频镜头策划首帧基准图、尾帧图、多宫格垫图时 |

## 04 生视频技法类（video_gen）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| VID-01 秒级切片器 | `04_video_gen_skills/skill_vid_second_slicer.md` | KB_08、KB_11 | 当需要按秒切分视频、执行一镜一动一主体台词、差分编译、口型排他锁与双管线分流时 |
| VID-02 技法选择器 | `04_video_gen_skills/skill_vid_method_selector.md` | KB_08、KB_09 | 当需要在首帧图生视频/首尾帧控制/分镜图转视频/多图参考融合/尾帧接力之间选型时 |

## 05 平台专属插件类（platform_plugins · 互斥加载）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| PLAT-00 公用默认 | `05_platform_plugins/plat_00_universal_default.md` | KB_08 | 当用户未指定平台时（产出公用标准提示词+平台推荐） |
| PLAT-01 豆包Seedream | `05_platform_plugins/plat_doubao_seedream.md` | KB_04、KB_08 | 当用户指定豆包/Seedream 生图时 |
| PLAT-02 即梦 | `05_platform_plugins/plat_jimeng.md` | KB_08、KB_11 | 当用户指定即梦/Seedance 生视频时 |
| PLAT-03 ComfyUI | `05_platform_plugins/plat_comfyui.md` | KB_06、KB_09 | 当用户指定ComfyUI（Flux/Wan2.1/2.2）时 |
| PLAT-04 MiniMax H3 | `05_platform_plugins/plat_minimax_h3.md` | KB_08、KB_11 | 当用户指定MiniMax海螺H3生视频时 |
| PLAT-05 可灵 | `05_platform_plugins/plat_kling.md` | KB_08、KB_11 | 当用户指定可灵/Kling生视频时 |

## 06 音频后期质检类（audio_edit_qc）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| QC-01 十分制评分官 | `06_audio_edit_qc_skills/skill_qc_prompt_scorer_10pt.md` | KB_10、KB_09 | 每条提示词产出后必触发（<9.0 打回重写） |
| AUD-01 音色克隆工作流 | `06_audio_edit_qc_skills/skill_tts_voice_clone_workflow.md` | KB_12 | 当需要制作角色音色或执行TTS克隆生成时 |
| EDT-01 剪映剪辑调音 | `06_audio_edit_qc_skills/skill_jianying_edit_sound_master.md` | KB_12 | 当需要输出剪辑手法、语速声调、音效BGM配置时 |
| EVO-01 复盘自进化 | `06_audio_edit_qc_skills/skill_retrospective_optimizer.md` | KB_09、KB_10 | 当用户填写"实际产出复盘"后自动触发 |

---

## 互斥与组合规则

1. **平台互斥**：05 类一次仅激活一个 plat_*；跨平台对比需分次产出独立代码块。
2. **固定组合**：任何 `plat_*` 激活时必伴随 KB_08（编译器）；评分 QC-01 对每条 Prompt 无条件触发。
3. **上下文预算**：单次任务建议挂载 ≤1 个平台插件 + ≤2 个 KB + ≤3 个技法 Skill。
4. **索引自检**：新增 Skill 必须同步登记本表（技能ID/路径/挂载KB/WHEN），否则总控视为不存在。
