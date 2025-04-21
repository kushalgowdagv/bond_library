
"""
Output adapters for exporting analysis results
"""

import pandas as pd
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from core.bond import Bond
from utils.logging import LogManager
from risk.metrics import RiskMetrics

class OutputAdapter(ABC):
    """Abstract base class for output adapters"""
    
    def __init__(self, output_directory: Optional[str] = None):
        """
        Initialize output adapter
        
        Args:
            output_directory: Directory where output files will be saved
        """
        self.logger = LogManager().get_logger(__name__)
        self.output_directory = output_directory or os.path.join(os.getcwd(), 'output')
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_directory, exist_ok=True)
    
    @abstractmethod
    def export_bond_analysis(self, analysis_results: Dict[str, Any], output_path: str) -> None:
        """
        Export bond analysis results
        
        Args:
            analysis_results: Dictionary containing analysis results
            output_path: Path where to save the results
        """
        pass
    
    @abstractmethod
    def export_portfolio_analysis(self, portfolio_results: Dict[str, Dict[str, Any]], output_path: str) -> None:
        """
        Export portfolio analysis results
        
        Args:
            portfolio_results: Dictionary mapping bond IDs to their analysis results
            output_path: Path where to save the results
        """
        pass
    
    @abstractmethod
    def export_yield_curve(self, curve_data: Dict[str, Any], output_path: str) -> None:
        """
        Export yield curve data
        
        Args:
            curve_data: Dictionary containing curve data
            output_path: Path where to save the data
        """
        pass
    
    def get_full_path(self, filename: str) -> str:
        """
        Get full path for a file in the output directory
        
        Args:
            filename: Name of the file
            
        Returns:
            Full path to the file
        """
        return os.path.join(self.output_directory, filename)


class CSVOutputAdapter(OutputAdapter):
    """Output adapter for CSV files"""
    
    def export_bond_analysis(self, analysis_results: Dict[str, Any], output_path: str) -> None:
        """
        Export bond analysis results to CSV
        
        Args:
            analysis_results: Dictionary containing analysis results
            output_path: Path where to save the CSV file (can be relative to output_directory)
        """
        try:
            # Handle relative path
            if not os.path.isabs(output_path):
                output_path = self.get_full_path(output_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Flatten nested dictionaries
            flattened = self._flatten_dict(analysis_results)
            
            # Create DataFrame with a single row
            df = pd.DataFrame([flattened])
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Bond analysis results exported to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to export bond analysis results to {output_path}: {e}")
            raise
    
    def export_portfolio_analysis(self, portfolio_results: Dict[str, Dict[str, Any]], output_path: str) -> None:
        """
        Export portfolio analysis results to CSV
        
        Args:
            portfolio_results: Dictionary mapping bond IDs to their analysis results
            output_path: Path where to save the CSV file (can be relative to output_directory)
        """
        try:
            # Handle relative path
            if not os.path.isabs(output_path):
                output_path = self.get_full_path(output_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create a list to hold flattened results
            rows = []
            
            # Process each bond's results
            for bond_id, results in portfolio_results.items():
                # Start with bond ID
                row = {'bond_id': bond_id}
                
                # Flatten and add results
                flattened = self._flatten_dict(results)
                row.update(flattened)
                
                rows.append(row)
            
            # Convert to DataFrame
            df = pd.DataFrame(rows)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Portfolio analysis results exported to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to export portfolio analysis results to {output_path}: {e}")
            raise
    
    def export_yield_curve(self, curve_data: Dict[str, Any], output_path: str) -> None:
        """
        Export yield curve data to CSV
        
        Args:
            curve_data: Dictionary containing curve data
            output_path: Path where to save the CSV file (can be relative to output_directory)
        """
        try:
            # Handle relative path
            if not os.path.isabs(output_path):
                output_path = self.get_full_path(output_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Extract data
            curve_date = curve_data.get('curve_date', datetime.now())
            tenors = curve_data.get('tenors', [])
            rates = curve_data.get('rates', [])
            
            # Format date as string if it's a datetime
            if isinstance(curve_date, datetime):
                curve_date_str = curve_date.strftime('%Y-%m-%d')
            else:
                curve_date_str = str(curve_date)
            
            # Create DataFrame
            data = []
            for tenor, rate in zip(tenors, rates):
                data.append({
                    'Date': curve_date_str,
                    'Tenor': tenor,
                    'Rate': rate
                })
            
            df = pd.DataFrame(data)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Yield curve exported to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to export yield curve to {output_path}: {e}")
            raise
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """
        Recursively flatten nested dictionaries
        
        Args:
            d: Dictionary to flatten
            parent_key: Key of the parent dictionary (for recursion)
            
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
                
        return dict(items)
    
    def export_risk_analysis(self, bond_id: str, risk_metrics: Dict[str, Any], output_path: str) -> None:
        """
        Export risk analysis results to CSV
        
        Args:
            bond_id: Identifier of the bond
            risk_metrics: Dictionary containing risk metrics
            output_path: Path where to save the CSV file (can be relative to output_directory)
        """
        try:
            # Handle relative path
            if not os.path.isabs(output_path):
                output_path = self.get_full_path(output_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Flatten risk metrics
            flattened = self._flatten_dict(risk_metrics)
            
            # Add bond ID
            flattened['bond_id'] = bond_id
            
            # Create DataFrame
            df = pd.DataFrame([flattened])
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Risk analysis results exported to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to export risk analysis results to {output_path}: {e}")
            raise
    
    def export_cash_flows(self, bond_id: str, cash_flows: List[Any], output_path: str) -> None:
        """
        Export cash flow data to CSV
        
        Args:
            bond_id: Identifier of the bond
            cash_flows: List of cash flow objects
            output_path: Path where to save the CSV file (can be relative to output_directory)
        """
        try:
            # Handle relative path
            if not os.path.isabs(output_path):
                output_path = self.get_full_path(output_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert cash flows to dictionary
            data = []
            for cf in cash_flows:
                data.append({
                    'bond_id': bond_id,
                    'payment_date': cf.payment_date.strftime('%Y-%m-%d'),
                    'amount': cf.amount
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Cash flows exported to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to export cash flows to {output_path}: {e}")
            raise
