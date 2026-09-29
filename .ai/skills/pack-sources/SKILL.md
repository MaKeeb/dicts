---
name: pack-sources
description: Add or update a language's dictionary data for MaKeeb: choosing a word-list and next-word source, checking licences (no GPL), pinning downloads, and where the builder code lives. Use when adding a language, changing a source, or answering a licence question about a pack.
---

# Pack sources

The builder lives in the app repository: `../app/makeeb/tools/dictionaries` (`PackSpecs`, `DictionaryBuilder`, the Leipzig counters). This repository only publishes what it builds, so a new language is a change there, then a release here.

## Current sources

| Data | Source | Licence |
|---|---|---|
| Word lists: de, es, fr, it, nl, pl, pt_BR, sv, en_US | AOSP LatinIME `dictionaries/<locale>_wordlist.combined.gz` at commit `8dd31a28ae774c0f5cd43404ad4b78bf46e5aeb6` | Apache-2.0 |
| Hungarian word list | counted from the Leipzig `hun_news_2024_1M` corpus: Hungarian letters only, seen at least 3 times, at most 300k words | CC BY 4.0 |
| Next-word statistics | Leipzig news corpora (`<lang>_news_2024_1M`; Swedish `swe_news_2023_1M`), 1 sentence in 250 held out for evaluation | CC BY 4.0 |

Pack licence: `Apache-2.0 AND CC-BY-4.0`, or `CC-BY-4.0` for Hungarian. `NOTICE.md` has the hashes and attribution.

## Adding a language

1. **Find a word list with frequencies.** AOSP LatinIME has cs, da, el, en_GB, fi, hr, iw, lt, lv, nb, pt_PT, ro, ru, sl, sr and tr at the pinned commit. Otherwise derive one from a Leipzig corpus as for Hungarian.
2. **Check the licence.** Apache-2.0, MIT, CC BY and CC BY-SA are fine. GPL and LGPL are never used (App Store), and neither is "non-commercial" data. Record the exact licence and the attribution text.
3. **Pin it.** Add the source to `PackSpecs` with its URL, SHA-256 and a mirror if there is one. The build fails on any hash mismatch.
4. **Language data.** The keyboard's accents and layouts for the language live in `../app/makeeb/engine/layout/data/languages/<tag>.json`; a pack without them still types, but offers no accents.
5. **Offensive words.** AOSP lists carry `possibly_offensive` flags. A corpus-derived list needs its own list, reviewed by a native speaker (the Hungarian one is in the builder's `CorpusWordList.kt`).
6. **Notices.** Update the app's `THIRD_PARTY_NOTICES.md` and this repository's `NOTICE.md` in step.
7. Build, check the pack's golden words, then publish (`publish-packs`).

## Traps

- Corpus-derived lists keep names and typos that recur; a minimum count and a letters-only filter keep most of them out. Capitalisation comes from use inside a sentence (90% rule), so "Hello" may be stored as a name. The app prefers another selected language's exact word over it.
- `pt` resolves to `pt_BR`; choosing between variants needs app UI first.
