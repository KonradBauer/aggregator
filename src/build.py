# -*- coding: utf-8 -*-
"""Sklada index.html: src/page.html + assety base64 (fonty, loga, favicon).

Uruchomienie:  python src/build.py
Wynik:         index.html w korzeniu repo
"""
import base64
import io
import os

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
ASSETS = os.path.join(SRC, "assets")
OUT = os.path.join(ROOT, "index.html")

# TODO: uzupelnic prawdziwymi danymi przed publikacja (stopka, sekcja kontakt)
LEGAL_NAME = "MKCRAFT"
PHONE = "+48000000000"
PHONE_DISPLAY = "+48 000 000 000"
EMAIL = "kontakt@mkcraft.com.pl"
ADDRESS_STREET = "ul. Przykladowa 1"
ADDRESS_POSTAL = "00-000"
ADDRESS_CITY = "Miasto"


def b64(fn):
    with open(os.path.join(ASSETS, fn), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def main():
    tpl = io.open(os.path.join(SRC, "page.html"), encoding="utf-8").read()
    tpl = tpl.replace("{FONT_LATIN}", b64("archivo-latin.woff2"))
    tpl = tpl.replace("{FONT_LATINEXT}", b64("archivo-latinext.woff2"))
    tpl = tpl.replace("{LOGO_GYM}", b64("mkgym-logo.png"))
    tpl = tpl.replace("{LOGO_MCRAFT}", b64("mcraft-logo.png"))
    tpl = tpl.replace("{FAVICON}", b64("favicon-64.png"))
    tpl = tpl.replace("{LEGAL_NAME}", LEGAL_NAME)
    tpl = tpl.replace("{PHONE_DISPLAY}", PHONE_DISPLAY)
    tpl = tpl.replace("{PHONE}", PHONE)
    tpl = tpl.replace("{EMAIL}", EMAIL)
    tpl = tpl.replace("{ADDRESS_STREET}", ADDRESS_STREET)
    tpl = tpl.replace("{ADDRESS_POSTAL}", ADDRESS_POSTAL)
    tpl = tpl.replace("{ADDRESS_CITY}", ADDRESS_CITY)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(tpl)
    print("written", OUT, len(tpl) // 1024, "KB")


if __name__ == "__main__":
    main()
