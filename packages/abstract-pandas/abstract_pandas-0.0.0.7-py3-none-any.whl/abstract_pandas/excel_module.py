from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from werkzeug.datastructures import FileStorage
import pandas as pd
from pyexcel_ods import get_data
import ezodf
import tempfile,shutil,os
from abstract_utilities import *
from odf import text, teletype
from odf.opendocument import load
from .general_functions import *
from datetime import datetime
from itertools import permutations
from difflib import get_close_matches
from datetime import datetime
import pandas as pd
from pyxlsb import open_workbook
import pandas as pd
import os
from io import BytesIO
# Example usage


def safe_excel_save(df,original_file_path,index=False, engine='openpyxl'):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        temp_file_name = tmp.name
        if not isinstance(headers_js,pd.DataFrame):
            df = pd.DataFrame(new_data = pd.DataFrame([headers_js]))
        df.to_excel(tmp.name, index=index, engine=engine)  # Save your DataFrame to the temp file
    if os.path.getsize(temp_file_name) > 0:
        shutil.move(temp_file_name, original_file_path)
    else:
        print("Temporary file is empty or wasn't written correctly. Original file is unchanged.")
    # Cleanup: Ensure the temporary file is deleted if it hasn't been moved
    if os.path.exists(temp_file_name):
        os.remove(temp_file_name)
def move_excel_file(current_path, target_path):
    """
    Moves an Excel file from the current_path to the target_path.
    
    Parameters:
    - current_path: str, the current path including filename of the Excel file.
    - target_path: str, the target path including filename where the Excel file should be moved.
    
    Returns:
    - bool: True if the file was successfully moved, False otherwise.
    """
    try:
        # Check if the current file exists
        if not os.path.isfile(current_path):
            print(f"The file {current_path} does not exist.")
            return False

        # Move the file
        shutil.move(current_path, target_path)
        print(f"File moved successfully from {current_path} to {target_path}")
        return True
    except Exception as e:
        print(f"Error moving the file: {e}")
        return False
def unique_name(base_path, suffix='_', ext='.xlsx'):
    """
    Generates a unique file path by appending a datetime stamp or incrementing a suffix.
    
    Parameters:
    - base_path (str): Base path of the file without extension.
    - suffix (str): Suffix to append for uniqueness.
    - ext (str): File extension.
    
    Returns:
    - str: A unique file path.
    """
    # Generate initial path with datetime suffix
    datetime_suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_path = f"{base_path}{suffix}{datetime_suffix}{ext}"
    
    # Check if this path exists, if it does, increment an index until a unique name is found
    counter = 1
    while os.path.isfile(unique_path):
        unique_path = f"{base_path}{suffix}{datetime_suffix}_{counter}{ext}"
        counter += 1
    
    return unique_path

def get_new_excel_path(source=None):
    """
    Derives a new non-conflicting Excel file path based on the input source.
    
    Parameters:
    - source (str, pd.DataFrame, or bytes): Original source which can be a path or DataFrame.
    
    Returns:
    - str: A unique file path for a new Excel file.
    """
    default_filename = "new_excel.xlsx"

    # Handle DataFrame directly
    if isinstance(source, pd.DataFrame):
        return unique_name(os.path.splitext(default_filename)[0])

    # Handle source as a string path or bytes (assuming bytes can be decoded to a path)
    elif isinstance(source, (str, bytes)):
        if isinstance(source, bytes):
            try:
                source = source.decode('utf-8')
            except UnicodeDecodeError:
                print("Error: Bytes source could not be decoded to a string.")
                return unique_name(os.path.splitext(default_filename)[0])

        if os.path.isfile(source):
            base_path, _ = os.path.splitext(source)
            return unique_name(base_path)
        else:
            return source  # Return the source itself if it's a non-existent file path

    # Handle None or any other type that doesn't fit the above categories
    else:
        return unique_name(os.path.splitext(default_filename)[0])
def read_ods_file(file_path):
    doc = ezodf.opendoc(file_path)
    sheets = {}
    
    for sheet in doc.sheets:
        data = []
        for row in sheet.rows():
            row_data = []
            for cell in row:
                if cell.value_type == 'date':
                    # Explicitly handle date cells
                    date_obj = convert_date_string(str(cell.value))
                    row_data.append(date_obj)
                else:
                    # Append other types of cells directly
                    row_data.append(cell.value)
            data.append(row_data)
        df = pd.DataFrame(data)
        sheets[sheet.name] = df
        print(f"Processed sheet: {sheet.name}")
    return sheets
def ods_to_xlsx(ods_path, xlsx_path):
    doc = load(ods_path)
    data_frames = []

    for table in doc.spreadsheet.getElementsByType(Table):
        rows = []
        for row in table.getElementsByType(TableRow):
            cells = []
            for cell in row.getElementsByType(TableCell):
                repeat = cell.getAttribute("numbercolumnsrepeated")
                if not repeat:
                    repeat = 1
                cell_data = teletype.extractText(cell) or ""
                cells.extend([cell_data] * int(repeat))
            if cells:
                rows.append(cells)
        df = pd.DataFrame(rows)
        data_frames.append(df)

    # Assuming you want to save the first sheet as an example
    if data_frames:
        data_frames[0].to_excel(xlsx_path, index=False)
def read_ods(file_path,xlsx_path=None):
    
    ods_to_xlsx(file_path,xlsx_path)
    return pd.read_excel(xlsx_path)

def get_df(source,nrows=None):
    if isinstance(source, pd.DataFrame):
        print("Already a DataFrame.")
        if nrows != None:
            return source.columns.tolist()
        return source
    
    if isinstance(source, str) and os.path.isfile(source):
        file_ext = os.path.splitext(source)[-1].lower()
        try:
            if file_ext == '.csv':
                return pd.read_csv(source, nrows=nrows)  # Read no rows of data, only headers
            elif file_ext == '.ods':
                return pd.read_excel(source, engine='odf', nrows=nrows)  # For .ods files
            elif file_ext in ('.xlsx', '.xls'):
                return pd.read_excel(source, engine='openpyxl', nrows=nrows)  # For Excel files
            elif file_ext == '.tsv':  # Handle TSV files
                return pd.read_csv(source, sep='\t', nrows=nrows)
            elif file_ext == '.xlsb':
                return pd.read_excel(source, engine = 'pyxlsb',nrows=nrows) # Custom function to handle .xlsb
        except Exception as e:
            print(f"Failed to read file: {e}")
    elif isinstance(source, FileStorage):  # Check if source is a FileStorage object
        try:
            # Read the file directly from the file object, considering Excel format
            return pd.read_excel(source.stream, nrows=nrows)
        except Exception as e:
            print(f"Failed to read file: {e}")
    else:
        print("Invalid source provided.")
    
    return None




def read_excel_as_dicts(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, engine='openpyxl')
    # Convert each row to a dictionary with column headers as keys
    rows_as_dicts = df.to_dict(orient='records')
    return rows_as_dicts

def update_or_append_data(df, new_data, search_column=None, search_value=None, clear_duplicate=True):
    """
    Update an existing row or append a new row with new_data while standardizing data types and optionally removing duplicates.
    Accepts new_data as a dictionary or DataFrame.
    """
    # Check if new_data is a DataFrame
    if isinstance(new_data, pd.DataFrame):
        # Directly use the DataFrame if provided
        new_df = new_data
    else:
        # Create a DataFrame from dictionary if new_data is a dict
        new_df = pd.DataFrame([new_data])

    # Ensure all columns in new_df exist in df, add them if not
    for col in new_df.columns:
        if col not in df.columns:
            df[col] = pd.NA  # Initialize new columns with missing values

    if search_column and search_value is not None:
        # Standardize data types for existing columns
        new_df = new_df.astype({col: df[col].dtype for col in df.columns.intersection(new_df.columns)})

        # Attempt to find matching rows
        mask = df[search_column] == search_value
        if mask.any():
            # Update existing rows
            for col in new_df.columns:
                df.loc[mask, col] = new_df.iloc[0][col]
            print(f"Updated rows where {search_column} = {search_value}.")
        else:
            # Append new row if no match is found
            df = pd.concat([df, new_df], ignore_index=True)
            print(f"Appended new data as no existing match found for {search_value}.")
    else:
        # Append new data if no specific search criteria are given
        df = pd.concat([df, new_df], ignore_index=True)
        print("Appended new data as no search criteria provided.")
    
    if clear_duplicate:
        df = df.drop_duplicates(subset=[search_column] if search_column else None, keep='last')
        print("Duplicates removed after update/append.")
        
    return df

def append_unique_to_excel(file_path, new_data, search_column=None, search_value=None, clear_duplicate=False):
    """
    Append new data or update existing data in an Excel file based on specified search column and value.
    Optionally clear duplicates based on the search column.
    """
    if isinstance(new_data, dict):
        new_data = pd.DataFrame([new_data])

    # If the file does not exist, create it with new_data
    if not os.path.isfile(file_path):
        safe_excel_save(new_data, file_path)
        print("Excel file created with new data.")
        return

    df = get_df(file_path)  # Read existing data
    
    # Standardize new_data keys to strings (in case they are not)
    #new_data = {str(k): v for k, v in new_data.items()}

    # Update or append new data, and optionally clear duplicates
    df = update_or_append_data(df, new_data, search_column, search_value, clear_duplicate)
    
   # Save the updated DataFrame back to the Excel file
    safe_excel_save(df, file_path)
    print(f"Data successfully saved to {file_path}.")
def get_headers(df):
    df = get_df(df)
    column_names = df.columns.tolist()
    return column_names
def get_row_as_list(df,index=0):
    df=get_df(df)
    if get_row_number(df)>index:
        return df.loc[index].astype(str).tolist()
def get_row_number(df):
    df=get_df(df)
    return len(df)
def search_df_for_values(df, column_name, query_list):
    """
    Search DataFrame column for rows matching any items in query_list.

    Parameters:
    - df (pd.DataFrame): The DataFrame to search.
    - column_name (str): The name of the column to search.
    - query_list (list): A list of values to search for in the column.

    Returns:
    - pd.DataFrame: A DataFrame of rows where the column values match any item in the query_list.
    """
    df=get_df(df)
    mask = df[column_name].isin(query_list)
    return df[mask]
def search_df_with_condition(df, column_name, condition_func):
    """
    Search DataFrame column to find rows where condition_func returns True.

    Parameters:
    - df (pd.DataFrame): The DataFrame to search.
    - column_name (str): The column to apply the condition on.
    - condition_func (function): A function that takes a single value and returns True or False.

    Returns:
    - pd.DataFrame: A DataFrame of rows where the column values satisfy the condition_func.
    """
    df=get_df(df)
    # Applying the condition function vectorized
    mask = df[column_name].apply(condition_func)
    return df[mask]
def query_dataframe(df, query_string):
    """
    Use DataFrame.query() to filter rows based on a query string.

    Parameters:
    - df (pd.DataFrame): The DataFrame to query.
    - query_string (str): The query string to evaluate.

    Returns:
    - pd.DataFrame: The filtered DataFrame.
    """
    return df.query(query_string)

def get_expected_headers(df,*expected_headers):
    if isinstance(expected_headers,tuple or set):
        expected_headers=list(expected_headers)
    else:
        expected_headers=make_list(expected_headers)
    expected_headers = {expected_header:"" for expected_header in expected_headers}
    return get_closest_headers(df,expected_headers)
def get_expected_address_headers(df):
    headers_js = {"address": "", "city": "", "state": "", "zip": "", "external": ""}
    return get_closest_headers(df,expected_headers=headers_js)
def get_closest_headers(df,expected_headers={}):
    actual_headers = get_headers(df)  # Extract the actual headers from the DataFrame

    # Mapping actual headers to expected headers based on closest match
    for expected_header in expected_headers:
        # Using get_close_matches to find the closest match; returns a list
        close_matches = get_close_matches(expected_header, actual_headers, n=1, cutoff=0.6)
        if close_matches:
            expected_headers[expected_header] = close_matches[0]
        else:
            # If no close matches found, leave as empty string which signifies no match found
            expected_headers[expected_header] = ""

    return expected_headers

def filter_and_deduplicate_df(df, filter_columns, filter_values, dedup_columns=None):
    """
    Filters a DataFrame based on specified values in given columns and removes duplicates.

    Parameters:
    - df (pd.DataFrame): The DataFrame to filter and deduplicate.
    - filter_columns (list of str): Column names to apply the filters on.
    - filter_values (list of list): Lists of values to include for each column in filter_columns.
    - dedup_columns (list of str, optional): Columns to consider for dropping duplicates. If not specified,
      duplicates will be dropped based on all columns.

    Returns:
    - pd.DataFrame: The filtered and deduplicated DataFrame.
    """
    # Ensure the input integrity
    assert len(filter_columns) == len(filter_values), "Each filter column must correspond to a list of filter values."

    # Apply filters based on the columns and corresponding values
    mask = pd.Series([True] * len(df))
    for col, vals in zip(filter_columns, filter_values):
        mask &= df[col].isin(vals)

    filtered_df = df[mask]

    # Drop duplicates based on specified columns
    if dedup_columns:
        deduplicated_df = filtered_df.drop_duplicates(subset=dedup_columns)
    else:
        deduplicated_df = filtered_df.drop_duplicates()

    return deduplicated_df

def get_first_for_each(df,headers,queries,new_file_path=None):
    new_file_path = new_file_path or get_new_excel_path(df)
    df=get_df(df)
    headers = get_expected_headers(df,headers).values()
    # Filter the DataFrame to only include rows with ZIP codes that are in the 'zips' list
    df=filter_and_deduplicate_df(df, headers, queries, dedup_columns=None)
    safe_excel_save(df,new_file_path)
    # Save the filtered and deduplicated DataFrame to a new Excel file
    return new_file_path
