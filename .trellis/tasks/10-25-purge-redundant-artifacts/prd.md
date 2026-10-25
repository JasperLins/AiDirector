# P1-E 冗余测试与残留物清理（含A/B/C裁决菜单）【挂起·待用户日后明示】

> **2026-10-25 用户裁决**：测试文档**全部保留**（豆包测试版、check_part*.txt、_onetake.py 等），供 Trellis 参考；用户**将于日后明示删除**。本任务据此挂起为"待删清单登记"，不执行任何删除动作。

## Goal

A组直接删（可恢复）：scripts/_onetake.py（git跟踪，已执行完的一次性补丁）；workspace/episodes/ 空目录。B组本地文件删前逐项确认（git忽略不可恢复）：check_part1/v3/v4+part2/v3/v4.txt 六日志2.2MB（gitignore明注临时校验产物）；豆包_archive/邪王追妻txt 27.2MB；两界/.lianjie_E01_DONE（引用失效路径）；两界/_archive/夜间长任务_E01全链路.md（自认空跑）。C组整目录裁决：两界食单_豆包测试版 workspace+memory——qc_linter最大审计语料（37+36+40+40块）+registry依赖，删除须连改 linter main() 重定向，保留则建议改名去『测试』字样。验收：删除留痕+qc_linter PASS。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
