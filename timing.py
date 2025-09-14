"""
Date and Time Utilities Module

This module provides comprehensive date and time functionality for the Rava
medical reporting application, specifically handling Persian (Shamsi/Jalali)
calendar conversions and formatting.

Key Features:
- Persian calendar date formatting (YYYY/MM/DD)
- Persian calendar time formatting (HH:MM:SS)
- Automatic conversion from Gregorian to Shamsi calendar
- Consistent date/time formatting for medical reports
"""

from imports import *


# =============================================================================
# PERSIAN CALENDAR DATE FUNCTIONS
# =============================================================================

def get_shamsi_date_str():
    """
    Get the current date in Persian (Shamsi/Jalali) calendar format.
    
    Converts the current Gregorian date to Persian calendar and returns
    it in a standardized YYYY/MM/DD format suitable for medical reports.
    
    Returns:
        str: Current date in Persian calendar format (YYYY/MM/DD)
        
    Example:
        >>> get_shamsi_date_str()
        '1403/09/15'
    """
    # Get current Gregorian date and time
    current_datetime = datetime.now()
    
    # Convert to Persian (Shamsi) calendar
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=current_datetime)
    
    # Format as YYYY/MM/DD with zero-padding
    return f"{persian_datetime.year:04d}/{persian_datetime.month:02d}/{persian_datetime.day:02d}"


def get_shamsi_time_str():
    """
    Get the current time in Persian calendar context.
    
    Returns the current time in HH:MM:SS format, maintaining consistency
    with the Persian calendar system used throughout the application.
    
    Returns:
        str: Current time in HH:MM:SS format
        
    Example:
        >>> get_shamsi_time_str()
        '14:30:25'
    """
    # Get current Gregorian date and time
    current_datetime = datetime.now()
    
    # Convert to Persian (Shamsi) calendar
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=current_datetime)
    
    # Format as HH:MM:SS with zero-padding
    return f"{persian_datetime.hour:02d}:{persian_datetime.minute:02d}:{persian_datetime.second:02d}"


# =============================================================================
# MODULE TESTING AND PROTECTION
# =============================================================================

if __name__ == "__main__":
    # Display current Persian date and time for testing
    print(f"Current Persian Date: {get_shamsi_date_str()}")
    print(f"Current Persian Time: {get_shamsi_time_str()}")
    raise RavaAppError("Please don't run this file directly. Run main.py instead.")