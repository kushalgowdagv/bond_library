"""
Floating rate bond implementation
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

from core.bond import Bond
from core.cash_flow import CashFlow
from core.date_utils import DateUtils
from core.interest_rate import InterestRateCurve

class FloatingRateBond(Bond):
    """Floating rate bond implementation"""
    
    def __init__(self, contract_id: str, security_desc: str, issue_date: str,
                 maturity_date: str, par_value: float, spread: float, reference_rate_name: str,
                 payment_frequency: int = 2):
        """
        Initialize floating rate bond
        
        Args:
            contract_id: Unique identifier for the bond
            security_desc: Description of the bond
            issue_date: Issue date of the bond
            maturity_date: Maturity date of the bond
            par_value: Par value of the bond
            spread: Spread over the reference rate
            reference_rate_name: Name of the reference rate (e.g., "LIBOR", "SOFR")
            payment_frequency: Number of coupon payments per year (default: 2 for semi-annual)
        """
        self.contract_id = contract_id
        self.security_desc = security_desc
        self.issue_date = DateUtils.parse_date(issue_date)
        self.maturity_date = DateUtils.parse_date(maturity_date)
        self.par_value = par_value
        self.spread = spread
        self.reference_rate_name = reference_rate_name
        self.payment_frequency = payment_frequency
        self.coupon_rate = spread  # For compatibility with Bond base class
        
        # Calculate payment interval in months
        self.payment_interval_months = 12 // payment_frequency
        
        # Future rates for each payment date (to be populated)
        self.forward_rates = {}
    
    def set_forward_curve(self, forward_curve: Dict[datetime, float]) -> None:
        """
        Set forward rates for calculating future cash flows
        
        Args:
            forward_curve: Dictionary mapping payment dates to forward rates
        """
        self.forward_rates = forward_curve
    
    def get_rate_for_date(self, date: datetime) -> float:
        """
        Get rate for a specific date
        
        Args:
            date: Date for which to get the rate
            
        Returns:
            Reference rate + spread
        """
        # If we have a forward curve, use it
        if date in self.forward_rates:
            return self.forward_rates[date] + self.spread
        
        # Otherwise, use the spread only (assume reference rate will be determined later)
        return self.spread
    
    def get_cash_flows(self, valuation_date: Optional[datetime] = None) -> List[CashFlow]:
        """
        Get all cash flows from issuance to maturity
        
        Args:
            valuation_date: Optional valuation date for forward rates
            
        Returns:
            List of all cash flows
        """
        cash_flows = []
        
        # Calculate first coupon date
        first_coupon_date = self.issue_date
        while first_coupon_date <= self.issue_date:
            first_coupon_date = DateUtils.add_months(first_coupon_date, self.payment_interval_months)
        
        # Generate all coupon dates from first coupon to maturity
        current_date = first_coupon_date
        while current_date <= self.maturity_date:
            # For past dates, we should have actual rates
            # For future dates, we use forward rates if available
            rate = self.get_rate_for_date(current_date)
            
            # Calculate coupon amount
            coupon_amount = self.par_value * rate / self.payment_frequency
            
            # Add coupon payment
            if current_date <= self.maturity_date:
                cash_flows.append(CashFlow(current_date, coupon_amount))
            
            # Move to next payment date
            current_date = DateUtils.add_months(current_date, self.payment_interval_months)
        
        # Add principal payment at maturity
        maturity_cf = next((cf for cf in cash_flows if cf.payment_date == self.maturity_date), None)
        if maturity_cf:
            # Update existing cash flow to include principal
            maturity_cf.amount += self.par_value
        else:
            # Add new cash flow for principal
            cash_flows.append(CashFlow(self.maturity_date, self.par_value))
        
        return cash_flows
    
    def get_remaining_cash_flows(self, valuation_date: datetime) -> List[CashFlow]:
        """
        Get cash flows from valuation date onwards
        
        Args:
            valuation_date: Date from which to calculate remaining cash flows
            
        Returns:
            List of remaining cash flows
        """
        all_cash_flows = self.get_cash_flows(valuation_date)
        return [cf for cf in all_cash_flows if cf.payment_date > valuation_date]
    