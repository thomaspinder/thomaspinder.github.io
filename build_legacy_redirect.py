"""Build the thomaspinder.github.io user site that 301-equivalents the old Impulso docs.

GitHub Pages cannot send real 301s, so every page listed in the old sitemap gets a
stub (canonical + meta refresh + JS that keeps ?query and #fragment), and a root
404.html catches everything else under /Impulso/ (static assets, _sources, any
page missing from the sitemap). Paths are carried across unchanged: the new site
has exactly the same layout, just on a new host.

Usage:
    python build_legacy_redirect.py <sitemap.xml> <out_dir>
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import sys

OLD = "https://thomaspinder.github.io/Impulso/"
NEW = "https://impulso.quantclimate.com/"

STUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Impulso documentation has moved</title>
<link rel="canonical" href="{href}">
<meta http-equiv="refresh" content="0; url={href}">
<script>location.replace({js} + location.search + location.hash);</script>
</head>
<body>
<p>The Impulso documentation has moved to <a href="{href}">{href}</a>.</p>
</body>
</html>
"""

NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Page not found</title>
<script>
  // Anything under /Impulso/ that has no stub (assets, _sources, unlisted pages)
  // still lands on the same path on the new host. Case-insensitive on purpose.
  var m = location.pathname.match(/^\\/impulso(\\/.*)?$/i);
  if (m) {
    location.replace("https://impulso.quantclimate.com" + (m[1] || "/") + location.search + location.hash);
  }
</script>
</head>
<body>
<p>Page not found. The Impulso documentation now lives at
<a href="https://impulso.quantclimate.com/">impulso.quantclimate.com</a>.</p>
</body>
</html>
"""


def main(sitemap_path: str, out_dir: str) -> None:
    """Write the redirect site into `out_dir`."""
    out = pathlib.Path(out_dir)
    locs = re.findall(r"<loc>([^<]+)</loc>", pathlib.Path(sitemap_path).read_text())
    paths = sorted({loc[len(OLD) :] for loc in locs if loc.startswith(OLD)})
    if not paths:
        sys.exit(f"no <loc> under {OLD} in {sitemap_path}")

    for rel in paths:
        target = NEW + rel
        stub = out / "Impulso" / rel
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(STUB.format(href=html.escape(target, quote=True), js=json.dumps(target)))

    (out / "404.html").write_text(NOT_FOUND)
    # Without this, Jekyll drops every path starting with `_` (Impulso/_modules/...).
    (out / ".nojekyll").write_text("")
    print(f"wrote {len(paths)} stubs + 404.html + .nojekyll to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
