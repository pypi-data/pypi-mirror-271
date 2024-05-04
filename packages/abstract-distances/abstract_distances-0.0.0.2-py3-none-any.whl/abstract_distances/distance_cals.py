import numpy as np
import pandas as pd
from .geo_pandas import *
from .excel_module import *
from .word_compare import *
from abstract_utilities import *
import math,re,requests, httpx, asyncio
from math import sin, cos, asin, atan2, radians, degrees, pi,atan2, sqrt
from openlocationcode import openlocationcode as olc
def get_default_google_api_key():
    return get_env_value(key="google_maps_api_key")
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    distance = 3959 * c  # Earth's radius in kilometers
    return distance
def get_closest_boudary(D_lat, D_lon, boundary_polygon=None):
    boundary_polygon = get_bp(boundary_polygon)
    # Assuming read_excel_as_dicts is meant to read Excel file and convert it into a list of dictionaries
    # Assuming each dict has 'lat' and 'lon' keys
    closest_point = None
    shortest_distance = float('inf')
    for i,dist in enumerate(boundary_polygon):
        lat, lon = dist[0], dist[1]

        distance = haversine(D_lat, D_lon, lat, lon)
        if distance < shortest_distance:
            shortest_distance = distance
            closest_point = (lat, lon)
    
    return shortest_distance, closest_point
def get_closest_exact_boudary(D_lat, D_lon, boundary_polygon=None,api_key=None):
    api_key = api_key or get_default_google_api_key()
    boundary_polygon = get_bp(boundary_polygon)
    shortest,coordinates = get_closest_boudary(D_lat, D_lon, boundary_polygon)
    address_2 = get_address_from_latlngs(coordinates[0],coordinates[1])
    return get_lat_long(address_2,api_key)
def is_point_inside_polygon(point_lat, point_lon, polygon):
    """
    Determine if a point is inside a given polygon or not.
    
    Polygon is a list of (latitude, longitude) tuples, and point is defined by (point_lat, point_lon).
    """
    num = len(polygon)
    inside = False
    x, y = point_lon, point_lat
    if None not in [x,y]:
  
        p1x, p1y = polygon[0]
        for i in range(num+1):
            p2x, p2y = polygon[i % num]
            
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y

    return inside
def get_lat_long(address,boundary_polygon=None, api_key=None):
    api_key =api_key or get_default_google_api_key()
    boundary_polygon = get_bp(boundary_polygon)
    
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None, None
    else:
        return None, None
def get_from_distance_response(json_response):
    text_finds = get_any_value(json_response, 'text')
    if text_finds:
        text_find_list = make_list(text_finds)
        if text_find_list and isinstance(text_find_list, list) and len(text_find_list) > 0:
            text_find_list = text_find_list[0]
        if text_find_list and isinstance(text_find_list, str):
            return text_find_list.split(' ')[0]
    return text_finds
async def calculateDistance(origin, destination,travelMode = 'DRIVING',api_key=None,return_all = False):
    api_key =api_key or get_default_google_api_key()
    base_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&travelMode={travelMode}&units=imperial&key={api_key}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url)
        
        if response.status_code != 200:
            # Handle error or retry as needed
            print(response.text)
            return None
        print(response.text)
        response = response.json()
        # Your existing logic to extract distance
        if return_all = False:
            response = get_from_distance_response(response)
        return response

def get_address_header_association(headers_js,df,index,spec_headers=False):
    print(headers_js)
    if not isinstance(headers_js,dict):
        headers_js = get_closest_headers(headers_js)
    if isinstance(headers_js,dict):
        address = f"{df[headers_js['address']].loc[index]} {df[headers_js['city']].loc[index]} {df[headers_js['state']].loc[index]} {df[headers_js['zip']].loc[index]}"
        if spec_headers and isinstance(spec_headers,list):
            address=""
            for spec_header in spec_headers:
                spec_header = headers_js.get(spec_header)
                if spec_header:                    
                    address+=f"{df[spec_header].loc[index]} "
            address = eatAll(address,' ')
        return address
async def calculate_distances(new_data, headers_js, api_key=None):
    api_key =api_key or get_default_google_api_key()
    distance = new_data.get('distance')
    address = None
    # Check if distance is 'NaN', None, an empty string, or zero (as string or number)
    if distance is None or distance == "" or isinstance(distance, str) and not distance.isdigit():
        address = get_address_header_association(headers_js, new_data)
        distance = await get_distance_calculation(address,boundary_polygon)
    elif isinstance(distance, (int, float)):  # Check if it is a number (int or float)
        if distance == 0 or math.isnan(distance):  # Explicit check for 0 and NaN
            address = get_address_header_association(headers_js, new_data)
            distance = await get_distance_calculation(address,boundary_polygon)
    elif isinstance(distance, str) and distance.isdigit():
        if int(distance) == 0:  # Additional check if the string number is zero
            address = get_address_header_association(headers_js, new_data)
            distance = await get_distance_calculation(address,boundary_polygon)

    return distance  # Return the processed or retrieved distance
async def get_distance_for_excel_row(df,file_path=None,row_itter=0,distance=None,row_data=None,address=None,headers_js=None,search_column=None,boundary_polygon=None, search_value=None):
    boundary_polygon = get_bp(boundary_polygon)
    df=get_df(df or file_path,make_excel=row_data)
    if row_data==None:
       row_data = get_row_as_list(df,index=row_itter) or {}
    if address == None:
        address = get_address_header_association(headers_js,df,row_itter)
    if distance == None:
        distance = await get_distance_calculation(address, boundary_polygon)
    row_data['distance'] = distance or 0
    return append_unique_to_excels(df,file_path = file_path, new_data = row_data,search_column=search_column, search_value=search_value)
async def get_distance_calculation(address, boundary_polygon=None,api_key=None):
    boundary_polygon = get_bp(boundary_polygon)
    if isinstance(address,str):
        dest_latitude,dest_longitude = get_lat_long(address,boundary_polygon)
    in_city_limit = is_point_inside_polygon(dest_latitude, dest_longitude, boundary_polygon)
    if in_city_limit:
        return 0
    coordinates = get_closest_exact_boudary(dest_latitude,dest_longitude,boundary_polygon)
    src_latitude,src_longitude= coordinates[0],coordinates[1]
    distance = await calculateDistance(f"{src_latitude} {src_longitude}",f"{dest_latitude} {dest_longitude}",travelMode="DRIVING")
    return distance
async def add_distance_calculatuions_to_excel_data(excel_file_path,boundary_polygon=None,append=False,new_excel_path="new_excel_file.xlsx"):
    boundary_polygon = get_bp(boundary_polygon)
    api_key = api_key or get_default_google_api_key()
    if not os.path.isfile(excel_file_path):
        return
    all_distance = safe_read_from_json("all_distances.json")
    headers_js = get_closest_headers(excel_file_path)
    main_df = get_df(excel_file_path)
    for index, row in main_df.iterrows():
            zip_now = str(row.get('ZIP'))
            all_dst = all_distance.get(zip_now)
            if not is_number(all_dst):
                
                all_distance[zip_now]=await get_distance_calculation(get_address_header_association(headers_js,main_df,index),boundary_polygon=boundary_polygon)
            if is_number(all_distance[zip_now]):
                row['distance'] = all_distance[zip_now]
            else:
                dist = main_df.at[index, 'distance']
                zip_now = str(row.get('ZIP'))
                all_dst = all_distance.get(zip_now)
                if is_number(all_dst):
                    row['distance'] = str(all_dst)
                
                    
                elif str(dist) != str(all_dst) or not is_number(all_dst) or pd.to_numeric(dist, errors='coerce') == 0 or dist == 'nan' or pd.isna(dist) or not is_number(dist):
                    address = get_address_header_association(headers_js,main_df,index)
                    row['distance']=await get_distance_calculation(address, boundary_polygon=boundary_polygon)
                    all_distance[zip_now] = row['distance']
                    safe_dump_to_json(data=all_distance,file_path=-'all_distances.js')
            main_df = append_unique_to_excels(main_df, new_data = row,search_column=headers_js['external'], search_value=row.get(headers_js['external']),print_it=False)
            
            safe_excel_save(main_df,new_excel_path)
def get_address_from_latlngs(lat, lng, api_key=None):
    api_key = api_key or get_default_google_api_key()
    # Endpoint URL
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # Parameters for the API request
    params = {
        "latlng": f"{lat},{lng}",
        "key": api_key
    }
    
    # Send request and get response data
    response = requests.get(base_url, params=params)
    
    # Convert response to JSON format

    results = response.json()
    
    # Check if any results were returned
    if results["status"] == "OK":
        # Return the formatted address of the first result
        address = results["results"][0]["formatted_address"]
        return f"{address.split(' ')[0].split('+')[0]} {' '.join(address.split(' ')[1:])}"
    else:
        # Return error message if no results found
        return "No address found for this latitude and longitude"

def convert_to_str_lalng(obj):
    if isinstance(obj,str):
        obj = obj.replace(',',' ').split(' ')
        return f"{obj[0]} {obj[-1]}"
    for ty in [set,list,tuple]:
        if isinstance(obj,ty):
            return f"{obj[0]} {obj[-1]}"
    return obj
def decode_plus_code(plus_code):
    decoded = olc.decode(plus_code)
    return (decoded.latitudeCenter, decoded.longitudeCenter)




