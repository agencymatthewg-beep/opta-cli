#!/bin/bash
# Rename Aider to Opta - Comprehensive Renaming Script
# Created: 2026-02-04
# Purpose: Rename all references from "opta" to "opta" throughout the codebase

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/rename-log.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

cd "$PROJECT_ROOT"

log "=== Starting Aider → Opta Rename Process ==="
log "Working directory: $PROJECT_ROOT"

# Check if opta directory exists
if [ ! -d "opta" ]; then
    error "opta directory not found!"
fi

# Step 1: Update all Python files BEFORE renaming directory
log "Step 1: Updating Python imports and references..."

# Count files to process
PY_FILES=$(find . -type f -name "*.py" | wc -l)
log "Found $PY_FILES Python files to process"

# Update imports
log "  - Updating 'from opta' imports..."
find . -type f -name "*.py" -exec sed -i '' 's/from opta/from opta/g' {} +

log "  - Updating 'import opta' statements..."
find . -type f -name "*.py" -exec sed -i '' 's/import opta/import opta/g' {} +

log "  - Updating 'opta.' references..."
find . -type f -name "*.py" -exec sed -i '' 's/opta\./opta./g' {} +

# Step 2: Update class and variable names
log "Step 2: Updating class and variable names..."
find . -type f -name "*.py" -exec sed -i '' 's/\bAider\b/Opta/g' {} +
find . -type f -name "*.py" -exec sed -i '' 's/\bAIDER\b/OPTA/g' {} +

# Step 3: Update configuration file references
log "Step 3: Updating config file references..."
find . -type f -name "*.py" -exec sed -i '' 's/\.opta\.conf\.yml/.opta.conf.yml/g' {} +
find . -type f -name "*.py" -exec sed -i '' 's/\.opta\//.opta\//g' {} +
find . -type f -name "*.py" -exec sed -i '' 's/\.opta"/.opta"/g' {} +
find . -type f -name "*.py" -exec sed -i '' "s/\.opta'/.opta'/g" {} +
find . -type f -name "*.py" -exec sed -i '' 's/AIDER\.md/OPTA.md/g' {} +

# Step 4: Update other file types
log "Step 4: Updating markdown and config files..."

# Update README.md
if [ -f "README.md" ]; then
    log "  - Updating README.md..."
    sed -i '' 's/opta-chat/opta-cli/g' README.md
    sed -i '' 's/Aider-AI\/opta/optamize\/opta-cli/g' README.md
    sed -i '' 's/# Aider/# Opta CLI/g' README.md
    sed -i '' 's/\bAider\b/Opta/g' README.md
fi

# Update pyproject.toml
if [ -f "pyproject.toml" ]; then
    log "  - Updating pyproject.toml..."
    sed -i '' 's/name = "opta-chat"/name = "opta-cli"/g' pyproject.toml
    sed -i '' 's/description = "Aider is AI pair programming in your terminal"/description = "Enhanced Claude Code CLI"/g' pyproject.toml
    sed -i '' 's|Homepage = "https://github.com/Aider-AI/opta"|Homepage = "https://github.com/optamize/opta-cli"|g' pyproject.toml
    sed -i '' 's/opta = "opta.main:main"/opta = "opta.main:main"/g' pyproject.toml
    sed -i '' 's/include = \["opta"\]/include = ["opta"]/g' pyproject.toml
    sed -i '' 's/write_to = "opta\/_version.py"/write_to = "opta\/_version.py"/g' pyproject.toml
    sed -i '' 's/skip = ".*opta\/website/skip = ".*opta\/website/g' pyproject.toml
fi

# Update shell scripts
log "  - Updating shell scripts..."
find scripts -type f \( -name "*.sh" -o -name "*.bash" \) -exec sed -i '' 's/opta/opta/g' {} + 2>/dev/null || true

# Update YAML files
log "  - Updating YAML files..."
find . -type f -name "*.yml" -o -name "*.yaml" -exec sed -i '' 's/opta/opta/g' {} + 2>/dev/null || true
find . -type f -name "*.yml" -o -name "*.yaml" -exec sed -i '' 's/Aider/Opta/g' {} + 2>/dev/null || true

# Step 5: Rename the main package directory
log "Step 5: Renaming main package directory opta/ → opta/..."
if [ -d "opta" ]; then
    mv opta opta
    log "  ✓ Directory renamed successfully"
else
    warn "  opta directory not found, may have been renamed already"
fi

# Step 6: Verify the rename
log "Step 6: Verifying rename..."

if [ ! -d "opta" ]; then
    error "opta directory not found after rename!"
fi

# Count remaining "opta" references in Python files
REMAINING=$(grep -r "opta" opta/ --include="*.py" 2>/dev/null | grep -v "# " | wc -l || echo "0")
log "  - Remaining 'opta' references in Python files: $REMAINING"

if [ "$REMAINING" -gt 50 ]; then
    warn "  High number of remaining 'opta' references detected. Manual review recommended."
fi

# Step 7: Test import
log "Step 7: Testing Python import..."
if python3 -c "import sys; sys.path.insert(0, '.'); import opta" 2>/dev/null; then
    log "  ✓ Python import successful"
else
    warn "  Python import test failed. May need manual fixes."
fi

# Step 8: Generate summary report
log ""
log "=== Rename Summary ==="
log "Total Python files updated: $PY_FILES"
log "Package directory: opta/ → opta/"
log "Package name: opta-chat → opta-cli"
log "Entry point: opta → opta"
log "Config references: .opta → .opta"
log ""
log "✓ Rename complete!"
log ""
log "Next steps:"
log "1. Review changes: git diff"
log "2. Run tests: pytest"
log "3. Test installation: pip install -e ."
log "4. Test command: opta --version"
log "5. Commit: git add -A && git commit -m 'refactor: rename opta to opta'"
log ""
log "Full log saved to: $LOG_FILE"
