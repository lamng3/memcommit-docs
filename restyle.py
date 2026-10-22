#!/usr/bin/env python3
"""Give a sibling manual the MemCommit manual's design: this stylesheet with the project's accent, and the same header.

    python3 restyle.py ../kroma-docs                  # new manual: stylesheet, header, favicon
    python3 restyle.py ../kroma-docs --favicon-only   # an already restyled manual, keeping its own CSS

Run the first form once per manual; it overwrites style.css. The page builders (or, for hand-written pages, the pages themselves) are patched in place.
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
    "memcommit-docs": dict(name="MemCommit", mark="M", accent="#0c6b52", dark="#3ddc9f", repo="lamng3/memcommit",
                           links=[("Install", "install.html"), ("Concepts", "concepts.html"), ("API", "api.html")], files=["build.py"]),
    "ontodb-docs": dict(name="OntoDB", mark="O", accent="#6d28d9", dark="#a78bfa", repo="lamng3/OntoDB",
                        links=[("Install", "install.html"), ("Tutorial", "tutorial.html"), ("SPARQL", "sparql.html")], files=["build.py"]),
    "kroma-docs": dict(name="KROMA", mark="K", accent="#c2410c", dark="#fb923c", repo="lamng3/kroma",
                       links=[("Pipeline", "pipeline.html"), ("Query", "query.html"), ("CLI", "cli.html")], files=["build.py"]),
    "aegis-docs": dict(name="Aegis", mark="A", accent="#1f5fae", dark="#6ea8ff", repo="lamng3/aegis",
                       links=[("Start", "getting-started.html"), ("Attacks", "attacks.html"), ("Reference", "reference.html")], files=["build.py"]),
    "hermes-docs": dict(name="Hermes", mark="H", accent="#be185d", dark="#f472b6", repo="lamng3/hermes",
                        links=[("Algebra", "algebra.html"), ("Verifier", "verifier.html"), ("Benchmarks", "benchmarks.html")], files=["build.py"]),
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


ICON = '<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'


def favicon(root, p):
    """favicon.svg in the project's accent, linked from every page and every page template."""
    mark = p["mark"]
    size = 15 if len(mark) == 1 else 11
    (root / "favicon.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="{p["accent"]}"/>'
        f'<text x="16" y="22" text-anchor="middle" font-family="system-ui,sans-serif" font-weight="700" font-size="{size + 5}" fill="#fff">{mark}</text></svg>\n'
    )
    link = '<link rel="stylesheet" href="style.css">'
    for f in [*root.glob("*.html"), *root.glob("*.py")]:
        text = f.read_text()
        if link in text and "favicon.svg" not in text:
            f.write_text(text.replace(link, ICON + link))


def main(target, favicon_only=False):
    root = Path(target).resolve()
    p = PROJECTS[root.name]
    if favicon_only:
        favicon(root, p)
        print(f"{root.name}: favicon")
        return
    (root / "style.css").write_text(stylesheet(p["accent"], p["dark"]))
    files = [root / f for f in p["files"]] if p["files"] else sorted(root.glob("*.html"))
    for f in files:
        f.write_text(patch(f.read_text(), p))
    favicon(root, p)
    print(f"{root.name}: stylesheet, {len(files)} file(s), favicon")


if __name__ == "__main__":
    main(sys.argv[1], "--favicon-only" in sys.argv)
