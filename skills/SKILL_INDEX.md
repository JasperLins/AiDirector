# SKILL_INDEX.md — 全局技能插件路由索引表

> 本索引是 `skills/` 目录的唯一路由入口（仿 anthropics/skills 按需加载规范）。
> **使用规则**：总控（AGENTS.md）根据任务匹配下表 `WHEN 触发条件`，**只提取读取命中的 Skill 文件本体**，未命中的不读取，以节省上下文 Token。
> 平台插件（05 类）互斥加载：一次任务最多激活一个 `plat_*`；未指定平台时激活 `plat_00`。

---

## 01 叙事编剧类（narrative）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| NARR-00 新剧立项问询器 | `01_narrative_skills/skill_series_intake.md` | KB_05、KB_01 | 当用户"新建一部剧/立项/开新项目"时第一个触发（先于三件套建立与 NARR-01/02）——两层立项参数收口（必答 7 项未声明必追问）+方案选择制构思轮+一页式立项书用户拍板（0.0 项目立项裁决位·R9-20261007-17） |
| NARR-01 市场钩子调研 | `01_narrative_skills/skill_market_hook_research.md` | KB_01 | 当需要分析目标市场受众、设计黄金前3秒钩子或情绪曲线时 |
| NARR-02 世界观与人物弧光 | `01_narrative_skills/skill_world_character_arc.md` | KB_01、KB_02 | 当需要构建世界观、人物立体小传、性格缺陷与潜台词时 |
| NARR-03 台词秒数精算 | `01_narrative_skills/skill_dialogue_second_calc.md` | KB_11、KB_12 | 当台词需要按字数/语速精算镜头时长与重音节点（声画先行）时 |
| NARR-04 单集剧本与脚本转化 | `01_narrative_skills/skill_episode_script_writer.md` | KB_01、KB_02、KB_12 | 当需要撰写单集完整文学剧本、把大纲/小说改编为可拍摄剧本、或界定"文学剧本/分镜脚本/生成提示词"三层边界（台词双轨隔离+音频ID 预埋）时 |

## 02 导演美术场记类（visual_director）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| VIS-01 导演分镜拆解 | `02_visual_director_skills/skill_director_storyboard.md` | KB_07、KB_11、KB_15（运镜选型按需） | 当需要拆解分镜、标注S/A/B算力分级（含冗余覆盖档·机位数×条数）、产出场次覆盖调度表（Master主镜+覆盖镜+blocking走位+平面点位·S/A级强制·2026-10-18）、**逐镜先填空间镜头卡（几何先行 8 字段+焦段数值表·KB_11 九节附·2026-10-25）**、规划Cutaway缓冲镜时 |
| VIS-02 美术风格穿搭道具 | `02_visual_director_skills/skill_art_style_costume_prop.md` | KB_02、KB_03、KB_04、KB_05 | 当需要确定画风、色彩脚本、人物穿搭、场景与道具视觉设定时 |
| VIS-03 纯中文零光影资产 | `02_visual_director_skills/skill_asset_pure_chinese_no_light.md` | KB_06、KB_08 | 当需要策划重要资产图并执行 @纯中文命名 与零高光阴影铁律时（核心） |
| VIS-04 连续性轴线守卫 | `02_visual_director_skills/skill_continuity_axis_guard.md` | KB_07 | 当需要校验180度轴线、左右站位、服装战损与跨集快照时 |
| SBM-01 分镜图总控 | `02_visual_director_skills/skill_storyboard_master.md` | KB_14、KB_06、KB_07、KB_15（渐变白名单按需） | 当 R2 分镜表定稿后规划分镜图生产（镜组四模式路由·A 分镜序列组双通道 A-1 宫格/A-2 逐镜序列/一致性链/**视频段分组·实验路径⑤段级直出（2026-10-18 降格·黑名单45 复测②）**/**冗余覆盖与素材留存规划（3机位×3条·S/A/B 投保·Step 5.7）**/**生产排期表与批次通告（拍摄顺序≠叙事顺序·Step 5.8）**），或用户问"这些镜头怎么出图/怎么保持一致/长镜头怎么办/九宫格质量差怎么办/怎么切段/怎么排生产顺序"时（R10 专属技能·R9-20261007-14 立·R9-20261007-16 修订·R9-20261010-18 修订·2026-10-18 回滚修订+传统拍摄制度化扩容） |
| VIS-05 资产设定板式路由器 | `02_visual_director_skills/skill_asset_sheet_board_router.md` | KB_06、KB_02、KB_03 | 当框架识别资产复杂度高（人物头部记忆点≥3项并发/服饰层次≥3层/非人形多形态/大型道具）需宫格设定板，或需宫格备用抽卡方案时按需触发——默认传统单视图五件套，同 IMG-02 多宫格分镜一样按需使用（R9-20261006-9） |

## 03 生图技法类（image_gen）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| IMG-01 生图技法路由器 | `03_image_gen_skills/skill_img_tech_router.md` | KB_06、KB_09 | 当需要为某个出图任务选择图生图/ControlNet/灰度图/LoRA/Inpainting策略时 |
| IMG-02 前置资源策划 | `03_image_gen_skills/skill_img_pre_resource_planner.md` | KB_06、KB_07、KB_08 | 当需要为视频镜头策划**分镜图（原首帧基准图·R9-20261010-18 更名）**、尾帧图、A-1 宫格垫图/A-2 逐镜分镜序列（弱模型九宫格质量差时）时 |

## 04 生视频技法类（video_gen）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| VID-01 秒级切片器 | `04_video_gen_skills/skill_vid_second_slicer.md` | KB_08、KB_09、KB_11、KB_14（分段/实验⑤按需）、KB_15（运镜选型按需） | 当需要按秒切分视频（单镜差分编译·默认，或实验路径⑤段级序列区间内容写作）、执行一镜一动一主体台词、台词五要素与静默声明必备件（补丁8）、差分编译、口型排他锁与音频可替换原则时 |
| VID-02 技法选择器 | `04_video_gen_skills/skill_vid_method_selector.md` | KB_08、KB_09、KB_14（实验⑤五节附校准按需）、KB_15（渐变白名单按需） | 当需要选技法时——四大默认技法（首帧I2V/首尾帧控制/多图参考融合/尾帧接力）与**⑤分镜序列长视频（段级直出·实验路径·2026-10-18 降格·仅用户明示启用）**之间路由；用户说"多张分镜图生成长视频/分段直出"时直达⑤（实验） |

## 05 平台专属插件类（platform_plugins · 互斥加载）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| PLAT-00 公用默认 | `05_platform_plugins/plat_00_universal_default.md` | KB_08 | 当用户未指定平台时（产出公用标准提示词+平台推荐） |
| PLAT-01 豆包Seedream | `05_platform_plugins/plat_doubao_seedream.md` | KB_04、KB_06、KB_08 | 当用户指定豆包/Seedream 生图时 |
| PLAT-02 即梦 | `05_platform_plugins/plat_jimeng.md` | KB_08、KB_11 | 当用户指定即梦/Seedance 生视频时 |
| PLAT-03 ComfyUI | `05_platform_plugins/plat_comfyui.md` | KB_06、KB_08、KB_09 | 当用户指定ComfyUI（Flux/Wan2.1/2.2）时 |
| PLAT-04 MiniMax H3 | `05_platform_plugins/plat_minimax_h3.md` | KB_02、KB_08、KB_11 | 当用户指定MiniMax海螺H3生视频时 |
| PLAT-05 可灵 | `05_platform_plugins/plat_kling.md` | KB_08、KB_09、KB_11 | 当用户指定可灵/Kling生视频时 |
| PLAT-06 ChatGPT生图 | `05_platform_plugins/plat_chatgpt_image.md` | KB_06、KB_08 | 当用户指定ChatGPT/GPT-4o生图，或需要记忆点精确锁定/文字入画/道具特写时（R9-20261005实测新增·工业级完整版） |
| PLAT-07 大香蕉生图 | `05_platform_plugins/plat_nano_banana.md` | KB_06、KB_08 | 当用户指定大香蕉/Nano Banana/Gemini生图，或需要气质定调/材质微光/多轮编辑修图时（R9-20261005实测新增·工业级完整版） |

## 06 音频后期质检类（audio_edit_qc）

| 技能ID | 路径 | 挂载KB | WHEN 触发条件 |
|---|---|---|---|
| QC-01 维度核查官 | `06_audio_edit_qc_skills/skill_qc_prompt_scorer_10pt.md` | KB_10、KB_09 | 每条提示词产出后必触发——视频 8 维/生图八层证据核查，缺一即打回重写（不打总分·2026-10-25 维度制立法，废 10 分自评） |
| AUD-01 音色克隆工作流 | `06_audio_edit_qc_skills/skill_tts_voice_clone_workflow.md` | KB_12 | 当需要制作角色音色（音色五维+平台注册号·补丁8）、执行TTS克隆生成或登记音色ID时 |
| EDT-01 剪映剪辑调音 | `06_audio_edit_qc_skills/skill_jianying_edit_sound_master.md` | KB_12 | 当需要输出剪辑手法、语速声调、音效BGM配置时 |
| EVO-01 问题直通与知识沉淀 | `06_audio_edit_qc_skills/skill_retrospective_optimizer.md` | KB_09、KB_10 | 当用户反馈"翻车/崩了/效果不对"要求即时修复，或要求"优化框架/更新黑名单/沉淀知识"时触发（2026-10-25 裁决：废逐条复盘占位，问题直通） |

---

## 互斥与组合规则

1. **平台互斥**：05 类一次仅激活一个 plat_*；跨平台对比需分次产出独立代码块。
2. **固定组合**：任何 `plat_*` 激活时必伴随 KB_08（编译器）；质检 QC-01 对每条 Prompt 无条件触发（维度制）。
3. **上下文预算**：单次任务建议挂载 ≤1 个平台插件 + ≤2 个 KB + ≤3 个技法 Skill。
4. **索引自检**：新增 Skill 必须同步登记本表（技能ID/路径/挂载KB/WHEN），否则总控视为不存在。
5. **KB_13 全局常驻（2026-10-25 补·修断链）**：任何产出**人类可读文档**（分镜/资产/视频提示词）的任务，产出文档头部必挂「📖 术语速查」精简行（权威源=`KB_13_框架术语白话词典.md` 按文档实际用词裁剪，新术语先在 KB_13 登记）——不占技能挂载位，随产出任务按需加载；执法位＝AGENTS 第七节术语速查硬性标准＋R7 核查行。
