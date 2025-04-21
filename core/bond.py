"""
Bond interfaces and base classes
"""

from abc import ABC, abstractmethod
from datetime import datetime
import math
from typing import List, Dict, Optional, Union, Tuple

from core.date_utils import DateUtils
from core.cash_flow import CashFlow
from core.interest_rate import InterestRateCurve
from utils.math import RootFinder

class Bond(ABC):
    """Abstract base class for bonds"""
    
    @abstractmethod
    def get_cash_flows(self, valuation_date: Optional[datetime] = None) -> List[CashFlow]:
        """Get all cash flows from issuance to maturity"""
        pass
    
    @abstractmethod
    def get_remaining_cash_flows(self, valuation_date: datetime) -> List[CashFlow]:
        """Get cash flows from valuation date onwards"""
        pass
    
    def price(self, valuation_date: datetime, curve: InterestRateCurve) -> float:
        """
        Calculate clean price of the bond
        
        Args:
            valuation_date: Date for which to calculate price
            curve: Interest rate curve for discounting
            
        Returns:
            Clean price of the bond (as a percentage of par)
        """
        cash_flows = self.get_remaining_cash_flows(valuation_date)
        pv = sum(cf.present_value(valuation_date, curve) for cf in cash_flows)
        return pv / self.par_value * 100
    
    # def yield_to_maturity(self, valuation_date: datetime, market_price: float) -> float:
    #     """
    #     Calculate yield to maturity given a market price
        
    #     Args:
    #         valuation_date: Date for which to calculate YTM
    #         market_price: Market price as percentage of par
            
    #     Returns:
    #         Yield to maturity
    #     """
    #     # Convert market price to decimal
    #     market_price_decimal = market_price / 100.0
    #     target_price = market_price_decimal * self.par_value
        
    #     cash_flows = self.get_remaining_cash_flows(valuation_date)
        
    #     def price_function(ytm: float) -> float:
    #         """Calculate bond price for a given yield"""
    #         pv = 0.0
    #         for cf in cash_flows:
    #             time_to_cf = DateUtils.year_fraction(valuation_date, cf.payment_date)
    #             discount_factor = math.exp(-ytm * time_to_cf)
    #             pv += cf.amount * discount_factor
    #         return pv - target_price
        
    #     # Initial guess for YTM (use coupon rate as starting point)
    #     initial_guess = self.coupon_rate
        
    #     # Derivative function for Newton-Raphson
    #     def price_derivative(ytm: float) -> float:
    #         """Calculate derivative of price function with respect to yield"""
    #         dpv = 0.0
    #         for cf in cash_flows:
    #             time_to_cf = DateUtils.year_fraction(valuation_date, cf.payment_date)
    #             discount_factor = math.exp(-ytm * time_to_cf)
    #             dpv -= cf.amount * time_to_cf * discount_factor
    #         return dpv
        
    #     # Try Newton-Raphson method first
    #     try:
    #         ytm, _ = RootFinder.newton_raphson(price_function, price_derivative, initial_guess)
    #         return ytm



        # except ValueError:
        #     # Fallback to bisection method
        #     # Use reasonable bounds for yield (0% to 20%)
        #     lower_bound = 0.0
        #     upper_bound = 0.2
        #     ytm, _ = RootFinder.bisection(price_function, lower_bound, upper_bound)
        #     return ytm

    def yield_to_maturity(self, valuation_date: datetime, market_price: float) -> float:
        """
        Calculate yield to maturity given a market price
        
        Args:
            valuation_date: Date for which to calculate YTM
            market_price: Market price as percentage of par
            
        Returns:
            Yield to maturity
        """
        # Convert market price to decimal
        market_price_decimal = market_price / 100.0
        target_price = market_price_decimal * self.par_value
        
        cash_flows = self.get_remaining_cash_flows(valuation_date)
        
        def price_function(ytm: float) -> float:
            """Calculate bond price for a given yield"""
            pv = 0.0
            for cf in cash_flows:
                time_to_cf = DateUtils.year_fraction(valuation_date, cf.payment_date)
                discount_factor = math.exp(-ytm * time_to_cf)
                pv += cf.amount * discount_factor
            return pv - target_price
        
        # Initial guess for YTM (use coupon rate as starting point)
        initial_guess = self.coupon_rate
        
        # Derivative function for Newton-Raphson
        def price_derivative(ytm: float) -> float:
            """Calculate derivative of price function with respect to yield"""
            dpv = 0.0
            for cf in cash_flows:
                time_to_cf = DateUtils.year_fraction(valuation_date, cf.payment_date)
                discount_factor = math.exp(-ytm * time_to_cf)
                dpv -= cf.amount * time_to_cf * discount_factor
            return dpv
        
        # Try Newton-Raphson method first
        try:
            ytm, _ = RootFinder.newton_raphson(price_function, price_derivative, initial_guess)
            return ytm
        except ValueError:
            # Fallback to bisection method
            # Use reasonable bounds for yield (0% to 20%)
            lower_bound = 0.0
            upper_bound = 0.2
            ytm, _ = RootFinder.bisection(price_function, lower_bound, upper_bound)
            return ytm



    def duration(self, valuation_date: datetime, yield_rate: float) -> float:
        """
        Calculate Macaulay duration
        
        Args:
            valuation_date: Date for which to calculate duration
            yield_rate: Yield rate to use for calculation
            
        Returns:
            Macaulay duration in years
        """
        cash_flows = self.get_remaining_cash_flows(valuation_date)
        duration_weighted_sum = 0.0
        price_sum = 0.0
        
        for cf in cash_flows:
            time_to_cf = DateUtils.year_fraction(valuation_date, cf.payment_date)
            discount_factor = math.exp(-yield_rate * time_to_cf)
            pv = cf.amount * discount_factor
            
            duration_weighted_sum += time_to_cf * pv
            price_sum += pv
            
        if price_sum == 0:
            return 0.0
            
        return duration_weighted_sum / price_sum
    
    def modified_duration(self, valuation_date: datetime, yield_rate: float) -> float:
        """
        Calculate modified duration
        
        Args:
            valuation_date: Date for which to calculate modified duration
            yield_rate: Yield rate to use for calculation
            
        Returns:
            Modified duration
        """
        mac_duration = self.duration(valuation_date, yield_rate)
        # For continuous compounding
        return mac_duration
    
    def convexity(self, valuation_date: datetime, yield_rate: float) -> float:
        """
        Calculate convexity
        
        Args:
            valuation_date: Date for which to calculate convexity
            yield_rate: Yield rate to use for calculation
            
        Returns:
            Convexity
        """
        cash_flows = self.get_remaining_cash_flows(valuation_date)
        convexity_weighted_sum = 0.0
        price_sum = 0.0
        
        for cf in cash_flows:
            time_to_cf = DateUtils.year_fraction(valuation_date, cf.payment_date)
            discount_factor = math.exp(-yield_rate * time_to_cf)
            pv = cf.amount * discount_factor
            
            convexity_weighted_sum += time_to_cf * time_to_cf * pv
            price_sum += pv
            
        if price_sum == 0:
            return 0.0
            
        return convexity_weighted_sum / price_sum
    
    def dv01(self, valuation_date: datetime, yield_rate: float) -> float:
        """
        Calculate DV01 (dollar value of 1 basis point)
        
        Args:
            valuation_date: Date for which to calculate DV01
            yield_rate: Yield rate to use for calculation
            
        Returns:
            DV01 in currency units
        """
        # Calculate price at current yield
        price_base = self._price_from_yield(valuation_date, yield_rate) * self.par_value / 100.0
        
        # Calculate price at yield + 1bp
        price_up = self._price_from_yield(valuation_date, yield_rate + 0.0001) * self.par_value / 100.0
        
        # DV01 is the change in price
        return abs(price_base - price_up)
    
    def _price_from_yield(self, valuation_date: datetime, yield_rate: float) -> float:
        """Helper method to calculate price from yield"""
        cash_flows = self.get_remaining_cash_flows(valuation_date)
        pv = 0.0
        
        for cf in cash_flows:
            time_to_cf = DateUtils.year_fraction(valuation_date, cf.payment_date)
            discount_factor = math.exp(-yield_rate * time_to_cf)
            pv += cf.amount * discount_factor
            
        return pv / self.par_value * 100
    