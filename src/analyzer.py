import numpy as np
import yfinance as yf
from arch import arch_model

class PortfolioRiskAnalyzer:
    def __init__(self, weights, initial_investment):
        if not np.isclose(sum(weights), 1.0):
            raise ValueError("Portfolio weights must sum up exactly to 1.0")
        self.weights = np.array(weights)
        self.initial_investment = initial_investment

    def run_monte_carlo_garch_simulation(self, returns_dataframe, days=30, simulations=10):
        """
        Executes an advanced Monte Carlo projection where daily random price walk drift
        is driven by GARCH volatility time-series forecasts rather than static historical averages.
        """
        tickers = returns_dataframe.columns
        garch_vols = {}
        
        # Calculate dynamic volatility metrics independently for each stock ticker
        for ticker in tickers:
            garch_vols[ticker] = forecast_garch_volatility(returns_dataframe[ticker].to_numpy(), horizon=days)
            
        portfolio_simulations = np.zeros((simulations, days))
        
        for sim in range(simulations):
            simulated_asset_prices = np.zeros((days, len(self.weights)))
            
            for t_idx, ticker in enumerate(tickers):
                # Apply the unique daily forecasted volatility curve for the specific asset
                daily_vols = garch_vols[ticker]
                rand_shocks = np.random.normal(0, 1, days)
                
                # Model price steps scaled precisely by time-series variance clustering curves
                simulated_asset_prices[:, t_idx] = rand_shocks * daily_vols
                
            # Aggregate the asset pathways down into weighted portfolio trajectory steps
            portfolio_returns = np.dot(simulated_asset_prices, self.weights)
            portfolio_simulations[sim] = self.initial_investment * np.cumprod(1 + portfolio_returns)
            
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



def forecast_garch_volatility(returns_vector, horizon=30):
    """
    Fits a GARCH(1,1) time-series model to an asset's historical returns
    to forecast dynamic conditional volatility over a 30-day projection horizon.
    """
    print("🤖 Estimating time-series conditional variance via GARCH(1,1)...")
    
    # Scale returns up to prevent optimization convergence warnings
    scaled_returns = returns_vector * 100
    
    # Define a standard GARCH(1,1) configuration
    model = arch_model(scaled_returns, p=1, q=1, vol='Garch', dist='normal', rescale=False)
    fitted_model = model.fit(disp='off')
    
    # Forecast variance boundaries out over the horizon
    forecasts = fitted_model.forecast(horizon=horizon)
    forecasted_variance = forecasts.variance.values[-1]
    
    # Convert variance back down to standard deviation return scales
    forecasted_volatility = np.sqrt(forecasted_variance) / 100
    return forecasted_volatility


# --- UPDATED DATA FETCH CHANNELS WITH SCALING INTEGRATION ---
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
    return returns_matrix

