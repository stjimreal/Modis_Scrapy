'''
Date: 2021-03-26 19:20:38
LastEditors: LIULIJING
LastEditTime: 2021-07-25 00:58:01
'''

short_name = ['MOD10A1'] # product name (DO NOT FORGET the square brackets)
version = '6' # version: 5 6 61
data_center = 'NSIDC_ECS' # NSIDC_ECS, LAADS, LPDAAC_ECS, ...
time_start = '2021-06-09T00:00:00Z' # begin date, try not changing the format
time_end = '2021-06-12T05:48:52Z' # end date
bounding_box = '62,26,105.0018536,46.000389' # W, S, E, N or other GeoJson format
polygon = '' # GeoJson Format
filename_filter = '' # Regular Expression

meta_proxy = 'socks5://127.0.0.1:7890'
OUTPUT_PATH = '/Users/jimlau/MODIS_NSIDC_DATABASE_Debug'
# 
#  OUTPUT_PATH = 'I:\\MODIS_NSIDC_DATABASE_Debug'
# 

# stitch&reproject options, affect when turned on.
turn_on_stitch_and_reproject = 'Y'      # 'yes' or 'Yes' or 'N' or 'No' or 'no' 
save_julian_date = 'N'                  # save as julia date OR normal date, only for NSIDC_ECS, 
                                        # unexpected behavior may arise with other DAACs
output_type = 'GTiff'                   # HDF4 GTiff NetCDF... see GDAL driver for more 
output_file_mosaic_path = '/Users/jimlau/MODIS_NSIDC_DATABASE_Debug/FSC_TP_DEM.tif'
# Raster file for decide extents(boundings, resolutions)
subset = '1 0 0 0 0 0 0 0 0 0 0 0'      # select channels
ALL_DONE_FILE_OUTPUT_PATH = '/Users/jimlau/MODIS_NSIDC_DATABASE_Debug/output'    

# !!! Important
# file persist options 
# which worked in case the REPROJECT OPTIONS were turned on.
# 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧
save_stitch_file = 'N'
save_origin_file = 'Y'
