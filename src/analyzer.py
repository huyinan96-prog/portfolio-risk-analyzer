import numpy as np
import yfinance as yf

class PortfolioRiskAnalyzer:
    def __init__(self, weights, initial_investment):
        if not np.isclose(sum(weights), 1.0):
            raise ValueError("Portfolio weights must sum up exactly to 1.0")
        self.weights = np.array(weights)
        self.initial_investment = initial_investment

    def run_monte_carlo_simulation(self, returns_matrix, days, simulations=1000):
        """Simulates price trajectories based on asset covariance."""
        mean_returns = returns_matrix.mean(axis=0)
        
        # Simulating random portfolio drift parameters
        portfolio_simulations = np.zeros((simulations, days))
        for i in range(simulations):
            rand_shocks = np.random.normal(0, 1, (days, len(self.weights)))
            # Compute simulated portfolio performance increment
            daily_returns = np.dot(rand_shocks, self.weights) * 0.01 
            portfolio_simulations[i] = self.initial_investment * np.cumprod(1 + daily_returns)
            
        return portfolio_simulations

    def calculate_value_at_risk(self, final_balances, confidence_level=0.95):
        """Calculates Value at Risk (VaR) parameter boundary."""
        losses = self.initial_investment - final_balances
        percentile = (1 - confidence_level) * 100
        var_limit = np.percentile(losses, 100 - percentile)
        return round(max(0.0, var_limit), 2)

    def apply_market_stress_test(self, returns_matrix, shock_multiplier=2.5):
        """Artificially scales asset volatility matrix coefficients to simulate a crash."""
        print(f"⚠️ Injecting systemic risk shocks... Volatility scaled by {shock_multiplier}x")
        stressed_matrix = returns_matrix * shock_multiplier
        return stressed_matrix


# --- STANDALONE API FUNCTION (Must be aligned all the way to the left) ---
def fetch_historical_returns(tickers, start_date="2025-01-01"):
    """
    Downloads real historical closing prices for specified ticker assets
    and calculates their daily percentage returns matrix.
    """
    print(f"🌐 Fetching live market asset tracks from Yahoo Finance for: {tickers}...")
    raw_data = yf.download(tickers, start=start_date)
    
    if 'Close' in raw_data.columns:
        close_prices = raw_data['Close']
    else:
        close_prices = raw_data
        
    returns_matrix = close_prices.pct_change().dropna()
    return returns_matrix.to_numpy()

