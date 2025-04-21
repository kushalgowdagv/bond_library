"""
Zero coupon bond implementation
"""

from datetime import datetime
from typing import List, Optional

from bond_library.core.bond import Bond
from bond_library.core.cash_flow import CashFlow
from bond_library.core.date_utils import DateUtils

class ZeroCouponBond(Bond):
    """Zero coupon bond implementation"""
    
    def __init__(self, contract_id: str, security_desc: str, issue_date: str,
                 maturity_date: str, par_value: float, discount_rate: float):
        """
        Initialize zero coupon bond
        
        Args:
            contract_id: Unique identifier for the bond
            security_desc: Description of the bond
            issue_date: Issue date of the bond
            maturity_date: Maturity date of the bond
            par_value: Par value of the bond
            discount_rate: Discount rate used for pricing
        """
        self.contract_id = contract_id
        self.security_desc = security_desc
        self.issue_date = DateUtils.parse_date(issue_date)
        self.maturity_date = DateUtils.parse_date(maturity_date)
        self.par_value = par_value
        self.discount_rate = discount_rate
        self.coupon_rate = 0.0  # Zero coupon bonds have no coupon rate
        self.payment_frequency = 0  # No regular payments
    
    def get_cash_flows(self, valuation_date: Optional[datetime] = None) -> List[CashFlow]:
        """
        Get all cash flows from issuance to maturity
        
        Args:
            valuation_date: Optional valuation date (not used for zero coupon bonds)
            
        Returns:
            List of all cash flows (only one at maturity)
        """
        # Zero coupon bonds only have one cash flow at maturity
        return [CashFlow(self.maturity_date, self.par_value)]
    
    def get_remaining_cash_flows(self, valuation_date: datetime) -> List[CashFlow]:
        """
        Get cash flows from valuation date onwards
        
        Args:
            valuation_date: Date from which to calculate remaining cash flows
            
        Returns:
            List of remaining cash flows
        """
        # If valuation date is after or equal to maturity, no cash flows remain
        if valuation_date >= self.maturity_date:
            return []
        
        # Otherwise, return the single cash flow at maturity
        return [CashFlow(self.maturity_date, self.par_value)]
    
    def yield_to_maturity(self, valuation_date: datetime, market_price: float) -> float:
        """
        Calculate yield to maturity given a market price
        For zero-coupon bonds, this can be calculated directly
        
        Args:
            valuation_date: Date for which to calculate YTM
            market_price: Market price as percentage of par
            
        Returns:
            Yield to maturity
        """
        # Convert market price to decimal
        market_price_decimal = market_price / 100.0
        
        # Calculate time to maturity in years
        years_to_maturity = DateUtils.year_fraction(valuation_date, self.maturity_date)
        
        if years_to_maturity <= 0 or market_price_decimal <= 0:
            return 0.0
        
        # For zero-coupon bonds, YTM can be calculated directly
        # (Par/Price)^(1/t) - 1 = YTM
        ytm = (self.par_value / (market_price_decimal * self.par_value)) ** (1 / years_to_maturity) - 1
        
        return ytm
    