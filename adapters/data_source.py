"""
Data source adapters for loading data
"""

import pandas as pd
import json
import sqlite3
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
import os

from ..core.interest_rate import InterestRateCurve
from ..instruments.fixed_rate import FixedRateBond
from ..instruments.floating_rate import FloatingRateBond
from ..instruments.zero_coupon import ZeroCouponBond
from ..utils.logging import LogManager

class DataSource(ABC):
    """Abstract base class for data sources"""
    
    def __init__(self):
        """Initialize data source"""
        self.logger = LogManager().get_logger(__name__)
    
    @abstractmethod
    def load_yield_curve(self, source_id: str) -> InterestRateCurve:
        """
        Load yield curve data
        
        Args:
            source_id: Identifier for the data source
            
        Returns:
            Interest rate curve
        """
        pass
    
    @abstractmethod
    def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
        """
        Load bond data
        
        Args:
            source_id: Identifier for the data source
            
        Returns:
            Bond object
        """
        pass
    
    @abstractmethod
    def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
        """
        Load multiple bonds
        
        Args:
            source_id: Identifier for the data source
            
        Returns:
            List of bond objects
        """
        pass
    
    @abstractmethod
    def load_historical_rates(self, source_id: str) -> pd.DataFrame:
        """
        Load historical interest rates
        
        Args:
            source_id: Identifier for the data source
            
        Returns:
            DataFrame containing historical rates
        """
        pass


class CSVDataSource(DataSource):
    """Data source for CSV files"""
    
    def __init__(self, data_directory: str):
        """
        Initialize CSV data source
        
        Args:
            data_directory: Directory containing CSV files
        """
        super().__init__()
        self.data_directory = data_directory
    
    def load_yield_curve(self, source_id: str) -> InterestRateCurve:
        """
        Load yield curve from CSV file
        
        Args:
            source_id: CSV file name
            
        Returns:
            Interest rate curve
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            df = pd.read_csv(file_path)
            return InterestRateCurve.from_dataframe(df)
        except Exception as e:
            self.logger.error(f"Failed to load yield curve from {file_path}: {e}")
            raise
    
    def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
        """
        Load bond from CSV file
        
        Args:
            source_id: CSV file name
            
        Returns:
            Bond object
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            df = pd.read_csv(file_path)
            
            # Assuming only one bond per file
            if len(df) == 0:
                raise ValueError(f"No bond data found in {file_path}")
            
            bond_data = df.iloc[0].to_dict()
            
            # Create appropriate bond type based on bond_type field
            bond_type = bond_data.get('bond_type', 'fixed')
            
            if bond_type.lower() == 'fixed':
                return FixedRateBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    coupon_rate=float(bond_data['coupon_rate']),
                    payment_frequency=int(bond_data.get('payment_frequency', 2))
                )
            elif bond_type.lower() == 'floating':
                return FloatingRateBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    spread=float(bond_data['spread']),
                    reference_rate_name=bond_data['reference_rate_name'],
                    payment_frequency=int(bond_data.get('payment_frequency', 2))
                )
            elif bond_type.lower() == 'zero':
                return ZeroCouponBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    discount_rate=float(bond_data['discount_rate'])
                )
            else:
                raise ValueError(f"Unknown bond type: {bond_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to load bond from {file_path}: {e}")
            raise
    
    def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
        """
        Load multiple bonds from CSV file
        
        Args:
            source_id: CSV file name
            
        Returns:
            List of bond objects
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            df = pd.read_csv(file_path)
            bonds = []
            
            for _, row in df.iterrows():
                bond_data = row.to_dict()
                bond_type = bond_data.get('bond_type', 'fixed')
                
                if bond_type.lower() == 'fixed':
                    bond = FixedRateBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        coupon_rate=float(bond_data['coupon_rate']),
                        payment_frequency=int(bond_data.get('payment_frequency', 2))
                    )
                elif bond_type.lower() == 'floating':
                    bond = FloatingRateBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        spread=float(bond_data['spread']),
                        reference_rate_name=bond_data['reference_rate_name'],
                        payment_frequency=int(bond_data.get('payment_frequency', 2))
                    )
                elif bond_type.lower() == 'zero':
                    bond = ZeroCouponBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        discount_rate=float(bond_data['discount_rate'])
                    )
                else:
                    self.logger.warning(f"Skipping bond with unknown type: {bond_type}")
                    continue
                
                bonds.append(bond)
            
            return bonds
                
        except Exception as e:
            self.logger.error(f"Failed to load bonds from {file_path}: {e}")
            raise
    
    def load_historical_rates(self, source_id: str) -> pd.DataFrame:
        """
        Load historical interest rates from CSV file
        
        Args:
            source_id: CSV file name
            
        Returns:
            DataFrame containing historical rates
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            return pd.read_csv(file_path, parse_dates=['Date'])
        except Exception as e:
            self.logger.error(f"Failed to load historical rates from {file_path}: {e}")
            raise


class JSONDataSource(DataSource):
    """Data source for JSON files"""
    
    def __init__(self, data_directory: str):
        """
        Initialize JSON data source
        
        Args:
            data_directory: Directory containing JSON files
        """
        super().__init__()
        self.data_directory = data_directory
    
    def load_yield_curve(self, source_id: str) -> InterestRateCurve:
        """
        Load yield curve from JSON file
        
        Args:
            source_id: JSON file name
            
        Returns:
            Interest rate curve
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            curve_date = data['curve_date']
            tenors = data['tenors']
            rates = data['rates']
            
            return InterestRateCurve(
                curve_date=pd.to_datetime(curve_date).to_pydatetime(),
                tenors=tenors,
                rates=rates
            )
        except Exception as e:
            self.logger.error(f"Failed to load yield curve from {file_path}: {e}")
            raise
    
    def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
        """
        Load bond from JSON file
        
        Args:
            source_id: JSON file name
            
        Returns:
            Bond object
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            with open(file_path, 'r') as f:
                bond_data = json.load(f)
            
            bond_type = bond_data.get('bond_type', 'fixed')
            
            if bond_type.lower() == 'fixed':
                return FixedRateBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    coupon_rate=float(bond_data['coupon_rate']),
                    payment_frequency=int(bond_data.get('payment_frequency', 2))
                )
            elif bond_type.lower() == 'floating':
                return FloatingRateBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    spread=float(bond_data['spread']),
                    reference_rate_name=bond_data['reference_rate_name'],
                    payment_frequency=int(bond_data.get('payment_frequency', 2))
                )
            elif bond_type.lower() == 'zero':
                return ZeroCouponBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    discount_rate=float(bond_data['discount_rate'])
                )
            else:
                raise ValueError(f"Unknown bond type: {bond_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to load bond from {file_path}: {e}")
            raise
    
    def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
        """
        Load multiple bonds from JSON file
        
        Args:
            source_id: JSON file name
            
        Returns:
            List of bond objects
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            bonds = []
            
            for bond_data in data:
                bond_type = bond_data.get('bond_type', 'fixed')
                
                if bond_type.lower() == 'fixed':
                    bond = FixedRateBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        coupon_rate=float(bond_data['coupon_rate']),
                        payment_frequency=int(bond_data.get('payment_frequency', 2))
                    )
                elif bond_type.lower() == 'floating':
                    bond = FloatingRateBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        spread=float(bond_data['spread']),
                        reference_rate_name=bond_data['reference_rate_name'],
                        payment_frequency=int(bond_data.get('payment_frequency', 2))
                    )
                elif bond_type.lower() == 'zero':
                    bond = ZeroCouponBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        discount_rate=float(bond_data['discount_rate'])
                    )
                else:
                    self.logger.warning(f"Skipping bond with unknown type: {bond_type}")
                    continue
                
                bonds.append(bond)
            
            return bonds
                
        except Exception as e:
            self.logger.error(f"Failed to load bonds from {file_path}: {e}")
            raise
    
    def load_historical_rates(self, source_id: str) -> pd.DataFrame:
        """
        Load historical interest rates from JSON file
        
        Args:
            source_id: JSON file name
            
        Returns:
            DataFrame containing historical rates
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return pd.DataFrame(data)
        except Exception as e:
            self.logger.error(f"Failed to load historical rates from {file_path}: {e}")
            raise


class DatabaseDataSource(DataSource):
    """Data source for SQL databases"""
    
    def __init__(self, db_path: str):
        """
        Initialize database data source
        
        Args:
            db_path: Path to SQLite database file
        """
        super().__init__()
        self.db_path = db_path
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def load_yield_curve(self, source_id: str) -> InterestRateCurve:
        """
        Load yield curve from database
        
        Args:
            source_id: Identifier for the yield curve (e.g., curve name or date)
            
        Returns:
            Interest rate curve
        """
        try:
            conn = self._get_connection()
            
            # Query yield curve header
            header_query = """
                SELECT curve_date FROM yield_curve_headers
                WHERE curve_id = ?
            """
            cursor = conn.execute(header_query, (source_id,))
            header = cursor.fetchone()
            
            if not header:
                raise ValueError(f"No yield curve found with ID {source_id}")
            
            curve_date = pd.to_datetime(header[0]).to_pydatetime()
            
            # Query yield curve points
            points_query = """
                SELECT tenor, rate FROM yield_curve_points
                WHERE curve_id = ?
                ORDER BY tenor
            """
            df = pd.read_sql(points_query, conn, params=(source_id,))
            
            conn.close()
            
            return InterestRateCurve(
                curve_date=curve_date,
                tenors=df['tenor'].tolist(),
                rates=df['rate'].tolist()
            )
        except Exception as e:
            self.logger.error(f"Failed to load yield curve {source_id} from database: {e}")
            raise
    
    def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
        """
        Load bond from database
        
        Args:
            source_id: Bond contract ID
            
        Returns:
            Bond object
        """
        try:
            conn = self._get_connection()
            
            # Query bond data
            query = """
                SELECT * FROM bonds
                WHERE contract_id = ?
            """
            cursor = conn.execute(query, (source_id,))
            row = cursor.fetchone()
            
            if not row:
                raise ValueError(f"No bond found with contract ID {source_id}")
            
            # Convert row to dict
            columns = [col[0] for col in cursor.description]
            bond_data = dict(zip(columns, row))
            
            conn.close()
            
            # Create appropriate bond type
            bond_type = bond_data.get('bond_type', 'fixed')
            
            if bond_type.lower() == 'fixed':
                return FixedRateBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    coupon_rate=float(bond_data['coupon_rate']),
                    payment_frequency=int(bond_data.get('payment_frequency', 2))
                )
            elif bond_type.lower() == 'floating':
                return FloatingRateBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    spread=float(bond_data['spread']),
                    reference_rate_name=bond_data['reference_rate_name'],
                    payment_frequency=int(bond_data.get('payment_frequency', 2))
                )
            elif bond_type.lower() == 'zero':
                return ZeroCouponBond(
                    contract_id=bond_data['contract_id'],
                    security_desc=bond_data['security_desc'],
                    issue_date=bond_data['issue_date'],
                    maturity_date=bond_data['maturity_date'],
                    par_value=float(bond_data['par_value']),
                    discount_rate=float(bond_data['discount_rate'])
                )
            else:
                raise ValueError(f"Unknown bond type: {bond_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to load bond {source_id} from database: {e}")
            raise
    
    def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
        """
        Load multiple bonds from database
        
        Args:
            source_id: Query identifier or filter criteria
            
        Returns:
            List of bond objects
        """
        try:
            conn = self._get_connection()
            
            # Query bonds
            # source_id could be a portfolio ID, issuer, bond type, etc.
            query = """
                SELECT * FROM bonds
                WHERE portfolio_id = ? OR issuer = ? OR bond_type = ?
            """
            df = pd.read_sql(query, conn, params=(source_id, source_id, source_id))
            
            conn.close()
            
            bonds = []
            
            for _, row in df.iterrows():
                bond_data = row.to_dict()
                bond_type = bond_data.get('bond_type', 'fixed')
                
                if bond_type.lower() == 'fixed':
                    bond = FixedRateBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        coupon_rate=float(bond_data['coupon_rate']),
                        payment_frequency=int(bond_data.get('payment_frequency', 2))
                    )
                elif bond_type.lower() == 'floating':
                    bond = FloatingRateBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        spread=float(bond_data['spread']),
                        reference_rate_name=bond_data['reference_rate_name'],
                        payment_frequency=int(bond_data.get('payment_frequency', 2))
                    )
                elif bond_type.lower() == 'zero':
                    bond = ZeroCouponBond(
                        contract_id=bond_data['contract_id'],
                        security_desc=bond_data['security_desc'],
                        issue_date=bond_data['issue_date'],
                        maturity_date=bond_data['maturity_date'],
                        par_value=float(bond_data['par_value']),
                        discount_rate=float(bond_data['discount_rate'])
                    )
                else:
                    self.logger.warning(f"Skipping bond with unknown type: {bond_type}")
                    continue
                
                bonds.append(bond)
            
            return bonds
                
        except Exception as e:
            self.logger.error(f"Failed to load bonds with criteria {source_id} from database: {e}")
            raise
    
    def load_historical_rates(self, source_id: str) -> pd.DataFrame:
        """
        Load historical interest rates from database
        
        Args:
            source_id: Rate type or identifier
            
        Returns:
            DataFrame containing historical rates
        """
        try:
            conn = self._get_connection()
            
            query = """
                SELECT * FROM historical_rates
                WHERE rate_type = ?
                ORDER BY date
            """
            df = pd.read_sql(query, conn, params=(source_id,))
            
            conn.close()
            
            return df
        except Exception as e:
            self.logger.error(f"Failed to load historical rates for {source_id} from database: {e}")
            raise