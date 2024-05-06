from odf.table import Table, TableRow, TableCell
from odf.opendocument import load
import pandas as pd
from odf import text, teletype
from datetime import datetime
import tempfile,shutil,os,ezodf,inspect
def source_ext():
    return {'.parquet':'pyarrow','.txt':'python','.xlsx':'openpyxl','.xls':'openpyxl','.xlsb':'pyxlsb','.ods':'odf'}
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
def read_ods(file_path,xlsx_path=None):
    ods_to_xlsx(file_path,xlsx_path)
    return pd.read_excel(xlsx_path)
def save_df(df,file_path,index=None,suffix=None,engine=None):
    df = get_df(df)
    suffix = suffix or os.path.splitext(original_file_path)[-1] or '.xlsx'
    logging.info(f"saving df with suffix {file_ext} to {file_path}")
    try:
        if file_ext in ['.ods','.xlsx', '.xls','.xlsb']:
            pd.to_excel(df,  engine=engine or source_ext().get(file_ext))
        elif file_ext in ['.csv','.tsv','.txt']:
            pd.to_csv(df,  engine=engine or source_ext().get(file_ext))
        elif file_ext in [".shp", ".cpg", ".dbf", ".shx"]:
            gpd.save_file(df, file_path)
        elif file_ext == '.parquet':
            pd.to_parquet(df, engine=engine or source_ext().get(file_ext))
        else:
            logging.info(f"could not find appropriate file type, attempting generic file save")
            try:
                df = save_to_file(file_path)
            except Exception as e:
                logging.info(f"file save for file path {file_path} unsuccesful:\n {e}")
                return False
    except Exception as e:
        logging.info(f"Failed to read file: {e}")
        return False
    logging.info(f"file save for file path {file_path} succesful")
    return True
def safe_excel_save(df,original_file_path,index=False,suffix=None,engine=None):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        temp_file_name = tmp.name
        result = save_df(df,file_path,index=index,suffix=suffix,engine=engine)  # Save your DataFrame to the temp file
    if result and os.path.getsize(temp_file_name) > 0:
        shutil.move(temp_file_name, original_file_path)
    else:
       logging.info("Temporary file is empty or wasn't written correctly. Original file is unchanged.")
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

def get_caller_path():
    """ Returns the absolute directory path of the script that calls this function. """
    stack = inspect.stack()
    caller_frame = stack[1]
    caller_path = os.path.abspath(caller_frame.filename)
    return os.path.dirname(caller_path)

def mkdir(base_path, subfolder):
    """ Ensure a subdirectory exists in the given base path and return its path. """
    full_path = os.path.join(base_path, subfolder)
    if not os.path.exists(full_path):
        os.makedirs(full_path, exist_ok=True)
    return full_path

def get_excels_dir(abs_dir=None):
    """ Get or create a directory named 'excels' in the specified or caller's directory. """
    abs_dir = abs_dir or get_caller_path()
    return mkdir(abs_dir, 'excels')

def get_filtered_dir():
    """ Get or create a directory named 'filtered' inside the 'excels' directory. """
    return mkdir(get_excels_dir(), 'filtered')

def get_original_dir():
    """ Get or create a directory named 'original' inside the 'excels' directory. """
    return mkdir(get_excels_dir(), 'original')

def get_path_pieces(file_path):
    directory = os.path.dirname(file_path)
    baseName = os.path.basename(file_path)
    fileName,ext = os.path.splitext(baseName)
    return baseName,fileName,ext
def get_filtered_file_path(file_path,filter_type='filtered'):
    baseName,fileName,ext = get_path_pieces(file_path)
    return os.path.join(get_filtered_dir(), f"{fileName}_{filter_type}{ext}")
def get_original_file_path(file_path):
    baseName,fileName,ext = get_path_pieces(file_path)
    return os.path.join(get_original_dir(), baseName)
def save_original_excel(file_path,original_dir=None):
    df = get_df(file_path)
    original_dir = original_dir or os.getcwd()
    original_file_path = get_original_file_path(file_path)
    safe_excel_save(df,original_file_path)
    return original_file_path
def save_filtered_excel(df,file_path,filter_type='filtered'):
    df = get_df(df)
    filtered_file_path = get_filtered_file_path(file_path,filter_type=filter_type)
    safe_excel_save(df,filtered_file_path)
    return filtered_file_path
