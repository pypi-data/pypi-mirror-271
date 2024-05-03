import os
from abstract_security.envy_it import *
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
def get_from_polygon_data(data):
    coordinates = str(data).split('POLYGON ((')[1].split('))')[0].replace('(','').replace(')','').split(', ')
    for i,coordinate in enumerate(coordinates):
        coordinate_spl = coordinate.split(' ')
        coordinates[i]=[float(coordinate_spl[1]),float(coordinate_spl[0])]
    return coordinates
def get_cell_value(gdf, column_header, row_index=1):
    """
    Retrieves the value from a specified cell in the GeoDataFrame.
    
    :param gdf: GeoDataFrame or filepath to the shapefile.
    :param column_header: The header of the column from which to retrieve the value.
    :param row_index: The index of the row from which to retrieve the value.
    :return: The value located at the specified column and row.
    """
    gdf = get_gdf(gdf)
    # Check if the column header is in the GeoDataFrame
    if column_header not in gdf.columns:
        raise ValueError(f"The column header '{column_header}' does not exist in the GeoDataFrame.")
    
    # Check if the row index is within the bounds of the GeoDataFrame
    if not (0 <= int(row_index) < len(gdf)):
        raise ValueError(f"The row index {row_index} is out of bounds for the GeoDataFrame.")
    
    # Retrieve and return the value from the specified cell
    return gdf.iloc[row_index][column_header]
def get_gdf(obj):
    # Check if the input is a string, which we assume to be a file path
    if isinstance(obj, str) and os.path.isfile(obj):
        # Read the shapefile into a GeoDataFrame
        gdf = gpd.read_file(obj)
    # Check if the input is already a GeoDataFrame
    elif isinstance(obj, gpd.GeoDataFrame):
        gdf = obj
    else:
        raise ValueError("The input should be a GeoDataFrame or a valid file path to a shapefile.")
    return gdf
class polygon_manager:
    def __init__(self,default_boundary=None,default_index=1):
        self.poly_track = []
        self.default_boundary = default_boundary or self.get_default_boundary_polygon_file_path()
        self.get_boundary_polygon(boundary_polygon=self.default_boundary,index=default_index)
    def get_default_boundary_polygon_file_path(self):
         return get_env_value(key="boundary_polygon")
    def get_boundary_polygon(self,boundary_polygon=None,index=1):
        boundary_polygon=boundary_polygon or get_default_boundary_polygon_file_path()
        if isinstance(boundary_polygon,list):
            return boundary_polygon
        if isinstance(boundary_polygon,str) and os.path.isfile(boundary_polygon):
            search_result = self.polygon_file_search(boundary_polygon)
            if search_result:
                return search_result['polygon']
            ext = os.path.splitext(boundary_polygon)[-1]
            poly_dict={"file_path":boundary_polygon}
            if ext == '.dbf':
                poly_dict['gdf']=get_gdf(boundary_polygon)
                poly_dict['index']=index
                poly_dict['geometry'] = get_cell_value(poly_dict['gdf'], 'geometry', row_index=poly_dict['index'])
                poly_dict['polygon'] = get_from_polygon_data(poly_dict['geometry'])
            elif ext == '.xlsx':
                poly_dict['polygon'] = read_excel_as_dicts(boundary_polygon)
            else:
                for i,dist in enumerate(boundary_polygon):
                    boundary_polygon[i] = list(dist.values())
                poly_dict['polygon'] = boundary_polygon
            self.poly_track.append(poly_dict)
            return poly_dict['polygon']
    def polygon_file_search(self,polygon_file_path):
        for poly_data in self.poly_track:
            if poly_data.get('file_path') == polygon_file_path:
                return poly_data

poly_mgr = polygon_manager()
def get_bp(bp,index=1):
    bp = bp or poly_mgr.get_default_boundary_polygon_file_path()
    return poly_mgr.get_boundary_polygon(bp,index=index)

def find_row_with_matching_cell(excel_datas,search_column='',search_value=''):
    matching_row = [excel_data for excel_data in excel_datas if isinstance(excel_data,dict) and excel_data.get(search_column) == search_value]
    if matching_row and isinstance(matching_row,list) and len(matching_row)>0:
        return matching_row[0]
    return {}
def get_itter(list_obj,target):
    for i,string in enumerate(list_obj):
        if string == target:
            return i
    return None
def safe_itter_get(list_obj,i):
    if len(list_obj)>i:
        return list_obj[i]
def get_gdf(obj):
    # Check if the input is a string, which we assume to be a file path
    if isinstance(obj, str) and os.path.isfile(obj):
        # Read the shapefile into a GeoDataFrame
        gdf = gpd.read_file(obj)
    # Check if the input is already a GeoDataFrame
    elif isinstance(obj, gpd.GeoDataFrame):
        gdf = obj
    else:
        raise ValueError("The input should be a GeoDataFrame or a valid file path to a shapefile.")
    return gdf
def get_headers(filepath_or_gdf):
    # Return the column headers
    return get_gdf(filepath_or_gdf).columns.tolist()
def get_int_from_column(obj,column):
    headers = get_headers(obj)
    return get_itter(headers,column)
def get_column_from_int(obj,i):
    headers = get_headers(obj)
    column = safe_itter_get(headers,i)
    # Return the column headers
    return column
def get_all_in_row(gdf,i=1):
    gdf = get_gdf(gdf)
    headers = get_headers(gdf)
    for column in headers:
        input(column)
        cell_value = get_cell_value(gdf, column, i)
        input(cell_value)

def read_gdp_file(file_path):
    return gpd.read_file(file_path)


