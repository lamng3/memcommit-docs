# MemCommit Manual

The manual for [MemCommit](https://github.com/lamng3/memcommit), a transactional memory layer for agents: declaring a memory structure, recording sessions, keeping notes with an index and tools, offline consolidation ("dreaming"), search, working-memory tiers, audit, the command line, benchmarks, and how the log works inside.

The site is static HTML. `python3 build.py` regenerates the pages from `content/`. Each page's front matter names its `part` (Getting started, Using MemCommit, Reference, Internals, Project) and its `order` within that part. The Decisions page is generated from `../memcommit/docs/decisions.md` on every build; do not edit `content/decisions.md` by hand.

## The live demo

The home page replays a log exported from the real library. After changing the scenario in `demo_data.py`, regenerate it
and rebuild (the build needs the library's Python, so use `uv run` from `../memcommit`):

```bash
cd ../memcommit && uv run python ../memcommit-docs/demo_data.py && uv run python ../memcommit-docs/build.py
```

## Shared structure

`normalize.py` (a copy of the one in `memcommit-docs`) runs at the end of the build. It gives every content page a search box, an "On this page" list, previous and next links, and one title format, and writes `search-index.json`. It is called by `build.py`.
