#!/usr/bin/env bash
# ==============================================================================
#  Travel Planning App - Frontend Test Suite Runner
# ==============================================================================

# ANSI Color codes for beautiful UI logs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${YELLOW}🍄  MARIO TOURS - FRONTEND TEST SUITE RUNNER  🍄${NC}"
echo -e "${BLUE}====================================================${NC}"

# Navigate to frontend directory relative to script path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONT_DIR="$SCRIPT_DIR/front"

if [ ! -d "$FRONT_DIR" ]; then
    echo -e "${RED}❌ Erreur : Dossier 'front' introuvable dans $SCRIPT_DIR${NC}"
    exit 1
fi

echo -e "${YELLOW}👉 Entrée dans le répertoire 'front'...${NC}"
cd "$FRONT_DIR" || exit 1

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 node_modules manquant. Installation des dépendances...${NC}"
    npm install
fi

echo -e "${YELLOW}🚀 Lancement de la suite de tests avec Vitest...${NC}"
echo ""

# Run Vitest in single-run mode
npm run test:unit -- --run

TEST_EXIT_CODE=$?

echo ""
echo -e "${BLUE}====================================================${NC}"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ SUCCÈS : Tous les tests du front-end sont au VERT !${NC}"
else
    echo -e "${RED}❌ ERREUR : Certains tests ont échoué. Veuillez vérifier les logs ci-dessus.${NC}"
fi
echo -e "${BLUE}====================================================${NC}"

exit $TEST_EXIT_CODE
