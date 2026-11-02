#!/usr/bin/env python3
"""Contrast + legibility audit for the README SVGs.

Thresholds come from the beautify-github-readme canvas reference, which judges type
at its rendered size inside GitHub's ~860px content column (0.717 of the 1200-unit
viewBox):

  essential diagram text   >= 20 SVG units  (~14.3 CSS px)
  supporting labels        >= 18 SVG units  (~12.9 CSS px)
  section titles           >= 40 SVG units  (~28.7 CSS px)
  below 18 units           non-essential metadata or decoration ONLY

Contrast: every text fill must reach 4.5:1 against every dark surface it can sit on.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RENDER = 860.0 / 1200.0

SURFACES = {"ink": "#09070D", "charcoal": "#17141F",
            "node": "#120F1C", "node_accent": "#1A1430"}

# SVG-unit thresholds
TITLE_MIN = 40.0
ESSENTIAL_MIN = 20.0
SUPPORT_MIN = 18.0


def srgb(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b)


def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/readme-assets")
    files = sorted(out.glob("*.svg"))
    problems = 0

    for f in files:
        root = ET.parse(f).getroot()
        worst = {}
        runs = []
        for el in root.iter():
            if el.tag.rsplit("}", 1)[-1] != "text":
                continue
            fill = el.get("fill") or ""
            size = float(el.get("font-size"))
            txt = (el.text or "").strip()
            runs.append((size, txt))
            if not fill.startswith("#"):
                continue
            for name, bgc in SURFACES.items():
                r = ratio(fill, bgc)
                key = (fill, name)
                if key not in worst or r < worst[key]:
                    worst[key] = r

        fails = 0
        low = [(fg, s, round(r, 2)) for (fg, s), r in worst.items() if r < 4.5]
        small = [(s, round(s * RENDER, 1), t) for s, t in runs
                 if s < SUPPORT_MIN and t]

        print(f"\n{f.name}")
        print(f"  runs={len(runs)}  sizes={sorted({s for s, _ in runs})}  "
              f"rendered {min(s for s, _ in runs) * RENDER:.1f}-{max(s for s, _ in runs) * RENDER:.1f}px")

        if low:
            fails += len(low)
            print(f"  FAIL contrast ({len(low)}):")
            for fg, s, r in low:
                print(f"    {fg} on {s} = {r}:1")
        else:
            print("  contrast: PASS (every fill >= 4.5:1 on every surface)")

        if small:
            fails += len(small)
            print(f"  FAIL size (<{SUPPORT_MIN}u = non-essential only) ({len(small)}):")
            for s, rp, t in small:
                print(f"    {s}u -> {rp}px  '{t[:50]}'")
        else:
            print(f"  size: PASS (min {min(s for s, _ in runs)}u >= {SUPPORT_MIN}u)")

        # verify the figures carry a real title at the section-title size
        if f.name in ("architecture.svg", "shared-copies.svg"):
            if max(s for s, _ in runs) < TITLE_MIN:
                fails += 1
                print(f"  FAIL title: largest run {max(s for s, _ in runs)}u < {TITLE_MIN}u")

        problems += fails

    print(f"\n{'ALL CLEAR' if problems == 0 else str(problems) + ' ISSUE(S)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
