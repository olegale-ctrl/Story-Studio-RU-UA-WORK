# Full original Story Studio: pinned Git submodule

The complete upstream repository is referenced through Git submodule `upstream/konlu-full`.

- Upstream: https://github.com/konlu/story-studio
- Pinned commit: `87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1`
- `.gitmodules` contains only the public upstream URL.
- The entire upstream version is available after `git submodule update --init --recursive` (including Chinese corpora and assets) and lives in its own isolated directory. The existing 40 upstream technical files under `upstream/konlu-story-studio/` are an additional directly committed, byte-for-byte engineering reference.
- Root RU/UA application must NOT depend on or execute this submodule by default.
- Upstream `LICENSE` at the pinned revision is CC BY-NC-SA 4.0: noncommercial, attribution and share-alike restrictions apply. Review separately before redistribution. No commercial Professional or Cloud use without written permission or rights-cleared alternative.
- Do not use unreviewed Chinese corpora, Writing-DNA, example scenarios, media, assets or voice service integrations in release packages.
- Since submodule files do not live in the parent Git tree, updates to upstream are explicitly controlled by changing the pinned SHA and reviewing differences.

Example commands:

```powershell
git submodule update --init --recursive
git -C upstream/konlu-full rev-parse HEAD
```

The RU/UA Sprint 25 local source was not in the destination repository at the moment this note was written. It must be imported separately, while preserving original upstream licenses and our `MASTER_PROMPT.md`.
