# 🚀 HOW TO RUN THE COINFLIP STRATEGY DEMO

## ⚡ Quick Start (5 Commands)

Open your terminal in the `coinflip_strategy_demo` folder and run:

```bash
# Navigate to the demo folder
cd coinflip_strategy_demo

# Install dependencies (only needed once)
pip install -r requirements.txt

# Run all 5 steps in sequence
python 01_generate_random_strategies.py
python 02_backtest_strategies.py
python 03_select_best_strategy.py
python 04_validate_strategy.py
python 05_visualize_results.py
```

**That's it!** Check the `plots/` folder for the devastating charts.

---

## 📋 Detailed Instructions

### Step 0: Setup (One-time only)

```bash
# Make sure you're in the right directory
cd D:\QUANT\GEA\coinflip_strategy_demo

# Install required packages
pip install -r requirements.txt
```

This installs:
- `numpy` - For numerical operations
- `pandas` - For data manipulation
- `matplotlib` - For creating charts
- `seaborn` - For better-looking charts

---

### Step 1: Generate Random Strategies

```bash
python 01_generate_random_strategies.py
```

**What it does:**
- Creates 100 completely random trading strategies (coin flips)
- Loads **REAL Bitcoin price data** from 5-minute candlesticks
- Splits data into training (70%) and validation (30%)
- Saves to `data/` folder

**Output files:**
- `data/strategies.json` (100 random strategies)
- `data/btc_price_data.csv` (real Bitcoin price data)

**Expected runtime:** < 5 seconds

---

### Step 2: Backtest All Strategies

```bash
python 02_backtest_strategies.py
```

**What it does:**
- Tests all 100 random strategies on training data
- Calculates win rate, returns, Sharpe ratio for each
- Sorts by performance
- Shows that some random strategies look "amazing"

**Output files:**
- `results/training_performance.csv` (all 100 results)

**Expected runtime:** < 10 seconds

**What to look for:**
- Top strategies with 65-75% win rates (by pure luck!)
- Bottom strategies with 25-35% win rates (unlucky)
- Average around 50% (as expected from randomness)

---

### Step 3: Select Best Strategy

```bash
python 03_select_best_strategy.py
```

**What it does:**
- Picks the "winning" strategy
- Displays impressive-looking statistics
- Saves the best performer

**Output files:**
- `results/best_strategy.json` (the "winner")

**Expected runtime:** < 2 seconds

**What to look for:**
- Win rate > 65% (looks amazing!)
- Remember: This is pure randomness!

---

### Step 4: Validate on Fresh Data

```bash
python 04_validate_strategy.py
```

**What it does:**
- Tests the "best" strategy on validation data (unseen)
- Compares training vs validation performance
- Reveals the truth: it's just random

**Output files:**
- `results/validation_results.json` (the reality check)

**Expected runtime:** < 2 seconds

**What to look for:**
- Win rate drops to ~50% (reality!)
- The devastating performance gap
- Proof that training performance was luck

---

### Step 5: Create Visualizations

```bash
python 05_visualize_results.py
```

**What it does:**
- Creates 3 professional charts
- Visualizes the overfitting trap
- Saves publication-ready images

**Output files:**
- `plots/all_strategies_histogram.png` (distribution of all 100)
- `plots/best_vs_validation.png` (train vs val comparison)
- `plots/overfitting_proof.png` (equity curve collapse)

**Expected runtime:** < 5 seconds

**What to look for:**
- Clear visual proof of overfitting
- Charts you can use in presentations
- Devastating evidence of the trap

---

## 🔄 Run Everything at Once (Advanced)

### Windows PowerShell:
```powershell
python 01_generate_random_strategies.py; python 02_backtest_strategies.py; python 03_select_best_strategy.py; python 04_validate_strategy.py; python 05_visualize_results.py
```

### Or create a batch file:

Create `run_all.bat`:
```batch
@echo off
echo Running Coinflip Strategy Demo...
python 01_generate_random_strategies.py
python 02_backtest_strategies.py
python 03_select_best_strategy.py
python 04_validate_strategy.py
python 05_visualize_results.py
echo.
echo All done! Check plots/ folder for results.
pause
```

Then just double-click `run_all.bat` or run:
```bash
.\run_all.bat
```

---

## 📂 Expected Output Structure

After running all steps, you should have:

```
coinflip_strategy_demo/
├── data/
│   ├── BTCUSD_Candlestick_5_M_BID_01.10.2024-10.11.2024.csv  ✅ Real BTC data (source)
│   ├── strategies.json                 ✅ 100 random strategies
│   └── btc_price_data.csv             ✅ Processed price data
├── results/
│   ├── training_performance.csv        ✅ All backtest results
│   ├── best_strategy.json              ✅ The "winner"
│   └── validation_results.json         ✅ Reality check
└── plots/
    ├── all_strategies_histogram.png    ✅ Distribution chart
    ├── best_vs_validation.png          ✅ Comparison chart
    └── overfitting_proof.png           ✅ Equity curve
```

---

## 🎯 What You're Demonstrating

After running all 5 steps, you can show:

1. **Random strategies can look profitable** (Step 2 output)
2. **One random strategy looks "amazing"** (Step 3 output)
3. **Performance collapses on new data** (Step 4 output)
4. **Visual proof of overfitting** (Step 5 charts)

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'numpy'`
**Solution:** Run `pip install -r requirements.txt`

### Issue: `FileNotFoundError: data/strategies.json`
**Solution:** Run steps in order! Each step depends on previous steps.

### Issue: Charts look weird or don't display
**Solution:** Make sure matplotlib is installed: `pip install matplotlib`

### Issue: Want to use different Python environment
**Solution:** 
```bash
# Activate your environment first
conda activate your_env_name
# Then install requirements
pip install -r requirements.txt
# Then run the scripts
```

---

## 🔧 Customization Options

Want to experiment? Edit these variables in the scripts:

### In `01_generate_random_strategies.py`:
```python
NUM_STRATEGIES = 100      # Try 500 for more dramatic results
NUM_SIGNALS = 500         # More trades = more randomness
TRAIN_SPLIT = 0.7         # Try 0.5 = less training data
```

### In `02_backtest_strategies.py`:
- No configuration needed, uses data from step 1

### Results:
- More strategies = higher chance of extreme outliers
- Less training data = easier to overfit
- More trades = more stable (closer to 50% mean)

---

## 💡 Using the Results

### For Presentations:
1. Open charts from `plots/` folder
2. Walk through the story:
   - "I generated 100 random strategies..."
   - "Look! This one has 73% win rate!"
   - "But on new data... 51%"
   - "This is overfitting"

### For Reports:
- Use the charts in your documents
- Reference the numerical results from `results/` folder
- Show the train-validation gap as the key metric

### For Teaching:
- Let others adjust parameters and re-run
- Show how more strategies = worse overfitting
- Demonstrate importance of validation

---

## ✅ Success Checklist

After running everything, verify:

- [ ] `data/` folder has 2 files
- [ ] `results/` folder has 3 files
- [ ] `plots/` folder has 3 PNG images
- [ ] Best strategy has >60% win rate on training
- [ ] Same strategy has ~50% on validation
- [ ] Charts clearly show the overfitting trap

If all checked, you're ready to present! 🎉

---

## 🎓 Next Steps

Want to extend the demo?

1. **Add transaction costs** - Make validation even worse
2. **Compare to buy-and-hold** - Show randomness vs baseline
3. **Test 1000 strategies** - See even more extreme outliers
4. **Add statistical tests** - P-values for significance
5. **Try different markets** - Crypto, stocks, forex

The code is modular and clean - easy to extend!

---

**Questions?** Check the README.md for more details about the concept.
