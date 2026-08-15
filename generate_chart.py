import os
import numpy as np
import matplotlib.pyplot as plt
from src.analyzer import PortfolioRiskAnalyzer, fetch_historical_returns

# Setup our tech stock portfolio distribution profile
tickers = ["AAPL", "MSFT", "GOOGL"]
weights = [0.40, 0.40, 0.20]
initial_investment = 100000
sim_days = 30

# 1. Gather live 2026 market returns data stream
returns_matrix = fetch_historical_returns(tickers, start_date="2026-01-01")

# 2. Instantiate core math analyzer engine 
analyzer = PortfolioRiskAnalyzer(weights=weights, initial_investment=initial_investment)

# 3. Simulate Normal Market Trajectories
normal_paths = analyzer.run_monte_carlo_simulation(returns_matrix, days=sim_days, simulations=5)

# 4. Generate Crash Scenario Return Streams & Simulate
stressed_matrix = analyzer.apply_market_stress_test(returns_matrix, shock_multiplier=3.0)
crash_paths = analyzer.run_monte_carlo_simulation(stressed_matrix, days=sim_days, simulations=5)

# 5. Build the Dual-Comparison Visual Graph Canvas
plt.figure(figsize=(10, 5))

# Plot normal market trajectories in solid green lines
for i in range(len(normal_paths)):
    lbl = "Normal Baseline" if i == 0 else ""
    plt.plot(normal_paths[i], color="#2ca02c", alpha=0.6, linewidth=1.5, label=lbl)

# Plot crash scenario trajectories in dashed red lines
for i in range(len(crash_paths)):
    lbl = "Market Crash Scenario" if i == 0 else ""
    plt.plot(crash_paths[i], color="#d62728", linestyle="--", alpha=0.7, linewidth=1.5, label=lbl)

plt.title(f"Quantitative Risk Analysis: Baseline vs Macroeconomic Stress Test ({tickers})", fontsize=11, fontweight='bold')
plt.xlabel("Trading Simulation Horizon (Days)", fontsize=10)
plt.ylabel("Projected Value Balance ($)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(loc="upper left")
plt.tight_layout()

# Save image asset file
os.makedirs("reports", exist_ok=True)
plt.savefig("reports/simulation_chart.png", dpi=300)
print("📈 Dual-scenario simulation comparison graph generated successfully!")

