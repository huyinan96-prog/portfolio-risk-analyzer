import pytest
import numpy as np
from src.analyzer import PortfolioRiskAnalyzer

def test_invalid_weights_error():
    # Asset weights do not sum up to 1.0 (Invalid portfolio)
    with pytest.raises(ValueError):
        PortfolioRiskAnalyzer(weights=[0.5, 0.2], initial_investment=100000)

def test_value_at_risk_calculation():
    # Setup a standard balanced asset profile
    analyzer = PortfolioRiskAnalyzer(weights=[0.6, 0.4], initial_investment=100000)
    
    # Generate mock random standard historical matrix for testing
    mock_final_balances = np.array([98000, 95000, 91000, 85000, 70000, 99000, 102000])
    var_result = analyzer.calculate_value_at_risk(mock_final_balances, confidence_level=0.95)
    
    # Ensure VaR calculates a valid non-negative threshold boundary loss asset limit
    assert isinstance(var_result, float)
    assert var_result >= 0.0

