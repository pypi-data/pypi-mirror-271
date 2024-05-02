import os
import numpy as np
import pandas as pd
from odhpy import utils



def read_res_csv(filename, custom_na_values=None, df=None, colprefix=None, allow_nonnumeric=False, **kwargs):
    """Reads a res csv data file into a DataFrame, and sets the index to the Date.

    Args:
        filename (_type_): _description_
        custom_na_values (_type_): A list of values to override the automatically-determined missing values. If None, the missing values will include any defined in the .res.csv file as well as ['', ' ', 'null', 'NULL', 'NAN', 'NaN', 'nan', 'NA', 'na', 'N/A' 'n/a', '#N/A', '#NA', '-NaN', '-nan'].

    Returns:
        _type_: _description_
    """
    # Handle custom na values
    if custom_na_values is None:
        na_values = ['', ' ', 'null', 'NULL', 'NAN', 'NaN', 'nan', 'NA', 'na', 'N/A' 'n/a', '#N/A', '#NA', '-NaN', '-nan']
    else:
        na_values = custom_na_values
    # If no df was supplied, instantiate a new one
    if df is None:
        df = pd.DataFrame()
    # Scrape through the header
    metadata_lines = []
    eoh_found = False
    with open(filename) as f:
        line = ""
        for line in f:
            metadata_lines.append(line)
            if line.strip().startswith("EOH"):
                eoh_found = True
                break
            if custom_na_values is None and line.strip().lower().startswith("missing data value,"):
                new_na_value = line.strip()[len("missing data value,"):] #e.g. "-9999"
                na_values.append(new_na_value)
    if not eoh_found:
        return None #maybe it's not a .res.csv
    col_header_line_number = len(metadata_lines) - 2
    lines_to_skip = [i for i in range(col_header_line_number)] + [col_header_line_number + 1]
    # Read the data
    temp = pd.read_csv(filename, na_values=na_values, skiprows=lines_to_skip)
    # Date index
    temp.set_index(temp.columns[0], inplace=True)
    temp.index = utils.standardize_datestring_format(temp.index)
    temp.index.name = "Date"
    # Check values
    if not allow_nonnumeric:
        for col in temp.columns:
            if not np.issubdtype(temp[col].dtype, np.number):
                raise Exception(f"ERROR: Column '{col}' is not numeric!")
    # Rename columns if required
    if colprefix is not None:
        for c in temp.columns:
            temp.rename(columns = {c:f"{colprefix}{c}"}, inplace = True)
    # Join to existing dataframe if required
    if df is None:
        df = temp
    else:
        if len(df) > 0:
            # Check that the dates overlap
            newdf_ends_before_df_starts = temp.index[0] < df.index[-1]
            df_ends_before_newdf_starts = df.index[-1] < temp.index[0]
            if newdf_ends_before_df_starts or df_ends_before_newdf_starts:
                raise Exception("ERROR: The dates in the new dataframe do not overlap with the existing dataframe!")
        df = df.join(temp, how="outer")
    # Return
    #utils.assert_df_format_standards(df)
    return df
