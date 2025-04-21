#!/usr/bin/env python


import os
import pandas as pd
from datetime import datetime

# Import adapters
from adapters.data_source import CSVDataSource
from adapters.output import CSVOutputAdapter

# Import core components
from core.date_utils import DateUtils
from core.interest_rate import InterestRateCurve

# Import risk modules
from risk.metrics import RiskMetrics
from risk.stress_test import StressTest

# Import utilities
from utils.logging import LogManager
from utils.config import Config

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
        sample_size = min(1, len(bonds))
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
        
        # # Run stress tests on the first bond
        # if bonds:
        #     logger.info("Running stress tests on first bond")
        #     first_bond = bonds[0]
            
        #     # Create stress test scenarios
        #     stress_tester = StressTest()
        #     stress_tester.create_standard_scenarios()
            
        #     # Run stress tests
        #     stress_results = stress_tester.run_all_scenarios(first_bond, valuation_date, yield_curve)
            
        #     # Print stress test results
        #     print("\nStress Test Results:")
        #     for scenario, result in stress_results.items():
        #         price_change = result["percentage_change"]
        #         print(f"{scenario}: {price_change:.2f}%")
            
        #     # Export stress test results
        #     stress_data = {
        #         "bond_id": first_bond.contract_id,
        #         "valuation_date": valuation_date.strftime('%Y-%m-%d'),
        #         "scenarios": {}
        #     }
            
        #     for scenario, result in stress_results.items():
        #         stress_data["scenarios"][scenario] = {
        #             "base_price": result["base_price"],
        #             "stressed_price": result["stressed_price"],
        #             "price_change": result["price_change"],
        #             "percentage_change": result["percentage_change"]
        #         }
            
        #     # Export flattened stress test results
        #     flattened_stress = {
        #         "bond_id": first_bond.contract_id,
        #         "valuation_date": valuation_date.strftime('%Y-%m-%d')
        #     }
            
        #     for scenario, result in stress_results.items():
        #         flattened_stress[f"{scenario}_base_price"] = result["base_price"]
        #         flattened_stress[f"{scenario}_stressed_price"] = result["stressed_price"]
        #         flattened_stress[f"{scenario}_price_change"] = result["price_change"]
        #         flattened_stress[f"{scenario}_percentage_change"] = result["percentage_change"]
            
        #     output_adapter.export_bond_analysis(flattened_stress, f"stress_test_{first_bond.contract_id}.csv")
            
        logger.info("Code completed")
        print("\nAll analysis results have been exported to the output directory:")
        print(f"  {output_dir}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
