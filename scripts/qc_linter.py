#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AiDirector 双擎联审门禁 · L1 硬核语法与数学检查器 (scripts/qc_linter.py)
职责分工：
  - L1 (本脚本): 查风格包禁词、变量外壳残留、句首媒介前置、资产注册表跨文件对账、
                 视频秒级时间轴数学规范、[details]零空行封包法、蒙太奇B计划落位、
                 技能 YAML 头完整性（SKILL_FRONTMATTER_*，2026-10-25 立·黑名单 47）。
  - L2 (R7 智能体): 在本脚本 PASS 后，按 KB_10 V3 维度制（视频 8 维/生图八层）执行证据核查——
                 每维必引证据（Prompt 行/镜头卡字段/注册表行），无证据=判缺失；缺一即打回，不打总分（2026-10-25 维度制立法）。
"""
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. 主代码块禁词与未展开外壳（2026-10-25 按画风包分流：通用外壳/版式禁词全包生效，
#    包级排斥禁词按项目注册表第五节 PACK-XX 绑定取表——修 PACK-02 A 轨词组被误杀缺口，
#    "环形无影棚/Flat Lit Albedo/正交投影相机" 在 PACK-02 项目是 KB_06 A 轨立法必挂词）
COMMON_FORBIDDEN_IN_PROMPT = [
    "严禁设定集排版",
    "严禁多视图分格",
    "画中画特写",
    "@画风锁",
    "[光位锁",
    "体积光替换为",
    "体积光氛围替换为",
]

# PACK-01 专属禁词（A 轨摄影工程词 + 写实引力词 = 漫剧包排斥项）
PACK01_ONLY_FORBIDDEN = [
    "环形无影棚",
    "Flat Lit Albedo",
    "正交投影相机",
    "写实厚涂",
    "8K电影感",
    "电影感构图",
    "毛孔可见",
    "轻熟",
]

# PACK-02 专属禁词（KB_05 PACK-02 ④画种排斥表：绘画/卡通引力词）
PACK02_ONLY_FORBIDDEN = [
    "插画",
    "漫剧",
    "二次元",
    "厚涂笔触",
    "平涂",
    "赛璐璐",
    "水墨晕染",
    "卡通渲染",
    "过度磨皮塑料感",
]

# PACK-03 专属禁词（我在南沙造火箭注册表第五节登记的 ④表全量）
PACK03_ONLY_FORBIDDEN = [
    "二维平涂",
    "赛璐璐硬边",
    "水彩手绘",
    "真人实拍写真",
    "粗粝毛孔",
    "塑料反光过曝",
    "低多边形",
]

PACK_FORBIDDEN_MAP = {
    "PACK-01": COMMON_FORBIDDEN_IN_PROMPT + PACK01_ONLY_FORBIDDEN,
    "PACK-02": COMMON_FORBIDDEN_IN_PROMPT + PACK02_ONLY_FORBIDDEN,
    "PACK-03": COMMON_FORBIDDEN_IN_PROMPT + PACK03_ONLY_FORBIDDEN,
    "PACK-04": COMMON_FORBIDDEN_IN_PROMPT,  # PACK-04 ④禁词表未立法前仅通用表
}

VALID_MEDIA_PREFIXES = (
    "国风仙侠漫剧插画",
    "现代都市漫剧插画",
    # PACK-03 3D 国漫 CG 系句首媒介（KB_05 四节 ①句首前置词 + ②锁文本场景/道具变体）
    "3D国漫次世代CG渲染",
    "3D国漫CG场景渲染",
    "3D国漫CG道具渲染",
    # PACK-02 真人写实系句首媒介（KB_05 PACK-02 ① + 剧集派生乡村/城镇变体，注册表登记后合法）
    "古装真人实拍电影剧照",
    "现代都市真人实拍电影剧照",
    "现代乡村真人实拍电影剧照",
    # PACK-04 赛璐璐系句首媒介（KB_05 PACK-04 ①）
    "二维日式赛璐璐动画番剧作画",
)


def detect_pack(reg_path: Path) -> str:
    """从项目《资产注册表.md》第五节画风绑定声明提取 PACK-XX；无法识别时回落 PACK-01（最保守禁词表，维持历史行为）"""
    if not reg_path.exists():
        return "PACK-01"
    txt = reg_path.read_text(encoding="utf-8")
    m = re.search(r"PACK-0[1-4]", txt)
    return m.group(0) if m else "PACK-01"

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
    forbidden_terms: list = None,
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
    if forbidden_terms is None:
        forbidden_terms = PACK_FORBIDDEN_MAP["PACK-01"]
    pack_label = next(
        (k for k, v in PACK_FORBIDDEN_MAP.items() if v is forbidden_terms), "?"
    )

    for i, p in enumerate(prompts, 1):
        p_clean = p.strip()
        # 1. 检查省略号偷懒
        if "..." in p_clean or ("…" in p_clean and ("（略）" in p_clean or "同上" in p_clean)):
            errors.append(f"[LAZY_ELLIPSIS] {filepath.relative_to(ROOT)} 主代码块 #{i} 含有偷懒省略符")
        # 2. 检查本包禁词与外壳残留（按注册表 PACK 绑定分流，{pack_label} 表）
        for bad in forbidden_terms:
            if bad in p_clean:
                errors.append(f"[FORBIDDEN_TERM] {filepath.relative_to(ROOT)} 主代码块 #{i} 命中禁词/外壳({pack_label}): '{bad}'")
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
        # 7. 块内元话语污染（补丁6·2026-10-26 立）：勘误/词源/注册表/日期等编译器备注禁入 prompt 块
        meta_hit = re.search(r"勘误|注册表|黑名单|词源|脑补|自洽·|R9-\d{8}|20\d{2}-\d{2}-\d{2}", p_clean)
        if meta_hit:
            errors.append(
                f"[META_NOTE_IN_BLOCK] {filepath.relative_to(ROOT)} 主代码块 #{i} 含编译器备注元话语（补丁6 违例·移至核查行）: '{meta_hit.group(0)}'"
            )

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
    for num in range(18, 58):
        if f"| {num} |" not in txt and f"| {num:02d} |" not in txt:
            errors.append(f"[BLACKLIST_INDEX] 全局复盘避坑黑名单第一部分速查表缺少正式编号 {num}")

def audit_skill_frontmatter(errors: list):
    """技能 YAML 头完整性门禁（2026-10-25 立·黑名单 47·技能头损坏·门禁盲区）：
    扫描 skills/ 全部子目录技能 .md（排除 SKILL_INDEX.md），逐文件校验——
      ① 以 --- 开头且存在第二个 --- 闭合头区；
      ② 头区内 name:/description:/required_kbs: 三键各自成完整键行（裸 nam 拼断残行=键缺失）；
      ③ name 值非空；
      ④ 头区内不允许"不以合法键名开头却含冒号"的断裂残行（如法则正文滞留头部+`e: xxx` 拼接残片）。
    损坏计 ERROR 硬失败——修 443b30b 法则迁移劈断 NARR-04 name 字段以"双门禁绿"入库的盲区
    （此前 qc_linter 与 audit_consistency 均不解析技能 YAML 头）。"""
    skills_dir = ROOT / "skills"
    if not skills_dir.exists():
        errors.append("[MISSING_FILE] 找不到 skills/ 目录")
        return
    targets = [p for p in sorted(skills_dir.rglob("*.md")) if p.name != "SKILL_INDEX.md"]
    if not targets:
        errors.append("[SKILL_FRONTMATTER_NO_FILES] skills/ 下未发现任何技能 .md 文件（扫描面异常）")
        return
    for fp in targets:
        rel = fp.relative_to(ROOT)
        lines = fp.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].strip() != "---":
            errors.append(f"[SKILL_FRONTMATTER_OPEN] {rel} 未以 --- 开头，缺 YAML 头")
            continue
        close = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                close = i
                break
        if close is None:
            errors.append(f"[SKILL_FRONTMATTER_CLOSE] {rel} YAML 头未闭合（缺第二个 ---）")
            continue
        header = [ln.strip() for ln in lines[1:close] if ln.strip()]
        keys_seen = set()
        for stripped in header:
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", stripped)
            if m:
                keys_seen.add(m.group(1))
            elif ":" in stripped:
                errors.append(f"[SKILL_FRONTMATTER_BROKEN_LINE] {rel} 头区存在断裂残行（不以合法键名开头却含冒号）: '{stripped[:40]}...'")
        for need in ("name", "description", "required_kbs"):
            if need not in keys_seen:
                errors.append(f"[SKILL_FRONTMATTER_MISSING_KEY] {rel} YAML 头缺少完整键行 '{need}:'")
        name_line = next((s for s in header if s.startswith("name:")), None)
        if name_line is not None and not name_line[len("name:"):].strip():
            errors.append(f"[SKILL_FRONTMATTER_EMPTY_NAME] {rel} name 值为空")

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
        reg_path = ROOT / rel_reg if rel_reg else ROOT / "_无注册表.md"
        audit_workspace_doc(
            ROOT / rel_doc,
            reg_path,
            require_media_prefix=(kind == "image"),
            check_no_at_in_image=(kind == "image"),
            errors=errors,
            stats=stats,
            optional=True,  # 本地管理目录缺失=跳过警告（fresh-clone 可运行）
            warnings=warnings,
            forbidden_terms=PACK_FORBIDDEN_MAP[detect_pack(reg_path)],
        )
    # 审 KB_05、黑名单 18~57、VIS-01 蒙太奇B计划、技能 YAML 头完整性
    audit_kb05_style_packs(errors)
    audit_blacklist(errors)
    audit_montage_plan_b(errors)
    audit_skill_frontmatter(errors)

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
