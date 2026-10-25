#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AiDirector 双擎联审门禁 · L1 硬核语法与数学检查器 (scripts/qc_linter.py)
职责分工：
  - L1 (本脚本): 查风格包禁词、变量外壳残留、句首媒介前置、资产注册表跨文件对账、
                 视频秒级时间轴数学规范、[details]零空行封包法、蒙太奇B计划落位。
  - L2 (R7 智能体): 在本脚本 PASS 后，按 KB_10 V3 维度制（视频 8 维/生图八层）执行证据核查——
                 每维必引证据（Prompt 行/镜头卡字段/注册表行），无证据=判缺失；缺一即打回，不打总分（2026-10-25 维度制立法）。
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
    # PACK-03 3D 国漫 CG 系句首媒介（KB_05 四节 ①句首前置词 + ②锁文本场景/道具变体）
    "3D国漫次世代CG渲染",
    "3D国漫CG场景渲染",
    "3D国漫CG道具渲染",
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
    """时间轴数学校验（R9-20261010-18 段级制修订·2026-10-18 回滚注记：单镜≤3 为默认口径，段级序列式仅为实验路径⑤产物）：
    - 单镜 Prompt：时间轴节点数 <=3；
    - 段级序列 Prompt（含总起句"参考图顺序推进"/`图N`/`对应素材位N` 绑定特征）：
      区间数=段内镜数，不受 <=3 限（KB_10 V4 段级口径），但须起止不倒挂、区间升序无重叠。
    - 修复留痕：旧正则 `(?:s\\vert{}秒)` 转义损坏致节点全不匹配、本检查整体失效（R9-20261010-18）。"""
    nodes = re.findall(r"\[(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:s|秒)\]", prompt_text)
    if not nodes:
        return
    is_segment_prompt = bool(
        re.search(r"参考图顺序推进", prompt_text)
        or re.search(r"对应素材位\d+", prompt_text)
        or re.search(r"\]\s*图\s*\d+", prompt_text)
    )
    # 节点数上限按 KB_08 四节 1/5 与 VID-01 边界 4 编码（R9-20261010-18 修复留痕）：
    # 标准单镜 ≤3；长条式（末节点止点 >8s，如 10s 母版 4 节点/30s 加密 5~7 段）≤7；段级序列=段内镜数（≤12 兜底）
    max_end = max(float(e) for _, e in nodes)
    if is_segment_prompt:
        limit = 12
    elif max_end > 8.0:
        limit = 7
    else:
        limit = 3
    if len(nodes) > limit:
        errors.append(f"[VIDEO_NODE_OVERFLOW] {filepath.relative_to(ROOT)} 主代码块 #{block_idx} 时间轴节点数为 {len(nodes)}（超上限 {limit}：标准单镜≤3(默认)/长条≤7/段级=段内镜数(实验⑤)）")
    prev_end = 0.0
    for start_s, end_s in nodes:
        dur = float(end_s) - float(start_s)
        if dur <= 0:
            errors.append(f"[VIDEO_TIME_INVALID] {filepath.relative_to(ROOT)} 主代码块 #{block_idx} 时间轴起止倒挂 [{start_s}-{end_s}s]")
        if float(start_s) < prev_end - 1e-9:
            errors.append(f"[VIDEO_SEG_OVERLAP] {filepath.relative_to(ROOT)} 主代码块 #{block_idx} 时间轴区间重叠（上一区间止于 {prev_end}s，本区间起于 {start_s}s）")
        prev_end = max(prev_end, float(end_s))

def audit_workspace_doc(
    filepath: Path,
    reg_path: Path,
    require_media_prefix: bool,
    check_no_at_in_image: bool,
    errors: list,
    stats: dict,
    optional: bool = False,
    warnings: list = None,
):
    if not filepath.exists():
        if optional:
            # 2026-10-25 修复 fresh-clone 必挂：workspace/* 与 memory/projects/* 为本地管理目录
            # （.gitignore），他机克隆天然缺失——降级为跳过警告而非硬错误
            if warnings is not None:
                shown = filepath.relative_to(ROOT) if filepath.is_absolute() else filepath
                warnings.append(f"[SKIP_LOCAL_ONLY] {shown} 不存在于本机（本地管理目录），跳过审计")
        else:
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
        # 5b. 台词镜时间轴收口（2026-10-25 维度制联动·⑦⑧维）：含台词/口型标记的 Prompt
        #     必须有时间节点或时长声明；分镜图（图像）块不含台词标记，天然免误伤
        if not check_no_at_in_image and re.search(r"张嘴|嘴唇|双唇|台词", p_clean):
            has_node = re.search(r"\[\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?\s*(?:s|秒)\]", p_clean)
            has_duration = re.search(r"\d+(?:\.\d+)?\s*(?:s|秒)\b", p_clean)
            if not has_node and not has_duration and warnings is not None:
                warnings.append(
                    f"[VIDEO_NO_TIMELINE] {filepath.relative_to(ROOT)} 主代码块 #{i} 含台词/口型标记但无秒级节点亦无时长声明（⑦动作与时间维嫌疑缺失，交 R7 维度核查）"
                )
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
    for num in range(18, 46):
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
    warnings = []
    stats = {}

    # ── 审计对象注册表（2026-10-25 重构：表驱动+自动发现，修 fresh-clone 必挂）──
    # 口径：image=句首媒介+去@（生图）；video=注册表对账（含台词时间轴收口警告）
    AUDIT_TARGETS = [
        ("workspace/两界食单_豆包测试版/重要资产图片提示词_豆包版.md", "memory/projects/两界食单_豆包测试版/资产注册表.md", "image"),
        ("workspace/两界食单_豆包测试版/E01_视频生成提示词_豆包版.md", "memory/projects/两界食单_豆包测试版/资产注册表.md", "video"),
        ("workspace/两界食单_豆包测试版/E02_视频生成提示词_豆包版.md", "memory/projects/两界食单_豆包测试版/资产注册表.md", "video"),
        ("workspace/两界食单_豆包测试版/E03_视频生成提示词_豆包版.md", "memory/projects/两界食单_豆包测试版/资产注册表.md", "video"),
        ("workspace/两界食单_豆包测试版/E04_视频生成提示词_豆包版.md", "memory/projects/两界食单_豆包测试版/资产注册表.md", "video"),
        ("workspace/两界食单/重要资产图片提示词.md", "memory/projects/两界食单/资产注册表.md", "image"),
        ("workspace/两界食单/E01_视频生成提示词.md", "memory/projects/两界食单/资产注册表.md", "video"),
        ("workspace/科普大赛2026/重要资产图片提示词.md", "memory/projects/我在南沙造火箭/资产注册表.md", "image"),
        ("workspace/科普大赛2026/E01_视频生成提示词.md", "memory/projects/我在南沙造火箭/资产注册表.md", "video"),
    ]
    # 旧代际样张豁免：示范剧集为 V1 历史格式（P2-I 将加代际头注），不入审
    LEGACY_SKIP = {"workspace/示范剧集_苍穹与烟火"}
    listed = {t[0] for t in AUDIT_TARGETS}

    # ── 自动发现：新剧集文档免改脚本入审（注册表按同名目录约定寻位）──
    for doc in sorted(ROOT.glob("workspace/*/*.md")):
        rel = doc.relative_to(ROOT).as_posix()
        if rel in listed or doc.parent.name.startswith("_") or f"workspace/{doc.parent.name}" in LEGACY_SKIP:
            continue
        if doc.name.startswith("重要资产图片提示词"):
            kind = "image"
        elif re.match(r"E\d+", doc.name) and "视频生成提示词" in doc.name:
            kind = "video"
        else:
            continue
        reg = ROOT / "memory/projects" / doc.parent.name / "资产注册表.md"
        if reg.exists():
            AUDIT_TARGETS.append((rel, reg.relative_to(ROOT).as_posix(), kind))
        else:
            AUDIT_TARGETS.append((rel, "", kind))
            warnings.append(f"[DISCOVER_NO_REG] 自动发现 {rel}，但未找到 memory/projects/{doc.parent.name}/资产注册表.md——@资产对账降级（仅查名称合法性）")

    for rel_doc, rel_reg, kind in AUDIT_TARGETS:
        audit_workspace_doc(
            ROOT / rel_doc,
            ROOT / rel_reg if rel_reg else ROOT / "_无注册表.md",
            require_media_prefix=(kind == "image"),
            check_no_at_in_image=(kind == "image"),
            errors=errors,
            stats=stats,
            optional=True,  # 本地管理目录缺失=跳过警告（fresh-clone 可运行）
            warnings=warnings,
        )
    # 审 KB_05、黑名单 18~45、VIS-01 蒙太奇B计划
    audit_kb05_style_packs(errors)
    audit_blacklist(errors)
    audit_montage_plan_b(errors)

    print("=" * 72)
    if warnings:
        print(f"⚠️ [L1 WARNINGS] — {len(warnings)} 条提示（不计入门禁，供 R7 维度核查/用户关注）：")
        for w in warnings:
            print(f"  · {w}")
    if errors:
        print(f"❌ [L1 MACHINE GATE: FAILED] — 共检出 {len(errors)} 处硬性违规（强制打回，请立即修复）：")
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
        print("🧠 [交棒 L2 · R7 维度核查必答单]（每维必引证据：Prompt 行/镜头卡字段/注册表行；无证据=判缺失；缺一即打回·不打总分）：")
        print("   [生图八层] ①句首媒介（PACK-XX 维度①） ②表情+正向构图锚 ③身份骨相记忆点+@注册在案 ④服饰四件套 ⑤单一姿态（微距配饰已剥离） ⑥空间三层/背景规范 ⑦光影轨道逐字（跨轨=缺层） ⑧尾锁+画幅规格；全层横切：崩坏词/语言纯净")
        print("   [视频 8 维] ①镜头规格（卡列↔Prompt 一致） ②构图（竖屏铁律） ③人物站位（象限+体型差+绑定） ④透视与空间（三层分句无悖论） ⑤一致性（@注册/骨相≤2/锁挂载/禁词零命中） ⑥连续性（轴线/光位/StateDiff） ⑦动作与时间（节点齐+单一主动作链；B级须时长声明） ⑧台词音色口型（五要素+口型锁；无台词须静默声明）")
        print("   [实验路径⑤启用时] ⑦维按段级口径（区间=段内镜数+图N绑定）；⑤维段内禁复述外貌")
        print("=" * 72)
        sys.exit(0)

if __name__ == "__main__":
    main()
