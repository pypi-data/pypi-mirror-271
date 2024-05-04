import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import .geopandas as gpd
def get_highest(highest,lowest,comp):
    if None in highest or None in lowest:
        highest= comp
        lowest =  comp
        return highest,lowest
    if (float(highest[0]) < float(comp[0])) and (float(highest[1]) < float(comp[1])):
        highest = comp
    elif (float(lowest[0]) > float(comp[0])) and (float(lowest[1]) > float(comp[1])):
        lowest = comp
    return highest,lowest
# Example: Loading your GeoDataFrame correctly set with its current CRS
gdf = gpd.read_file("/home/gamook/Documents/pythonScripts/modules/abstract_distances/src/abstract_distances/ZipCodes_3170383398510875265(1)/California_Zip_Codes.dbf")  # assuming the file is loaded directly
gdf.crs = 'epsg:32619'  # Replace 32619 with your actual EPSG code of the original data

# Transform the coordinates to WGS84 (Lat, Long)
gdf = gdf.to_crs('epsg:4326')  # Correct usage of EPSG code


# Example data loading
for i,row in gpd.points_from_xy:
    pass
# Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(
    gdf, geometry=gpd.points_from_xy(gdf.geometry.y, gdf.geometry.x))
input(gdf)
# Define the latitude and longitude to compare
latitude_cutoff = 33.953350
longitude_cutoff = -117.396156, 

# Filter GeoDataFrame based on latitude and longitude
filtered_gdf = gdf[(gdf.geometry.y < latitude_cutoff) & (gdf.geometry.x < longitude_cutoff)]

print(filtered_gdf)
