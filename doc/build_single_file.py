# -*- coding: utf-8 -*-
"""
build_single_file.py — 把 training.html 里的 ../reference/运镜50/N.png 引用
压缩（≈820px JPEG）并内嵌为 base64，原地写回，生成"单文件版"。

用法：python doc/build_single_file.py
以后修改了 training.html（含新增图片引用）后重跑本脚本即可重新内嵌；
没有待内嵌引用时脚本会直接退出（幂等）。
"""
import base64
import io
import re
import sys
from pathlib import Path

from PIL import Image

try:  # Windows 控制台中文输出
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "doc" / "training.html"
IMGDIR = ROOT / "reference" / "运镜50"
MAX_WIDTH = 820
JPEG_QUALITY = 82

PAT = re.compile(r"\.\./reference/运镜50/(\d+)\.png")


def to_data_uri(png: Path) -> str:
    im = Image.open(png).convert("RGB")
    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    nums = sorted({int(m.group(1)) for m in PAT.finditer(html)})
    if not nums:
        print("没有发现待内嵌的图片引用（可能已内嵌），无需处理。")
        return
    print(f"待内嵌 {len(nums)} 张：{nums}")
    added = 0

    def repl(m: "re.Match[str]") -> str:
        nonlocal added
        n = int(m.group(1))
        src = IMGDIR / f"{n}.png"
        if not src.exists():
            print(f"  缺失 {n}.png，跳过")
            return m.group(0)
        uri = to_data_uri(src)
        added += len(uri)
        print(f"  内嵌 {n}.png -> {len(uri) // 1024} KB")
        return uri

    html = PAT.sub(repl, html)
    HTML.write_text(html, encoding="utf-8")
    print(f"完成：新增 {added // 1024} KB；training.html 总大小 {HTML.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
