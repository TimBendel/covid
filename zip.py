import pandas as pd
import numpy as np
from uszipcode import SearchEngine

# Function to check if string could be a ZIP code
def looks_like_zip(string):
    if pd.isnull(string):
        return False
    if isinstance(string, float) and string.is_integer():
        string = str(int(string))
    elif isinstance(string, str):
        string = string.split('-')[0]  # If it's a ZIP+4, ignore the +4 part
    else:
        return False
    return len(string) in [5, 9]

# Function to check if a ZIP code is valid
def is_valid_zip(string):
    search = SearchEngine(simple_zipcode=True)  # Set up ZIP code search engine
    if isinstance(string, float) and string.is_integer():
        string = str(int(string)).zfill(5)  # Pad with zeros if necessary
    elif isinstance(string, str):
        string = string.split('-')[0]  # If it's a ZIP+4, ignore the +4 part
        string = string.zfill(5)  # Pad with zeros if necessary
    else:
        return False
    zipcode = search.by_zipcode(string)
    return zipcode.Zipcode is not None

# Load the data
df = pd.read_csv('path_to_your_file.csv')

# Check each column for ZIP codes
for col in df.columns:
    # Check if this column looks like it could contain ZIP codes
    if df[col].apply(looks_like_zip).any():
        # If it does, validate those potential ZIP codes
        df[col + '_valid_zip'] = df[col].apply(is_valid_zip)

# Save the results
df.to_csv('output.csv', index=False)

