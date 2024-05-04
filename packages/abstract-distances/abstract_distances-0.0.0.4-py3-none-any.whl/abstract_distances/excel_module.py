import pandas as pd
import tempfile,shutil,os
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from werkzeug.datastructures import FileStorage
from abstract_utilities import *
def safe_excel_save(df,original_file_path,index=False,engine='openpyxl'):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        temp_file_name = tmp.name
        df.to_excel(tmp.name, index=index, engine=engine)  # Save your DataFrame to the temp file
    if os.path.getsize(temp_file_name) > 0:
        shutil.move(temp_file_name, original_file_path)
    else:
        print("Temporary file is empty or wasn't written correctly. Original file is unchanged.")
    # Cleanup: Ensure the temporary file is deleted if it hasn't been moved
    if os.path.exists(temp_file_name):
        os.remove(temp_file_name)
def get_excel_data(excel_data):
    if isinstance(excel_data,str):
        if os.path.isfile(excel_data):
            excel_data=read_excels(excel_data)[0]
    return excel_data
def merge_dataframes(dataframes):
    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df
def filter_zips(zip_text):
    total_zips = []
    if isinstance(zip_text,str):
    	zip_text = zip_text.split('\n')
    for piece in zip_text:
        if piece:
            zip_codes = piece.replace('-',' ').replace(',',' ').split(' ')
            total_zips = list(set(total_zips))
            for zip_code in zip_codes:
                if zip_code and is_number(zip_code) and len(str(zip_code))==5 and zip_code not in total_zips:
                    total_zips.append(zip_code)
    return total_zips
def modify_duplicates_in_column(excel_file_path, column_name):
    # Read the Excel file into a DataFrame
    df = get_df(excel_file_path)
    
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        print("Error: Specified column does not exist in the Excel file.")
        return
    
    # Dictionary to keep track of counts
    count_dict = {}
    
    # Function to process each item in the column
    def process_item(item):
        if item in count_dict:
            count_dict[item] += 1
            return f"{item}_{count_dict[item]}"
        else:
            count_dict[item] = 0
            return item
    
    # Apply the function to the specified column
    df[column_name] = df[column_name].apply(process_item)
    
    # Save the modified DataFrame back to a new Excel file
    safe_excel_save(df,excel_file_path)
    

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
def read_csv_to_dataframe(file_path):
    """
    Reads a CSV file and converts it into a pandas DataFrame.
    
    Parameters:
    - file_path (str): The path to the CSV file to be read.
    
    Returns:
    - DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        print("CSV file has been successfully loaded into a DataFrame.")
        return df
    except Exception as e:
        print(f"An error occurred while loading the CSV file: {e}")
        return None
def get_df(source,file_path=None,make_excel=False):
    if isinstance(source, pd.DataFrame):
        return source
    if isinstance(source,str) and make_excel:
        if isinstance(source,str) and file_path == None:
            file_path=source
        if not isinstance(make_excel,dict):
            if isinstance(make_excel,list):
                make_excel_ls = make_excel
                make_excel = {}
                for make_obj in make_excel_ls:
                    make_excel[make_obj] = ""
            else:
                make_excel = {}
        new_df = pd.DataFrame([make_excel])
        if file_path:
            safe_excel_save(new_df,file_path,index=False, engine='openpyxl')
        return new_df
    if isinstance(source, str) and os.path.isfile(source):
        file_ext = os.path.splitext(source)[-1].lower()
        try:
            if file_ext == '.csv':
                return pd.read_csv(source)
            elif file_ext == '.ods':
                return read_ods(source)
            elif file_ext in ('.xlsx', '.xls'):
                return pd.read_excel(source, engine='openpyxl')
            elif file_ext == '.tsv':  # Handle TSV files
                return pd.read_csv(source, sep='\t')

        except Exception as e:
            print(f"Failed to read file: {e}")
    elif isinstance(source, FileStorage):  # Check if source is a FileStorage object
        try:
            # Read the file directly from the file object
            return pd.read_excel(source)
        except Exception as e:
            print(f"Failed to read file: {e}")
    else:
        print("Invalid source provided.")
    
    return None
import pandas as pd

def add_or_update_headers(df, column_name, default_value=None):
    """
    Add a new column to a DataFrame with a default value if it does not already exist.

    Parameters:
    df (DataFrame): The DataFrame to modify.
    column_name (str): The name of the column to add.
    default_value (Any, optional): The default value to assign to the new column. Defaults to None.

    Returns:
    DataFrame: The modified DataFrame with the new column added if it didn't exist.
    """
    if column_name not in df.columns:
        df[column_name] = default_value
    else:
        print(f"Column '{column_name}' already exists in the DataFrame. No changes made.")

    return df


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
def read_csv_to_dataframe(file_path):
    """
    Reads a CSV file and converts it into a pandas DataFrame.
    
    Parameters:
    - file_path (str): The path to the CSV file to be read.
    
    Returns:
    - DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        print("CSV file has been successfully loaded into a DataFrame.")
        return df
    except Exception as e:
        print(f"An error occurred while loading the CSV file: {e}")
        return None
def get_raw_data(raw_data_dir,before=None,after=None):
    after = after or int(time.time())+1000
    before = before or 0
    datas=[]
    if os.path.isdir(raw_data_dir):
        for raw_data_file in os.listdir(raw_data_dir):
            raw_data_file_path = os.path.join(raw_data_dir,raw_data_file)
            raw_data = safe_read_from_json(raw_data_file_path)
            if raw_data and isinstance(raw_data,dict):
                raw_data_time_stamp = raw_data.get("Timestamp") or raw_data.get("Data_Time_Stamp")
                if raw_data_time_stamp:
                    if is_number(raw_data_time_stamp):
                        raw_data_time_stamp=int(raw_data_time_stamp)
                    raw_data_time_stamp = convert_date_to_timestamp(raw_data_time_stamp)
                    if raw_data_time_stamp and raw_data_time_stamp>int(before) and raw_data_time_stamp<int(after):
                        datas.append(raw_data)
    return datas
def count_rows_columns(df):
    """
    Counts the number of rows and columns in a pandas DataFrame.

    Parameters:
    - df (DataFrame): The pandas DataFrame whose dimensions will be counted.

    Returns:
    - tuple: A tuple containing two elements, the number of rows and the number of columns in the DataFrame.
    """
    rows, columns = df.shape  # df.shape returns a tuple (number of rows, number of columns)
    return rows, columns
def row_to_list_of_strings(df, row_index):
    """
    Converts a specified row of a DataFrame into a list of strings.
    
    Parameters:
    - df (DataFrame): The pandas DataFrame from which to select the row.
    - row_index (int): The index of the row to be converted.
    
    Returns:
    - list: A list of strings representing the values in the row.
    """
    # Select the row with .iloc[] and convert all its elements to strings
    row_as_strings = df.iloc[row_index].astype(str).tolist()
    return row_as_strings
def filter_out_rows_with_query(query_string,data,column_names):
    
    mask = df[column_names].apply(lambda x: x.str.lower().contains(str(int(query_string)).lower())).any(axis=1)
    
    # Apply the mask to get a DataFrame with only the rows where the query_string is present in at least one of the specified columns
    filtered_df = df[mask]
    return filtered_df
def get_itteration(objs,string):
    for i,obj in enumerate(objs):
        if string == obj:
            return i
def filter_rows_based_on_keywords(df, column_names, keywords):
    """
    Filter rows in a DataFrame based on the presence or absence of specified keywords in given columns.

    Parameters:
    - df (pd.DataFrame): The DataFrame to filter.
    - column_names (list): The names of the columns to search for the keywords.
    - keywords (list): The keywords to search for in the specified columns.

    Returns:
    - pd.DataFrame: A DataFrame filtered based on the specified criteria.
    """
    # Create a mask initialized to False for each row
    mask = pd.Series([False] * len(df))
    
    for column_name in column_names:
        if column_name in df.columns:
            # Update the mask to include rows where the column contains any of the keywords
            for keyword in keywords:
                mask = mask | df[column_name].astype(str).str.contains(keyword, case=False, na=False)
    
    # Invert the mask to filter out rows that match the keywords
    return df[~mask]
def identify_common_rows(df_1,df_2):
    # Find the indices of rows that are common in both battery_df and solar_panel_df
    return df_1.index.intersection(df_2.index)
def filter_by_queries_in_column(df,column,queries):
    return df[df[column].isin(queries)]
def remove_rows(target_csv,common_indices):
    # Remove the common rows from battery_df
    return target_csv.drop(common_indices)
def read_excels(file_storage_objects):
    dataframes = []
    for file_storage in file_storage_objects:
        # Determine if file_storage is a file path (str) or a file-like object
        if isinstance(file_storage, str):  # File path
            if file_storage.endswith('.xlsx') or file_storage.endswith('.xls'):
                df = pd.read_excel(file_storage)  # Directly use the file path
            elif file_storage.endswith('.csv'):
                df = pd.read_csv(file_storage)  # Directly use the file path
        else:  # Assuming file_storage is a file-like object
            if file_storage.filename.endswith('.xlsx') or file_storage.filename.endswith('.xls'):
                df = pd.read_excel(file_storage.stream)  # Use .stream for file-like objects
            elif file_storage.filename.endswith('.csv'):
                df = pd.read_csv(file_storage.stream)  # Use .stream for file-like objects

        # Append the dataframe if one was created
        if 'df' in locals():
            dataframes.append(df)
            del df  # Clear df to avoid wrongfully appending it again

    if not dataframes:
        raise ValueError("No valid dataframes were read from the files.")
    return dataframes

def convert_xlsx_to_csv(xlsx_file_path, csv_file_path, sheet_name=0):
    """
    Converts an Excel file to a CSV file.

    Parameters:
    - xlsx_file_path (str): The path to the source Excel file.
    - csv_file_path (str): The path where the CSV file will be saved.
    - sheet_name (str|int): The name or index of the sheet to convert. Defaults to the first sheet.

    Returns:
    - Nonea
    """
    # Load the Excel file
    df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name)
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)  # Set index=False to exclude row indices from the CSV

    print(f"Excel sheet saved as CSV at: {csv_file_path}")
def get_column_names(data):
    try:
        df = pd.DataFrame(data)
    except:
        df = data
    # Parse the first row into a list of strings
    row_as_list = df.iloc[0].astype(str).tolist()

    # For a specific row by index
    index = 0  # Change the index as needed
    row_as_list_by_index = df.loc[index].astype(str).tolist()
    column_names = df.columns.tolist()
    return column_names
def safe_read_excel(file_path):
    try:
        # Try reading the Excel file directly with pandas
        df = pd.read_excel(file_path, engine='openpyxl')
    except zipfile.BadZipFile:
        # If reading fails due to a BadZipFile error, try repairing by resaving the file
        try:
            # Attempt to open the workbook with openpyxl
            wb = load_workbook(filename=file_path)
            # Save the workbook to a temporary file
            with NamedTemporaryFile(delete=False) as tmp:
                wb.save(tmp.name)
                # Try reading the repaired file into a pandas DataFrame
                df = pd.read_excel(tmp.name, engine='openpyxl')
        except Exception as e:
            # If the process fails, raise the original BadZipFile error
            raise zipfile.BadZipFile("File is not a zip file and cannot be repaired") from e
        finally:
            # Clean up: remove the temporary file if it exists
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
    return df
def read_excel_as_dicts(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, engine='openpyxl')
    # Convert each row to a dictionary with column headers as keys
    rows_as_dicts = df.to_dict(orient='records')
    return rows_as_dicts
def find_matching_rows(rows_as_dicts, criteria_dict):
    """
    Find rows that match the given criteria.
    :param rows_as_dicts: List of dictionaries representing the rows.
    :param criteria_dict: A dictionary where each key-value pair is a condition to match.
    :return: A list of dictionaries (rows) that match all criteria.
    """
    matching_rows = []
    for row in rows_as_dicts:
        if all(row.get(key) == value for key, value in criteria_dict.items()):
            matching_rows.append(row)
    return matching_rows
def append_new_data(df,new_data):
    # No matching row, append new data as a new row
    new_index = len(df)
    for key, value in new_data.items():
        if key in df.columns and value not in [None, '']:
            df.at[new_index, key] = value
    return df
def get_first_for_each(df,headers,queries,new_file_path=None):
    new_file_path = new_file_path or get_new_excel_path(df)
    df=get_df(df)
    headers = get_expected_headers(df,headers).values()
    # Filter the DataFrame to only include rows with ZIP codes that are in the 'zips' list
    df=filter_and_deduplicate_df(df, headers, queries, dedup_columns=None)
    safe_excel_save(df,new_file_path)
    # Save the filtered and deduplicated DataFrame to a new Excel file
    return new_file_path
def get_column_headers(df):
    df=read_excel_input(df)
    return df.columns.tolist()
def get_column_values(df,heads=10):
    df=read_excel_input(df)
    return {col: df[col].head(heads).dropna().tolist() for col in df.columns}
def get_row_as_list(df,index=0):
    df=get_df(df)
    if get_row_number(df)>index:
        return df.loc[index].astype(str).tolist()
def get_row_number(df):
    df=get_df(df)
    return len(df)


def read_excel_as_dicts(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, engine='openpyxl')
    # Convert each row to a dictionary with column headers as keys
    rows_as_dicts = df.to_dict(orient='records')
    return rows_as_dicts

def convert_to_dict(data, format_type='list_of_dicts'):
    # Load data from Excel if the input is not a DataFrame
    if isinstance(data, str):
        try:
            data = pd.read_excel(data)
        except Exception as e:
            return f"Failed to load Excel file: {e}"
    
    if not isinstance(data, pd.DataFrame):
        return "Input must be an Excel file path or a DataFrame"

    # Convert DataFrame to dictionary
    if format_type == 'list_of_dicts':
        return data.to_dict(orient='records')
    elif format_type == 'dict_of_lists':
        return data.to_dict(orient='list')
    elif format_type == 'nested_dicts':
        # This assumes the first column is the key, adjust logic as needed
        key = data.columns[0]
        return {row[key]: row.to_dict() for index, row in data.drop(columns=[key]).iterrows()}
    else:
        return "Invalid format type specified"


def find_matching_rows(rows_as_dicts, criteria_dict):
    """
    Find rows that match the given criteria.
    :param rows_as_dicts: List of dictionaries representing the rows.
    :param criteria_dict: A dictionary where each key-value pair is a condition to match.
    :return: A list of dictionaries (rows) that match all criteria.
    """
    matching_rows = []
    for row in rows_as_dicts:
        if all(row.get(key) == value for key, value in criteria_dict.items()):
            matching_rows.append(row)
    return matching_rows
def append_new_data(df,new_data):
    # No matching row, append new data as a new row
    new_index = len(df)
    for key, value in new_data.items():
        if key in df.columns and value not in [None, '']:
            df.at[new_index, key] = value
    return df
def append_unique_to_excels(df,new_data,file_path=None, search_column= None, search_value=None,print_it=False):
    """
    Updates or appends data in an Excel file based on the contents of a specified column.

    Parameters:
    - file_path: str, the path including filename of the Excel file.
    - new_data: dict, data to update or append.
    - search_column: str, the name of the column to search for the search_value.
    - search_value: str, the value to search for in the search_column.
    """
    # If the Excel file doesn't exist, create a new DataFrame from new_data and save it
    if file_path and not os.path.isfile(file_path):
        new_df = pd.DataFrame([new_data])
        safe_excel_save(new_df,file_path,index=False, engine='openpyxl')
        print("Excel file created with new data.")
        return new_df
    if isinstance(df,str) and os.path.isfile(df):
        file_path=df
    # Load the existing DataFrame from the Excel file
    df = get_df(df)

    # Standardize data types for existing columns based on new_data types
    for key, value in new_data.items():
        if key in df.columns:
            # Determine desired column data type based on the new value's type
            if isinstance(value, str):
                df[key] = df[key].astype(str, errors='ignore')
            elif isinstance(value, float):
                df[key] = df[key].astype(float, errors='ignore')
            elif isinstance(value, int):
                # If value is integer but fits in float without losing precision, consider converting to float
                # This is because pandas uses NaN (a float value) to represent missing data for numeric columns
                df[key] = df[key].astype(float, errors='ignore')

    # Find if there's a row that matches the search_value in search_column
    match = None
    if search_column and search_value:
        match = df[df[search_column] == search_value]
        if not match.empty:
            # There's a matching row, update only if new data is not None or ''
            row_index = match.index[0]  # Assuming the first match should be updated
            for key, value in new_data.items():
                if key in df.columns:
                    # Check if value is not None or empty string
                    if value not in [None, '']:
                        # Determine the column data type
                        column_dtype = df[key].dtype
                        
                        # If the column is of integer type but the value is a string that represents an integer,
                        # explicitly cast the value to int. Otherwise, keep it as string.
                        if pd.api.types.is_integer_dtype(column_dtype) and value.isdigit():
                            df.at[row_index, key] = int(value)
                        elif pd.api.types.is_float_dtype(column_dtype) and is_number(value):
                            # For floating-point numbers
                            df.at[row_index, key] = float(value)
                        else:
                            # For other types, including cases where casting to int/float isn't appropriate
                            df.at[row_index, key] = value
            if print_it:
                print(f"Updated row where {search_column} matches {search_value}.")
        else:
            append_new_data(df,new_data)
    else:
        append_new_data(df,new_data)
        if print_it:
            print(f"Appended new data since no matching {search_column} found for {search_value}.")

    # Save the updated DataFrame back to the Excel file
    if file_path:
        safe_excel_save(df,file_path)
    return df
def append_unique_to_excel(file_path, new_data_list, key_columns=None):
    """
    Append new data to an Excel file, ensuring no duplicate rows are added.
    
    :param file_path: Path to the Excel file.
    :param new_data_list: List of dictionaries representing the rows to add.
    :param key_columns: Optional list of columns to use for identifying duplicates. If None, all columns are used.
    """
    # Convert new_data_list to DataFrame and convert all columns to string type
    new_data_df = pd.DataFrame(new_data_list).astype(str)
    
    if not os.path.isfile(file_path):
        # If the Excel file doesn't exist, save the new DataFrame directly
        new_data_df.to_excel(file_path, index=False, engine='openpyxl')
    else:
        # If the Excel file exists, load it and append the new data
        existing_df = pd.read_excel(file_path, engine='openpyxl').astype(str)

        # Concatenate the existing data with the new data
        combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        
        # Drop duplicates. If key_columns is not specified, all columns are considered
        if key_columns is None:
            combined_df = combined_df.drop_duplicates(keep='first')
        else:
            combined_df = combined_df.drop_duplicates(subset=key_columns, keep='first')
        
        # Save the updated DataFrame back to the Excel file
        combined_df.to_excel(file_path, index=False, engine='openpyxl')


def get_last_hours(excel_file_path,data,hours=1):
    # Load the Excel file
    df = pd.read_excel(excel_file_path, engine='openpyxl')

    # Ensure the Timestamp column is in datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Get the current time
    
    hours_ago = get_hourls_ago(hours=hours)
    filtered_df = df[df['Timestamp'] > hours_ago]

    # Define the directory structure
    daily_folder_name = get_daily_output()
    hourly_folder_name = now.strftime('%H') + '00'  # This will create a folder like '1400' for 2 PM
    base_directory = os.path.dirname(excel_file_path)


    daily_folder_path = get_daily_folder(base_directory)
    hourly_folder_path = get_hourly_folder(daily_folder_path)
    
    # Define the new Excel file path
    file_name = os.path.basename(excel_file_path)
    new_excel_file_path = os.path.join(hourly_folder_path, file_name)

    # Save the filtered DataFrame to the new Excel file path
    filtered_df.to_excel(new_excel_file_path, engine='openpyxl', index=False)

    return new_excel_file_path  # Optional: return the path of the saved file

def get_timely_LT(original_excel_file_path,output_excel_file_path=None,hours=1):
    if output_excel_file_path == None:
        output_excel_file_path = f'last_{hours}_hours.xlsx'  # Define your output file path
    # Load the Excel file into a DataFrame
    
    if not os.path.isfile(file_path):
        new_df = pd.DataFrame([new_data])
        # Convert all columns to string type to avoid dtype incompatibility
        new_df = new_df.astype(str)
        new_df.to_excel(file_path, index=False, engine='openpyxl')
        return
    df = pd.read_excel(file_path)
    # Ensure the 'Timestamp' column is in datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Define your desired timeframe based on the current time
    end_date = datetime.now()  # Use datetime.utcnow() if the times are in UTC
    start_date = end_date - timedelta(hours=1)
    
    # Filter the DataFrame for rows where the date falls within the specified timeframe
    filtered_df = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] < end_date)]
    
    # Output filtered DataFrame to Excel
    filtered_df.to_excel(output_excel_file_path, index=False)
    
    return output_excel_file_path  # Assuming get_formatted_string() formats the path
def find_matching_row_path(excel_file_path="",datas={},rows_as_dicts={}):
    if excel_file_path and os.path.isfile(excel_file_path):
        rows_as_dicts = read_excel_as_dicts(excel_file_path)
    if rows_as_dicts:
        matching_rows = find_matching_rows(rows_as_dicts, datas)
        if matching_rows:
            matching_rows = matching_rows[0]
        return matching_rows
def filter_query_from_column(excel_file_path,column_header,include_only,new_file_path=None):
    # Load the Excel file
    df = pd.read_excel(excel_file_path)

    # Filter the DataFrame
    filtered_df = df[pd.isnull(df[column_header])]

    # Save the filtered DataFrame back to a new Excel file
    filtered_df.to_excel(new_file_path or excel_file_path, index=False)
def get_last_hour_from_excel(file_path, raw_datas):
    raw_datas = get_raw_data(file_path,before=get_hours_ago()+(60*60),after=get_hours_ago())
    return get_timely_LT(file_path,new_data=raw_datas)

def get_last_day_from_excel(file_path, raw_datas):
    return get_timely_LT(file_path,before=get_day_time_stamp(),after=get_day_ago_time_stamp())

def create_full_excel(file_path, raw_datas):
    # raw_datas is expected to be a list of dictionaries
    append_unique_to_excel(file_path, raw_datas)
    
def append_lt_excels():
    excel_lt_directory_dir = create_full_excel(get_raw_lt_excel_file_path(),get_raw_lt_data())
    get_last_hour_from_excel(get_hourly_raw_lt_excel_file_path(), get_raw_lt_data())
    create_full_excel(get_daily_raw_lt_excel_file_path(),get_raw_lt_data())
    
def append_dnc_excels():
    excel_dnc_directory_dir = create_full_excel(get_raw_dnc_excel_file_path(),get_raw_dnc_data())
    get_last_hour_from_excel(get_hourly_raw_dnc_excel_file_path(), get_raw_dnc_data())
    create_full_excel(get_daily_raw_dnc_excel_file_path(), get_raw_dnc_data())

#filter_query_from_column("new_excel_file.xlsx","Addr2",None,new_file_path="new_clean_excel_file.xlsx")
