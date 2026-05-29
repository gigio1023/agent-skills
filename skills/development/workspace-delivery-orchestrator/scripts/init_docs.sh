#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [target_dir]" >&2
}

if [ "$#" -gt 1 ]; then
  usage
  exit 2
fi

target_dir="${1:-.}"
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
skill_dir="$(CDPATH= cd -- "$script_dir/.." && pwd)"
templates_dir="$skill_dir/assets/templates"

if [ ! -d "$templates_dir" ]; then
  echo "error: templates directory not found: $templates_dir" >&2
  exit 1
fi

if [ -e "$target_dir" ] && [ ! -d "$target_dir" ]; then
  echo "error: target is not a directory: $target_dir" >&2
  exit 1
fi
mkdir -p "$target_dir"

copy_if_missing() {
  src="$1"
  dst="$2"
  if [ ! -f "$src" ]; then
    echo "error: missing template: $src" >&2
    return 1
  fi
  if [ -e "$dst" ]; then
    echo "skip: $dst"
    return 0
  fi
  cp "$src" "$dst"
  echo "create: $dst"
}

copy_if_missing "$templates_dir/plan.template.md" "$target_dir/plan.md"
copy_if_missing "$templates_dir/progress.template.md" "$target_dir/progress.md"
copy_if_missing "$templates_dir/result.template.md" "$target_dir/result.md"
