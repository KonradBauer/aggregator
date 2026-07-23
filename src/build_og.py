# -*- coding: utf-8 -*-
"""Generuje og-image.jpg, favicon.png, apple-touch-icon.png oraz
src/assets/favicon-64.png (wpinany potem do index.html przez build.py).

Pipeline: sklada strony OG/favicon z szablonow, screenshotuje headless
Edge/Chrome, skaluje przez Pillow do docelowych rozmiarow.

Uruchomienie:  python src/build_og.py
Wymaga:        Pillow, Microsoft Edge lub Chrome
"""
import base64
import io
import os
import subprocess
import tempfile

from PIL import Image

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
ASSETS = os.path.join(SRC, "assets")

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def browser():
    for p in BROWSERS:
        if os.path.exists(p):
            return p
    raise RuntimeError("brak Edge/Chrome do headless screenshotu")


def b64(fn):
    with open(os.path.join(ASSETS, fn), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def render(template):
    t = io.open(os.path.join(SRC, template), encoding="utf-8").read()
    t = t.replace("{FONT_LATIN}", b64("archivo-latin.woff2"))
    t = t.replace("{FONT_LATINEXT}", b64("archivo-latinext.woff2"))
    return t


def screenshot(html, width, height, out_png):
    with tempfile.TemporaryDirectory() as td:
        page = os.path.join(td, "page.html")
        io.open(page, "w", encoding="utf-8").write(html)
        subprocess.run(
            [
                browser(),
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--virtual-time-budget=3000",
                f"--window-size={width},{height}",
                f"--screenshot={out_png}",
                "file:///" + page.replace(os.sep, "/"),
            ],
            check=True,
            capture_output=True,
        )


def save(shot, size, dst, **kw):
    im = Image.open(shot).convert("RGB").resize(size, Image.LANCZOS)
    im.save(dst, optimize=True, **kw)
    print("saved", dst, size, os.path.getsize(dst) // 1024, "KB")


def main():
    with tempfile.TemporaryDirectory() as td:
        og_shot = os.path.join(td, "og.png")
        fav_shot = os.path.join(td, "fav.png")
        screenshot(render("og-page.html"), 1200, 630, og_shot)
        screenshot(render("favicon-page.html"), 256, 256, fav_shot)

        save(og_shot, (1200, 630), os.path.join(ROOT, "og-image.jpg"), quality=87)
        save(fav_shot, (180, 180), os.path.join(ROOT, "apple-touch-icon.png"))
        save(fav_shot, (64, 64), os.path.join(ASSETS, "favicon-64.png"))
        save(fav_shot, (32, 32), os.path.join(ROOT, "favicon.png"))

    print("uwaga: po zmianie favicon-64.png odpal tez src/build.py")


if __name__ == "__main__":
    main()
