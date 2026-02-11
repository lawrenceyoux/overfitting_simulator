"""
Step 2: Backtest All Random Strategies
Test all 100 strategies on training data

This will show that some random strategies look "amazing" on training data.
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path

# ============================================
# FUNCTIONS
# ============================================

def calculate_strategy_metrics(signals, prices):
    """
    Calculate performance metrics for a trading strategy
    
    Simple logic:
    - When signal = 1: Enter trade (buy at current price, sell at next price)
    - When signal = 0: No action
    
    Args:
        signals: Array of buy signals (0 or 1)
        prices: Array of price data
    
    Returns:
        dict with keys: [win_rate, total_return, sharpe_ratio, max_drawdown, num_trades]
    """
    if len(signals) != len(prices):
        # Match lengths - use minimum
        min_len = min(len(signals), len(prices))
        signals = signals[:min_len]
        prices = prices[:min_len]
    
    # Track trades
    trades = []
    returns = []
    
    # Execute strategy
    for i in range(len(signals) - 1):  # -1 because we need next price
        if signals[i] == 1:  # Buy signal
            entry_price = prices[i]
            exit_price = prices[i + 1]
            
            # Calculate return
            trade_return = (exit_price - entry_price) / entry_price
            returns.append(trade_return)
            
            # Track win/loss
            trades.append(1 if trade_return > 0 else 0)
    
    # Handle case of no trades
    if len(trades) == 0:
        return {
            'win_rate': 0.0,
            'total_return': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'num_trades': 0
        }
    
    # Calculate metrics
    win_rate = sum(trades) / len(trades)
    total_return = sum(returns)
    
    # Sharpe ratio (annualized assuming daily data)
    if len(returns) > 1 and np.std(returns) > 0:
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0
    
    # Max drawdown
    cumulative = np.cumprod([1 + r for r in returns])
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = abs(np.min(drawdown)) if len(drawdown) > 0 else 0.0
    
    return {
        'win_rate': win_rate,
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'num_trades': len(trades)
    }


def backtest_all_strategies(strategies, price_data):
    """
    Backtest all strategies on training period
    
    Args:
        strategies: Dict with strategy IDs and their signal arrays
        price_data: DataFrame with price information (training split only)
    
    Returns:
        DataFrame with performance metrics for all strategies
    """
    results = []
    
    prices = price_data['price'].values
    
    for strategy_id, signals in strategies.items():
        # Calculate metrics
        metrics = calculate_strategy_metrics(signals, prices)
        
        # Store results
        results.append({
            'strategy_id': strategy_id,
            'win_rate': metrics['win_rate'],
            'total_return': metrics['total_return'],
            'sharpe_ratio': metrics['sharpe_ratio'],
            'max_drawdown': metrics['max_drawdown'],
            'num_trades': metrics['num_trades']
        })
    
    return pd.DataFrame(results)


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Main execution:
    1. Load strategies from data/strategies.json
    2. Load training price data
    3. Backtest each strategy
    4. Save results to results/training_performance.csv
    """
    print("=" * 60)
    print("STEP 2: Backtesting All Strategies on Training Data")
    print("=" * 60)
    
    # Load strategies
    print("\n📂 Loading strategies...")
    with open('data/strategies.json', 'r') as f:
        strategies = json.load(f)
    print(f"   ✓ Loaded {len(strategies)} strategies")
    
    # Load price data (training period only)
    print("\n📂 Loading REAL Bitcoin price data...")
    price_df = pd.read_csv('data/btc_price_data.csv')
    train_data = price_df[price_df['split'] == 'train'].copy()
    print(f"   ✓ Loaded {len(train_data)} training data points")
    print(f"   ✓ Price range: ${train_data['price'].min():.2f} - ${train_data['price'].max():.2f}")
    
    # Backtest all strategies
    print(f"\n🔬 Backtesting {len(strategies)} random strategies...")
    print("   (This may take a moment...)")
    
    results_df = backtest_all_strategies(strategies, train_data)
    
    # Sort by win rate
    results_df = results_df.sort_values('win_rate', ascending=False)
    
    # Display summary statistics
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY (Training Data)")
    print("=" * 60)
    print(f"\nWin Rate Distribution:")
    print(f"   Best:   {results_df['win_rate'].max():.1%}")
    print(f"   Worst:  {results_df['win_rate'].min():.1%}")
    print(f"   Mean:   {results_df['win_rate'].mean():.1%}")
    print(f"   Median: {results_df['win_rate'].median():.1%}")
    
    print(f"\n🏆 TOP 5 STRATEGIES (by Win Rate):")
    print("-" * 60)
    for idx, row in results_df.head(5).iterrows():
        print(f"{row['strategy_id']:15s} | Win Rate: {row['win_rate']:6.1%} | "
              f"Return: {row['total_return']:7.1%} | Sharpe: {row['sharpe_ratio']:5.2f}")
    
    print(f"\n💥 BOTTOM 5 STRATEGIES (by Win Rate):")
    print("-" * 60)
    for idx, row in results_df.tail(5).iterrows():
        print(f"{row['strategy_id']:15s} | Win Rate: {row['win_rate']:6.1%} | "
              f"Return: {row['total_return']:7.1%} | Sharpe: {row['sharpe_ratio']:5.2f}")
    
    # Save results
    print(f"\n💾 Saving results...")
    output_path = Path('results/training_performance.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)
    print(f"   ✓ Saved to {output_path}")
    
    # Final message
    print("\n" + "=" * 60)
    print("✅ STEP 2 COMPLETE!")
    print("=" * 60)
    print("Key Insight: Some random strategies look AMAZING!")
    print(f"The best strategy has {results_df['win_rate'].max():.1%} win rate.")
    print("But remember: These are completely random coin flips!")
    print(f"\nNext: Run 03_select_best_strategy.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
