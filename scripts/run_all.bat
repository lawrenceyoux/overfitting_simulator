@echo off
echo.
echo ============================================================
echo    Coinflip Strategy Overfitting Demo
echo ============================================================
echo.
echo Running all steps in sequence...
echo.

echo [1/5] Generating random strategies and price data...
python 01_generate_random_strategies.py
if errorlevel 1 goto error
echo.

echo [2/5] Backtesting all strategies on training data...
python 02_backtest_strategies.py
if errorlevel 1 goto error
echo.

echo [3/5] Selecting best strategy...
python 03_select_best_strategy.py
if errorlevel 1 goto error
echo.

echo [4/5] Validating on fresh data...
python 04_validate_strategy.py
if errorlevel 1 goto error
echo.

echo [5/5] Creating visualizations...
python 05_visualize_results.py
if errorlevel 1 goto error
echo.

echo ============================================================
echo    SUCCESS! All steps completed.
echo ============================================================
echo.
echo Check these folders for results:
echo   - data/       (generated strategies and prices)
echo   - results/    (performance metrics)
echo   - plots/      (charts proving overfitting)
echo.
goto end

:error
echo.
echo ============================================================
echo    ERROR! Something went wrong.
echo ============================================================
echo.
echo Troubleshooting:
echo   1. Make sure you installed dependencies: pip install -r requirements.txt
echo   2. Make sure you're running from the coinflip_strategy_demo folder
echo   3. Check that Python is in your PATH
echo.

:end
pause
