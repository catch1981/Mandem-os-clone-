const fs = require('fs');

function generateCodeFromPrompt(prompt, filename = "output.sh") {
    const bashScript = `#!/bin/sh
# Script generated from prompt
# "${prompt.replace(/"/g, '\"')}"

find . -type f -name "*.jpg" | while read file; do
  base=$(basename "$file")
  if echo "$base" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}_'; then
    echo "Skipping already renamed: $file"
  else
    date=$(date +"%Y-%m-%d")
    dir=$(dirname "$file")
    mv "$file" "$dir/\${date}_$base"
    echo "Renamed $file -> $dir/\${date}_$base"
  fi
done
`;
    fs.writeFileSync(filename, bashScript);
    console.log(`Script saved to ${filename}`);
}

module.exports = { generateCodeFromPrompt };