# -*- coding: utf-8 -*-
"""AGENTS ↔ SKILL_INDEX ↔ skills 目录 三方一致性审计（2026-10-25 门禁工程修复版）

修复记录：
  1. KB 区间记法展开（KB_02~KB_07 / KB_01～KB_15 现在展开为逐个编号——
     修复旧版对区间内编号（如 KB_03）的漏报）；
  2. 硬性差异（索引↔目录技能不一致 / AGENTS 引用不存在的技能）非零退出码，
     可并入门禁回路（旧版永远 exit 0，从未真正拦截）。
KB 引用清单仍为信息性输出（AGENTS/SKILL_INDEX 挂载差异属 P0-D 设计裁决，不作硬失败）。
"""
import os
import re
import sys


def expand_kb_ranges(text: str) -> set:
    """提取 KB 编号并展开区间记法（KB_02~KB_07 / KB_02～KB_07 / KB_02~07）"""
    out = set(re.findall(r"KB_\d{2}", text))
    for m in re.finditer(r"KB_(\d{2})\s*[~～]\s*(?:KB_)?(\d{2})", text):
        a, b = int(m.group(1)), int(m.group(2))
        if a < b <= 15:
            for n in range(a, b + 1):
                out.add(f"KB_{n:02d}")
    return out


def main():
    report = []

    # 1. Check AGENTS.md vs SKILL_INDEX.md skills
    with open('skills/SKILL_INDEX.md', 'r', encoding='utf-8') as f:
        skill_index_content = f.read()

    registered_skills = re.findall(r'`(0[1-6]_[^/]+/skill_[^.]+)\.md`', skill_index_content)
    registered_plats = re.findall(r'`(05_platform_plugins/plat_[^.]+)\.md`', skill_index_content)
    all_index_skills = [s.split('/')[-1] for s in registered_skills + registered_plats]

    report.append("--- Skills registered in SKILL_INDEX.md ---")
    report.append(f"Count: {len(all_index_skills)}")

    # Check actual files
    actual_skills = []
    for root, dirs, files in os.walk('skills'):
        for file in files:
            if file.endswith('.md') and file != 'SKILL_INDEX.md':
                actual_skills.append(file.replace('.md', ''))

    report.append("--- Actual skills in skills/ directory ---")
    report.append(f"Count: {len(actual_skills)}")
    missing_in_index = set(actual_skills) - set(all_index_skills)
    missing_in_dir = set(all_index_skills) - set(actual_skills)
    report.append(f"Skills in dir but not in index: {missing_in_index or '{}'}")
    report.append(f"Skills in index but not in dir: {missing_in_dir or '{}'}")

    # 2. Check AGENTS.md references
    with open('AGENTS.md', 'r', encoding='utf-8') as f:
        agents_content = f.read()

    agents_skills = re.findall(r'skill_[a-zA-Z0-9_]+|plat_[a-zA-Z0-9_]+', agents_content)
    agents_skills = set(agents_skills) - {'plat_00_universal_default', 'plat_00'}

    report.append("--- Skills mentioned in AGENTS.md ---")
    missing_in_agents = set([s for s in agents_skills if s not in actual_skills and 'plat_' not in s])
    report.append(f"Skills in AGENTS.md but not in actual directory: {missing_in_agents or '{}'}")

    # 3. Check KBs referenced in AGENTS.md and SKILL_INDEX.md（区间已展开）
    agents_kbs = expand_kb_ranges(agents_content)
    index_kbs = expand_kb_ranges(skill_index_content)

    report.append("--- KB references (ranges expanded) ---")
    report.append(f"KBs in AGENTS.md: {sorted(list(agents_kbs))}")
    report.append(f"KBs in SKILL_INDEX.md: {sorted(list(index_kbs))}")

    # 4. Check README.md（信息性）
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    readme_kbs = expand_kb_ranges(readme_content)
    report.append("--- KB references in README.md ---")
    report.append(f"KBs in README.md: {sorted(list(readme_kbs))}")

    for line in report:
        print(line)

    # 5. 硬性差异判定（非零退出，可入闸）
    hard_fail = bool(missing_in_index or missing_in_dir or missing_in_agents)
    if hard_fail:
        print("=" * 60)
        print("❌ [CONSISTENCY GATE: FAILED] 技能三方对账存在差异（见上）——exit 1")
        sys.exit(1)
    print("✅ [CONSISTENCY GATE: PASSED] 技能三方零差异")


if __name__ == '__main__':
    main()
