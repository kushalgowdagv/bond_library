"""
Interest rate models and curves
"""

import pandas as pd
import math
from datetime import datetime
from typing import List, Dict, Optional, Union
from core.date_utils import DateUtils

class InterestRateCurve:
    """Class representing an interest rate curve with interpolation capabilities"""
    
    def __init__(self, curve_date: datetime, tenors: List[float], rates: List[float]):
        """
        Initialize interest rate curve
        
        Args:
            curve_date: The reference date for the curve
            tenors: List of tenors in years
            rates: List of interest rates corresponding to tenors
        """
        self.curve_date = curve_date
        self.tenors = tenors
        self.rates = rates
        
        # Validate inputs
        if len(tenors) != len(rates):
            raise ValueError("Tenors and rates must have the same length")
        if len(tenors) < 2:
            raise ValueError("At least two points are needed for interpolation")
            
        # Sort by tenor
        sorted_data = sorted(zip(tenors, rates))
        self.tenors = [x[0] for x in sorted_data]
        self.rates = [x[1] for x in sorted_data]
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'InterestRateCurve':
        """Create an interest rate curve from a pandas DataFrame"""
        curve_date = DateUtils.parse_date(df['Date'].iloc[0])
        tenors = df['Tenor'].tolist()
        rates = df['Rate'].tolist()
        return cls(curve_date, tenors, rates)
    
    def get_rate(self, tenor: float) -> float:
        """
        Get interpolated rate for a given tenor
        
        Args:
            tenor: The tenor in years for which to get the rate
            
        Returns:
            Interpolated interest rate
        """
        # Handle out of bounds
        if tenor <= self.tenors[0]:
            return self.rates[0]
        if tenor >= self.tenors[-1]:
            return self.rates[-1]
        
        # Linear interpolation
        for i in range(len(self.tenors) - 1):
            if self.tenors[i] <= tenor <= self.tenors[i + 1]:
                t0, t1 = self.tenors[i], self.tenors[i + 1]
                r0, r1 = self.rates[i], self.rates[i + 1]
                
                # Linear interpolation formula
                return r0 + (r1 - r0) * (tenor - t0) / (t1 - t0)
        
        # Should never get here
        raise ValueError(f"Failed to interpolate rate for tenor {tenor}")
    
    def get_discount_factor(self, valuation_date: datetime, future_date: datetime) -> float:
        """
        Calculate discount factor from valuation date to future date
        
        Args:
            valuation_date: The reference date
            future_date: The future date for which to calculate discount factor
            
        Returns:
            Discount factor
        """
        # Calculate year fraction
        year_fraction = DateUtils.year_fraction(valuation_date, future_date)
        if year_fraction <= 0:
            return 1.0
            
        # Get corresponding rate and calculate discount factor
        rate = self.get_rate(year_fraction)
        return math.exp(-rate * year_fraction)
    