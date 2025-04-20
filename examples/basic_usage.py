#!/usr/bin/env python
"""
Basic usage example of the bond library
"""

import os
import pandas as pd
from datetime import datetime

from bond_library.core.date_utils import DateUtils
from bond_library.core.interest_rate import InterestRateCurve
from bond_library.instruments.fixed_rate import FixedRateBond
from bond_library.instruments.floating_rate import FloatingRateBond
from bond_library.instruments.zero_coupon import ZeroCouponBond
from bond_library.adapters.data_source import CSVDataSource
from bond_library.adapters.output import JSONOutputAdapter
from bond_library.utils.config import Config
from bond_library.utils.logging import LogManager

def main():
    """Main function demonstrating basic usage"""
    # Set up logging
    logger = LogManager().get_logger(__name__)
    logger.info("Starting basic usage example")
    
    # Set up configuration
    config = Config()
    config.set('io', 'default_format', 'json')
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a fixed rate bond
    logger.info("Creating a fixed rate bond")
    fixed_bond = FixedRateBond(
        contract_id="US-TREAS-5Y",
        security_desc="US Treasury 5-Year Note",
        issue_date="2022-01-15",
        maturity_date="2027-01-15",
        par_value=1000.0,
        coupon_rate=0.025,  # 2.5%
        payment_frequency=2  # Semi-annual
    )
    
    # Create a zero coupon bond
    logger.info("Creating a zero coupon bond")
    zero_bond = ZeroCouponBond(
        contract_id="US-ZERO-2Y",
        security_desc="US Treasury 2-Year Zero Coupon",
        issue_date="2022-01-15",
        maturity_date="2024-01-15",
        par_value=1000.0,
        discount_rate=0.02  # 2%
    )
    
    # Create a floating rate bond
    logger.info("Creating a floating rate bond")
    floating_bond = FloatingRateBond(
        contract_id="US-FLOAT-3Y",
        security_desc="US Treasury 3-Year Floating Rate Note",
        issue_date="2022-01-15",
        maturity_date="2025-01-15",
        par_value=1000.0,
        spread=0.005,  # 0.5% spread over reference rate
        reference_rate_name="SOFR",
        payment_frequency=4  # Quarterly
    )
    
    # Create yield curve
    logger.info("Creating yield curve")
    curve_date = datetime.now()
    tenors = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0]
    rates = [0.0050, 0.0075, 0.0125, 0.0175, 0.0200, 0.0250, 0.0275, 0.0300, 0.0325, 0.0350]
    curve = InterestRateCurve(curve_date, tenors, rates)
    
    # Calculate bond prices
    valuation_date = datetime.now()
    fixed_price = fixed_bond.price(valuation_date, curve)
    zero_price = zero_bond.price(valuation_date, curve)
    
    # Set forward rates for floating rate bond
    forward_dates = [
        DateUtils.add_months(valuation_date, 3),
        DateUtils.add_months(valuation_date, 6),
        DateUtils.add_months(valuation_date, 9),
        DateUtils.add_months(valuation_date, 12)
    ]
    forward_rates = {
        forward_dates[0]: 0.02,  # 2%
        forward_dates[1]: 0.022,  # 2.2%
        forward_dates[2]: 0.024,  # 2.4%
        forward_dates[3]: 0.026   # 2.6%
    }
    floating_bond.set_forward_curve(forward_rates)
    floating_price = floating_bond.price(valuation_date, curve)
    
    # Print results
    print(f"Fixed Rate Bond Price: {fixed_price:.4f}")
    print(f"Zero Coupon Bond Price: {zero_price:.4f}")
    print(f"Floating Rate Bond Price: {floating_price:.4f}")
    
    # Get cash flows for fixed rate bond
    cash_flows = fixed_bond.get_remaining_cash_flows(valuation_date)
    print("\nFixed Rate Bond Cash Flows:")
    for cf in cash_flows:
        print(f"Date: {cf.payment_date.strftime('%Y-%m-%d')}, Amount: ${cf.amount:.2f}")
    
    # Calculate YTM for fixed rate bond
    ytm = fixed_bond.yield_to_maturity(valuation_date, fixed_price)
    print(f"\nFixed Rate Bond YTM: {ytm*100:.4f}%")
    
    # Calculate duration and convexity
    duration = fixed_bond.duration(valuation_date, ytm)
    modified_duration = fixed_bond.modified_duration(valuation_date, ytm)
    convexity = fixed_bond.convexity(valuation_date, ytm)
    
    print(f"Duration: {duration:.4f} years")
    print(f"Modified Duration: {modified_duration:.4f}")
    print(f"Convexity: {convexity:.4f}")
    
    # Export results using JSON adapter
    logger.info("Exporting results")
    output_adapter = JSONOutputAdapter()
    
    bond_analysis = {
        "contract_id": fixed_bond.contract_id,
        "security_desc": fixed_bond.security_desc,
        "price": fixed_price,
        "ytm": ytm,
        "duration": duration,
        "modified_duration": modified_duration,
        "convexity": convexity
    }
    
    output_path = os.path.join(output_dir, 'bond_analysis.json')
    output_adapter.export_bond_analysis(bond_analysis, output_path)
    
    # Export yield curve
    curve_data = {
        "curve_date": curve_date,
        "tenors": tenors,
        "rates": rates
    }
    
    curve_path = os.path.join(output_dir, 'yield_curve.json')
    output_adapter.export_yield_curve(curve_data, curve_path)
    
    logger.info("Basic usage example completed")

if __name__ == "__main__":
    main()