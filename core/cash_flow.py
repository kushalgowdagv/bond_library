"""
Cash flow models and calculations.
"""

from datetime import datetime
from typing import List, Dict, Optional
from core.interest_rate import InterestRateCurve
from core.date_utils import DateUtils

class CashFlow:
    """Base class for cash flows"""
    
    def __init__(self, payment_date: datetime, amount: float):
        """
        Initialize cash flow
        
        Args:
            payment_date: Date when the cash flow occurs
            amount: Amount of the cash flow
        """
        self.payment_date = payment_date
        self.amount = amount
    
    def present_value(self, valuation_date: datetime, curve: InterestRateCurve) -> float:
        """
        Calculate present value of the cash flow using discrete compounding
        
        Args:
            valuation_date: Date for which to calculate present value
            curve: Interest rate curve for discounting
            
        Returns:
            Present value of the cash flow
        """
        if self.payment_date <= valuation_date:
            return 0.0
        
        # Get discount factor from the curve
        # Note: We need to modify the InterestRateCurve class to use discrete compounding too
        discount_factor = curve.get_discount_factor(valuation_date, self.payment_date)
        return self.amount * discount_factor
    