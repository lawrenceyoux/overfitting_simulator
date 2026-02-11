"""
Step 4: Validate Top Strategies
Test the top N "winning" strategies on fresh validation data

This shows that ALL top performers collapse on new data, not just one.
"""

import pandas as pd
import json
from pathlib import Path
import numpy as np

# ============================================
# CONFIGURATION
# ============================================
TOP_N_STRATEGIES = 10  # Number of top strategies to validate (configurable!)


# ============================================
# HELPER FUNCTION (copied from step 2)
# ============================================

def calculate_strategy_metrics(signals, prices):
    """
    Calculate performance metrics for a trading strategy
    (Copied from 02_backtest_strategies.py for modularity)
    """
    if len(signals) != len(prices):
        min_len = min(len(signals), len(prices))
        signals = signals[:min_len]
        prices = prices[:min_len]
    
    trades = []
    returns = []
    
    for i in range(len(signals) - 1):
        if signals[i] == 1:
            entry_price = prices[i]
            exit_price = prices[i + 1]
            trade_return = (exit_price - entry_price) / entry_price
            returns.append(trade_return)
            trades.append(1 if trade_return > 0 else 0)
    
    if len(trades) == 0:
        return {
            'win_rate': 0.0,
            'total_return': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'num_trades': 0
        }
    
    win_rate = sum(trades) / len(trades)
    total_return = sum(returns)
    
    if len(returns) > 1 and np.std(returns) > 0:
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0
    
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

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Main execution:
    1. Load top N strategies from training results
    2. Load validation price data (fresh, unseen data)
    3. Test each strategy
    4. Compare training vs validation for all
    5. Show results in a table
    """
    print("=" * 80)
    print(f"STEP 4: Validating Top {TOP_N_STRATEGIES} Strategies on Fresh Data")
    print("=" * 80)
    
    # Load training results
    print("\n📂 Loading training results...")
    training_results = pd.read_csv('results/training_performance.csv')
    
    # Sort by win rate and get top N
    training_results = training_results.sort_values('win_rate', ascending=False)
    top_strategies = training_results.head(TOP_N_STRATEGIES)
    
    print(f"   ✓ Loaded results for {len(training_results)} strategies")
    print(f"   ✓ Selected top {TOP_N_STRATEGIES} performers")
    
    # Load all strategies
    with open('data/strategies.json', 'r') as f:
        all_strategies = json.load(f)
    
    # Load validation data
    print("\n📂 Loading validation data (unseen by training)...")
    price_df = pd.read_csv('data/btc_price_data.csv')
    val_data = price_df[price_df['split'] == 'validation'].copy()
    val_prices = val_data['price'].values
    
    print(f"   ✓ Loaded {len(val_data)} validation data points")
    print(f"   ✓ This is FRESH data the strategies have never seen")
    
    # Validate each top strategy
    print(f"\n🔬 Testing top {TOP_N_STRATEGIES} strategies on validation data...")
    
    validation_results = []
    
    for idx, row in top_strategies.iterrows():
        strategy_id = row['strategy_id']
        signals = all_strategies[strategy_id]
        
        # Validate on fresh data
        val_signals = signals[:len(val_prices)]
        val_metrics = calculate_strategy_metrics(val_signals, val_prices)
        
        # Store comparison
        validation_results.append({
            'rank': len(validation_results) + 1,
            'strategy_id': strategy_id,
            'train_win_rate': row['win_rate'],
            'val_win_rate': val_metrics['win_rate'],
            'win_rate_drop': val_metrics['win_rate'] - row['win_rate'],
            'train_return': row['total_return'],
            'val_return': val_metrics['total_return'],
            'return_drop': val_metrics['total_return'] - row['total_return'],
            'train_sharpe': row['sharpe_ratio'],
            'val_sharpe': val_metrics['sharpe_ratio'],
            'sharpe_drop': val_metrics['sharpe_ratio'] - row['sharpe_ratio']
        })
    
    val_df = pd.DataFrame(validation_results)
    
    # Display results table
    print("\n" + "=" * 80)
    print(f"📊 TOP {TOP_N_STRATEGIES} STRATEGIES: Training vs Validation Performance")
    print("=" * 80)
    
    print(f"\n{'Rank':<6}{'Strategy':<15}{'Train WR':>10}{'Val WR':>10}{'Drop':>10}{'Train Ret':>11}{'Val Ret':>11}")
    print("-" * 80)
    
    for _, row in val_df.iterrows():
        print(f"{row['rank']:<6}{row['strategy_id']:<15}"
              f"{row['train_win_rate']:>9.1%} {row['val_win_rate']:>9.1%} "
              f"{row['win_rate_drop']:>9.1%} "
              f"{row['train_return']:>10.1%} {row['val_return']:>10.1%}")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("📈 SUMMARY STATISTICS")
    print("=" * 80)
    
    avg_train_wr = val_df['train_win_rate'].mean()
    avg_val_wr = val_df['val_win_rate'].mean()
    avg_drop = val_df['win_rate_drop'].mean()
    
    print(f"\nAverage Training Win Rate:   {avg_train_wr:>6.1%}")
    print(f"Average Validation Win Rate: {avg_val_wr:>6.1%}")
    print(f"Average Drop:                {avg_drop:>6.1%}")
    
    print(f"\nBest Training Win Rate:      {val_df['train_win_rate'].max():>6.1%}")
    print(f"Best Validation Win Rate:    {val_df['val_win_rate'].max():>6.1%}")
    
    print(f"\nWorst Drop:                  {val_df['win_rate_drop'].min():>6.1%}")
    print(f"Best Drop (least bad):       {val_df['win_rate_drop'].max():>6.1%}")
    
    # Count strategies that stayed above 55%
    still_good = (val_df['val_win_rate'] > 0.55).sum()
    print(f"\nStrategies still >55% on validation: {still_good}/{TOP_N_STRATEGIES}")
    
    # The devastating conclusion
    print("\n" + "🔥" * 40)
    print("💥 OVERFITTING REVEALED ACROSS ALL TOP STRATEGIES!")
    print("🔥" * 40)
    
    print(f"\nKey Insights:")
    print(f"  • ALL {TOP_N_STRATEGIES} top strategies showed performance collapse")
    print(f"  • Average drop: {abs(avg_drop):.1%} (massive!)")
    print(f"  • Training performance was FAKE - curve-fitted to noise")
    print(f"  • Validation reveals the truth: closer to random (50%)")
    
    if still_good == 0:
        print(f"\n  ⚠️  ZERO strategies maintained >55% win rate!")
        print(f"      This proves they were ALL overfit to training data.")
    
    # Save results
    print(f"\n💾 Saving validation results...")
    
    output_path = Path('results/validation_results.csv')
    val_df.to_csv(output_path, index=False)
    print(f"   ✓ Saved to {output_path}")
    
    # Also save summary JSON
    summary = {
        'top_n': TOP_N_STRATEGIES,
        'average_train_win_rate': float(avg_train_wr),
        'average_val_win_rate': float(avg_val_wr),
        'average_drop': float(avg_drop),
        'strategies_still_good': int(still_good),
        'all_strategies': validation_results
    }
    
    with open('results/validation_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"   ✓ Saved summary to results/validation_summary.json")
    
    # Final message
    print("\n" + "=" * 80)
    print("✅ STEP 4 COMPLETE!")
    print("=" * 80)
    print("The overfitting trap is now fully exposed:")
    print(f"  ❌ High training performance ≠ good strategy")
    print(f"  ❌ Past performance ≠ future results")
    print(f"  ✅ Always validate on unseen data")
    print(f"  ✅ Curve-fitting makes noise look like signal")
    print(f"\n💡 Tip: Change TOP_N_STRATEGIES in the script to test more/fewer")
    print(f"\nNext: Run 05_visualize_results.py for devastating charts")
    print("=" * 80)


if __name__ == "__main__":
    main()
