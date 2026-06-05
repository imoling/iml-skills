#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: preview_pptx.sh <pptx> <output-dir> [size]" >&2
  exit 2
fi

pptx="$1"
out_dir="$2"
size="${3:-1672}"

mkdir -p "$out_dir"
qlmanage -t -s "$size" -o "$out_dir" "$pptx"

preview="$out_dir/$(basename "$pptx").png"
if [[ -f "$preview" ]]; then
  echo "preview_png=$preview"
else
  echo "preview_pptx.sh: preview was requested but no PNG was found at $preview" >&2
  exit 1
fi
