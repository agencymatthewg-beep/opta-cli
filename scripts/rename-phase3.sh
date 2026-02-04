#!/bin/bash
# Rename Aider to Opta - Phase 3: Specific Cases
# Created: 2026-02-04

set -e

cd ~/Documents/Opta/apps/opta-cli

echo "Phase 3: Fixing specific references..."

# Fix help prompts and documentation
echo "  - Updating help prompts..."
find opta -type f -name "*.py" -exec sed -i '' 's/aider doc urls/opta doc urls/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider docs/opta docs/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/use aider as a CLI/use opta as a CLI/g' {} +

# Fix version check references
echo "  - Updating version check..."
find opta -type f -name "*.py" -exec sed -i '' 's/"aider-chat"/"opta-cli"/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider-chat/opta-cli/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/version of aider/version of opta/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider version/opta version/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/Re-run aider/Re-run opta/g' {} +

# Fix model settings
echo "  - Updating model settings..."
find opta -type f -name "*.py" -exec sed -i '' 's/"aider\/extra_params"/"opta\/extra_params"/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider\/extra_params/opta\/extra_params/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/"aider\/{__version__}"/"opta\/{__version__}"/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider naming convention/opta naming convention/g' {} +

# Fix callback URLs
echo "  - Updating callback URLs..."
find opta -type f -name "*.py" -exec sed -i '' 's/\/callback\/aider/\/callback\/opta/g' {} +

# Fix variable names in repo.py
echo "  - Updating repo.py variables..."
find opta -type f -name "*.py" -exec sed -i '' 's/aider_ignore_file/opta_ignore_file/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider_ignore_spec/opta_ignore_spec/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider_ignore_ts/opta_ignore_ts/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider_ignore_last_check/opta_ignore_last_check/g' {} +

# Fix email addresses
echo "  - Updating email addresses..."
find opta -type f -name "*.py" -exec sed -i '' 's/aider@opta\.chat/opta@opta.chat/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider </opta </g' {} +

# Fix author/committer references
echo "  - Updating author/committer references..."
find opta -type f -name "*.py" -exec sed -i '' 's/(aider)/(opta)/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/You(aider)/You(opta)/g' {} +

# Fix file path examples in code
echo "  - Updating file path examples..."
find opta -type f -name "*.py" -exec sed -i '' 's/"aider\/io\.py"/"opta\/io.py"/g' {} +

echo "  ✓ Phase 3 complete!"

# Final count
REMAINING=$(grep -r "aider" opta/ --include="*.py" 2>/dev/null | wc -l || echo "0")
REMAINING_CODE=$(grep -r "aider" opta/ --include="*.py" 2>/dev/null | grep -v "^[^:]*:.*#" | wc -l || echo "0")
echo ""
echo "Total 'aider' references remaining: $REMAINING"
echo "In code (excluding comments): $REMAINING_CODE"
