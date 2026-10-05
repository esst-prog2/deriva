#!/usr/bin/env bash
# hw4 spike: does deriva load the 2022, 2023 and 2024 persona dictionaries unchanged?
# Runs deriva on 2021 vs each year, then 2024 vs 2025 (are they the same?), and saves
# all terminal output to spike/output.txt.
# Uses --labels-template (same reader, no cosmetic/real verdicts) so the held-out
# middle-round pair stays unseen; the CSVs it writes go to a throwaway temp dir.
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
# Keep the venv out of iCloud-synced Documents (see PLANNING_LOG.md).
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-$HOME/.venvs/deriva}"
out="$root/spike/output.txt"
work="$(mktemp -d)"
base="$root/data/Diccionario de Datos_persona_anual_2021.xlsx"

{
  echo "deriva spike — $(date '+%Y-%m-%d %H:%M:%S') — commit $(git -C "$root" rev-parse --short HEAD)"
  for year in 2022 2023 2024; do
    other="$(ls "$root"/data/Diccionario\ de\ Datos_person*_anual_"$year".xlsx)"
    echo
    echo "=== 2021 vs $year: $(basename "$other") ==="
    (cd "$work" && uv run --project "$root" deriva --labels-template "$base" "$other")
    echo "exit code: $?"
  done

  y2024="$root/data/Diccionario de Datos_persona_anual_2024.xlsx"
  y2025="$root/data/Diccionario de Datos_persona_anual_2025.xlsx"
  echo
  echo "=== 2024 vs 2025: $(basename "$y2024") vs $(basename "$y2025") ==="
  (cd "$work" && uv run --project "$root" deriva --labels-template "$y2024" "$y2025")
  echo "exit code: $?"
} > "$out" 2>&1

rm -rf "$work"
cat "$out"
