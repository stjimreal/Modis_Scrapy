'''
Date: 2021-03-26 19:20:38
LastEditors: LIULIJING
LastEditTime: 2021-07-25 00:58:01
'''

short_name = ['MOD10A1', 'MYD10A1'] # product name
version = '6' # version: 5 6 61
data_center = 'NSIDC_ECS' # NSIDC_ECS, LAADS, LPDAAC_ECS, ...
time_start = '2021-07-19T00:00:00Z' # begin date, try not changing the format
time_end = '2021-07-20T05:48:52Z' # end date
bounding_box = '62,26,105.0018536,46.000389' # W, S, E, N or other GeoJson format
polygon = '' # GeoJson Format
filename_filter = '' # Regular Expression

meta_proxy = 'socks5://127.0.0.1:7890'
OUTPUT_PATH = '/Volumes/jimDisk/MODIS_NSIDC_DATABASE_Debug'
# 
#  OUTPUT_PATH = 'I:\\\\MODIS_NSIDC_DATABASE_Debug'
# 
