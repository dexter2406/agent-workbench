#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"
python "$script_dir/import-third-party-skill.py" "$@"
