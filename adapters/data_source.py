# """
# Data source adapters for loading data
# """

# import pandas as pd
# import json
# import sqlite3
# from abc import ABC, abstractmethod
# from typing import Dict, List, Any, Optional, Union
# import os

# from ..core.interest_rate import InterestRateCurve
# from ..instruments.fixed_rate import FixedRateBond
# from ..instruments.floating_rate import FloatingRateBond
# from ..instruments.zero_coupon import ZeroCouponBond
# from ..utils.logging import LogManager

# class DataSource(ABC):
#     """Abstract base class for data sources"""
    
#     def __init__(self):
#         """Initialize data source"""
#         self.logger = LogManager().get_logger(__name__)
    
#     @abstractmethod
#     def load_yield_curve(self, source_id: str) -> InterestRateCurve:
#         """
#         Load yield curve data
        
#         Args:
#             source_id: Identifier for the data source
            
#         Returns:
#             Interest rate curve
#         """
#         pass
    
#     @abstractmethod
#     def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
#         """
#         Load bond data
        
#         Args:
#             source_id: Identifier for the data source
            
#         Returns:
#             Bond object
#         """
#         pass
    
#     @abstractmethod
#     def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
#         """
#         Load multiple bonds
        
#         Args:
#             source_id: Identifier for the data source
            
#         Returns:
#             List of bond objects
#         """
#         pass
    
#     @abstractmethod
#     def load_historical_rates(self, source_id: str) -> pd.DataFrame:
#         """
#         Load historical interest rates
        
#         Args:
#             source_id: Identifier for the data source
            
#         Returns:
#             DataFrame containing historical rates
#         """
#         pass


# class CSVDataSource(DataSource):
#     """Data source for CSV files"""
    
#     def __init__(self, data_directory: str):
#         """
#         Initialize CSV data source
        
#         Args:
#             data_directory: Directory containing CSV files
#         """
#         super().__init__()
#         self.data_directory = data_directory
    
#     def load_yield_curve(self, source_id: str) -> InterestRateCurve:
#         """
#         Load yield curve from CSV file
        
#         Args:
#             source_id: CSV file name
            
#         Returns:
#             Interest rate curve
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             df = pd.read_csv(file_path)
#             return InterestRateCurve.from_dataframe(df)
#         except Exception as e:
#             self.logger.error(f"Failed to load yield curve from {file_path}: {e}")
#             raise
    
#     def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
#         """
#         Load bond from CSV file
        
#         Args:
#             source_id: CSV file name
            
#         Returns:
#             Bond object
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             df = pd.read_csv(file_path)
            
#             # Assuming only one bond per file
#             if len(df) == 0:
#                 raise ValueError(f"No bond data found in {file_path}")
            
#             bond_data = df.iloc[0].to_dict()
            
#             # Create appropriate bond type based on bond_type field
#             bond_type = bond_data.get('bond_type', 'fixed')
            
#             if bond_type.lower() == 'fixed':
#                 return FixedRateBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     coupon_rate=float(bond_data['coupon_rate']),
#                     payment_frequency=int(bond_data.get('payment_frequency', 2))
#                 )
#             elif bond_type.lower() == 'floating':
#                 return FloatingRateBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     spread=float(bond_data['spread']),
#                     reference_rate_name=bond_data['reference_rate_name'],
#                     payment_frequency=int(bond_data.get('payment_frequency', 2))
#                 )
#             elif bond_type.lower() == 'zero':
#                 return ZeroCouponBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     discount_rate=float(bond_data['discount_rate'])
#                 )
#             else:
#                 raise ValueError(f"Unknown bond type: {bond_type}")
                
#         except Exception as e:
#             self.logger.error(f"Failed to load bond from {file_path}: {e}")
#             raise
    
#     def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
#         """
#         Load multiple bonds from CSV file
        
#         Args:
#             source_id: CSV file name
            
#         Returns:
#             List of bond objects
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             df = pd.read_csv(file_path)
#             bonds = []
            
#             for _, row in df.iterrows():
#                 bond_data = row.to_dict()
#                 bond_type = bond_data.get('bond_type', 'fixed')
                
#                 if bond_type.lower() == 'fixed':
#                     bond = FixedRateBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         coupon_rate=float(bond_data['coupon_rate']),
#                         payment_frequency=int(bond_data.get('payment_frequency', 2))
#                     )
#                 elif bond_type.lower() == 'floating':
#                     bond = FloatingRateBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         spread=float(bond_data['spread']),
#                         reference_rate_name=bond_data['reference_rate_name'],
#                         payment_frequency=int(bond_data.get('payment_frequency', 2))
#                     )
#                 elif bond_type.lower() == 'zero':
#                     bond = ZeroCouponBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         discount_rate=float(bond_data['discount_rate'])
#                     )
#                 else:
#                     self.logger.warning(f"Skipping bond with unknown type: {bond_type}")
#                     continue
                
#                 bonds.append(bond)
            
#             return bonds
                
#         except Exception as e:
#             self.logger.error(f"Failed to load bonds from {file_path}: {e}")
#             raise
    
#     def load_historical_rates(self, source_id: str) -> pd.DataFrame:
#         """
#         Load historical interest rates from CSV file
        
#         Args:
#             source_id: CSV file name
            
#         Returns:
#             DataFrame containing historical rates
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             return pd.read_csv(file_path, parse_dates=['Date'])
#         except Exception as e:
#             self.logger.error(f"Failed to load historical rates from {file_path}: {e}")
#             raise


# class JSONDataSource(DataSource):
#     """Data source for JSON files"""
    
#     def __init__(self, data_directory: str):
#         """
#         Initialize JSON data source
        
#         Args:
#             data_directory: Directory containing JSON files
#         """
#         super().__init__()
#         self.data_directory = data_directory
    
#     def load_yield_curve(self, source_id: str) -> InterestRateCurve:
#         """
#         Load yield curve from JSON file
        
#         Args:
#             source_id: JSON file name
            
#         Returns:
#             Interest rate curve
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             with open(file_path, 'r') as f:
#                 data = json.load(f)
                
#             curve_date = data['curve_date']
#             tenors = data['tenors']
#             rates = data['rates']
            
#             return InterestRateCurve(
#                 curve_date=pd.to_datetime(curve_date).to_pydatetime(),
#                 tenors=tenors,
#                 rates=rates
#             )
#         except Exception as e:
#             self.logger.error(f"Failed to load yield curve from {file_path}: {e}")
#             raise
    
#     def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
#         """
#         Load bond from JSON file
        
#         Args:
#             source_id: JSON file name
            
#         Returns:
#             Bond object
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             with open(file_path, 'r') as f:
#                 bond_data = json.load(f)
            
#             bond_type = bond_data.get('bond_type', 'fixed')
            
#             if bond_type.lower() == 'fixed':
#                 return FixedRateBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     coupon_rate=float(bond_data['coupon_rate']),
#                     payment_frequency=int(bond_data.get('payment_frequency', 2))
#                 )
#             elif bond_type.lower() == 'floating':
#                 return FloatingRateBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     spread=float(bond_data['spread']),
#                     reference_rate_name=bond_data['reference_rate_name'],
#                     payment_frequency=int(bond_data.get('payment_frequency', 2))
#                 )
#             elif bond_type.lower() == 'zero':
#                 return ZeroCouponBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     discount_rate=float(bond_data['discount_rate'])
#                 )
#             else:
#                 raise ValueError(f"Unknown bond type: {bond_type}")
                
#         except Exception as e:
#             self.logger.error(f"Failed to load bond from {file_path}: {e}")
#             raise
    
#     def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
#         """
#         Load multiple bonds from JSON file
        
#         Args:
#             source_id: JSON file name
            
#         Returns:
#             List of bond objects
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             with open(file_path, 'r') as f:
#                 data = json.load(f)
            
#             bonds = []
            
#             for bond_data in data:
#                 bond_type = bond_data.get('bond_type', 'fixed')
                
#                 if bond_type.lower() == 'fixed':
#                     bond = FixedRateBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         coupon_rate=float(bond_data['coupon_rate']),
#                         payment_frequency=int(bond_data.get('payment_frequency', 2))
#                     )
#                 elif bond_type.lower() == 'floating':
#                     bond = FloatingRateBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         spread=float(bond_data['spread']),
#                         reference_rate_name=bond_data['reference_rate_name'],
#                         payment_frequency=int(bond_data.get('payment_frequency', 2))
#                     )
#                 elif bond_type.lower() == 'zero':
#                     bond = ZeroCouponBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         discount_rate=float(bond_data['discount_rate'])
#                     )
#                 else:
#                     self.logger.warning(f"Skipping bond with unknown type: {bond_type}")
#                     continue
                
#                 bonds.append(bond)
            
#             return bonds
                
#         except Exception as e:
#             self.logger.error(f"Failed to load bonds from {file_path}: {e}")
#             raise
    
#     def load_historical_rates(self, source_id: str) -> pd.DataFrame:
#         """
#         Load historical interest rates from JSON file
        
#         Args:
#             source_id: JSON file name
            
#         Returns:
#             DataFrame containing historical rates
#         """
#         file_path = os.path.join(self.data_directory, source_id)
        
#         try:
#             with open(file_path, 'r') as f:
#                 data = json.load(f)
            
#             return pd.DataFrame(data)
#         except Exception as e:
#             self.logger.error(f"Failed to load historical rates from {file_path}: {e}")
#             raise


# class DatabaseDataSource(DataSource):
#     """Data source for SQL databases"""
    
#     def __init__(self, db_path: str):
#         """
#         Initialize database data source
        
#         Args:
#             db_path: Path to SQLite database file
#         """
#         super().__init__()
#         self.db_path = db_path
    
#     def _get_connection(self) -> sqlite3.Connection:
#         """Get database connection"""
#         return sqlite3.connect(self.db_path)
    
#     def load_yield_curve(self, source_id: str) -> InterestRateCurve:
#         """
#         Load yield curve from database
        
#         Args:
#             source_id: Identifier for the yield curve (e.g., curve name or date)
            
#         Returns:
#             Interest rate curve
#         """
#         try:
#             conn = self._get_connection()
            
#             # Query yield curve header
#             header_query = """
#                 SELECT curve_date FROM yield_curve_headers
#                 WHERE curve_id = ?
#             """
#             cursor = conn.execute(header_query, (source_id,))
#             header = cursor.fetchone()
            
#             if not header:
#                 raise ValueError(f"No yield curve found with ID {source_id}")
            
#             curve_date = pd.to_datetime(header[0]).to_pydatetime()
            
#             # Query yield curve points
#             points_query = """
#                 SELECT tenor, rate FROM yield_curve_points
#                 WHERE curve_id = ?
#                 ORDER BY tenor
#             """
#             df = pd.read_sql(points_query, conn, params=(source_id,))
            
#             conn.close()
            
#             return InterestRateCurve(
#                 curve_date=curve_date,
#                 tenors=df['tenor'].tolist(),
#                 rates=df['rate'].tolist()
#             )
#         except Exception as e:
#             self.logger.error(f"Failed to load yield curve {source_id} from database: {e}")
#             raise
    
#     def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
#         """
#         Load bond from database
        
#         Args:
#             source_id: Bond contract ID
            
#         Returns:
#             Bond object
#         """
#         try:
#             conn = self._get_connection()
            
#             # Query bond data
#             query = """
#                 SELECT * FROM bonds
#                 WHERE contract_id = ?
#             """
#             cursor = conn.execute(query, (source_id,))
#             row = cursor.fetchone()
            
#             if not row:
#                 raise ValueError(f"No bond found with contract ID {source_id}")
            
#             # Convert row to dict
#             columns = [col[0] for col in cursor.description]
#             bond_data = dict(zip(columns, row))
            
#             conn.close()
            
#             # Create appropriate bond type
#             bond_type = bond_data.get('bond_type', 'fixed')
            
#             if bond_type.lower() == 'fixed':
#                 return FixedRateBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     coupon_rate=float(bond_data['coupon_rate']),
#                     payment_frequency=int(bond_data.get('payment_frequency', 2))
#                 )
#             elif bond_type.lower() == 'floating':
#                 return FloatingRateBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     spread=float(bond_data['spread']),
#                     reference_rate_name=bond_data['reference_rate_name'],
#                     payment_frequency=int(bond_data.get('payment_frequency', 2))
#                 )
#             elif bond_type.lower() == 'zero':
#                 return ZeroCouponBond(
#                     contract_id=bond_data['contract_id'],
#                     security_desc=bond_data['security_desc'],
#                     issue_date=bond_data['issue_date'],
#                     maturity_date=bond_data['maturity_date'],
#                     par_value=float(bond_data['par_value']),
#                     discount_rate=float(bond_data['discount_rate'])
#                 )
#             else:
#                 raise ValueError(f"Unknown bond type: {bond_type}")
                
#         except Exception as e:
#             self.logger.error(f"Failed to load bond {source_id} from database: {e}")
#             raise
    
#     def load_bonds(self, source_id: str) -> List[Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]]:
#         """
#         Load multiple bonds from database
        
#         Args:
#             source_id: Query identifier or filter criteria
            
#         Returns:
#             List of bond objects
#         """
#         try:
#             conn = self._get_connection()
            
#             # Query bonds
#             # source_id could be a portfolio ID, issuer, bond type, etc.
#             query = """
#                 SELECT * FROM bonds
#                 WHERE portfolio_id = ? OR issuer = ? OR bond_type = ?
#             """
#             df = pd.read_sql(query, conn, params=(source_id, source_id, source_id))
            
#             conn.close()
            
#             bonds = []
            
#             for _, row in df.iterrows():
#                 bond_data = row.to_dict()
#                 bond_type = bond_data.get('bond_type', 'fixed')
                
#                 if bond_type.lower() == 'fixed':
#                     bond = FixedRateBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         coupon_rate=float(bond_data['coupon_rate']),
#                         payment_frequency=int(bond_data.get('payment_frequency', 2))
#                     )
#                 elif bond_type.lower() == 'floating':
#                     bond = FloatingRateBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         spread=float(bond_data['spread']),
#                         reference_rate_name=bond_data['reference_rate_name'],
#                         payment_frequency=int(bond_data.get('payment_frequency', 2))
#                     )
#                 elif bond_type.lower() == 'zero':
#                     bond = ZeroCouponBond(
#                         contract_id=bond_data['contract_id'],
#                         security_desc=bond_data['security_desc'],
#                         issue_date=bond_data['issue_date'],
#                         maturity_date=bond_data['maturity_date'],
#                         par_value=float(bond_data['par_value']),
#                         discount_rate=float(bond_data['discount_rate'])
#                     )
#                 else:
#                     self.logger.warning(f"Skipping bond with unknown type: {bond_type}")
#                     continue
                
#                 bonds.append(bond)
            
#             return bonds
                
#         except Exception as e:
#             self.logger.error(f"Failed to load bonds with criteria {source_id} from database: {e}")
#             raise
    
#     def load_historical_rates(self, source_id: str) -> pd.DataFrame:
#         """
#         Load historical interest rates from database
        
#         Args:
#             source_id: Rate type or identifier
            
#         Returns:
#             DataFrame containing historical rates
#         """
#         try:
#             conn = self._get_connection()
            
#             query = """
#                 SELECT * FROM historical_rates
#                 WHERE rate_type = ?
#                 ORDER BY date
#             """
#             df = pd.read_sql(query, conn, params=(source_id,))
            
#             conn.close()
            
#             return df
#         except Exception as e:
#             self.logger.error(f"Failed to load historical rates for {source_id} from database: {e}")
#             raise

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
from ..core.date_utils import DateUtils

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
            # Load the CSV file
            df = pd.read_csv(file_path)
            
            # Check if the CSV has the expected columns
            if all(col in df.columns for col in ['Date', 'Tenor', 'Rate']):
                # Format is already correct
                pass
            else:
                # Try to map other column names to expected format
                column_map = {}
                
                # Look for date column
                date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
                if date_columns:
                    column_map[date_columns[0]] = 'Date'
                
                # Look for tenor column
                tenor_columns = [col for col in df.columns if 'tenor' in col.lower() or 'term' in col.lower() or 'maturity' in col.lower()]
                if tenor_columns:
                    column_map[tenor_columns[0]] = 'Tenor'
                
                # Look for rate column
                rate_columns = [col for col in df.columns if 'rate' in col.lower() or 'yield' in col.lower() or 'interest' in col.lower()]
                if rate_columns:
                    column_map[rate_columns[0]] = 'Rate'
                
                # Rename columns if mapping found
                if column_map:
                    df = df.rename(columns=column_map)
            
            # Ensure data types are correct
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            
            if 'Tenor' in df.columns:
                df['Tenor'] = pd.to_numeric(df['Tenor'])
            
            if 'Rate' in df.columns:
                df['Rate'] = pd.to_numeric(df['Rate'])
            
            # Create yield curve
            curve_date = df['Date'].iloc[0].to_pydatetime()
            tenors = df['Tenor'].tolist()
            rates = df['Rate'].tolist()
            
            return InterestRateCurve(curve_date, tenors, rates)
        except Exception as e:
            self.logger.error(f"Failed to load yield curve from {file_path}: {e}")
            raise
    
    def load_bond(self, source_id: str) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
        """
        Load a single bond from CSV file
        
        Args:
            source_id: CSV file name or bond ID
            
        Returns:
            Bond object
        """
        file_path = os.path.join(self.data_directory, source_id)
        
        try:
            # Check if the file exists
            if os.path.isfile(file_path):
                # Load the CSV file
                df = pd.read_csv(file_path)
                
                # Assuming only one bond in the file
                if len(df) == 0:
                    raise ValueError(f"No bond data found in {file_path}")
                
                return self._create_bond_from_row(df.iloc[0])
            else:
                # Try to load from bonds.csv using source_id as bond ID
                bonds_file = os.path.join(self.data_directory, "bonds.csv")
                if not os.path.isfile(bonds_file):
                    raise FileNotFoundError(f"Neither {file_path} nor bonds.csv exists")
                
                df = pd.read_csv(bonds_file)
                
                # Find bond by ID
                bond_row = None
                id_columns = [col for col in df.columns if 'id' in col.lower() or 'contract' in col.lower()]
                
                if id_columns:
                    id_col = id_columns[0]
                    bond_row = df[df[id_col] == source_id]
                    
                    if len(bond_row) == 0:
                        raise ValueError(f"No bond with ID {source_id} found in bonds.csv")
                    
                    return self._create_bond_from_row(bond_row.iloc[0])
                else:
                    raise ValueError("Could not identify ID column in bonds.csv")
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
            # Load the CSV file
            df = pd.read_csv(file_path)
            
            bonds = []
            for _, row in df.iterrows():
                try:
                    bond = self._create_bond_from_row(row)
                    bonds.append(bond)
                except Exception as e:
                    self.logger.warning(f"Skipping bond due to error: {e}")
                    continue
            
            if not bonds:
                self.logger.warning(f"No valid bonds found in {file_path}")
            
            return bonds
        except Exception as e:
            self.logger.error(f"Failed to load bonds from {file_path}: {e}")
            raise
    
    def _create_bond_from_row(self, row: pd.Series) -> Union[FixedRateBond, FloatingRateBond, ZeroCouponBond]:
        """
        Create a bond object from a DataFrame row
        
        Args:
            row: DataFrame row containing bond data
            
        Returns:
            Bond object
        """
        # Convert row to dictionary
        bond_data = row.to_dict()
        
        # Standardize column names to lowercase
        standardized_data = {k.lower(): v for k, v in bond_data.items()}
        
        # Map column names to expected fields
        field_mapping = {
            'contractid': 'contract_id',
            'securitydesc': 'security_desc',
            'issuedate': 'issue_date',
            'maturitydate': 'maturity_date',
            'parvalue': 'par_value',
            'parvalue_multiplier': 'par_value',  # Alternative name
            'coupon': 'coupon_rate',
            'couponrate': 'coupon_rate',
            'spread': 'spread',
            'referencerate': 'reference_rate_name',
            'referencerate_name': 'reference_rate_name',
            'paymentfrequency': 'payment_frequency',
            'bondtype': 'bond_type',
            'discountrate': 'discount_rate'
        }
        
        # Create a new dict with standardized field names
        data = {}
        for old_key, new_key in field_mapping.items():
            if old_key in standardized_data:
                data[new_key] = standardized_data[old_key]
        
        # Determine bond type
        bond_type = data.get('bond_type', '')
        
        # Check security description for type hints if bond_type is not explicitly set
        if not bond_type and 'security_desc' in data:
            desc = str(data['security_desc']).lower()
            if 'zero' in desc or desc.startswith('s 0'):
                bond_type = 'zero'
            elif 'float' in desc:
                bond_type = 'floating'
            else:
                bond_type = 'fixed'
        
        # Set default par value if not present
        if 'par_value' not in data:
            data['par_value'] = 1000.0
        
        # Set default payment frequency if not present
        if 'payment_frequency' not in data:
            data['payment_frequency'] = 2  # Semi-annual is common default
        
        # Ensure numeric types
        for field in ['par_value', 'coupon_rate', 'spread', 'discount_rate', 'payment_frequency']:
            if field in data and not pd.isna(data[field]):
                data[field] = float(data[field])
        
        # Create appropriate bond type
        if bond_type.lower() == 'zero':
            # Zero coupon bonds may not have explicit discount rate
            if 'discount_rate' not in data:
                data['discount_rate'] = 0.0
                
            return ZeroCouponBond(
                contract_id=data.get('contract_id', ''),
                security_desc=data.get('security_desc', ''),
                issue_date=data.get('issue_date', ''),
                maturity_date=data.get('maturity_date', ''),
                par_value=data.get('par_value', 1000.0),
                discount_rate=data.get('discount_rate', 0.0)
            )
        elif bond_type.lower() == 'floating':
            # Floating rate bonds need a spread and reference rate
            if 'spread' not in data:
                data['spread'] = 0.0
                
            return FloatingRateBond(
                contract_id=data.get('contract_id', ''),
                security_desc=data.get('security_desc', ''),
                issue_date=data.get('issue_date', ''),
                maturity_date=data.get('maturity_date', ''),
                par_value=data.get('par_value', 1000.0),
                spread=data.get('spread', 0.0),
                reference_rate_name=data.get('reference_rate_name', 'LIBOR'),
                payment_frequency=int(data.get('payment_frequency', 2))
            )
        else:  # Default to fixed rate
            # Fixed rate bonds need a coupon rate
            if 'coupon_rate' not in data and 'coupon' in standardized_data:
                data['coupon_rate'] = float(standardized_data['coupon'])
                
            return FixedRateBond(
                contract_id=data.get('contract_id', ''),
                security_desc=data.get('security_desc', ''),
                issue_date=data.get('issue_date', ''),
                maturity_date=data.get('maturity_date', ''),
                par_value=data.get('par_value', 1000.0),
                coupon_rate=data.get('coupon_rate', 0.0),
                payment_frequency=int(data.get('payment_frequency', 2))
            )
    
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
            # Try to parse dates in the DataFrame
            return pd.read_csv(file_path, parse_dates=True)
        except Exception as e:
            self.logger.error(f"Failed to load historical rates from {file_path}: {e}")
            raise