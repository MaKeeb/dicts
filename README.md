# MaKeeb dictionaries

Dictionary packs for [MaKeeb](https://github.com/MaKeeb/app), an on-screen keyboard for Android and iOS. The MaKeeb app downloads them during setup or from Settings, checks each against its SHA-256, and the keyboard then uses them offline.

The packs are the assets of this repository's [releases](https://github.com/MaKeeb/dicts/releases); the app reads `catalogue.json` from the latest one. This repository holds the notices and the publishing script, not the packs.

| Language | Word list | Next words | Licence |
|---|---|---|---|
| Deutsch, Español, Français, Italiano, Nederlands, Polski, Português (Brasil), Svenska | AOSP LatinIME | Leipzig news corpora | Apache-2.0 AND CC-BY-4.0 |
| Magyar | Leipzig Hungarian news corpus | Leipzig news corpus | CC-BY-4.0 |

English is built into the app. Sources, hashes and attribution: [NOTICE.md](NOTICE.md).

## Publishing

Packs are built by the app repository (`./gradlew :tools:dictionaries:packRelease`), then published from here:

```
scripts/publish.sh --check               # verify the release folder
scripts/publish.sh packs-YYYY-MM-DD      # create the release (new tag every time)
```

The scripts in this repository are MIT licensed; each pack carries its own licence.
