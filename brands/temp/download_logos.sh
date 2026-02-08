#!/usr/bin/env bash
set -euo pipefail

# Path to your merged JSON file
JSON_FILE="merged_uav_companies.json"

# Output folder for logo files
OUT_DIR="logos"
mkdir -p "$OUT_DIR"

echo "Processing $JSON_FILE..."

# Requires jq and curl installed
command -v jq >/dev/null 2>&1 || { echo "jq is required but not installed."; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "curl is required but not installed."; exit 1; }

# Extract every object that has both "website" and "logo_file" (anywhere in the JSON)
jq -r '
  .. | objects
  | select(has("website") and has("logo_file"))
  | [.website, .logo_file]
  | @tsv
' "$JSON_FILE" | while IFS=$'\t' read -r website logo_file; do
    # Skip if website is empty
    if [ -z "$website" ]; then
      echo "  Skipping entry with empty website"
      continue
    fi

    # Normalize website (drop trailing slash) and build favicon URL
    website_trimmed="${website%/}"
    url="${website_trimmed}/favicon.ico"

    out_path="${OUT_DIR}/${logo_file}"

    echo "  Downloading: $url -> $out_path"

    # Download favicon as "logo". Ignore failures but log them.
    if ! curl -L --fail --silent --show-error "$url" -o "$out_path"; then
      echo "    ⚠️ Failed to download logo from $url"
      rm -f "$out_path" || true
    fi
done

# Create a zip archive with all downloaded logos
ZIP_NAME="logos.zip"
echo "Creating zip archive: $ZIP_NAME"
zip -r "$ZIP_NAME" "$OUT_DIR"

echo "Done."
echo "Logos directory: $OUT_DIR/"
echo "ZIP archive: $ZIP_NAME"
