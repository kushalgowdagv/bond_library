"""
Utilities for date calculations and manipulations
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Union, Optional

class DateUtils:
    """Utility class for date calculations with actual/365 day count convention"""
    
    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse date string to datetime object"""
        try:
            # Try MM/DD/YYYY format
            return datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            try:
                # Try M/D/YYYY format
                return datetime.strptime(date_str, "%-m/%-d/%Y")
            except ValueError:
                # Fallback to basic parser
                return pd.to_datetime(date_str).to_pydatetime()
    
    @staticmethod
    def year_fraction(start_date: datetime, end_date: datetime) -> float:
        """Calculate year fraction between two dates using actual/365 convention"""
        days = (end_date - start_date).days
        return days / 365.0

    @staticmethod
    def add_months(input_date: datetime, months: int) -> datetime:
        """Add specified number of months to a date"""
        month = input_date.month - 1 + months
        year = input_date.year + month // 12
        month = month % 12 + 1
        day = min(input_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 
                                   31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return input_date.replace(year=year, month=month, day=day)
    