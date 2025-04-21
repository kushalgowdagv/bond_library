# # #!/usr/bin/env python
# # """
# # Basic usage example of the bond library
# # """

# # import os
# # import pandas as pd
# # from datetime import datetime

# # from bond_library.core.date_utils import DateUtils
# # from bond_library.core.interest_rate import InterestRateCurve
# # from bond_library.instruments.fixed_rate import FixedRateBond
# # from bond_library.instruments.floating_rate import FloatingRateBond
# # from bond_library.instruments.zero_coupon import ZeroCouponBond
# # from bond_library.adapters.data_source import CSVDataSource
# # from bond_library.adapters.output import JSONOutputAdapter
# # from bond_library.utils.config import Config
# # from bond_library.utils.logging import LogManager

# # def main():
# #     """Main function demonstrating basic usage"""
# #     # Set up logging
# #     logger = LogManager().get_logger(__name__)
# #     logger.info("Starting basic usage example")
    
# #     # Set up configuration
# #     config = Config()
# #     config.set('io', 'default_format', 'json')
    
# #     # Create output directory if it doesn't exist
# #     output_dir = os.path.join(os.path.dirname(__file__), 'output')
# #     os.makedirs(output_dir, exist_ok=True)
    
# #     # Create a fixed rate bond
# #     logger.info("Creating a fixed rate bond")
# #     fixed_bond = FixedRateBond(
# #         contract_id="US-TREAS-5Y",
# #         security_desc="US Treasury 5-Year Note",
# #         issue_date="2022-01-15",
# #         maturity_date="2027-01-15",
# #         par_value=1000.0,
# #         coupon_rate=0.025,  # 2.5%
# #         payment_frequency=2  # Semi-annual
# #     )
    
# #     # Create a zero coupon bond
# #     logger.info("Creating a zero coupon bond")
# #     zero_bond = ZeroCouponBond(
# #         contract_id="US-ZERO-2Y",
# #         security_desc="US Treasury 2-Year Zero Coupon",
# #         issue_date="2022-01-15",
# #         maturity_date="2024-01-15",
# #         par_value=1000.0,
# #         discount_rate=0.02  # 2%
# #     )
    
# #     # Create a floating rate bond
# #     logger.info("Creating a floating rate bond")
# #     floating_bond = FloatingRateBond(
# #         contract_id="US-FLOAT-3Y",
# #         security_desc="US Treasury 3-Year Floating Rate Note",
# #         issue_date="2022-01-15",
# #         maturity_date="2025-01-15",
# #         par_value=1000.0,
# #         spread=0.005,  # 0.5% spread over reference rate
# #         reference_rate_name="SOFR",
# #         payment_frequency=4  # Quarterly
# #     )
    
# #     # Create yield curve
# #     logger.info("Creating yield curve")
# #     curve_date = datetime.now()
# #     tenors = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0]
# #     rates = [0.0050, 0.0075, 0.0125, 0.0175, 0.0200, 0.0250, 0.0275, 0.0300, 0.0325, 0.0350]
# #     curve = InterestRateCurve(curve_date, tenors, rates)
    
# #     # Calculate bond prices
# #     valuation_date = datetime.now()
# #     fixed_price = fixed_bond.price(valuation_date, curve)
# #     zero_price = zero_bond.price(valuation_date, curve)
    
# #     # Set forward rates for floating rate bond
# #     forward_dates = [
# #         DateUtils.add_months(valuation_date, 3),
# #         DateUtils.add_months(valuation_date, 6),
# #         DateUtils.add_months(valuation_date, 9),
# #         DateUtils.add_months(valuation_date, 12)
# #     ]
# #     forward_rates = {
# #         forward_dates[0]: 0.02,  # 2%
# #         forward_dates[1]: 0.022,  # 2.2%
# #         forward_dates[2]: 0.024,  # 2.4%
# #         forward_dates[3]: 0.026   # 2.6%
# #     }
# #     floating_bond.set_forward_curve(forward_rates)
# #     floating_price = floating_bond.price(valuation_date, curve)
    
# #     # Print results
# #     print(f"Fixed Rate Bond Price: {fixed_price:.4f}")
# #     print(f"Zero Coupon Bond Price: {zero_price:.4f}")
# #     print(f"Floating Rate Bond Price: {floating_price:.4f}")
    
# #     # Get cash flows for fixed rate bond
# #     cash_flows = fixed_bond.get_remaining_cash_flows(valuation_date)
# #     print("\nFixed Rate Bond Cash Flows:")
# #     for cf in cash_flows:
# #         print(f"Date: {cf.payment_date.strftime('%Y-%m-%d')}, Amount: ${cf.amount:.2f}")
    
# #     # Calculate YTM for fixed rate bond
# #     ytm = fixed_bond.yield_to_maturity(valuation_date, fixed_price)
# #     print(f"\nFixed Rate Bond YTM: {ytm*100:.4f}%")
    
# #     # Calculate duration and convexity
# #     duration = fixed_bond.duration(valuation_date, ytm)
# #     modified_duration = fixed_bond.modified_duration(valuation_date, ytm)
# #     convexity = fixed_bond.convexity(valuation_date, ytm)
    
# #     print(f"Duration: {duration:.4f} years")
# #     print(f"Modified Duration: {modified_duration:.4f}")
# #     print(f"Convexity: {convexity:.4f}")
    
# #     # Export results using JSON adapter
# #     logger.info("Exporting results")
# #     output_adapter = JSONOutputAdapter()
    
# #     bond_analysis = {
# #         "contract_id": fixed_bond.contract_id,
# #         "security_desc": fixed_bond.security_desc,
# #         "price": fixed_price,
# #         "ytm": ytm,
# #         "duration": duration,
# #         "modified_duration": modified_duration,
# #         "convexity": convexity
# #     }
    
# #     output_path = os.path.join(output_dir, 'bond_analysis.json')
# #     output_adapter.export_bond_analysis(bond_analysis, output_path)
    
# #     # Export yield curve
# #     curve_data = {
# #         "curve_date": curve_date,
# #         "tenors": tenors,
# #         "rates": rates
# #     }
    
# #     curve_path = os.path.join(output_dir, 'yield_curve.json')
# #     output_adapter.export_yield_curve(curve_data, curve_path)
    
# #     logger.info("Basic usage example completed")

# # if __name__ == "__main__":
# #     main()

# #!/usr/bin/env python
# """
# Improved basic usage example for bond analysis
# """

# import os
# import pandas as pd
# from datetime import datetime

# # Import our helper functions for CSV loading
# from csv_loading_fix import load_yield_curve_from_csv, load_bonds_from_csv

# # Import core components
# from core.date_utils import DateUtils
# from adapters.output import CSVOutputAdapter  
# from risk.metrics import RiskMetrics
# from risk.stress_test import StressTest
# from utils.logging import LogManager

# def main():
#     """Main function demonstrating basic usage with proper data loading"""
#     # Set up logging
#     logger = LogManager().get_logger(__name__)
#     logger.info("Starting bond analysis example")
    
#     # Define data directory (where CSV files are located)
#     data_dir = os.path.dirname(os.path.abspath(__file__))
    
#     # Create output directory if it doesn't exist
#     output_dir = os.path.join(data_dir, 'output')
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Load yield curve from CSV
#     try:
#         curve_path = os.path.join(data_dir, 'interest_rates.csv')
#         yield_curve = load_yield_curve_from_csv(curve_path)
#         logger.info("Loaded yield curve successfully")
#     except Exception as e:
#         logger.error(f"Failed to load yield curve: {e}")
#         raise
    
#     # Load bonds from CSV
#     try:
#         bonds_path = os.path.join(data_dir, 'bonds.csv')
#         bonds = load_bonds_from_csv(bonds_path)
#         logger.info(f"Loaded {len(bonds)} bonds successfully")
#     except Exception as e:
#         logger.error(f"Failed to load bonds: {e}")
#         raise
    
#     # Use current date for valuation
#     valuation_date = datetime.now()
#     logger.info(f"Valuation date: {valuation_date.strftime('%Y-%m-%d')}")
    
#     # Initialize output adapter
#     output_adapter = CSVOutputAdapter()
    
#     # Analyze all bonds and export results
#     portfolio_results = {}
    
#     for idx, bond in enumerate(bonds[:5]):  # Process first 5 bonds for demo
#         logger.info(f"Analyzing bond {idx+1}/{min(len(bonds), 5)}: {bond.contract_id}")
        
#         # Calculate price
#         price = bond.price(valuation_date, yield_curve)
        
#         # Calculate YTM
#         ytm = bond.yield_to_maturity(valuation_date, price)
        
#         # Calculate risk metrics
#         risk_calculator = RiskMetrics()
#         risk_metrics = risk_calculator.interest_rate_risk(bond, valuation_date, ytm)
        
#         # Print basic results
#         print(f"\nBond: {bond.security_desc} ({bond.contract_id})")
#         print(f"Issue Date: {bond.issue_date.strftime('%Y-%m-%d')}")
#         print(f"Maturity Date: {bond.maturity_date.strftime('%Y-%m-%d')}")
#         print(f"Price: {price:.4f}")
#         print(f"YTM: {ytm*100:.4f}%")
#         print(f"Duration: {risk_metrics['duration']:.4f} years")
#         print(f"Modified Duration: {risk_metrics['modified_duration']:.4f}")
        
#         # Store results for portfolio analysis
#         portfolio_results[bond.contract_id] = {
#             "security_desc": bond.security_desc,
#             "price": price,
#             "ytm": ytm,
#             "risk_metrics": risk_metrics
#         }
    
#     # Export portfolio results
#     output_path = os.path.join(output_dir, 'portfolio_analysis.csv')
#     output_adapter.export_portfolio_analysis(portfolio_results, output_path)
#     logger.info(f"Portfolio analysis results exported to {output_path}")
    
#     # Perform stress tests on the first bond
#     if bonds:
#         logger.info("Running stress tests on first bond")
#         stress_tester = StressTest()
#         stress_tester.create_standard_scenarios()
        
#         first_bond = bonds[0]
#         stress_results = stress_tester.run_all_scenarios(first_bond, valuation_date, yield_curve)
        
#         print("\nStress Test Results:")
#         for scenario, result in stress_results.items():
#             price_change = result["percentage_change"]
#             print(f"{scenario}: {price_change:.2f}%")
    
#     logger.info("Bond analysis example completed")

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python


import os
import pandas as pd
from datetime import datetime

# Import adapters
from adapters.data_source import CSVDataSource
from adapters.output import CSVOutputAdapter

# Import core components
from bond_library.core.date_utils import DateUtils
from bond_library.core.interest_rate import InterestRateCurve

# Import risk modules
from bond_library.risk.metrics import RiskMetrics
from bond_library.risk.stress_test import StressTest

# Import utilities
from bond_library.utils.logging import LogManager
from bond_library.utils.config import Config

def main():
    """Main function demonstrating basic usage"""
    # Set up logging
    logger = LogManager().get_logger(__name__)
    logger.info("Starting basic usage example")
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define data and output directories
    data_dir = os.path.join(script_dir, 'data')
    output_dir = os.path.join(script_dir, 'output')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create data directory if it doesn't exist and copy CSV files there if needed
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize data source and output adapter
    data_source = CSVDataSource(data_dir)
    output_adapter = CSVOutputAdapter(output_dir)
    
    # Set current date for valuation
    valuation_date = datetime.now()
    logger.info(f"Valuation date: {valuation_date.strftime('%Y-%m-%d')}")
    
    try:
        # Load yield curve
        logger.info("Loading yield curve from CSV")
        yield_curve = data_source.load_yield_curve("interest_rates.csv")
        
        # Export the yield curve
        curve_data = {
            'curve_date': yield_curve.curve_date,
            'tenors': yield_curve.tenors,
            'rates': yield_curve.rates
        }
        output_adapter.export_yield_curve(curve_data, "yield_curve.csv")
        
        # Load bonds
        logger.info("Loading bonds from CSV")
        bonds = data_source.load_bonds("bonds.csv")
        logger.info(f"Loaded {len(bonds)} bonds")
        
        # Process first 5 bonds as a sample
        sample_size = min(5, len(bonds))
        logger.info(f"Processing first {sample_size} bonds for analysis")
        
        # Prepare dictionary for portfolio analysis
        portfolio_results = {}
        
        # Process each bond
        for i, bond in enumerate(bonds[:sample_size]):
            logger.info(f"Analyzing bond {i+1}/{sample_size}: {bond.contract_id}")
            
            # Calculate price
            price = bond.price(valuation_date, yield_curve)
            
            # Calculate YTM
            ytm = bond.yield_to_maturity(valuation_date, price)
            
            # Get cash flows
            cash_flows = bond.get_remaining_cash_flows(valuation_date)
            
            # Calculate risk metrics
            risk_calculator = RiskMetrics()
            risk_metrics = risk_calculator.interest_rate_risk(bond, valuation_date, ytm)
            
            # Create bond analysis results
            bond_analysis = {
                "contract_id": bond.contract_id,
                "security_desc": bond.security_desc,
                "issue_date": bond.issue_date.strftime('%Y-%m-%d'),
                "maturity_date": bond.maturity_date.strftime('%Y-%m-%d'),
                "price": price,
                "ytm": ytm,
                "duration": risk_metrics["duration"],
                "modified_duration": risk_metrics["modified_duration"],
                "convexity": risk_metrics["convexity"],
                "dv01": risk_metrics["dv01"],
                "price_100bp": risk_metrics["price_100bp"]
            }
            
            # Export bond analysis
            output_file = f"bond_analysis_{bond.contract_id}.csv"
            output_adapter.export_bond_analysis(bond_analysis, output_file)
            
            # Export cash flows
            cash_flow_file = f"cash_flows_{bond.contract_id}.csv"
            output_adapter.export_cash_flows(bond.contract_id, cash_flows, cash_flow_file)
            
            # Export risk analysis
            risk_file = f"risk_analysis_{bond.contract_id}.csv"
            output_adapter.export_risk_analysis(bond.contract_id, risk_metrics, risk_file)
            
            # Add to portfolio results
            portfolio_results[bond.contract_id] = bond_analysis
            
            # Print summary
            print(f"\nBond: {bond.security_desc} ({bond.contract_id})")
            print(f"Issue Date: {bond.issue_date.strftime('%Y-%m-%d')}")
            print(f"Maturity Date: {bond.maturity_date.strftime('%Y-%m-%d')}")
            print(f"Price: {price:.4f}")
            print(f"YTM: {ytm*100:.4f}%")
            print(f"Duration: {risk_metrics['duration']:.4f} years")
            print(f"Modified Duration: {risk_metrics['modified_duration']:.4f}")
            print(f"Convexity: {risk_metrics['convexity']:.4f}")
        
        # Export portfolio analysis
        logger.info("Exporting portfolio analysis")
        output_adapter.export_portfolio_analysis(portfolio_results, "portfolio_analysis.csv")
        
        # Run stress tests on the first bond
        if bonds:
            logger.info("Running stress tests on first bond")
            first_bond = bonds[0]
            
            # Create stress test scenarios
            stress_tester = StressTest()
            stress_tester.create_standard_scenarios()
            
            # Run stress tests
            stress_results = stress_tester.run_all_scenarios(first_bond, valuation_date, yield_curve)
            
            # Print stress test results
            print("\nStress Test Results:")
            for scenario, result in stress_results.items():
                price_change = result["percentage_change"]
                print(f"{scenario}: {price_change:.2f}%")
            
            # Export stress test results
            stress_data = {
                "bond_id": first_bond.contract_id,
                "valuation_date": valuation_date.strftime('%Y-%m-%d'),
                "scenarios": {}
            }
            
            for scenario, result in stress_results.items():
                stress_data["scenarios"][scenario] = {
                    "base_price": result["base_price"],
                    "stressed_price": result["stressed_price"],
                    "price_change": result["price_change"],
                    "percentage_change": result["percentage_change"]
                }
            
            # Export flattened stress test results
            flattened_stress = {
                "bond_id": first_bond.contract_id,
                "valuation_date": valuation_date.strftime('%Y-%m-%d')
            }
            
            for scenario, result in stress_results.items():
                flattened_stress[f"{scenario}_base_price"] = result["base_price"]
                flattened_stress[f"{scenario}_stressed_price"] = result["stressed_price"]
                flattened_stress[f"{scenario}_price_change"] = result["price_change"]
                flattened_stress[f"{scenario}_percentage_change"] = result["percentage_change"]
            
            output_adapter.export_bond_analysis(flattened_stress, f"stress_test_{first_bond.contract_id}.csv")
            
        logger.info("Basic usage example completed")
        print("\nAll analysis results have been exported to the output directory:")
        print(f"  {output_dir}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
