# Quick Start Script for Windows
# Run this script to set up and start the overfitting demo

Write-Host "🎲 Overfitting Demo - Quick Start Script" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.11 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "➜ Creating virtual environment..." -ForegroundColor Blue
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "➜ Activating virtual environment..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "➜ Installing dependencies..." -ForegroundColor Blue
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create necessary directories
Write-Host "➜ Creating directories..." -ForegroundColor Blue
New-Item -ItemType Directory -Force -Path data, results, plots | Out-Null
Write-Host "✓ Directories created" -ForegroundColor Green

# Check if data files exist
if (-not (Test-Path "results\best_strategy.json")) {
    Write-Host "⚠ No results found. Running data generation pipeline..." -ForegroundColor Yellow
    
    Write-Host "➜ Step 1: Generating random strategies..." -ForegroundColor Blue
    python scripts/01_generate_strategies.py
    
    Write-Host "➜ Step 2: Backtesting strategies..." -ForegroundColor Blue
    python scripts/02_backtest_strategies.py
    
    Write-Host "➜ Step 3: Selecting best strategy..." -ForegroundColor Blue
    python scripts/03_select_best_strategy.py
    
    Write-Host "➜ Step 4: Validating strategy..." -ForegroundColor Blue
    python scripts/04_validate_strategy.py
    
    Write-Host "➜ Step 5: Creating visualizations..." -ForegroundColor Blue
    python scripts/05_visualize_results.py
    
    Write-Host "✓ Data pipeline completed!" -ForegroundColor Green
} else {
    Write-Host "✓ Results already exist" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "🚀 Setup complete! You can now:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Run the Streamlit app:" -ForegroundColor Yellow
Write-Host "   streamlit run src/app.py" -ForegroundColor White
Write-Host ""
Write-Host "2. Run with Docker:" -ForegroundColor Yellow
Write-Host "   cd infrastructure/docker" -ForegroundColor White
Write-Host "   docker-compose up" -ForegroundColor White
Write-Host ""
Write-Host "3. Run tests:" -ForegroundColor Yellow
Write-Host "   pytest" -ForegroundColor White
Write-Host ""
Write-Host "4. Deploy to AWS:" -ForegroundColor Yellow
Write-Host "   See DEPLOYMENT.md for instructions" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Blue

# Ask if user wants to start the app
Write-Host ""
$response = Read-Host "Would you like to start the Streamlit app now? (y/n)"
if ($response -eq 'y') {
    Write-Host "🚀src/ Starting Streamlit app..." -ForegroundColor Green
    streamlit run app.py
}
