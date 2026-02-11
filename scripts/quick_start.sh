#!/bin/bash
# Quick start script for the overfitting demo project
# This script sets up and runs the entire project

set -e  # Exit on error

echo "🎲 Overfitting Demo - Quick Start Script"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}➜${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

print_success "Python is installed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_step "Creating virtual environment..."
    python -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
print_step "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed"

# Create necessary directories
print_step "Creating directories..."
mkdir -p data results plots
print_success "Directories created"

# Check if data files exist
if [ ! -f "results/best_strategy.json" ]; then
    print_warning "No results found. Running data generation pipeline..."
    
    print_step "Step 1: Generating random strategies..."
    python 01_generate_random_strategies.py
    
    print_step "Step 2: Backtesting strategies..."
    python 02_backtest_strategies.py
    
    print_step "Step 3: Selecting best strategy..."
    python 03_select_best_strategy.py
    
    print_step "Step 4: Validating strategy..."
    python 04_validate_strategy.py
    
    print_step "Step 5: Creating visualizations..."
    python 05_visualize_results.py
    
    print_success "Data pipeline completed!"
else
    print_success "Results already exist"
fi

echo ""
echo "========================================"
echo "🚀 Setup complete! You can now:"
echo ""
echo "1. Run the Streamlit app:"
echo "   ${GREEN}streamlit run app.py${NC}"
echo ""
echo "2. Run with Docker:"
echo "   ${GREEN}docker-compose up${NC}"
echo ""
echo "3. Run tests:"
echo "   ${GREEN}pytest${NC}"
echo ""
echo "4. Deploy to AWS:"
echo "   See DEPLOYMENT.md for instructions"
echo ""
echo "========================================"
