#!/bin/bash
# Rename Aider to Opta - Phase 4: Final Cleanup
# Created: 2026-02-04

set -e

cd ~/Documents/Opta/apps/opta-cli

echo "Phase 4: Final cleanup..."

# Fix analytics keys
echo "  - Updating analytics keys..."
find opta -type f -name "*.py" -exec sed -i '' 's/"aider_version"/"opta_version"/g' {} +

# Fix descriptions and help text
echo "  - Updating descriptions..."
find opta -type f -name "*.py" -exec sed -i '' 's/aider is AI pair programming/opta is an enhanced Claude Code CLI/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/about aider/about opta/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/improve aider/improve opta/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/between aider and web UI/between opta and web UI/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/Run aider in your browser/Run opta in your browser/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/Upgrade aider to the latest/Upgrade opta to the latest/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/the aider ignore file/the opta ignore file/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/so aider can edit/so opta can edit/g' {} +

# Fix variable names
echo "  - Updating variable names..."
find opta -type f -name "*.py" -exec sed -i '' 's/_aider_coders/_opta_coders/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/sys\.argv = \["aider"\]/sys.argv = ["opta"]/g' {} +

# Fix method names
echo "  - Updating method names..."
find opta -type f -name "*.py" -exec sed -i '' 's/refresh_aider_ignore/refresh_opta_ignore/g' {} +

# Fix commit message prefixes
echo "  - Updating commit message prefixes..."
find opta -type f -name "*.py" -exec sed -i '' 's/"aider: "/"opta: "/g' {} +
find opta -type f -name "*.py" -exec sed -i '' "s/'aider: '/'opta: '/g" {} +

# Fix attribute descriptions (but not in URLs)
echo "  - Updating attribute descriptions..."
find opta -type f -name "*.py" -exec sed -i '' 's/Attribute aider code changes/Attribute opta code changes/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/Attribute aider commits/Attribute opta commits/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/Attribute aider edits/Attribute opta edits/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/for aider edits/for opta edits/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/if aider authored/if opta authored/g' {} +
find opta -type f -name "*.py" -exec sed -i '' "s/with 'aider: '/with 'opta: '/g" {} +

# Fix os.walk paths
echo "  - Updating os.walk paths..."
find opta -type f -name "*.py" -exec sed -i '' 's/os\.walk("aider")/os.walk("opta")/g' {} +

# Fix error messages
echo "  - Updating error messages..."
find opta -type f -name "*.py" -exec sed -i '' 's/made by aider/made by opta/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/done by aider/done by opta/g' {} +
find opta -type f -name "*.py" -exec sed -i '' "s/keep aider's internal/keep opta's internal/g" {} +
find opta -type f -name "*.py" -exec sed -i '' 's/but not in aider/but not in opta/g' {} +

# Fix shell completion examples
echo "  - Updating shell completion examples..."
find opta -type f -name "*.py" -exec sed -i '' 's/Example: aider --shell-completions/Example: opta --shell-completions/g' {} +

# Update Co-authored-by messages (but keep the format)
echo "  - Updating Co-authored-by format..."
find opta -type f -name "*.py" -exec sed -i '' 's/Co-authored-by: aider/Co-authored-by: opta/g' {} +

echo "  ✓ Phase 4 complete!"

# Final count
REMAINING=$(grep -r "aider" opta/ --include="*.py" 2>/dev/null | wc -l || echo "0")
REMAINING_CODE=$(grep -r "aider" opta/ --include="*.py" 2>/dev/null | grep -v "^[^:]*:.*#" | grep -v "github.com" | grep -v "Aider-AI" | wc -l || echo "0")
echo ""
echo "Total 'aider' references remaining: $REMAINING"
echo "In code (excluding comments and GitHub URLs): $REMAINING_CODE"
echo ""
echo "Note: Remaining references to 'Aider-AI' GitHub URLs are intentional (historical references)"
