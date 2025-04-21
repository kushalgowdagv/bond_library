"""
Bond Pricing Library

A comprehensive library for fixed income pricing, risk analysis, and portfolio management.
Supports multiple bond types, yield curve construction, and risk metrics calculation.

Usage:
    from bond_lib import FixedRateBond, FloatingRateBond, ZeroCouponBond
    from bond_lib import InterestRateCurve, RiskMetrics

Version: 0.1.0
"""

# Import core components
from core.bond import Bond
from core.interest_rate import InterestRateCurve
from core.cash_flow import CashFlow
from core.date_utils import DateUtils

# Import instrument implementations
from instruments.fixed_rate import FixedRateBond
from instruments.floating_rate import FloatingRateBond
from instruments.zero_coupon import ZeroCouponBond

# Import risk components
from risk.metrics import RiskMetrics
from risk.stress_test import StressTest
from risk.var import ValueAtRisk

# Import adapters
from adapters.data_source import DataSource, CSVDataSource
from adapters.output import OutputAdapter, CSVOutputAdapter

# Import utilities
from utils.config import Config
from utils.logging import LogManager

# Package version
__version__ = '0.1.0'

# Export public interface
__all__ = [
    # Core
    'Bond', 'InterestRateCurve', 'CashFlow', 'DateUtils',
    
    # Instruments
    'FixedRateBond', 'FloatingRateBond', 'ZeroCouponBond',
    
    # Risk
    'RiskMetrics', 'StressTest', 'ValueAtRisk',
    
    # Adapters
    'DataSource', 'CSVDataSource', 'OutputAdapter', 'CSVOutputAdapter',
    
    # Utils
    'Config', 'LogManager'
]