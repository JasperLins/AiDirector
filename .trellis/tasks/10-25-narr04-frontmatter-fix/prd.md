# NARR-04技能头修复+技能头完整性门禁

## Goal

修复提交 443b30b 中"铁律7 迁入 NARR-04"造成的技能 YAML 头损坏：`skills/01_narrative_skills/skill_episode_script_writer.md` 的 `name:` 字段被从中间劈断为 `nam`＋空行＋铁律7 正文＋`e: skill_episode_script_writer`，且铁律7 正文滞留头部区、正文法则清单仅 6 条（与标题"7 条硬核铁律"不符）。同时补上双门禁盲区：qc_linter 与 audit_consistency 均不解析技能 YAML 头，故该损坏曾以"双门禁绿"入库（①级实测证据）。

## Requirements

1. **修复技能文件**：YAML 头恢复为合法 frontmatter（`name: skill_episode_script_writer` 单行完整、description/required_kbs 原样保留）；铁律7（剧本闸前用户裁决位·R9-20261006-7·立法背景黑名单 36）从头部移入正文"一、核心职责与工业级法则"作为第 7 条，内容一字不丢。
2. **qc_linter 新增技能头完整性门禁**：扫描 `skills/` 下全部技能 .md，校验 YAML 头存在且含合法 `name:`/`description:`/`required_kbs:` 三键、无中断行（如裸 `nam`）；损坏即 ERROR 硬失败。实现后自测：临时构造一个损坏样本确认能报错，再删样本。
3. **黑名单 47 号条目**：技能头损坏·门禁盲区（症状/根因=法则迁移编辑无机械校验＋门禁不解析技能头/修复=本任务/证据位阶①）；qc_linter 黑名单索引检查范围 18~46 → 18~47。
4. **AGENTS 所有权表核对**："剧本闸用户裁决位→NARR-04"路由行已准确，铁律7 归位后无需改动 AGENTS.md（确认即可，不重复立法）。

## Acceptance Criteria

- [x] skill_episode_script_writer.md 头部合法（三键完整单行），铁律7 位于正文第 7 条，标题与清单数一致（2026-10-25 check 复核：头 7 行合法 YAML、铁律7 一字不丢收尾句号、清单实数 7 条、diff 仅两处无被动）
- [x] qc_linter 技能头检查覆盖 skills/ 全部技能且 0 错误；损坏样本自测能报 ERROR（2026-10-25 check 复跑：27 技能 0 错误；自构 `nam`+`。e: skill` 损坏样本报 4 处 SKILL_FRONTMATTER_* 后已删）
- [x] 黑名单 47 号落盘＋qc_linter 范围同步 18~47（2026-10-25 check 复核：47 号与 46 号同构、三处计数同步、range(18,48) 覆盖 47、无 46 残留）
- [x] `python scripts/qc_linter.py` 0 ERRORS；`python scripts/audit_consistency.py` fail=0（2026-10-25 check 复跑：L1 PASSED exit=0；CONSISTENCY PASSED fail=0）

## Notes

- 诊断来源：2026-10-25 会话调研 grep 实证（`git show HEAD` 比对）；诊断即登记纪律。
- 单源铁律：铁律7 唯一源=NARR-04 正文；AGENTS 只路由不复写。
- 关联提案：本任务=「框架始终引导」调研方案 D（门禁自防御）的第一步落地。
