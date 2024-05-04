from abstract_security import *
import os
def capitalize(string):
   string = str(string)
   return  string[0].upper()+string[1:]
def add_to_dict(key,value,_dict={}):
   _dict[key]=value
   return _dict
def get_dict(is_true=False,*args,**kwargs):
   return {key:value for key,value in kwargs.items() if is_true or value}      
def get_env(key=None,path=None):
   return get_env_value(**get_dict(key=key,path=path))
def unique_name(file_path,ext=None):
     dirName=os.path.dirname(file_path)
     baseName=os.path.basename(file_path)
     fileName,exts=os.path.splitext(baseName)
     ext=ext or exts
     dir_list = os.listdir(dirName)
     new_file_name=f"{fileName}{ext}"
     for i,file_name in enumerate(dir_list):
         if new_file_name not in dir_list:
             break
         new_file_name = f"{fileName}_{i}{ext}"
     file_path = f"{os.path.join(dirName,new_file_name)}"
     return file_path
def generate_date_formats():
    """
    Generates a list of datetime formats to try parsing date strings.
    Includes common and less-common variations with different separators.
    """
    base_formats = ['%Y', '%m', '%d', '%H', '%M', '%S', '%f']
    date_parts = ['%Y', '%m', '%d']
    time_parts = ['%H', '%M', '%S', '%f']
    separators = ['-', '/', ' ']
    
    date_formats = []
    for sep in separators:
        for order in permutations(date_parts, 3):
            date_format = f"{order[0]}{sep}{order[1]}{sep}{order[2]}"
            for time_sep in [':', '.']:
                for time_order in permutations(time_parts, 3):
                    time_format = f"{time_order[0]}{time_sep}{time_order[1]}{time_sep}{time_order[2]}"
                    date_formats.append(f"{date_format} {time_format}")
                    if '%f' in time_order:  # include formats with and without microseconds
                        short_time_format = time_format.replace('%f', '').rstrip(time_sep)
                        date_formats.append(f"{date_format} {short_time_format}")
            # Also add formats without time
            date_formats.append(date_format)
    
    return list(set(date_formats))  # Use set to remove duplicates and then convert back to list

def convert_date_string(date_str):
    """
    Attempts to convert a date string into a standardized datetime object using predefined formats.
    Returns the datetime object if successful, or None if all formats fail.
    """
    date_formats = generate_date_formats()
    for format in date_formats:
        try:
            return datetime.strptime(date_str, format)
        except ValueError:
            continue
    return None
def is_file_path(file_path):
    """
    Check if the provided file_path is a valid file path pointing to an existing file.
    
    Args:
    file_path (str): The file path to check.

    Returns:
    bool: True if file_path is a string referring to a valid file, False otherwise.
    """
    if not isinstance(file_path, str):
        return False
    try:
        # This will return True if file_path is a file that exists
        return os.path.isfile(file_path)
    except OSError as e:
        # Optionally log the error or handle it if needed
        print(f"An error occurred: {e}")
        return False
