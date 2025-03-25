#!/bin/bash

find . -name "*.py" -type f ! -path "./env/*" \
  -exec wc -l {} + | sort -nr | awk 'BEGIN { printf "%-6s %s\n", "Lines", "File" } { printf "%-6s %s\n", $1, $2 }'
