#!/bin/sh
# Publishes a dictionary release: the packs, catalogue.json, en_US.mkd and SHA256SUMS that
# `./gradlew :tools:dictionaries:packRelease` wrote in the app repository.
#
#   scripts/publish.sh <tag> [release-dir]      verify, then create the GitHub release
#   scripts/publish.sh --check [release-dir]    verify only
#
# release-dir defaults to the app checkout next to this one. Tags are never reused: a
# published release is immutable, and a new build gets a new tag (packs-YYYY-MM-DD).
set -eu

repo=MaKeeb/dicts
default_dir="$(cd "$(dirname "$0")/.." && pwd)/../app/makeeb/tools/dictionaries/build/pack-release"

if [ "${1:-}" = "--check" ]; then
  tag=""
  dir=${2:-$default_dir}
else
  tag=${1:?usage: scripts/publish.sh <tag> [release-dir] | --check [release-dir]}
  dir=${2:-$default_dir}
fi

[ -f "$dir/catalogue.json" ] || { echo "no catalogue.json in $dir: run ./gradlew :tools:dictionaries:packRelease in the app" >&2; exit 1; }

echo "checking $dir"
(cd "$dir" && shasum -a 256 -c SHA256SUMS >/dev/null) || { echo "SHA256SUMS does not match the files" >&2; exit 1; }
notes=$(mktemp)
python3 "$(dirname "$0")/check_catalogue.py" "$dir" "$notes"

[ -z "$tag" ] && { echo "release folder OK"; exit 0; }

if gh release view "$tag" --repo "$repo" >/dev/null 2>&1; then
  echo "release $tag already exists: releases are immutable, use a new tag" >&2
  exit 1
fi

gh release create "$tag" --repo "$repo" --title "Dictionaries $tag" --notes-file "$notes" --latest \
  "$dir"/catalogue.json "$dir"/SHA256SUMS "$dir"/*.mkd
echo "published $tag"
echo "catalogue: https://github.com/$repo/releases/latest/download/catalogue.json"
