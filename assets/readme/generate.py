#!/usr/bin/env python3
"""GitHub-safe SVG assets for hermes-engineering-profiles.

Tokens: iam.alan.abreu Brand System v1.0.0
  Ink 950 #09070D · Charcoal 800 #17141F · Purple 700 #5B21B6
  Purple 500 #7C3AED · Lavender 300 #C4B5FD · Paper 50 #F7F7F5

Type scale is set for GitHub's ~860px content column (1200-unit asset, 0.717 factor):
  node title  22u -> 15.8px   sub label 18u -> 12.9px
  body copy   21u -> 15.1px   metadata  14u -> 10.0px (non-essential only)

Geometry rules enforced (see audit_svg.py):
  - no connector crosses a label (8px clearance)
  - annotation bands sit outside the flow lane
  - arrowheads pulled back 3px so they never touch a node border
"""

from pathlib import Path

INK = "#09070D"
CHARCOAL = "#17141F"
PURPLE_700 = "#5B21B6"
PURPLE_500 = "#7C3AED"
LAVENDER = "#C4B5FD"
PAPER = "#F7F7F5"
DEEP = "#2E1065"
MUTED = "#B4ACC6"
# #7C3AED is the brand interactive accent but only reaches 3.52:1 as text on
# Ink 950, so type uses the lighter brand tone (#A78BFA, 7.36:1). Purple 500
# stays on shapes, strokes and gradients where contrast rules do not apply.
ACCENT_TEXT = "#A78BFA"

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

SYMBOL_PATHS = [
    ("M500 92 C528 92 548 108 563 137 L926 874 C947 916 922 952 875 952 H711 L486 494 "
     "C468 458 439 458 421 494 L199 952 H42 C-5 952 -29 913 -9 872 L385 137 C401 108 422 92 450 92 Z",
     PAPER, "1"),
    ("M446 92 C419 92 398 108 382 137 L-8 872 C-29 913 -5 952 42 952 H202 L514 305 "
     "C531 270 510 234 472 234 H410 Z", "url(#gPurple)", "1"),
    ("M150 772 C275 708 377 628 487 553 C561 503 629 502 694 547 C730 572 758 608 783 656 "
     "L720 791 C689 741 657 714 617 704 C577 694 540 706 499 733 C401 800 314 872 231 927 "
     "C189 955 137 945 111 909 C81 867 96 805 150 772 Z", "url(#gDeep)", "1"),
    ("M183 771 C304 704 398 629 494 565 C550 528 601 522 650 541 C599 536 559 552 516 581 "
     "C414 649 322 724 207 790 C173 810 148 839 140 873 C124 830 141 795 183 771 Z",
     LAVENDER, "0.25"),
]


def defs():
    return f"""  <defs>
    <linearGradient id="gPurple" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{PURPLE_700}"/>
      <stop offset="0.52" stop-color="{PURPLE_500}"/>
      <stop offset="1" stop-color="{LAVENDER}"/>
    </linearGradient>
    <linearGradient id="gDeep" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{DEEP}"/>
      <stop offset="0.70" stop-color="{PURPLE_700}"/>
      <stop offset="1" stop-color="{PURPLE_500}"/>
    </linearGradient>
    <linearGradient id="gBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{INK}"/>
      <stop offset="0.62" stop-color="{CHARCOAL}"/>
      <stop offset="1" stop-color="#130A25"/>
    </linearGradient>
    <linearGradient id="gRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{PURPLE_500}" stop-opacity="0.0"/>
      <stop offset="0.10" stop-color="{LAVENDER}" stop-opacity="0.45"/>
      <stop offset="1" stop-color="{PURPLE_700}" stop-opacity="0.0"/>
    </linearGradient>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" markerHeight="5.5"
            orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{LAVENDER}"/>
    </marker>
  </defs>
"""


def symbol(x, y, size, opacity="1.0"):
    sc = size / 1000.0
    body = "".join(f'      <path d="{d}" fill="{f}" opacity="{o}"/>\n' for d, f, o in SYMBOL_PATHS)
    return f'  <g transform="translate({x} {y}) scale({sc})" opacity="{opacity}">\n{body}  </g>\n'


def T(x, y, s, size, fill=PAPER, weight="400", anchor="start", family=FONT, ls="0"):
    return (f'  <text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}">{s}</text>\n')


def eyebrow(x, y, s):
    return T(x, y, s, 18, LAVENDER, "600", "start", MONO, "1.6")


def rule(x1, y, x2, grad=True):
    stroke = "url(#gRule)" if grad else "#2A2440"
    return f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{stroke}" stroke-width="1"/>\n'


def bg(w, h):
    return f'  <rect width="{w}" height="{h}" fill="url(#gBg)"/>\n'


def head(w, title_lines, eyebrow_text, h):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="tt dd">']
    s.append(f'  <title id="tt">{title_lines[0]}</title>\n')
    s.append(f'  <desc id="dd">{eyebrow_text}</desc>\n')
    s.append(defs())
    s.append(bg(w, h))
    return s


# ------------------------------------------------------------------- 1. hero
def hero_root():
    w, h = 1200, 420
    s = head(w, ["Hermes Engineering Profiles"], "Base versionada com tres especialistas independentes.", h)
    s.append(symbol(768, 50, 480, "0.12"))
    s.append(symbol(896, 106, 296))
    s.append(rule(72, 72, 580))
    s.append(eyebrow(72, 56, "IAM.ALAN.ABREU  //  SYS.001"))
    s.append(T(72, 156, "Hermes Engineering", 54, PAPER, "700", ls="-1.2"))
    s.append(T(72, 212, "Profiles", 54, LAVENDER, "700", ls="-1.2"))
    s.append(T(72, 260, "Três especialistas independentes.", 21, "#CFCADD"))
    s.append(T(72, 290, "Uma base versionada, auditável,", 21, "#CFCADD"))
    s.append(T(72, 320, "sem estado de cliente, conta ou cloud.", 21, "#CFCADD"))
    cw, gap, cy = 178, 14, 348
    for i, label in enumerate(["DEVSECOPS", "AI ENGINEERING", "SOFTWARE"]):
        accent = i == 0
        s.append(f'  <rect x="{72 + i * (cw + gap)}" y="{cy}" width="{cw}" height="44" rx="8" '
                 f'fill="{"#1C1630" if accent else "#12101A"}" '
                 f'stroke="{"#C4B5FD" if accent else "#3B3350"}" stroke-width="1"/>\n')
        s.append(T(72 + i * (cw + gap) + cw / 2, cy + 28, label, 18,
                   LAVENDER if accent else "#B9B2C9", "600", "middle"))
    s.append(T(1128, 396, "v0.1.0", 18, "#8F87A6", "500", "end", MONO, "1.4"))
    s.append("</svg>\n")
    return "".join(s)


# ------------------------------------------------------- 2. profile heroes
PROFILES = [
    dict(idx="01 / 03", slug="ai-devsecops-engineer", file="hero-ai-devsecops.svg",
         accent=ACCENT_TEXT, a="DevSecOps and", b="Reliability",
         l1="Infraestrutura, segurança, GitOps e confiabilidade.",
         l2="Do estado observado a um resultado autorizado e verificado.",
         skills="8 SKILLS", scope="INFRA · SEC · SRE"),
    dict(idx="02 / 03", slug="ai-engineer", file="hero-ai-engineer.svg",
         accent=LAVENDER, a="AI", b="Engineering",
         l1="Agentes, providers, RAG, avaliação e LLMOps.",
         l2="Sistemas de IA com guardrails, medição e custo explícito.",
         skills="8 SKILLS", scope="AGENTS · RAG · EVALS"),
    dict(idx="03 / 03", slug="software-engineer", file="hero-software-engineer.svg",
         accent="#A78BFA", a="Software", b="Engineering",
         l1="Full-stack, SaaS, APIs, ferramentas locais e qualidade.",
         l2="Produto real, comportamento verificado, sem complexidade extra.",
         skills="12 SKILLS", scope="PRODUCT · API · QUALITY"),
]


def hero_profile(p):
    w, h = 1200, 340
    s = head(w, [f'{p["a"]} {p["b"]}'], f'Perfil {p["slug"]}.', h)
    s.append(symbol(868, 62, 340, "0.11"))
    s.append(symbol(974, 126, 146, "0.8"))
    s.append(rule(72, 68, 540))
    s.append(eyebrow(72, 52, f"PROFILE {p['idx']}  //  {p['skills']}"))
    s.append(T(72, 142, p["a"], 46, PAPER, "700", ls="-1"))
    s.append(T(72, 192, p["b"], 46, p["accent"], "700", ls="-1"))
    s.append(T(72, 238, p["l1"], 18, "#CFCADD"))
    s.append(T(72, 264, p["l2"], 18, "#CFCADD"))
    s.append(rule(72, 288, 700, grad=False))
    s.append(T(72, 314, p["slug"], 18, LAVENDER, "600", "start", MONO, "0.6"))
    s.append(T(1128, 314, p["scope"], 18, "#8F87A6", "500", "end", MONO, "1.4"))
    s.append("</svg>\n")
    return "".join(s)


# ---------------------------------------------------- 3. architecture figure
def architecture():
    import math
    w, h = 1200, 710
    s = head(w, ["Fluxo: tres fontes, tres distribuicoes, quatro portoes"],
             "shared-skills, catalog.json e distribution.yaml alimentam tres profiles, que passam por build, validate, tests e install.", h)

    def node(x, y, bw, bh, title, subs, accent=False, tsize=20):
        stroke = LAVENDER if accent else "#332C4A"
        fill = "#1A1430" if accent else "#120F1C"
        out = (f'  <rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="1.2"/>\n')
        out += T(x + 20, y + 40, title, tsize, PAPER if accent else "#EDE8F5", "600", family=MONO, ls="0.1")
        for i, sub in enumerate(subs):
            out += T(x + 20, y + 74 + i * 27, sub, 18, MUTED)
        return out

    def arrow(x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        return (f'  <line x1="{x1}" y1="{y1}" x2="{x2 - 3 * dx / n:.1f}" y2="{y2 - 3 * dy / n:.1f}" '
                f'stroke="{LAVENDER}" stroke-width="1.4" opacity="0.7" marker-end="url(#ar)"/>\n')

    def dash(points):
        pts = [(float(x), float(y)) for x, y in points]
        (px, py), (qx, qy) = pts[-2], pts[-1]
        dx, dy = qx - px, qy - py
        n = math.hypot(dx, dy) or 1
        pts[-1] = (qx - 3 * dx / n, qy - 3 * dy / n)
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return (f'  <polyline points="{p}" fill="none" stroke="{LAVENDER}" stroke-width="1.3" '
                f'opacity="0.5" stroke-dasharray="6 5" marker-end="url(#ar)"/>\n')

    ROWS = [172, 320, 468]
    CEN = [y + 58 for y in ROWS]

    s.append(eyebrow(72, 50, "MECANISMO  //  SYS.002"))
    s.append(T(72, 92, "Uma fonte, três distribuições,", 42, PAPER, "600", ls="-0.5"))
    s.append(T(72, 128, "zero cópia manual", 42, LAVENDER, "600", ls="-0.5"))
    s.append(rule(72, 150, 1128, grad=False))

    # col 1 — the three sources  72..340
    s.append(node(72, ROWS[0], 268, 128, "shared-skills/", ["2 skills", "fonte única"]))
    s.append(node(72, ROWS[1], 268, 128, "catalog.json", ["inventário", "24 skills / 3 profiles"]))
    s.append(node(72, ROWS[2], 268, 128, "distribution.yaml", ["manifesto", "feature floor v0.22.5"]))

    # col 2 — the three distributions  402..732
    for i, slug in enumerate(["ai-devsecops-engineer", "ai-engineer", "software-engineer"]):
        s.append(node(402, ROWS[i], 330, 128, slug, ["profiles/ · 1 distribuicão"], accent=True))

    # col 3 — gates  790..970
    s.append(node(790, ROWS[0], 180, 128, "build", ["gera as cópias", "--write aplica"]))
    s.append(node(790, ROWS[1], 180, 128, "validate", ["contratos", "falha fechada"]))
    s.append(node(790, ROWS[2], 180, 128, "tests", ["suite + evals", "evidência"]))

    # col 4 — native install  1008..1128
    s.append(node(1008, ROWS[2], 120, 128, "Hermes", ["profile", "install"], accent=True, tsize=18))

    # fan-out: three sources -> one rail -> the three distributions
    for y in CEN:
        s.append(f'  <line x1="340" y1="{y}" x2="370" y2="{y}" stroke="{LAVENDER}" '
                 f'stroke-width="1.3" opacity="0.5" stroke-dasharray="6 5"/>\n')
    s.append(f'  <line x1="370" y1="{CEN[0]}" x2="370" y2="{CEN[2]}" stroke="{LAVENDER}" '
             f'stroke-width="1.3" opacity="0.5"/>\n')
    for y in CEN:
        s.append(arrow(370, y, 402, y))

    # fan-in: the three distributions -> one rail -> build
    for y in CEN:
        s.append(f'  <line x1="732" y1="{y}" x2="760" y2="{y}" stroke="{LAVENDER}" '
                 f'stroke-width="1.3" opacity="0.55"/>\n')
    s.append(f'  <line x1="760" y1="{CEN[0]}" x2="760" y2="{CEN[2]}" stroke="{LAVENDER}" '
             f'stroke-width="1.3" opacity="0.55"/>\n')
    s.append(arrow(760, CEN[0], 790, CEN[0]))

    # pipeline
    s.append(arrow(880, ROWS[0] + 128, 880, ROWS[1]))
    s.append(arrow(880, ROWS[1] + 128, 880, ROWS[2]))
    s.append(arrow(970, CEN[2], 1008, CEN[2]))

    # annotation band — full width, outside the flow lane
    s.append(rule(72, 640, 1128, grad=False))
    s.append(T(72, 668, "As cópias compartilhadas são geradas por build: edite shared-skills/ e rode --write.", 18, MUTED))
    s.append(T(72, 692, "Nunca edite profiles/*/skills/ à mão — o validador falha fechado.", 18, MUTED))
    s.append("</svg>\n")
    return "".join(s)


# ------------------------------------------------------- 4. shared-copy figure
def shared_copies():
    import math
    w, h = 1200, 430
    s = head(w, ["Duas skills compartilhadas geram seis copias geradas"],
             "agent-folder-architect e project-context-architect existem uma vez em shared-skills.", h)

    def node(x, y, bw, bh, title, sub, accent=False):
        stroke = LAVENDER if accent else "#332C4A"
        fill = "#1A1430" if accent else "#120F1C"
        return (f'  <rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="1.2"/>\n'
                + T(x + 20, y + 38, title, 22, PAPER if accent else "#EDE8F5", "600", family=MONO, ls="0.2")
                + T(x + 20, y + 68, sub, 18, MUTED))

    def route(points):
        pts = [(float(x), float(y)) for x, y in points]
        (px, py), (qx, qy) = pts[-2], pts[-1]
        dx, dy = qx - px, qy - py
        n = math.hypot(dx, dy) or 1
        pts[-1] = (qx - 3 * dx / n, qy - 3 * dy / n)
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return (f'  <polyline points="{p}" fill="none" stroke="{LAVENDER}" stroke-width="1.3" '
                f'opacity="0.5" stroke-dasharray="6 5" marker-end="url(#ar)"/>\n')

    s.append(eyebrow(72, 50, "REGRA  //  SYS.003"))
    s.append(T(72, 94, "Duas skills compartilhadas, seis cópias geradas", 40, PAPER, "600", ls="-0.4"))
    s.append(rule(72, 118, 1128, grad=False))

    s.append(node(72, 142, 300, 104, "shared-skills/", "2 skills · fonte única", accent=True))
    targets = ["ai-devsecops-engineer", "ai-engineer", "software-engineer"]
    for i, t in enumerate(targets):
        y = 142 + i * 84
        s.append(node(788, y, 340, 72, t, "skills/ · 2 cópias geradas"))
        s.append(route([(372, 194), (720, 194), (720, y + 36), (788, y + 36)]))

    s.append(rule(72, 396, 1128, grad=False))
    s.append(T(72, 422, "Editar uma cópia gerada cria drift: o build a sobrescreve ou o validador falha.", 18, MUTED))
    s.append("</svg>\n")
    return "".join(s)


# ------------------------------------------------------------- 5. footer mark
def footer():
    w, h = 1200, 132
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="ftT ftD">']
    s.append('  <title id="ftT">iam.alan.abreu - DEVSECOPS</title>\n')
    s.append('  <desc id="ftD">Secure by design. Built to evolve.</desc>\n')
    s.append(defs())
    s.append(f'  <rect width="{w}" height="{h}" fill="{INK}"/>\n')
    s.append(rule(0, 1, w))
    s.append(symbol(58, 34, 64))
    s.append(T(142, 62, "iam.alan.abreu", 22, PAPER, "600", ls="0.2"))
    s.append(T(142, 90, "DEVSECOPS", 18, LAVENDER, "600", "start", MONO, "2.2"))
    s.append(T(1142, 62, "Secure by design.", 18, "#CFCADD", "500", "end"))
    s.append(T(1142, 90, "Built to evolve.", 18, LAVENDER, "600", "end"))
    s.append("</svg>\n")
    return "".join(s)


def main():
    out = Path("/tmp/readme-assets")
    out.mkdir(parents=True, exist_ok=True)
    files = {"hero.svg": hero_root(), "architecture.svg": architecture(),
             "shared-copies.svg": shared_copies(), "footer.svg": footer()}
    for p in PROFILES:
        files[p["file"]] = hero_profile(p)
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
    for f in sorted(out.iterdir()):
        print(f.name, f.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
