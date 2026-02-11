# Implementation Checklist

Follow these steps in order:

## □ Step 1: Generate Random Strategies
**File**: `01_generate_random_strategies.py`

Tasks:
- [ ] Create function to generate N random buy/sell signals (0s and 1s)
- [ ] Generate 100 different random strategies
- [ ] Save to `data/strategies.json`
- [ ] Each strategy = list of random 0/1 values (e.g., 500 trades)

Expected output: File with 100 arrays of random signals

---

## □ Step 2: Generate Price Data
**File**: Same as above or separate

Tasks:
- [ ] Generate synthetic price series (500-1000 data points)
- [ ] Use random walk or GBM (Geometric Brownian Motion)
- [ ] Split: 70% training, 30% validation
- [ ] Save to `data/synthetic_price_data.csv`
- [ ] Columns: [timestamp, price, returns, split]

Expected output: CSV with realistic price movement

---

## □ Step 3: Backtest on Training Data
**File**: `02_backtest_strategies.py`

Tasks:
- [ ] Load strategies from JSON
- [ ] Load training period from CSV
- [ ] For each of 100 strategies:
  - [ ] Calculate win rate
  - [ ] Calculate total return
  - [ ] Calculate Sharpe ratio
  - [ ] Calculate max drawdown
- [ ] Save results to `results/training_performance.csv`

Expected output: Table with 100 rows (1 per strategy)

---

## □ Step 4: Select Best Strategy
**File**: `03_select_best_strategy.py`

Tasks:
- [ ] Load `results/training_performance.csv`
- [ ] Sort by win rate (or Sharpe)
- [ ] Select top performer
- [ ] Print impressive statistics
- [ ] Save to `results/best_strategy.json`

Expected output: One "amazing" strategy saved

---

## □ Step 5: Validate Best Strategy
**File**: `04_validate_strategy.py`

Tasks:
- [ ] Load best strategy from JSON
- [ ] Load validation period from CSV
- [ ] Run same metrics as training
- [ ] Compare training vs validation
- [ ] Save to `results/validation_results.csv`

Expected output: Reality check showing ~50% performance

---

## □ Step 6: Create Visualizations
**File**: `05_visualize_results.py`

Tasks:
- [ ] Chart 1: Histogram of all 100 win rates
- [ ] Chart 2: Training vs Validation bar comparison
- [ ] Chart 3: Equity curves (train | validation split)
- [ ] Save all to `plots/` directory

Expected output: 3 devastating charts

---

## ✅ Validation

Run all scripts in sequence:
```bash
python 01_generate_random_strategies.py
python 02_backtest_strategies.py
python 03_select_best_strategy.py
python 04_validate_strategy.py
python 05_visualize_results.py
```

Check that:
- ✓ `data/` has strategies and price data
- ✓ `results/` has performance files
- ✓ `plots/` has 3 charts
- ✓ Best strategy has >65% win rate on training
- ✓ Same strategy has ~50% on validation
- ✓ Overfitting proof is clear and visual

---

## 🎯 Core Logic (Pseudocode)

### Backtest Function
```
function backtest(signals, prices):
    trades = []
    for i in range(len(signals)):
        if signals[i] == 1:  # Buy signal
            entry_price = prices[i]
            exit_price = prices[i+1]
            profit = (exit_price - entry_price) / entry_price
            trades.append(profit > 0)  # Win or loss
    
    win_rate = sum(trades) / len(trades)
    return win_rate, total_return, sharpe, etc.
```

Keep it simple!
