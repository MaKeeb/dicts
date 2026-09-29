---
name: publish-packs
description: Build, verify and publish a MaKeeb dictionary release (the packs, catalogue.json and en_US.mkd as GitHub release assets) and point the app at it. Use when publishing new or updated dictionaries, or when app downloads fail.
---

# Publish a dictionary release

## 1. Build the release folder (app repository)

```
cd ../app/makeeb
./gradlew :tools:dictionaries:packRelease
ls tools/dictionaries/build/pack-release/    # <lang>.mkd …, en_US.mkd, catalogue.json, SHA256SUMS
```

The first build downloads the pinned sources, about 2.6 GB of word lists and Leipzig corpora, into `tools/dictionaries/build/downloads/` and caches their counts; later builds reuse them. Every pack is read back and checked at build time (golden words, accent folds, completions, next words).

## 2. Verify

```
scripts/publish.sh --check
```

It checks `SHA256SUMS`, that each catalogue entry matches its file's size and SHA-256, that URLs are the bare file names, and that no pack is missing from the catalogue.

## 3. Publish

```
gh auth status                               # an account with write access to MaKeeb/dicts
scripts/publish.sh packs-YYYY-MM-DD          # a new tag every time; never reuse one
```

The release is created as the latest, with notes listing each pack's words, size, licence and attribution. Installed apps pick it up through `releases/latest/download/catalogue.json`.

Never edit or replace the assets of a published release: apps hold their SHA-256. To withdraw a broken pack, publish a new release without it (or with a fixed one).

## 4. Point the app at it (first time only)

In `../app/makeeb/gradle.properties`:

```
makeeb.packs.catalogueUrl=https://github.com/MaKeeb/dicts/releases/latest/download/catalogue.json
```

- The repository must stay public: GitHub serves release assets without a login only for public repositories, and the app downloads without one.
- With the URL set, the app's build downloads `en_US.mkd` from the release instead of rebuilding it; its SHA-256 is pinned in `PackSpecs.ENGLISH_US_RELEASE_SHA256`. Bump the pin when a release changes `en_US.mkd`; otherwise builds fall back to building it (slow, but correct).

## 5. Check on devices

Settings → Languages → pick one with a pack → Dictionaries → Download. Watch the progress, then type in the language (accents restored, next words). The app's `docs/dictionaries/pack-catalogue.md` lists the full device checks (offline, cancel, update, remove, iOS without Full Access).

## Traps

- `latest` follows the release marked latest; a draft or pre-release is not served to apps.
- Asset names must match the catalogue's `file` exactly (case-sensitive; `pt_BR.mkd`).
- Downloads reveal the user's IP address and chosen language to GitHub; the privacy policy (`../site`) says so. If hosting moves, update it.
