from abstract_distances.geo_pandas import *
# import osgeo.ogr as a convenience
from osgeo.gdal import deprecation_warn
deprecation_warn('ogr')

from osgeo.ogr import *
#import osgeo.osr as a convenience
from osgeo.gdal import deprecation_warn
deprecation_warn('osr')

from osgeo.osr import *
from osgeo import gdal
from osgeo import ogr, osr
import geopandas as gpd
def transform_and_print_coords(geom):
    for point in geom.exterior.coords:
        ogr_point = ogr.Geometry(ogr.wkbPoint)
        ogr_point.AddPoint(point[0], point[1])
        ogr_point.Transform(transform)
        lon, lat = ogr_point.GetX(), ogr_point.GetY()
        print("Longitude:", lon, "Latitude:", lat)
# Define the projection string for the California Teale Albers projection
proj_string = """PROJCS["WGS_1984_California_Teale_Albers_FtUS",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Foot_US",0.3048006096012192]]"""
from osgeo import ogr, osr, gdal
ca_zip_dbf = "/home/gamook/Documents/pythonScripts/modules/abstract_distances/src/shape_data/clalifornia_shape_file/zip_codes/California_Zip_Codes.dbf"
ca_zip_gdf = get_gdf(ca_zip_dbf)
source_crs = osr.SpatialReference()
source_crs.ImportFromWkt(proj_string)
target_crs = osr.SpatialReference()
target_crs.ImportFromEPSG(4326)  # WGS 84
transform = osr.CoordinateTransformation(source_crs, target_crs)
for polygon in ca_zip_gdf['geometry']:
    if polygon.geom_type == 'MultiPolygon':
        for geom in polygon.geoms:  # Iterate over each polygon in a MultiPolygon
            transform_and_print_coords(geom)
    elif polygon.geom_type == 'Polygon':
        transform_and_print_coords(polygon)
