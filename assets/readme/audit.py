#!/usr/bin/env python3
"""Deterministic geometry audit for the generated README SVGs.

Checks, per figure:
  1. every text bbox inside the viewBox
  2. no text bbox crosses a node rect (unless fully contained)
  3. no connector segment crosses a text bbox (8px clearance required)
  4. no two node rects overlap
  5. arrow endpoint clearance from the target border
"""
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PAD = 8.0  # required clearance between connectors and text


def bbox_of_text(el):
    x = float(el.get("x")); y = float(el.get("y"))
    fs = float(el.get("font-size"))
    s = el.text or ""
    mono = "mono" in (el.get("font-family") or "").lower()
    ls = float(el.get("letter-spacing") or 0)
    w = len(s) * (fs * (0.62 if mono else 0.545) + ls)
    a = el.get("text-anchor", "start")
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return (x0, y - fs * 0.80, w, fs * 1.02, s)


def seg_rect(x1, y1, x2, y2, rect, pad=0.0):
    rx, ry, rw, rh = rect
    rx -= pad; ry -= pad; rw += 2 * pad; rh += 2 * pad
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - rx), (dx, rx + rw - x1), (-dy, y1 - ry), (dy, ry + rh - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                if t > t1:
                    return False
                t0 = max(t0, t)
            else:
                if t < t0:
                    return False
                t1 = min(t1, t)
    return True


def rects_intersect(a, b):
    ax, ay, aw, ah = a[:4]
    bx, by, bw, bh = b[:4]
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def audit(path):
    root = ET.parse(path).getroot()
    vb = root.get("viewBox").split()
    W, H = float(vb[2]), float(vb[3])
    rects, texts, segs, issues = [], [], [], []

    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag == "rect" and el.get("width"):
            w, h = float(el.get("width")), float(el.get("height"))
            if w > 40 and h >= 56 and not (w >= W - 1 and h >= H - 1):  # node, not canvas/chip
                rects.append((float(el.get("x", 0)), float(el.get("y", 0)), w, h))
        elif tag == "text":
            texts.append(bbox_of_text(el))
        elif tag == "line" and el.get("marker-end"):
            segs.append(("line", [(float(el.get("x1")), float(el.get("y1"))),
                                  (float(el.get("x2")), float(el.get("y2")))]))
        elif tag == "polyline":
            nums = [float(v) for v in el.get("points").replace(",", " ").split()]
            pts = list(zip(nums[0::2], nums[1::2]))
            segs.append(("poly", pts))

    # 1. inside canvas
    for x, y, w, h, s in texts:
        if x < 0 or y < 0 or x + w > W + 0.5 or y + h > H + 0.5:
            issues.append(f"OUT-OF-CANVAS text '{s[:34]}' x={x:.0f}..{x+w:.0f} y={y:.0f}..{y+h:.0f} (canvas {W:.0f}x{H:.0f})")

    # 2. text vs node rect (partial overlap only)
    for x, y, w, h, s in texts:
        for i, r in enumerate(rects):
            if rects_intersect((x, y, w, h), r):
                inside = (x >= r[0] and y >= r[1] and x + w <= r[0] + r[2] + 0.5
                          and y + h <= r[1] + r[3] + 0.5)
                if not inside:
                    issues.append(f"TEXT-OVERLAP '{s[:34]}' vs rect#{i} {tuple(round(v) for v in r)}")

    # 3. connectors vs text, 8px clearance
    for kind, pts in segs:
        pairs = list(zip(pts, pts[1:])) if kind == "poly" else [tuple(pts)]
        for (x1, y1), (x2, y2) in pairs:
            for x, y, w, h, s in texts:
                if seg_rect(x1, y1, x2, y2, (x, y, w, h), pad=PAD):
                    issues.append(f"CONNECTOR-CROSSES-TEXT ({x1:.0f},{y1:.0f})->({x2:.0f},{y2:.0f}) '{s[:34]}'")

    # 4. rect overlaps
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            if rects_intersect(rects[i], rects[j]):
                issues.append(f"RECT-OVERLAP {tuple(round(v) for v in rects[i])} x {tuple(round(v) for v in rects[j])}")

    # 5. arrowhead clearance
    for kind, pts in segs:
        if kind == "line":
            (x1, y1), (x2, y2) = pts
        else:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
        best = min((math.hypot(max(r[0] - x2, 0, x2 - (r[0] + r[2])),
                               max(r[1] - y2, 0, y2 - (r[1] + r[3]))) for r in rects),
                   default=999)
        if best > 12:
            issues.append(f"ARROW-FLOATING end=({x2:.0f},{y2:.0f}) nearest node edge {best:.1f}px")

    return W, H, len(rects), len(texts), len(segs), issues


def main():
    files = sorted(Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/readme-assets").glob("*.svg"))
    bad = 0
    for f in files:
        W, H, nr, nt, ns, issues = audit(f)
        status = "PASS" if not issues else f"FAIL ({len(issues)})"
        print(f"{f.name:28s} {W:.0f}x{H:.0f}  nodes={nr} texts={nt} connectors={ns}  {status}")
        for i in issues:
            print(f"    - {i}")
        bad += len(issues)
    print(f"\n{'ALL CLEAR' if bad == 0 else str(bad) + ' ISSUE(S)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
