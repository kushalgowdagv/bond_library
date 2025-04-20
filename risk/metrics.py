"""
Risk metrics implementation
"""

import numpy as np
from typing import List, Dict, Union, Tuple, Optional
from datetime import datetime

from ..core.bond import Bond
from ..core.interest_rate import InterestRateCurve
from ..utils.logging import LogManager

class RiskMetrics:
    """Class for calculating risk metrics for bonds"""
    
    def __init__(self):
        """Initialize risk metrics calculator"""
        self.logger = LogManager().get_logger(__name__)
    
    @staticmethod
    def price_sensitivity(bond: Bond, valuation_date: datetime, yield_shift: float = 0.0001) -> float:
        """
        Calculate price sensitivity (percentage change) for a small yield shift
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate risk metrics
            yield_shift: Yield shift in decimal (default: 1 basis point)
            
        Returns:
            Price sensitivity as a percentage
        """
        # Get current yield
        current_yield = bond.yield_to_maturity(valuation_date, bond.price(valuation_date, None))
        
        # Calculate price at current yield
        price_base = bond._price_from_yield(valuation_date, current_yield)
        
        # Calculate price at shifted yield
        price_shifted = bond._price_from_yield(valuation_date, current_yield + yield_shift)
        
        # Calculate price sensitivity
        sensitivity = (price_shifted - price_base) / price_base * 100
        
        return sensitivity
    
    @staticmethod
    def interest_rate_risk(bond: Bond, valuation_date: datetime, yield_rate: float) -> Dict[str, float]:
        """
        Calculate interest rate risk metrics
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate risk metrics
            yield_rate: Yield rate to use for calculation
            
        Returns:
            Dictionary containing various interest rate risk metrics
        """
        # Calculate duration
        duration = bond.duration(valuation_date, yield_rate)
        
        # Calculate modified duration
        modified_duration = bond.modified_duration(valuation_date, yield_rate)
        
        # Calculate convexity
        convexity = bond.convexity(valuation_date, yield_rate)
        
        # Calculate DV01
        dv01 = bond.dv01(valuation_date, yield_rate)
        
        # Price exposure to a 100bp move
        price_100bp = -modified_duration * 0.01 * 100 + 0.5 * convexity * (0.01 ** 2) * 100
        
        return {
            "duration": duration,
            "modified_duration": modified_duration,
            "convexity": convexity,
            "dv01": dv01,
            "price_100bp": price_100bp
        }
    
    @staticmethod
    def basis_point_value(bond: Bond, valuation_date: datetime, yield_rate: float) -> float:
        """
        Calculate basis point value (BPV) - same as DV01
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate BPV
            yield_rate: Yield rate to use for calculation
            
        Returns:
            Basis point value in currency units
        """
        return bond.dv01(valuation_date, yield_rate)
    
    @staticmethod
    def key_rate_duration(bond: Bond, valuation_date: datetime, curve: InterestRateCurve, 
                         key_tenors: List[float], shift: float = 0.0001) -> Dict[float, float]:
        """
        Calculate key rate durations
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate key rate durations
            curve: Interest rate curve
            key_tenors: List of key tenors for which to calculate durations
            shift: Yield shift in decimal (default: 1 basis point)
            
        Returns:
            Dictionary mapping tenors to key rate durations
        """
        # Get base price
        base_price = bond.price(valuation_date, curve)
        
        # Calculate key rate durations
        krd = {}
        for tenor in key_tenors:
            # Create a shifted curve for this tenor
            shifted_rates = curve.rates.copy()
            tenor_index = None
            
            # Find the closest tenor
            for i, t in enumerate(curve.tenors):
                if abs(t - tenor) < 1e-6:
                    tenor_index = i
                    break
            
            if tenor_index is not None:
                # Shift this tenor's rate
                shifted_rates[tenor_index] += shift
                
                # Create a new curve with the shifted rate
                shifted_curve = InterestRateCurve(curve.curve_date, curve.tenors.copy(), shifted_rates)
                
                # Calculate price with shifted curve
                shifted_price = bond.price(valuation_date, shifted_curve)
                
                # Calculate key rate duration
                krd[tenor] = -1 * (shifted_price - base_price) / (shift * base_price)
            
        return krd
    
    @staticmethod
    def calculate_spread_risk(bond: Bond, valuation_date: datetime, credit_spread_shift: float = 0.0001) -> float:
        """
        Calculate sensitivity to credit spread changes
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to calculate spread risk
            credit_spread_shift: Credit spread shift in decimal (default: 1 basis point)
            
        Returns:
            Spread duration
        """
        # For simple implementation, spread duration is approximately equal to modified duration
        current_yield = bond.yield_to_maturity(valuation_date, bond.price(valuation_date, None))
        modified_duration = bond.modified_duration(valuation_date, current_yield)
        
        return modified_duration
    