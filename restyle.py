#!/usr/bin/env python3
"""Give a sibling manual the MemCommit manual's design: this stylesheet with the project's accent, and the same header.

    python3 restyle.py ../kroma-docs

Run once per manual. The page builders (or, for hand-written pages, the pages themselves) are patched in place.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TikTok+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
"""

PROJECTS = {
    "ontodb-docs": dict(name="OntoDB", mark="O", accent="#6d28d9", dark="#a78bfa", repo="lamng3/OntoDB",
                        links=[("Install", "install.html"), ("Tutorial", "tutorial.html"), ("SPARQL", "sparql.html")], files=["build.py"]),
    "kroma-docs": dict(name="KROMA", mark="K", accent="#c2410c", dark="#fb923c", repo="lamng3/kroma",
                       links=[("Pipeline", "pipeline.html"), ("Query", "query.html"), ("CLI", "cli.html")], files=["build.py"]),
    "aegis-docs": dict(name="Aegis", mark="A", accent="#1f5fae", dark="#6ea8ff", repo="lamng3/aegis",
                       links=[("Start", "getting-started.html"), ("Attacks", "attacks.html"), ("Reference", "reference.html")], files=["build.py"]),
    "agentic-ontologist-docs": dict(name="Agentic Ontologist", mark="AO", accent="#0d857a", dark="#2dd4bf", repo="lamng3/agentic-ontologist",
                                    links=[("Start", "getting-started.html"), ("Agents", "agents.html"), ("Architecture", "architecture.html")], files=None),
}


def rgb(hex_):
    return ", ".join(str(int(hex_[i : i + 2], 16)) for i in (1, 3, 5))


def stylesheet(accent, dark):
    css = (HERE / "style.css").read_text()
    css = css.replace("#0c6b52", accent).replace("12, 107, 82", rgb(accent))
    css = css.replace("#3ddc9f", dark).replace("61, 220, 159", rgb(dark))
    return css


def header(p):
    links = "\n".join(f'    <a href="{href}">{label}</a>' for label, href in p["links"])
    brand = p["name"]
    return f"""<header class="site">
  <a class="logo" href="index.html"><span class="logo-mark">{p["mark"]}</span><span>{brand}</span></a>
  <nav class="site">
{links}
    <label class="nav-button" for="nav-toggle">Menu</label>
    <a href="https://github.com/{p["repo"]}" class="pill">GitHub ↗</a>
  </nav>
</header>"""


def patch(text, p):
    text = re.sub(r'<header class="top">.*?</header>', lambda _: header(p), text, flags=re.S)
    if "fonts.googleapis.com" not in text:
        text = text.replace('<link rel="stylesheet" href="style.css">', FONTS + '<link rel="stylesheet" href="style.css">')
    return text


def main(target):
    root = Path(target).resolve()
    p = PROJECTS[root.name]
    (root / "style.css").write_text(stylesheet(p["accent"], p["dark"]))
    files = [root / f for f in p["files"]] if p["files"] else sorted(root.glob("*.html"))
    for f in files:
        f.write_text(patch(f.read_text(), p))
    print(f"{root.name}: stylesheet, {len(files)} file(s)")


if __name__ == "__main__":
    main(sys.argv[1])
