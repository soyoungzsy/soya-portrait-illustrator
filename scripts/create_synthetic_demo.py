#!/usr/bin/env python3
"""Create original geometric fixtures and run the offline library workflow."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from ip_library import outside_source


def create_masters(folder):
    folder.mkdir(parents=True)
    cutout = Image.new("RGBA", (600, 800))
    d = ImageDraw.Draw(cutout)
    # An invented geometric mascot, without a reference photo or real identity.
    d.rounded_rectangle((145, 75, 455, 355), radius=105, fill="#F1C597", outline="#264653", width=10)
    d.pieslice((140, 20, 460, 310), 180, 355, fill="#264653")
    d.ellipse((215, 200, 235, 220), fill="#264653")
    d.ellipse((365, 200, 385, 220), fill="#264653")
    d.arc((260, 240, 340, 290), 0, 180, fill="#264653", width=7)
    d.rounded_rectangle((120, 365, 480, 725), radius=75, fill="#E76F51", outline="#264653", width=10)
    d.polygon(((120, 410), (55, 520), (100, 555), (190, 440)), fill="#E76F51")
    d.polygon(((470, 410), (545, 320), (575, 355), (500, 510)), fill="#E76F51")
    d.ellipse((535, 295, 590, 360), fill="#F1C597", outline="#264653", width=6)
    cutout.save(folder / "cutout.png")
    square = Image.new("RGBA", (800, 800), "#FFF8EE")
    square.alpha_composite(cutout.resize((540, 720)), (130, 60))
    square.save(folder / "square.png")


def run(*args):
    subprocess.run([sys.executable, str(Path(__file__).with_name("ip_library.py")), *map(str, args)], check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    out = outside_source(args.out)
    if out.exists():
        p.error("choose a new --out directory")
    create_masters(out / "synthetic-inputs")
    brief = {"schema_version": "1.0", "title": "把想法变成小实验", "point": "先验证一个小假设，再决定下一步。"}
    (out / "brief.json").write_text(json.dumps(brief, ensure_ascii=False), encoding="utf-8")
    run("record", "--library", out / "library", "--identity-id", "demo-mascot", "--style", "anime",
        "--square", out / "synthetic-inputs/square.png", "--cutout", out / "synthetic-inputs/cutout.png",
        "--synthetic", "--confirmed")
    run("build", "--library", out / "library", "--version", "v0001", "--brief", out / "brief.json", "--out", out / "first-share")
    brief["title"] = "让好奇心多走一步"
    (out / "next-brief.json").write_text(json.dumps(brief, ensure_ascii=False), encoding="utf-8")
    run("build", "--library", out / "library", "--version", "v0001", "--brief", out / "next-brief.json", "--out", out / "next-share")
    print(f"Synthetic only; no image service was called. Open {out / 'first-share/preview.html'}")


if __name__ == "__main__":
    main()
