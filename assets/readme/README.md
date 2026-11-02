# README assets

SVG figures for the repository and profile READMEs, generated from the
**iam.alan.abreu Brand System v1.0.0** tokens. No external stylesheet, no web font,
no `<script>`, no `foreignObject` — only shapes, gradients, paths and text, so GitHub
renders them identically everywhere.

| File | Used by | Size |
|---|---|---|
| `hero.svg` | repository README | 1200×420 |
| `architecture.svg` | repository README | 1200×710 |
| `shared-copies.svg` | repository README | 1200×360 |
| `hero-ai-devsecops.svg` | `profiles/ai-devsecops-engineer/README.md` | 1200×340 |
| `hero-ai-engineer.svg` | `profiles/ai-engineer/README.md` | 1200×340 |
| `hero-software-engineer.svg` | `profiles/software-engineer/README.md` | 1200×340 |
| `footer.svg` | repository README | 1200×132 |

## Tokens

| Token | HEX | Use here |
|---|---|---|
| Ink 950 | `#09070D` | canvas |
| Charcoal 800 | `#17141F` | canvas mid-stop |
| Purple 700 | `#5B21B6` | gradient start |
| Purple 500 | `#7C3AED` | gradient midpoint, strokes, shapes |
| Lavender 300 | `#C4B5FD` | eyebrow labels, connectors, emphasis |
| Paper 50 | `#F7F7F5` | headings, symbol body |

Fonts: `Inter` with a system fallback stack. Weight 400 / 600 / 700. No font binary is
bundled.

## Regenerate

```sh
python3 assets/readme/generate.py                       # writes all 7 SVG
python3 assets/readme/audit.py assets/readme            # geometry gate
python3 assets/readme/audit-contrast.py assets/readme   # contrast + size gate
```

Both audits exit non-zero on failure, so they can run in CI unchanged.

## Two gates, not one

Contrast ratio and legibility are separate concerns, and passing one does not pass the
other. Both are measured, never eyeballed:

**`audit.py`** — deterministic geometry, 8px connector clearance:

1. every text bbox inside the viewBox
2. no text bbox partially overlapping a node rect
3. no connector segment within 8px of a text bbox
4. no two node rects overlapping
5. every arrowhead landing on a node edge, not floating

**`audit-contrast.py`** — two independent passes:

1. numeric: every text fill ≥ 4.5:1 against every dark surface it can sit on
2. size: every text run ≥ 18 SVG units (≈12.9 CSS px at GitHub's ~860px column)

### Two rules these gates caught

**Purple 500 is not a text colour.** `#7C3AED` is the brand interactive accent, but on
Ink 950 it reaches only **3.52:1** — it fails 4.5:1 as type. Purple 500 therefore stays
on shapes, strokes and gradients; type uses `#A78BFA` (7.36:1). The brand is unchanged;
only the surface each tone is allowed to touch is constrained.

**Error state never stands alone.** Colour-only encoding of state is a WCAG 1.4.1 (Use of
Color) failure even when the contrast number passes. These figures carry no error state
today; if one is added it must ship a second channel — an icon, the literal text `ERRO`,
or a distinct border style. A passing ratio is not permission to encode state by hue.

## Adding a figure

1. Add a function to `generate.py` using the shared `head()`, `T()`, `node()` helpers.
2. Reserve a gutter for every connector; route around labels, never through them.
3. Put annotations in a full-width band **outside** the flow lane, never between nodes.
4. Run both audits. They must print `ALL CLEAR` before the asset is committed.
