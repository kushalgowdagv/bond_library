"""
Output adapters for exporting analysis results
"""

import pandas as pd
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union

from ..core.bond import Bond
from ..utils.logging import LogManager
from ..risk.metrics import RiskMetrics

class OutputAdapter(ABC):
    """Abstract base class for output adapters"""
    
    def __init__(self):
        """Initialize output adapter"""
        self.logger = LogManager().get_logger(__name__)
    
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


class CSVOutputAdapter(OutputAdapter):
    """Output adapter for CSV files"""
    
    def export_bond_analysis(self, analysis_results: Dict[str, Any], output_path: str) -> None:
        """
        Export bond analysis results to CSV
        
        Args:
            analysis_results: Dictionary containing analysis results
            output_path: Path where to save the CSV file
        """
        try:
            # Handle different types of analysis results
            if 'risk_metrics' in analysis_results:
                # Flatten nested dictionaries
                flattened = {}
                for key, value in analysis_results.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            flattened[f"{key}_{subkey}"] = subvalue
                    else:
                        flattened[key] = value
                
                # Create DataFrame with a single row
                df = pd.DataFrame([flattened])
            else:
                # Simple conversion for flat dictionaries
                df = pd.DataFrame([analysis_results])
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
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
            output_path: Path where to save the CSV file
        """
        try:
            # Create a list to hold flattened results
            rows = []
            
            # Process each bond's results
            for bond_id, results in portfolio_results.items():
                # Start with bond ID
                row = {'bond_id': bond_id}
                
                # Flatten nested dictionaries
                for key, value in results.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            row[f"{key}_{subkey}"] = subvalue
                    else:
                        row[key] = value
                
                rows.append(row)
            
            # Convert to DataFrame
            df = pd.DataFrame(rows)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Portfolio analysis results exported to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to export portfolio analysis results to {output_path}: {e}")
            raise
    
