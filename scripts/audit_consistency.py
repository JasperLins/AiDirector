import os
import re

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
    report.append(f"List: {all_index_skills}")

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
    report.append(f"Skills in dir but not in index: {missing_in_index}")
    report.append(f"Skills in index but not in dir: {missing_in_dir}")

    # 2. Check AGENTS.md references
    with open('AGENTS.md', 'r', encoding='utf-8') as f:
        agents_content = f.read()
    
    agents_skills = re.findall(r'skill_[a-zA-Z0-9_]+|plat_[a-zA-Z0-9_]+', agents_content)
    agents_skills = set(agents_skills) - {'plat_00_universal_default', 'plat_00'}
    
    report.append("--- Skills mentioned in AGENTS.md ---")
    missing_in_agents = set([s for s in agents_skills if s not in actual_skills and 'plat_' not in s])
    report.append(f"Skills in AGENTS.md but not in actual directory: {missing_in_agents}")

    # 3. Check KBs referenced in AGENTS.md and SKILL_INDEX.md
    agents_kbs = set(re.findall(r'KB_\d{2}', agents_content))
    index_kbs = set(re.findall(r'KB_\d{2}', skill_index_content))
    
    report.append("--- KB references ---")
    report.append(f"KBs in AGENTS.md: {sorted(list(agents_kbs))}")
    report.append(f"KBs in SKILL_INDEX.md: {sorted(list(index_kbs))}")

    # 4. Check README.md
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    readme_kbs = set(re.findall(r'KB_\d{2}', readme_content))
    report.append("--- KB references in README.md ---")
    report.append(f"KBs in README.md: {sorted(list(readme_kbs))}")

    # Print output
    for line in report:
        print(line)

if __name__ == '__main__':
    main()
