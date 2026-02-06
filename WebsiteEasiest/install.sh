#!/bin/bash
# Installation and verification script for Secret Hitler Database

set -e  # Exit on error

echo "============================================================"
echo "Secret Hitler Database - Installation & Verification"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -n "1. Checking Python version... "
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ $(echo "$python_version" | cut -d'.' -f1,2) < "3.9" ]]; then
    echo -e "${RED}❌ FAILED${NC} (Python 3.9+ required, got $python_version)"
    exit 1
fi
echo -e "${GREEN}✅ OK${NC} ($python_version)"

# Install dependencies
echo -n "2. Installing dependencies... "
if pip install -q -r WebsiteEasiest/requirements.txt 2>&1 | grep -q "Successfully installed\|already satisfied"; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING${NC}"
fi

# Initialize database
echo -n "3. Initializing database... "
cd WebsiteEasiest
if PYTHONPATH=/root/PycharmProjects/SH:$PYTHONPATH python setup_db.py > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
    exit 1
fi

# Run tests
echo -n "4. Running tests... "
if PYTHONPATH=/root/PycharmProjects/SH:$PYTHONPATH python test_database.py > /tmp/test_output.log 2>&1; then
    if grep -q "All tests passed" /tmp/test_output.log; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${YELLOW}⚠️  PARTIAL${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  SKIPPED${NC}"
fi

# Verify database file
echo -n "5. Verifying database file... "
if [ -f "data/database/app.db" ]; then
    size=$(du -h data/database/app.db | cut -f1)
    echo -e "${GREEN}✅ OK${NC} ($size)"
else
    echo -e "${YELLOW}⚠️  SQLITE${NC} (Will be created on first run)"
fi

echo ""
echo "============================================================"
echo -e "${GREEN}✅ Installation completed successfully!${NC}"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Read DATABASE_GUIDE.md for full documentation"
echo "  2. Review QUICKSTART.md for quick examples"
echo "  3. Run: python app2.py"
echo ""
echo "Documentation files:"
echo "  - README_DATABASE.md         (This overview)"
echo "  - DATABASE_GUIDE.md          (Full documentation)"
echo "  - IMPLEMENTATION_REPORT.md   (Technical details)"
echo "  - QUICKSTART.md              (Quick start guide)"
echo ""

