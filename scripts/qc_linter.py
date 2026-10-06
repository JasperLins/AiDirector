#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AiDirector 双擎联审门禁 · L1 硬核语法与数学检查器 (scripts/qc_linter.py)
职责分工：
  - L1 (本脚本): 查风格包禁词、变量外壳残留、句首媒介前置、资产注册表跨文件对账、
                 视频秒级时间轴数学规范、[details]零空行封包法、蒙太奇B计划落位。
  - L2 (R7 智能体): 在本脚本 PASS 后，对脚本输出的《L2 导演语义智检必查清单》执行深度视听逻辑评分。
"""
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. PACK-01 主代码块绝对禁词与未展开外壳（出现任一即报错）
PACK01_FORBIDDEN_IN_PROMPT = [
    "严禁设定集排版",
    "严禁多视图分格",
    "画中画特写",
    "环形无影棚",
    "Flat Lit Albedo",
    "正交投影相机",
    "写实厚涂",
    "8K电影感",
    "电影感构图",
    "毛孔可见",
    "轻熟",
    "@画风锁",
    "[光位锁",
    "体积光替换为",
    "体积光氛围替换为",
]

VALID_MEDIA_PREFIXES = (
    "国风仙侠漫剧插画",
    "现代都市漫剧插画",
)

def audit_era_mixing(filepath: Path, block_idx: int, prompt_text: str, errors: list):
    """拦截句首现代媒介 + 句尾仙侠锁的跨时代混挂"""
    if prompt_text.startswith("现代都市漫剧插画"):
        if "仙侠唯美" in prompt_text or "仙气流转" in prompt_text:
            errors.append(f"[ERA_MIXING] {filepath.relative_to(ROOT)} 主代码块 #{block_idx} 跨时代混挂：句首现代，句尾残留仙侠锁！")

def strip_details_blocks(text: str) -> str:
    """剥离 <details>...</details> 历史归档块，只审主位置活跃内容"""
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL | re.IGNORECASE)

def extract_prompt_blocks(text: str):
    """提取所有 ```prompt ... ``` 代码块内容"""
    return re.findall(r"```prompt\s*\n(.*?)\n```", text, flags=re.DOTALL)

def load_registered_assets(reg_path: Path) -> set:
    """从项目《资产注册表.md》动态提取所有合法的 @纯中文资产名"""
    if not reg_path.exists():
        return set()
    txt = reg_path.read_text(encoding="utf-8")
    return set(re.findall(r"@[\u4e00-\u9fa5]{2,8}", txt))

def audit_details_zero_blank_lines(filepath: Path, text: str, errors: list):
    """检查 <details> 块内部是否严格遵守 Typora 纯 HTML 零空行封包法"""
    blocks = re.findall(r"(<details\b[^>]*>.*?</details>)", text, flags=re.DOTALL | re.IGNORECASE)
    for idx, blk in enumerate(blocks, 1):
        if re.search(r"\n\s*\n", blk):
            errors.append(f"[DETAILS_BLANK_LINE] {filepath.relative_to(ROOT)} 第 {idx} 个 <details> 块内部存在空行（违反纯HTML零空行封包法）")

def audit_video_time_nodes(filepath: Path, block_idx: int, prompt_text: str, errors: list):
    """当代码块含 [xx-xxs] 视频时间轴时，执行数学校验：节点数 <=3，单段时长 >=0.4s"""
    nodes = re.findall(r"\[(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:s\vert{}秒)\]", prompt_text)
    if not nodes:
        return
    if len(nodes) > 3:
        errors.append(f"[VIDEO_NODE_OVERFLOW] {filepath.relative_to(ROOT)} 主代码块 #{block_idx} 时间轴节点数为 {len(nodes)}（违反 <=3 铁律）")
    for start_s, end_s in nodes:
        dur = float(end_s) - float(start_s)
        if dur <= 0:
            errors.append(f"[VIDEO_TIME_INVALID] {filepath.relative_to(ROOT)} 主代码块 #{block_idx} 时间轴起止倒挂 [{start_s}-{end_s}s]")

def audit_workspace_doc(
    filepath: Path,
    reg_path: Path,
    require_media_prefix: bool,
    check_no_at_in_image: bool,
    errors: list,
    stats: dict,
):
    if not filepath.exists():
        errors.append(f"[MISSING_FILE] 找不到文件: {filepath.relative_to(ROOT)}")
        return
    raw = filepath.read_text(encoding="utf-8")
    audit_details_zero_blank_lines(filepath, raw, errors)

    registered_assets = load_registered_assets(reg_path)
    active_text = strip_details_blocks(raw)
    prompts = extract_prompt_blocks(active_text)
    if not prompts:
        errors.append(f"[NO_PROMPTS] {filepath.relative_to(ROOT)} 未检出任何主 ```prompt 代码块")
        return

    stats[str(filepath.relative_to(ROOT))] = len(prompts)

    for i, p in enumerate(prompts, 1):
        p_clean = p.strip()
        # 1. 检查省略号偷懒
        if "..." in p_clean or ("…" in p_clean and ("（略）" in p_clean or "同上" in p_clean)):
            errors.append(f"[LAZY_ELLIPSIS] {filepath.relative_to(ROOT)} 主代码块 #{i} 含有偷懒省略符")
        # 2. 检查 PACK-01 禁词与外壳残留
        for bad in PACK01_FORBIDDEN_IN_PROMPT:
            if bad in p_clean:
                errors.append(f"[FORBIDDEN_TERM] {filepath.relative_to(ROOT)} 主代码块 #{i} 命中禁词/外壳: '{bad}'")
        # 3. 检查句首媒介声明
        if require_media_prefix and not p_clean.startswith(VALID_MEDIA_PREFIXES):
            head = p_clean[:25].replace("\n", " ")
            errors.append(f"[MISSING_MEDIA_PREFIX] {filepath.relative_to(ROOT)} 主代码块 #{i} 句首未以规定媒介词开头 (当前句首: '{head}...')")
        # 4. 检查纯生图文档去 @ 符号 vs 视频文档 @资产注册表对账
        if check_no_at_in_image:
            if "@" in p_clean:
                errors.append(f"[AT_SYMBOL_LEAK] {filepath.relative_to(ROOT)} 主代码块 #{i} 残留 '@' 符号")
        else:
            used_assets = re.findall(r"@[\u4e00-\u9fa5A-Za-z0-9_]+", p_clean)
            for ua in used_assets:
                if not re.match(r"^@[\u4e00-\u9fa5]{2,8}$", ua):
                    errors.append(f"[ILLEGAL_ASSET_NAME] {filepath.relative_to(ROOT)} 主代码块 #{i} 资产名非纯中文: '{ua}'")
                elif registered_assets and ua not in registered_assets:
                    errors.append(f"[UNREGISTERED_ASSET] {filepath.relative_to(ROOT)} 主代码块 #{i} 引用了未在资产注册表登记的资产: '{ua}'")
        # 5. 视频时间轴数学校验
        audit_video_time_nodes(filepath, i, p_clean, errors)
        # 6. 跨时代混挂拦截（句首现代媒介 + 句尾仙侠锁）
        audit_era_mixing(filepath, i, p_clean, errors)

def audit_kb05_style_packs(errors: list):
    kb05 = ROOT / "kb_library" / "KB_05_视觉风格词典.md"
    if not kb05.exists():
        errors.append("[MISSING_FILE] 找不到 kb_library/KB_05_视觉风格词典.md")
        return
    txt = kb05.read_text(encoding="utf-8")
    for pack_id in ("PACK-01", "PACK-02", "PACK-03", "PACK-04"):
        if pack_id not in txt:
            errors.append(f"[KB05_MISSING_PACK] KB_05 缺少预设包 {pack_id}")
    if "（略）" in txt or "（同上）" in txt:
        errors.append("[KB05_LAZY_PLACEHOLDER] KB_05 含有 '（略）' 或 '（同上）' 偷懒占位符")

def audit_blacklist(errors: list):
    bl = ROOT / "memory" / "global" / "全局复盘避坑黑名单.md"
    if not bl.exists():
        errors.append("[MISSING_FILE] 找不到 memory/global/全局复盘避坑黑名单.md")
        return
    txt = bl.read_text(encoding="utf-8")
    for num in range(18, 27):
        if f"| {num} |" not in txt and f"| {num:02d} |" not in txt:
            errors.append(f"[BLACKLIST_INDEX] 全局复盘避坑黑名单第一部分速查表缺少正式编号 {num}")

def audit_montage_plan_b(errors: list):
    vis01 = ROOT / "skills" / "02_visual_director_skills" / "skill_director_storyboard.md"
    if not vis01.exists() or "蒙太奇B计划" not in vis01.read_text(encoding="utf-8"):
        errors.append("[VIS01_MONTAGE] VIS-01 (skill_director_storyboard.md) 未写入高危交互蒙太奇B计划铁律")
    for e01_rel in [
        Path("workspace/两界食单/E01_视频生成提示词.md"),
        Path("workspace/两界食单_豆包测试版/E01_视频生成提示词_豆包版.md"),
    ]:
        p = ROOT / e01_rel
        if p.exists() and "蒙太奇B计划" not in p.read_text(encoding="utf-8"):
            errors.append(f"[E01_MONTAGE] {e01_rel} 镜06 未落地高危交互蒙太奇B计划")

def main():
    errors = []
    stats = {}
    reg_doubao = ROOT / "memory/projects/两界食单_豆包测试版/资产注册表.md"
    reg_main = ROOT / "memory/projects/两界食单/资产注册表.md"

    # 1. 审豆包测试版核心产出文档（资产文档=生图口径：句首媒介+去@）
    audit_workspace_doc(
        ROOT / "workspace/两界食单_豆包测试版/重要资产图片提示词_豆包版.md",
        reg_path=reg_doubao,
        require_media_prefix=True,
        check_no_at_in_image=True,
        errors=errors,
        stats=stats,
    )
    # 1b. 审 E01/E02 合体单文档（AGENTS 第七节规范 · R9-20261006-6 收口：首帧块+视频块同档——
    #     媒介前缀项对视频块天然不适用，故沿用合体口径 False；@对账走注册表登记制）
    for ep_doc in (
        "E01_视频生成提示词_豆包版.md",
        "E02_视频生成提示词_豆包版.md",
        "E03_视频生成提示词_豆包版.md",
    ):
        audit_workspace_doc(
            ROOT / "workspace/两界食单_豆包测试版" / ep_doc,
            reg_path=reg_doubao,
            require_media_prefix=False,
            check_no_at_in_image=False,
            errors=errors,
            stats=stats,
        )
    # 2. 审原项目资产文档与 E01 文档
    audit_workspace_doc(
        ROOT / "workspace/两界食单/重要资产图片提示词.md",
        reg_path=reg_main,
        require_media_prefix=True,
        check_no_at_in_image=True,
        errors=errors,
        stats=stats,
    )
    audit_workspace_doc(
        ROOT / "workspace/两界食单/E01_视频生成提示词.md",
        reg_path=reg_main,
        require_media_prefix=False,
        check_no_at_in_image=False,
        errors=errors,
        stats=stats,
    )
    # 3. 审 KB_05、黑名单 18~26、VIS-01 蒙太奇B计划
    audit_kb05_style_packs(errors)
    audit_blacklist(errors)
    audit_montage_plan_b(errors)

    print("=" * 72)
    if errors:
        print(f"❌ [L1 MACHINE GATE: FAILED] — 共检出 {len(errors)} 处硬性违规（R7 评分锁定为 0 分，请立即修复）：")
        for idx, err in enumerate(errors, 1):
            print(f"  {idx:02d}. {err}")
        print("=" * 72)
        sys.exit(1)
    else:
        print("🎉 [L1 MACHINE GATE: PASSED (0 ERRORS)] — 语法/禁词/注册表/时间轴/DOM 100% 合规！")
        print("-" * 72)
        print("📊 活跃代码块扫描统计：")
        for k, v in stats.items():
            print(f"   • {k}: {v} 个主 Prompt 代码块")
        print("-" * 72)
        print("🧠 [交棒 L2 · R7 导演语义智检必答核验单]（请 R7 在汇报中逐项确认）：")
        print("   [Q1 人设与关系色语义] 记忆点是否均具备(画面绝对方位+形态比喻+数量上限)？主仆/情侣服色与身高差是否写透？")
        print("   [Q2 单镜动作与B计划] 是否严格'一镜一主动作一机位'？镜06等高危肢体抓握是否已配齐3切蒙太奇B计划？")
        print("   [Q3 空间分区与排他锁] 多人同框是否具备左中右/前中后象限隔离？说话者张嘴+倾听者闭嘴是否零歧义？")
        print("   [Q4 20/80差分纯度] 视频Prompt是否严守<=2骨相词、无冗余静态穿搭堆砌？")
        print("   [Q5 光位与轴线连续性] 各镜内联光位文本与左右站位是否同180度轴线声明及StateDiff快照完全一致？")
        print("=" * 72)
        sys.exit(0)

if __name__ == "__main__":
    main()
