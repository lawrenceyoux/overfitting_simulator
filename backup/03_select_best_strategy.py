"""
Step 3: Select Best Strategy
Pick the "winning" strategy from training results

This shows how a random strategy can look amazing on training data.
"""

import pandas as pd
import json
from pathlib import Path

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Main execution:
    1. Load training performance results
    2. Select the top performer
    3. Display impressive statistics
    4. Save to results/best_strategy.json
    """
    print("=" * 60)
    print("STEP 3: Selecting Best Strategy")
    print("=" * 60)
    
    # Load results
    print("\n📂 Loading training results...")
    results_df = pd.read_csv('results/training_performance.csv')
    print(f"   ✓ Loaded results for {len(results_df)} strategies")
    
    # Find best strategy (by win rate)
    print("\n🔍 Finding best performer...")
    best_idx = results_df['win_rate'].idxmax()
    best_strategy = results_df.loc[best_idx]
    
    # Load the actual strategy signals
    with open('data/strategies.json', 'r') as f:
        all_strategies = json.load(f)
    
    best_signals = all_strategies[best_strategy['strategy_id']]
    
    # Create best strategy record
    best_strategy_record = {
        'strategy_id': best_strategy['strategy_id'],
        'signals': best_signals,
        'training_metrics': {
            'win_rate': float(best_strategy['win_rate']),
            'total_return': float(best_strategy['total_return']),
            'sharpe_ratio': float(best_strategy['sharpe_ratio']),
            'max_drawdown': float(best_strategy['max_drawdown']),
            'num_trades': int(best_strategy['num_trades'])
        }
    }
    
    # Display impressive statistics
    print("\n" + "=" * 60)
    print("🏆 BEST STRATEGY FOUND!")
    print("=" * 60)
    print(f"\nStrategy ID: {best_strategy['strategy_id']}")
    print(f"\nImpressive Training Performance:")
    print(f"  ✨ Win Rate:       {best_strategy['win_rate']:.1%}")
    print(f"  ✨ Total Return:   {best_strategy['total_return']:.1%}")
    print(f"  ✨ Sharpe Ratio:   {best_strategy['sharpe_ratio']:.2f}")
    print(f"  ✨ Max Drawdown:   {best_strategy['max_drawdown']:.1%}")
    print(f"  ✨ Number of Trades: {int(best_strategy['num_trades'])}")
    
    # The trap message
    print("\n" + "⚠️ " * 20)
    print("WARNING: This looks AMAZING! But remember...")
    print("This is a COMPLETELY RANDOM strategy (coin flips)!")
    print("It only looks good because we tested 100 random strategies.")
    print("Let's see what happens on fresh data...")
    print("⚠️ " * 20)
    
    # Rankings context
    print(f"\nContext:")
    print(f"  • Ranked #1 out of {len(results_df)} strategies")
    print(f"  • Average win rate across all strategies: {results_df['win_rate'].mean():.1%}")
    print(f"  • Median win rate: {results_df['win_rate'].median():.1%}")
    print(f"  • This strategy is {((best_strategy['win_rate'] / results_df['win_rate'].mean()) - 1) * 100:.0f}% better than average")
    
    # Save best strategy
    print(f"\n💾 Saving best strategy...")
    output_path = Path('results/best_strategy.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(best_strategy_record, f, indent=2)
    
    print(f"   ✓ Saved to {output_path}")
    
    # Final message
    print("\n" + "=" * 60)
    print("✅ STEP 3 COMPLETE!")
    print("=" * 60)
    print("We've identified a 'winning' strategy from random noise!")
    print("This is exactly how retail traders lose money:")
    print("  1. Test many strategies")
    print("  2. Pick the best backtested result")
    print("  3. Assume it will work in the future")
    print("  4. Lose real money when it doesn't")
    print(f"\nNext: Run 04_validate_strategy.py to see the TRUTH")
    print("=" * 60)


if __name__ == "__main__":
    main()
