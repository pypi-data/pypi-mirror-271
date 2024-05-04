import asyncio,json,shutil
from .distance_cals import *
def get_abs_dir():
    return os.path.dirname(os.path.abspath(__file__))
def get_json_data(file_path):
    if not os.path.isfile(file_path):
        safe_dump_to_file(data={},file_path=file_path)
    return safe_read_from_json(file_path)
def get_all_distance_data(data_file_path=None):
    data_file_path = data_file_path or get_all_distance_file_path()
    return get_json_data(file_path=data_file_path)
def save_all_distances(data,data_file_path=None):
    safe_dump_to_file(data=data, file_path=data_file_path or get_all_distance_file_path())
def get_all_distance_file_path():
    return os.path.join(get_abs_dir(),"all_distances.json")
def update_excel_to_column_values(df,update_header,value_header,values_js):
    df = get_df(df)
    df[update_header] = df[value_header].apply(lambda x: values_js.get(str(x)))
    return df
def get_all_excels_dir():
    excel_dir = os.path.join(get_abs_dir(),'all_excels')
    os.makedirs(excel_dir,exist_ok=True)
    return excel_dir
def get_original_excels_dir():
    curr_original_dir = os.path.join(get_all_excels_dir(),'originals')
    os.makedirs(curr_original_dir,exist_ok=True)
    return curr_original_dir
def get_filtered_excels_dir():
    curr_filtered_dir = os.path.join(get_all_excels_dir(),'filtered')
    os.makedirs(curr_filtered_dir,exist_ok=True)
    return curr_filtered_dir
def get_original_ext_dir(ext):
    original_ext_dir = os.path.join(get_original_excels_dir(),eatAll(ext,['.']))
    os.makedirs(original_ext_dir,exist_ok=True)
    return original_ext_dir
def get_filtered_ext_dir(ext):
    filtered_ext_dir = os.path.join(get_filtered_excels_dir(),eatAll(ext,['.']))
    os.makedirs(filtered_ext_dir,exist_ok=True)
    return filtered_ext_dir
def get_original_filepath(baseName):
    directory = os.path.dirname(baseName)
    if os.path.isdir(directory):
        baseName= os.path.basename(baseName)
    ext=os.path.splitext(baseName)
    return os.path.join(get_original_ext_dir(ext[-1]),baseName)
def get_filtered_filepath(baseName):
    directory = os.path.dirname(baseName)
    if os.path.isdir(directory):
        baseName= os.path.basename(baseName)
    ext=os.path.splitext(baseName)
    return os.path.join(get_filtered_ext_dir(ext[-1]),baseName)
def get_file_associations(file_path):
    original_file_path = get_original_filepath(file_path)
    filtered_file_path = get_filtered_filepath(file_path)
    if file_path != original_file_path and os.path.isfile(file_path):
        shutil.copy(file_path,original_file_path)
    return original_file_path,filtered_file_path
def check_if_none_val(value):
    if value in [0,'null',None,'None','nan','NaN','0.0',0.0]:
        return True
    return False
async def update_distances(df,update_header,value_header,values_js,data_file_path=None,boundary_polygon=None,api_key=None):
    """Asynchronously update distances in the DataFrame."""
    df = get_df(df)
    boundary_polygon = get_bp(boundary_polygon)
    headers_js = get_closest_headers(df,value_header,update_header)
    values_js = values_js or get_all_distance_data(data_file_path=data_file_path)
    for index, row in df.iterrows():
        # Check if the current cell in update_header column is not a number
        
        if not is_number(row[update_header]) or str(row[update_header]) in ['nan','NaN','None',None,0,'0.0']:
            # Use the value in the value_header column as the key for the json_dict
            key = df.at[index, value_header]
            value = values_js.get(str(key))
            # Check if the key exists in json_dict and if its value can be converted to a number
            if value and is_number(value) and (float(value) != float(0) or str(row[update_header]) in ['nan','NaN','None',None,0,'0.0']):
                # Update the cell with the value from json_dict
                df.at[index, update_header] = value
            else:
                # Mark the cell for update
                if key != 'nan':
                    values_js[key] = await get_distance_calculation(get_address_header_association(headers_js, df, index),boundary_polygon,api_key)
                    if check_if_none_val(values_js[key]):
                        for i in range(1,3):
                            values_js[key] = await get_distance_calculation(get_address_header_association(headers_js, df, index,['city','state','zip'][-i:]),boundary_polygon,api_key)
                            if not check_if_none_val(values_js[key]):
                                break
                    df.at[index, update_header] = values_js[key]
                    save_all_distances(data=values_js,data_file_path=data_file_path)
    # Write the distances back to file once all updates are completed
    return df,values_js
async def update_excel(df,update_header,value_header,values_js,data_file_path=None):
    df = get_df(df)
    values_js = values_js or get_all_distance_data(data_file_path=data_file_path)
    df = add_or_update_headers(df,'distance')
    values_js = convert_values(values_js,[float,str],elim=True)
    values_js = convert_keys(values_js,[float,int,str])
    df = convert_column(df,'ZIP',[float,int,str])
    df = convert_column(df,'distance',[float,str])
    df,values_js = await update_distances(df,update_header,value_header,values_js,data_file_path=data_file_path)
    return df,values_js
def convert_column(df,column,ty):
    df = get_df(df)
    ty= make_list(ty)
    df = add_or_update_headers(df,column)
    for typ in ty:
        try:
            df[column] = df[column].astype(typ)
        except:
            pass
    return df
def convert_keys(values_js,ty):
    new_js = {}
    ty= make_list(ty)
    for key,values in values_js.items():
        if key not in [None,'None','nan','NaN']:
            for typ in ty:
                key = typ(key)
        new_js[key]=values
    return new_js
def convert_values(values_js,ty,elim=False):
    new_js = {}
    ty= make_list(ty)
    for key,values in values_js.items():
        if values not in [None,'None','nan','NaN']:
            for typ in ty:
                
                values = typ(values)
            new_js[key]=values
    return new_js
def convert_all(df,values_js,column,ty):
    ty= make_list(ty)
    for typ in ty:
        df = convert_column(df,column,typ)
    return df,values_js
def update_all_values_js(df,value_header,values_js={},data_file_path=None):
    data_file_path = data_file_path or get_all_distance_file_path()
    original_file_path,filtered_file_path = get_file_associations(df)
    df = get_df(df)
    values_js = values_js or get_all_distance_data(data_file_path=data_file_path)

    values_js = convert_values(values_js,[float,str],elim=True)
    values_js = convert_keys(values_js,[float,int,str])
    df = convert_column(df,'ZIP',[float,int,str])
    df = convert_column(df,'distance',[str])
    needs_update = ~df[value_header].apply(lambda x: is_number(values_js.get(str(x))))
    update_indices = df[needs_update].index
    for i in update_indices:
        values_js[df['ZIP'][i]] = df['distance'][i]
    safe_excel_save(df,filtered_file_path)
    save_all_distances(data=values_js,data_file_path=data_file_path)
    
async def tryoit(directory=None,all_distance_path=None,destination_directory=None,ext='xlsx'):
    save_paths = []
    all_distance_path = all_distance_path or get_all_distance_file_path()
    directory = directory or get_original_ext_dir(ext)
    if os.path.isdir(directory):
        directory = os.listdir(directory)
    else:
        directory = make_list(directory)
    for excel_file_path in directory:
        values_js = get_json_data(all_distance_path)
        if not os.path.isfile(excel_file_path):
            excel_file_path = os.path.join(directory,excel_file_path)
        original_file_path,filtered_file_path = get_file_associations(excel_file_path)
        df,values_js= await update_excel(original_file_path,'distance','ZIP',values_js=values_js,data_file_path=all_distance_path)
        safe_dump_to_file(data=values_js, file_path=all_distance_path)
        safe_excel_save(df,filtered_file_path)
        save_paths.append(filtered_file_path)
        if destination_directory:
            move_file = os.path.join(destination_directory,os.path.basename(filtered_file_path))
            shutil.move(filtered_file_path,move_file)
            save_paths[-1]=move_file
    return save_paths
def associate_distances(directory=None,all_distance_path=None,destination_directory=None,ext='xlsx'):
    return asyncio.run(tryoit(directory=directory,all_distance_path=all_distance_path,destination_directory=destination_directory,ext=ext))
