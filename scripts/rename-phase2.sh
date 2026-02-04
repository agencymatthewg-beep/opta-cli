#!/bin/bash
# Rename Aider to Opta - Phase 2: Variable Names and Documentation
# Created: 2026-02-04

set -e

cd ~/Documents/Opta/apps/opta-cli

echo "Phase 2: Fixing variable names, file references, and documentation..."

# Fix variable names
echo "  - Updating variable names..."
find opta -type f -name "*.py" -exec sed -i '' 's/last_aider_commit/last_opta_commit/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider_edited_files/opta_edited_files/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider_commit_hashes/opta_commit_hashes/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider_edits/opta_edits/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider_commit/opta_commit/g' {} +

# Fix .aiderignore references
echo "  - Updating .aiderignore → .optaignore..."
find opta -type f -name "*.py" -exec sed -i '' 's/aiderignore/optaignore/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/\.aider/.opta/g' {} +

# Fix documentation strings (be careful not to break URLs or technical terms)
echo "  - Updating documentation strings..."
find opta -type f -name "*.py" -exec sed -i '' 's/using aider/using opta/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/with aider/with opta/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/each aider commit/each opta commit/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider docs/opta docs/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/aider documentation/opta documentation/g' {} +
find opta -type f -name "*.py" -exec sed -i '' 's/to the aider/to the opta/g' {} +

# Fix function parameter names
echo "  - Updating function parameters..."
find opta -type f -name "*.py" -exec sed -i '' 's/aider_commit_hashes=/opta_commit_hashes=/g' {} +

# Update tests directory
if [ -d "tests" ]; then
    echo "  - Updating tests directory..."
    find tests -type f -name "*.py" -exec sed -i '' 's/from aider/from opta/g' {} +
    find tests -type f -name "*.py" -exec sed -i '' 's/import aider/import opta/g' {} +
    find tests -type f -name "*.py" -exec sed -i '' 's/aider\./opta./g' {} +
    find tests -type f -name "*.py" -exec sed -i '' 's/\.aider/.opta/g' {} +
    find tests -type f -name "*.py" -exec sed -i '' 's/aiderignore/optaignore/g' {} +
fi

# Update benchmark directory
if [ -d "benchmark" ]; then
    echo "  - Updating benchmark directory..."
    find benchmark -type f -name "*.py" -exec sed -i '' 's/from aider/from opta/g' {} +
    find benchmark -type f -name "*.py" -exec sed -i '' 's/import aider/import opta/g' {} +
    find benchmark -type f -name "*.py" -exec sed -i '' 's/aider\./opta./g' {} +
fi

echo "  ✓ Phase 2 complete!"

# Count remaining references
REMAINING=$(grep -r "aider" opta/ --include="*.py" 2>/dev/null | grep -v "^[^:]*:.*#.*aider" | wc -l || echo "0")
echo "Remaining 'aider' references in Python code (excluding comments): $REMAINING"
