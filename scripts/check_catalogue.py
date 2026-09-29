"""Checks a release folder against its catalogue.json and writes the release notes.

    check_catalogue.py <release-dir> <notes-file>

Every pack the catalogue lists must be in the folder with the size and SHA-256 it states,
and every .mkd in the folder must be listed (en_US.mkd is the bundled English pack, which the
app's build downloads and is not in the catalogue). Fails with a message on the first problem.
"""
import hashlib
import json
import os
import sys

release, notes_path = sys.argv[1], sys.argv[2]
catalogue = json.load(open(os.path.join(release, "catalogue.json"), encoding="utf-8"))
if catalogue.get("format") != 1:
    sys.exit(f"catalogue format {catalogue.get('format')!r}: this script knows format 1")

packs = catalogue["packs"]
languages = [p["language"] for p in packs]
if len(set(languages)) != len(languages):
    sys.exit(f"a language is listed twice: {languages}")

for pack in packs:
    path = os.path.join(release, pack["file"])
    if not os.path.isfile(path):
        sys.exit(f"{pack['file']} is in the catalogue but not in the folder")
    data = open(path, "rb").read()
    if len(data) != pack["size"]:
        sys.exit(f"{pack['file']}: {len(data)} bytes, the catalogue says {pack['size']}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != pack["sha256"]:
        sys.exit(f"{pack['file']}: SHA-256 {digest}, the catalogue says {pack['sha256']}")
    if pack["url"] != pack["file"]:
        sys.exit(f"{pack['file']}: url {pack['url']!r} must be the file name (relative to the catalogue)")

listed = {p["file"] for p in packs} | {"en_US.mkd"}
extra = sorted(f for f in os.listdir(release) if f.endswith(".mkd") and f not in listed)
if extra:
    sys.exit(f"packs in the folder but not in the catalogue: {extra}")

rows = "\n".join(
    f"| {p['name']} (`{p['language']}`) | {p['words']:,} | {p['size'] / 1_000_000:.1f} MB | {'yes' if p['nextWords'] else 'no'} | {p['licence']} |"
    for p in packs
)
attributions = "\n".join(f"- **{p['name']}:** {p['attribution']}" for p in packs)
with open(notes_path, "w", encoding="utf-8") as notes:
    notes.write(
        "Dictionary packs for MaKeeb. The app reads `catalogue.json` from the latest release and checks every pack "
        "against its SHA-256 before using it.\n\n"
        "| Language | Words | Size | Next words | Licence |\n|---|---|---|---|---|\n"
        f"{rows}\n\n`en_US.mkd` is the English pack the app bundles; its build downloads it from here.\n\n"
        f"## Attribution\n\n{attributions}\n"
    )
print(f"{len(packs)} packs match the catalogue")
