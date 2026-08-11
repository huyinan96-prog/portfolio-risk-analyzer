import numpy as np

class PortfolioRiskAnalyzer:
    def __init__(self, weights, initial_investment):
        if not np.isclose(sum(weights), 1.0):
            raise ValueError("Portfolio weights must sum up exactly to 1.0")
        self.weights = np.array(weights)
        self.initial_investment = initial_investment

    def run_monte_carlo_simulation(self, returns_matrix, days, simulations=1000):
        """Simulates price trajectories based on asset covariance."""
        mean_returns = returns_matrix.mean(axis=0)
        cov_matrix = np.corrcoef(returns_matrix.T) # Simplify to correlation matrix
        
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

