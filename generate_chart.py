import os
import numpy as np
import matplotlib.pyplot as plt

# Generate mock data: 10 random paths over 30 days starting at 100,000
np.random.seed(42)
days = 30
simulations = 10
paths = np.zeros((simulations, days))
for i in range(simulations):
    shocks = np.random.normal(0.0005, 0.01, days)
    paths[i] = 100000 * np.cumprod(1 + shocks)

# Create the plot
plt.figure(figsize=(10, 5))
for i in range(simulations):
    plt.plot(paths[i], alpha=0.7, linewidth=1.5)

plt.title("Monte Carlo Portfolio Trajectory Simulations (30 Days)", fontsize=12, fontweight='bold')
plt.xlabel("Trading Days", fontsize=10)
plt.ylabel("Portfolio Value ($)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Ensure reports folder exists and save the image
os.makedirs("reports", exist_ok=True)
plt.savefig("reports/simulation_chart.png", dpi=300)
print("📈 Chart successfully generated and saved to reports/simulation_chart.png")

