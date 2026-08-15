import os
import numpy as np
import matplotlib.pyplot as plt
from src.analyzer import PortfolioRiskAnalyzer, fetch_historical_returns

tickers = ["AAPL", "MSFT", "GOOGL"]
weights = [0.40, 0.40, 0.20]
initial_investment = 100000
sim_days = 30

# 1. Fetch data stream dataframes
returns_df = fetch_historical_returns(tickers, start_date="2025-01-01")

# 2. Instantiate core portfolio infrastructure
analyzer = PortfolioRiskAnalyzer(weights=weights, initial_investment=initial_investment)

# 3. Project paths driven entirely by GARCH econometric time-series curves
garch_paths = analyzer.run_monte_carlo_garch_simulation(returns_df, days=sim_days, simulations=10)

# 4. Generate the performance visualization chart canvas
plt.figure(figsize=(10, 5))
for i in range(len(garch_paths)):
    lbl = "GARCH Volatility Clustered Path" if i == 0 else ""
    plt.plot(garch_paths[i], color="#1f77b4", alpha=0.7, linewidth=1.5, label=lbl)

plt.title("GARCH(1,1) Time-Series Clustered Portfolio Risk Projections", fontsize=11, fontweight='bold')
plt.xlabel("Trading Simulation Horizon (Days)", fontsize=10)
plt.ylabel("Projected Value Balance ($)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(loc="upper left")
plt.tight_layout()

# Save image asset profile file
os.makedirs("reports", exist_ok=True)
plt.savefig("reports/simulation_chart.png", dpi=300)
print("📈 GARCH econometric model visual chart successfully refreshed inside reports/simulation_chart.png!")

