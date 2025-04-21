"""
Stress testing framework
"""

import numpy as np
from typing import List, Dict, Union, Tuple, Optional, Callable
from datetime import datetime

from bond_library.core.bond import Bond
from bond_library.core.interest_rate import InterestRateCurve
from bond_library.utils.logging import LogManager

class StressTest:
    """Class for stress testing bonds under various scenarios"""
    
    def __init__(self):
        """Initialize stress test framework"""
        self.logger = LogManager().get_logger(__name__)
        self.scenarios = {}
    
    def add_scenario(self, name: str, yield_curve_shift: Callable[[List[float]], List[float]]) -> None:
        """
        Add a stress test scenario
        
        Args:
            name: Name of the scenario
            yield_curve_shift: Function that takes a list of yields and returns modified yields
        """
        self.scenarios[name] = yield_curve_shift
    
    def add_parallel_shift_scenario(self, name: str, shift: float) -> None:
        """
        Add a parallel shift scenario
        
        Args:
            name: Name of the scenario
            shift: Amount to shift yields in basis points
        """
        def parallel_shift(yields: List[float]) -> List[float]:
            return [y + shift/10000 for y in yields]
        
        self.add_scenario(name, parallel_shift)
    
    def add_steepening_scenario(self, name: str, short_shift: float, long_shift: float, pivot_index: int) -> None:
        """
        Add a steepening/flattening scenario
        
        Args:
            name: Name of the scenario
            short_shift: Shift for short-term rates in basis points
            long_shift: Shift for long-term rates in basis points
            pivot_index: Index in the yield list where transition occurs
        """
        def steepening_shift(yields: List[float]) -> List[float]:
            result = yields.copy()
            n = len(yields)
            
            for i in range(n):
                if i < pivot_index:
                    # Short end
                    result[i] += short_shift/10000
                else:
                    # Long end
                    result[i] += long_shift/10000
                    
            return result
        
        self.add_scenario(name, steepening_shift)
    
    def run_single_scenario(self, bond: Bond, valuation_date: datetime, curve: InterestRateCurve, 
                          scenario_name: str) -> Dict[str, float]:
        """
        Run a single stress test scenario
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to run the stress test
            curve: Interest rate curve
            scenario_name: Name of the scenario to run
            
        Returns:
            Dictionary containing stress test results
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")
        
        # Get the yield curve shift function
        yield_curve_shift = self.scenarios[scenario_name]
        
        # Calculate base price
        base_price = bond.price(valuation_date, curve)
        
        # Apply the yield curve shift
        shifted_rates = yield_curve_shift(curve.rates)
        shifted_curve = InterestRateCurve(curve.curve_date, curve.tenors.copy(), shifted_rates)
        
        # Calculate new price
        stressed_price = bond.price(valuation_date, shifted_curve)
        
        # Calculate price change
        price_change = stressed_price - base_price
        percentage_change = price_change / base_price * 100
        
        return {
            "scenario": scenario_name,
            "base_price": base_price,
            "stressed_price": stressed_price,
            "price_change": price_change,
            "percentage_change": percentage_change
        }
    
    def run_all_scenarios(self, bond: Bond, valuation_date: datetime, curve: InterestRateCurve) -> Dict[str, Dict[str, float]]:
        """
        Run all stress test scenarios
        
        Args:
            bond: Bond to analyze
            valuation_date: Date for which to run the stress tests
            curve: Interest rate curve
            
        Returns:
            Dictionary mapping scenario names to their results
        """
        results = {}
        
        for scenario_name in self.scenarios:
            results[scenario_name] = self.run_single_scenario(bond, valuation_date, curve, scenario_name)
            
        return results
    
    def run_multi_bond_scenario(self, bonds: List[Bond], valuation_date: datetime, curve: InterestRateCurve,
                             scenario_name: str) -> Dict[str, Dict[str, float]]:
        """
        Run a scenario across multiple bonds
        
        Args:
            bonds: List of bonds to analyze
            valuation_date: Date for which to run the stress test
            curve: Interest rate curve
            scenario_name: Name of the scenario to run
            
        Returns:
            Dictionary mapping bond IDs to their results
        """
        results = {}
        
        for bond in bonds:
            bond_id = getattr(bond, 'contract_id', f"Bond_{id(bond)}")
            results[bond_id] = self.run_single_scenario(bond, valuation_date, curve, scenario_name)
            
        return results
    
    def create_standard_scenarios(self) -> None:
        """Create a set of standard stress test scenarios"""
        # Parallel shifts
        self.add_parallel_shift_scenario("parallel_up_50bp", 50)
        self.add_parallel_shift_scenario("parallel_up_100bp", 100)
        self.add_parallel_shift_scenario("parallel_up_200bp", 200)
        self.add_parallel_shift_scenario("parallel_down_50bp", -50)
        self.add_parallel_shift_scenario("parallel_down_100bp", -100)
        
        # Steepening and flattening (assuming index 3 is roughly the 2-5 year point)
        self.add_steepening_scenario("steepening_50bp", 0, 50, 3)
        self.add_steepening_scenario("flattening_50bp", 50, 0, 3)
        
        # Custom historical scenarios
        def financial_crisis_2008(yields: List[float]) -> List[float]:
            # Approximate yield curve shifts during 2008 financial crisis
            # Short rates down, long rates up
            result = yields.copy()
            n = len(yields)
            
            for i in range(n):
                if i < 2:  # Very short end
                    result[i] -= 0.02  # -200 bps
                elif i < 4:  # Short/intermediate
                    result[i] -= 0.01  # -100 bps
                else:  # Long end
                    result[i] += 0.005  # +50 bps
                    
            return result
        
        def taper_tantrum_2013(yields: List[float]) -> List[float]:
            # Approximate yield curve shifts during 2013 taper tantrum
            # Parallel shift up with more impact on intermediate yields
            result = yields.copy()
            n = len(yields)
            
            for i in range(n):
                if i < 2:  # Very short end
                    result[i] += 0.001  # +10 bps
                elif i < 4:  # Short/intermediate
                    result[i] += 0.01  # +100 bps
                elif i < 7:  # Intermediate
                    result[i] += 0.014  # +140 bps
                else:  # Long end
                    result[i] += 0.008  # +80 bps
                    
            return result
        
        self.add_scenario("financial_crisis_2008", financial_crisis_2008)
        self.add_scenario("taper_tantrum_2013", taper_tantrum_2013)
        