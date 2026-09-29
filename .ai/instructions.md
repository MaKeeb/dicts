# MaKeeb dicts: agent instructions

Dictionary packs for MaKeeb, an on-screen keyboard for Android and iOS. The packs are published as the assets of this repository's GitHub releases, with a `catalogue.json` the app reads to offer and verify downloads; the repository itself holds the notices, the documentation and the publishing script, never the packs. This file is the single source of instructions for every AI tool: `AGENTS.md` (Codex), `CLAUDE.md`, `CODEX.md`, `GEMINI.md` and `.github/copilot-instructions.md` are symlinks to it. Edit only `.ai/instructions.md`. Skills live in `.ai/skills` and are linked from `.claude/skills`, `.agents/skills` (Codex, Gemini CLI), `.codex/skills` and `.github/skills`; agents live in `.ai/agents`, linked from `.claude/agents` and `.github/agents`.

This is the `MaKeeb/dicts` repository (GitHub org MaKeeb). Its siblings sit next to it in the workspace: `../app` (the keyboard, `MaKeeb/app`, which builds the packs) and `../site` (the website, `MaKeeb/site`).

## Layout

```
NOTICE.md               sources, licences and attribution of the pack data (kept in step with the app's THIRD_PARTY_NOTICES.md)
LICENSE                 MIT, for this repository's own scripts and docs (the packs carry their own licences)
scripts/
  publish.sh            verify a release folder and create the GitHub release (--check: verify only)
  check_catalogue.py    catalogue ↔ files check; writes the release notes
.ai/                    instructions.md (this file), agents/, skills/, commands/, plans/; local/ is untracked
```

## Hard rules (never break these)

- **Never commit a pack.** `.mkd` files, catalogues and release folders go to GitHub releases only; `.gitignore` blocks them. A pack in git history bloats every clone for good.
- **Published releases are immutable.** Never replace, delete or re-upload an asset of a published release: installed apps have its SHA-256. A new build gets a new tag (`packs-YYYY-MM-DD`); `publish.sh` refuses an existing tag.
- **Every pack is verified before it is published.** `scripts/publish.sh` checks `SHA256SUMS` and that each catalogue entry matches its file's size and SHA-256. Don't upload by hand around it.
- **The catalogue stays format 1 and its URLs stay relative** (`"url": "<file>"`), so one release works from any mirror. A format change needs an app release that reads it first.
- **No GPL data, ever** (the App Store). Share-alike (CC BY-SA) is acceptable, and a pack built from it is CC BY-SA. Every source is pinned by SHA-256 in the app's builder.
- **Attribution travels with the data.** Release notes list each pack's attribution (generated from the catalogue), and `NOTICE.md` names every source. CC BY requires it.

## How the app uses this

- The app's catalogue URL (`makeeb.packs.catalogueUrl` in `../app/makeeb/gradle.properties`) is `https://github.com/MaKeeb/dicts/releases/latest/download/catalogue.json`, so a new release reaches installed apps without an app update. Packs are downloaded by the companion app only; the keyboard maps installed packs and never uses the network.
- GitHub serves release assets without a login only for public repositories, and the app downloads without one, so this repository stays public.
- The app's build downloads `en_US.mkd` from the same release, pinned by SHA-256 (`PackSpecs.ENGLISH_US_RELEASE_SHA256` in `../app/makeeb/tools/dictionaries`); a release with a different `en_US.mkd` needs that pin bumped.

## Build and test

The packs are built in the app repository:

```
cd ../app/makeeb && ./gradlew :tools:dictionaries:packRelease   # → tools/dictionaries/build/pack-release/
cd ../../dicts
scripts/publish.sh --check                                        # verify the release folder
scripts/publish.sh packs-YYYY-MM-DD                               # publish (needs gh, logged in with repo access)
```

After publishing, check the release page, then test a download on a device (the app's `docs/dictionaries/pack-catalogue.md` has the device checks).

## Conventions

- Work is tracked on the app's board (`../app/.ai/kanban`, worked with the `kanban` skill; packs are APP-37). One commit per finished, verified task, its subject starting with the card's ticket (`APP-37: What changed`). No Co-Authored-By or other AI attribution trailers. Push only when asked; publishing a release counts as pushing.
- **This repository is public:** never commit secrets (tokens, keys), real IP addresses or device identifiers, and never a pack (above).
- Investigation notes, logs and scratch files go under `.ai/local/` (not tracked).

## Skills, agents, plans

- `.ai/skills/publish-packs`: building, verifying and publishing a release, and pointing the app at it.
- `.ai/skills/pack-sources`: adding or updating a language: choosing a source, licences, pinning, and where the builder lives.
- `.ai/agents/dicts-reviewer.agent.md`: reviews changes for committed packs, licence and attribution gaps, catalogue integrity and release immutability.
- `.ai/plans/roadmap.md`: pointing the app at the releases, reviews, more languages.
