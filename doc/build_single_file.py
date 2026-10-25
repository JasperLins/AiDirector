# -*- coding: utf-8 -*-
"""
build_single_file.py — 把 training.html 里的 ../reference/运镜50/N.png 引用
压缩（≈820px JPEG）并内嵌为 base64，原地写回，生成"单文件版"。

【2026-10-25 退役注记】reference/运镜50/ 图片载体已按用户裁决移除（减包）——
本脚本转为退役护栏：图片源不存在时直接提示退出；training.html（已内嵌版）
继续可用，重新生成 training 页面需用户日后自行恢复图片源。

用法：python doc/build_single_file.py
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
    if not IMGDIR.exists():
        print("[退役] reference/运镜50/ 已于 2026-10-25 移除（减包裁决）——无可内嵌图片源，脚本退出。")
        return
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
