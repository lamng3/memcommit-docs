# MemCommit Manual

The manual for [MemCommit](https://github.com/lamng3/memcommit), a transactional memory layer for agents: declaring a memory structure, recording sessions, keeping notes with an index and tools, offline consolidation ("dreaming"), search, working-memory tiers, audit, the command line, benchmarks, and how the log works inside.

The site is static HTML. `python3 build.py` regenerates the pages from `content/`. Each page's front matter names its `part` (Getting started, Using MemCommit, Reference, Internals, Project) and its `order` within that part. The Decisions page is generated from `../memcommit/docs/decisions.md` on every build; do not edit `content/decisions.md` by hand.
