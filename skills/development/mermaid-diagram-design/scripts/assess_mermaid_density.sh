#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <markdown-file>" >&2
  exit 2
fi

md_file="$1"
if [[ ! -f "$md_file" ]]; then
  echo "MERMAID_DENSITY_FAIL reason=file_not_found path=$md_file" >&2
  exit 2
fi

awk '
BEGIN {
  in_block = 0
  idx = 0
}
/^```mermaid[[:space:]]*$/ {
  in_block = 1
  idx++
  block[idx] = ""
  next
}
/^```[[:space:]]*$/ {
  if (in_block == 1) {
    in_block = 0
  }
  next
}
{
  if (in_block == 1) {
    block[idx] = block[idx] $0 "\n"
  }
}
END {
  if (idx == 0) {
    print "MERMAID_DENSITY_OK blocks=0 note=no_mermaid_block"
    exit 0
  }

  has_warn = 0

  for (i = 1; i <= idx; i++) {
    node_count = 0
    edge_count = 0
    long_label_count = 0
    edge_style_present = 0
    colored_node_style_present = 0

    n = split(block[i], lines, "\n")
    for (j = 1; j <= n; j++) {
      line = lines[j]

      if (line ~ /-->|==>|-.->|===/) {
        edge_count++
      }

      if (line ~ /^[[:space:]]*[A-Za-z0-9_]+[[:space:]]*\[/) {
        node_count++
      }

      if (line ~ /linkStyle[[:space:]]+default[[:space:]]+stroke:/) {
        edge_style_present = 1
      }

      if (line ~ /style[[:space:]]+[A-Za-z0-9_,]+[[:space:]]+fill:#/ || line ~ /classDef[[:space:]]+[A-Za-z0-9_]+[[:space:]]+fill:#/) {
        colored_node_style_present = 1
      }

      line_copy = line
      while (match(line_copy, /"[^"]+"/)) {
        label = substr(line_copy, RSTART + 1, RLENGTH - 2)
        gsub(/<[^>]+>/, "", label)
        gsub(/&nbsp;/, " ", label)
        gsub(/[[:space:]]+/, " ", label)
        if (length(label) > 40) {
          long_label_count++
        }
        line_copy = substr(line_copy, RSTART + RLENGTH)
      }
    }

    risk = "low"
    if (node_count >= 12 || edge_count >= 16 || long_label_count >= 4) {
      risk = "high"
      has_warn = 1
    } else if (node_count >= 9 || edge_count >= 12 || long_label_count >= 2) {
      risk = "medium"
      has_warn = 1
    }

    edge_style = (edge_style_present == 1) ? "present" : "absent"
    contrast_risk = "low"
    if (colored_node_style_present == 1 && edge_style_present == 0) {
      contrast_risk = "high"
      has_warn = 1
    }

    printf "MERMAID_DENSITY block=%d nodes=%d edges=%d long_labels=%d risk=%s edge_style=%s contrast_risk=%s\n", i, node_count, edge_count, long_label_count, risk, edge_style, contrast_risk
  }

  if (has_warn == 1) {
    printf "MERMAID_DENSITY_WARN blocks=%d\n", idx
  } else {
    printf "MERMAID_DENSITY_OK blocks=%d\n", idx
  }
}
' "$md_file"
