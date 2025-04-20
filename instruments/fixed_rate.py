"""
Fixed rate bond implementation
"""

from datetime import datetime
from typing import List, Optional

from ..core.bond import Bond
from ..core.cash_flow import CashFlow
from ..core.date_utils import DateUtils

class FixedRateBond(Bond):
    """Fixed rate bond implementation"""
    
    def __init__(self, contract_id: str, security_desc: str, issue_date: str, 
                 maturity_date: str, par_value: float, coupon_rate: float, 
                 payment_frequency: int = 2):
        """
        Initialize fixed rate bond
        
        Args:
            contract_id: Unique identifier for the bond
            security_desc: Description of the bond
            issue_date: Issue date of the bond
            maturity_date: Maturity date of the bond
            par_value: Par value of the bond
            coupon_rate: Annual coupon rate as a decimal
            payment_frequency: Number of coupon payments per year (default: 2 for semi-annual)
        """
        self.contract_id = contract_id
        self.security_desc = security_desc
        self.issue_date = DateUtils.parse_date(issue_date)
        self.maturity_date = DateUtils.parse_date(maturity_date)
        self.par_value = par_value
        self.coupon_rate = coupon_rate
        self.payment_frequency = payment_frequency
        
        # Calculate payment interval in months
        self.payment_interval_months = 12 // payment_frequency
    
    def get_cash_flows(self, valuation_date: Optional[datetime] = None) -> List[CashFlow]:
        """
        Get all cash flows from issuance to maturity
        
        Args:
            valuation_date: Optional valuation date (not used for all cash flows)
            
        Returns:
            List of all cash flows
        """
        cash_flows = []
        
        # Calculate first coupon date - move forward from issue date by payment interval
        # Start with issue date and move to the next payment period
        first_coupon_date = self.issue_date
        while first_coupon_date <= self.issue_date:
            first_coupon_date = DateUtils.add_months(first_coupon_date, self.payment_interval_months)
        
        # Generate all coupon dates from first coupon to maturity
        current_date = first_coupon_date
        while current_date <= self.maturity_date:
            # Calculate coupon amount
            coupon_amount = self.par_value * self.coupon_rate / self.payment_frequency
            
            # Add coupon payment if it's not beyond maturity
            if current_date <= self.maturity_date:
                cash_flows.append(CashFlow(current_date, coupon_amount))
            
            # Move to next payment date
            current_date = DateUtils.add_months(current_date, self.payment_interval_months)
        
        # Add principal payment at maturity
        # Check if we already have a cash flow on maturity date
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
        all_cash_flows = self.get_cash_flows()
        return [cf for cf in all_cash_flows if cf.payment_date > valuation_date]
    