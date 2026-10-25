# 仓库结构与命名法（文档框架版）

本仓库是 Markdown 提示词工程框架，非代码项目。结构铁律：
- `AGENTS.md`=总控路由（宪法层，只立法不抄词表）；`kb_library/KB_01~15`=词典与编译器规范唯一源；`skills/27技能`=插件（YAML frontmatter，按需加载）；`memory/global`=全局知识库；`memory/projects/<剧名>/`=三件套（剧集圣经与世界观设定.md/资产注册表.md/跨集状态快照_StateDiff.md——文件名三项目统一，禁自创名）；`workspace/<剧名>/`=按剧隔离产出。
- .gitignore 约定：`workspace/*` 与 `memory/projects/*` 本地管理，仅示范剧集_苍穹与烟火入库；`check_part*.txt`=临时校验产物。改这两个目录=本机变更，不产生提交。
- 引用规范：跨册引用写"KB_XX 节名/节号"（节号必须实存——2026-10-25 曾修 8 处错号）；技能挂载以 frontmatter required_kbs 为唯一事实源（SKILL_INDEX 行须与之一致，AGENTS 路由行=并集）。
