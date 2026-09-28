# thomaspinder.github.io

This user site exists only to keep the **retired Impulso docs URL**,
`https://thomaspinder.github.io/Impulso/`, working after the repository moved to
[QuantClimate/Impulso](https://github.com/QuantClimate/Impulso) and the docs moved
to [impulso.quantclimate.com](https://impulso.quantclimate.com/).

GitHub does not redirect Pages sites when a repository is transferred. It also
deletes the repository redirect if anything is created at the old
`thomaspinder/Impulso` path. So the redirect lives here instead: once the project
site left, this repo's `Impulso/` folder started serving that path.

## What's in it

- `Impulso/<path>.html`: one stub per page in the old sitemap (155 of them). Each
  has a canonical link, a 0-second meta refresh, and JS that keeps `?query` and
  `#fragment`. The path is unchanged; only the host changes.
- `404.html`: catches everything else under `/Impulso/`, in any case (static
  assets, `_sources/`, unlisted pages), and sends it to the same path on the new
  host.
- `.nojekyll`: **required**. Without it Jekyll drops every `_`-prefixed path,
  including all of `Impulso/_modules/`.
- `build_legacy_redirect.py` + `impulso-sitemap-2026-09-28.xml`: the generator and
  the snapshot it was built from.

Regenerate with:

```bash
python build_legacy_redirect.py impulso-sitemap-2026-09-28.xml .
```

## Rules

- **Never set a custom domain on this site.** A user-site custom domain re-homes
  every other `thomaspinder` project site under it.
- **Never create a repository named `Impulso` under `thomaspinder`.** That
  includes forking `QuantClimate/Impulso` into this account without renaming it.
  Doing so permanently deletes GitHub's redirect from the old repository URL.
- Keep this repository indefinitely.
