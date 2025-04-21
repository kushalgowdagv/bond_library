"""
Value at Risk calculations
"""

import numpy as np
from typing import List, Dict, Union, Tuple, Optional
from datetime import datetime, timedelta

from bond_library.core.bond import Bond
from bond_library.utils.logging import LogManager

class ValueAtRisk:
    """Class for calculating Value at Risk metrics"""
    
    def __init__(self):
        """Initialize Value at Risk calculator"""
        self.logger = LogManager().get_logger(__name__)
    
    @staticmethod
    def historical_var(bond: Bond, valuation_date: datetime, 
                       historical_yields: List[float], confidence_level: float = 0.95, 
                       time_horizon: int = 10) -> float:
        """
        Calculate historical Value at Risk
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate VaR
            historical_yields: List of historical yield observations
            confidence_level: Confidence level (default: 95%)
            time_horizon: Time horizon in days (default: 10 days)
            
        Returns:
            Value at Risk as a percentage of portfolio value
        """
        # Calculate current price
        current_yield = bond.yield_to_maturity(valuation_date, bond.price(valuation_date, None))
        current_price = bond._price_from_yield(valuation_date, current_yield)
        
        # Calculate daily yield changes
        daily_changes = []
        for i in range(1, len(historical_yields)):
            daily_changes.append(historical_yields[i] - historical_yields[i-1])
        
        # Calculate price changes for each yield change
        price_changes = []
        for change in daily_changes:
            new_yield = current_yield + change
            new_price = bond._price_from_yield(valuation_date, new_yield)
            price_changes.append((new_price - current_price) / current_price)
        
        # Sort price changes
        price_changes.sort()
        
        # Scale daily changes to the time horizon
        scaling_factor = np.sqrt(time_horizon)
        
        # Find the VaR at the given confidence level
        var_index = int(len(price_changes) * (1 - confidence_level))
        var = abs(price_changes[var_index] * scaling_factor) * 100  # Convert to percentage
        
        return var
    
    @staticmethod
    def parametric_var(bond: Bond, valuation_date: datetime, 
                      yield_volatility: float, confidence_level: float = 0.95, 
                      time_horizon: int = 10) -> float:
        """
        Calculate parametric Value at Risk using modified duration
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate VaR
            yield_volatility: Annual yield volatility
            confidence_level: Confidence level (default: 95%)
            time_horizon: Time horizon in days (default: 10 days)
            
        Returns:
            Value at Risk as a percentage of portfolio value
        """
        # Calculate current yield
        current_yield = bond.yield_to_maturity(valuation_date, bond.price(valuation_date, None))
        
        # Calculate modified duration
        modified_duration = bond.modified_duration(valuation_date, current_yield)
        
        # Calculate daily volatility
        daily_volatility = yield_volatility / np.sqrt(252)  # Assuming 252 trading days
        
        # Scale to time horizon
        time_horizon_volatility = daily_volatility * np.sqrt(time_horizon)
        
        # Calculate Z-score for confidence level
        z_score = abs(np.percentile(np.random.normal(0, 1, 100000), (1 - confidence_level) * 100))
        
        # Calculate VaR
        var = modified_duration * time_horizon_volatility * z_score * 100  # Convert to percentage
        
        return var
    
    @staticmethod
    def monte_carlo_var(bond: Bond, valuation_date: datetime, 
                       yield_mean: float, yield_volatility: float, 
                       confidence_level: float = 0.95, time_horizon: int = 10, 
                       num_simulations: int = 10000) -> float:
        """
        Calculate Monte Carlo Value at Risk
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate VaR
            yield_mean: Mean of the yield changes
            yield_volatility: Volatility of the yield changes
            confidence_level: Confidence level (default: 95%)
            time_horizon: Time horizon in days (default: 10 days)
            num_simulations: Number of Monte Carlo simulations (default: 10,000)
            
        Returns:
            Value at Risk as a percentage of portfolio value
        """
        # Calculate current yield and price
        current_yield = bond.yield_to_maturity(valuation_date, bond.price(valuation_date, None))
        current_price = bond._price_from_yield(valuation_date, current_yield)
        
        # Scale parameters to time horizon
        time_horizon_mean = yield_mean * time_horizon / 252  # Assuming 252 trading days
        time_horizon_volatility = yield_volatility * np.sqrt(time_horizon / 252)
        
        # Simulate yield changes
        np.random.seed(42)  # For reproducibility
        simulated_changes = np.random.normal(time_horizon_mean, time_horizon_volatility, num_simulations)
        
        # Calculate price changes for each yield change
        price_changes = []
        for change in simulated_changes:
            new_yield = current_yield + change
            new_price = bond._price_from_yield(valuation_date, new_yield)
            price_changes.append((new_price - current_price) / current_price)
        
        # Sort price changes
        price_changes.sort()
        
        # Find the VaR at the given confidence level
        var_index = int(num_simulations * (1 - confidence_level))
        var = abs(price_changes[var_index]) * 100  # Convert to percentage
        
        return var
    
    @staticmethod
    def expected_shortfall(bond: Bond, valuation_date: datetime, 
                          yield_volatility: float, confidence_level: float = 0.95, 
                          time_horizon: int = 10, num_simulations: int = 10000) -> float:
        """
        Calculate Expected Shortfall (Conditional VaR)
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate ES
            yield_volatility: Annual yield volatility
            confidence_level: Confidence level (default: 95%)
            time_horizon: Time horizon in days (default: 10 days)
            num_simulations: Number of Monte Carlo simulations (default: 10,000)
            
        Returns:
            Expected Shortfall as a percentage of portfolio value
        """
        # Calculate current yield and price
        current_yield = bond.yield_to_maturity(valuation_date, bond.price(valuation_date, None))
        current_price = bond._price_from_yield(valuation_date, current_yield)
        
        # Scale parameters to time horizon
        time_horizon_volatility = yield_volatility * np.sqrt(time_horizon / 252)
        
        # Simulate yield changes
        np.random.seed(42)  # For reproducibility
        simulated_changes = np.random.normal(0, time_horizon_volatility, num_simulations)
        
        # Calculate price changes for each yield change
        price_changes = []
        for change in simulated_changes:
            new_yield = current_yield + change
            new_price = bond._price_from_yield(valuation_date, new_yield)
            price_changes.append((new_price - current_price) / current_price)
        
        # Sort price changes
        price_changes.sort()
        
        # Find the VaR at the given confidence level
        var_index = int(num_simulations * (1 - confidence_level))
        
        # Calculate ES as the average of losses beyond VaR
        es_values = price_changes[:var_index]
        es = abs(np.mean(es_values)) * 100  # Convert to percentage
        
        return es
    