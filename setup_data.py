#!/usr/bin/env python
"""
Setup script to prepare data directory for bond analysis
"""

import os
import shutil
import sys

def setup_data_directory():
    """
    Set up data directory and copy CSV files
    """
    # Get the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define data directory
    data_dir = os.path.join(script_dir, 'data')
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")
    else:
        print(f"Data directory already exists: {data_dir}")
    
    # List of CSV files to copy
    csv_files = ['bonds.csv', 'interest_rates.csv']
    
    # Copy each file to the data directory if it doesn't exist there
    for filename in csv_files:
        source_path = os.path.join(script_dir, filename)
        dest_path = os.path.join(data_dir, filename)
        
        if os.path.exists(source_path):
            if not os.path.exists(dest_path):
                shutil.copy2(source_path, dest_path)
                print(f"Copied {filename} to data directory")
            else:
                print(f"{filename} already exists in data directory")
        else:
            print(f"Warning: Source file {filename} not found in {script_dir}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(script_dir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    else:
        print(f"Output directory already exists: {output_dir}")
    
    print("\nSetup complete! You can now run basic_usage.py")

if __name__ == "__main__":
    setup_data_directory()
