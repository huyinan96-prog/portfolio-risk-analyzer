# 🏦 End-to-End Quantitative Portfolio Risk Analyzer

An algorithmic trading and risk infrastructure built to evaluate multi-asset portfolio distributions, compute daily volatility matrices, and calculate quantitative Value at Risk (VaR) parameters.

## 📊 Quantitative Workflow Engine
```mermaid
graph LR
    Weights[Asset Allocations] -->|Covariance Weighting| Sim[Monte Carlo Simulator]
    Sim -->|Price Drift Paths| Yields[Simulation Array Outputs]
    Yields -->|Percentile Thresholding| VaR[Value at Risk Report]
```

## 📈 Simulated Trajectory Distribution Bounds
The analyzer projects asset distributions under simulated pricing shock constraints. The model maps potential portfolio value degradation to determine loss limits (VaR (95%)):
![Portfolio Simulation Chart](reports/simulation_chart.png)

## ⚠️ Volatility Stress Testing & Scenario Profiling
To protect asset positions against heavy tail-risk anomalies, the core engine introduces artificial macroeconomic shocks (scaling historical return variance matrices by a 3.0x multiplier factor). This simulates systemic contraction events—such as the 2008 Liquidity Crisis or the 2020 Volatility Spikes—enabling quantitative analysts to calculate max drawdown expectations under high-stress constraints.

## 🛠️ Financial Computing Stack
- **Language Environment:** Python 3.11
- **Computational Math Library:** NumPy Array Projections
- **Pipeline Quality Assurance:** Pytest Matrix Checkpoints

## 💻 Local Workspace Run
```bash
git clone https://github.com/huyinan96-prog/portfolio-risk-analyzer
cd portfolio-risk-analyzer
pip install pytest
pytest
```
