'''
Date: 2021-07-23 00:35:09
LastEditors: LIULIJING
LastEditTime: 2021-07-29 14:24:06
'''

import logging
from osgeo import gdal
from utils.convertmodis_gdal import createMosaicGDAL
from utils.utilities import parse_save_url
import os

def get_output_ext(path:str):
    ds = gdal.Open(path)
    return ds.GetGeoTransform(), (ds.RasterXSize, ds.RasterYSize), ds.GetProjection()

def parse_tiles_by_day(list_of_tiles:list) -> dict:
    list_of_tiles = [file for file in list_of_tiles if not file.endswith('xml')]
    all_crates = {}
    for l in list_of_tiles:
        date_code, save_path = parse_save_url(l)
        all_crates.setdefault(date_code, set())
        all_crates[date_code].add(save_path)
    return all_crates

def stitch_and_reproject(file_list:list, output_path:str, product:str, date:str,
                        reproject_options:tuple, subset = '1 0 0 0 0 0 0 0 0', 
                        outformat='GTiff', save_stitch_file = True
                        ):
    gt_out, (xSize, ySize), dstSRS = reproject_options
    if not os.path.exists(output_path):
        raise FileNotFoundError("output directory not exists.")

    extent = [gt_out[0], gt_out[3]+gt_out[5]*ySize,
            gt_out[0]+gt_out[1]*xSize, gt_out[3]]
    modisOgg = createMosaicGDAL(file_list, subset, outformat=outformat)
    output_path = os.path.join(output_path, product)
    os.makedirs(output_path, exist_ok=True)
    stitch_path = "{outdir}/stitch.{fi}.{da}.tif".format(
        outdir=output_path, fi = product, da = date)
    if not os.path.exists(stitch_path):
        try:
            modisOgg.run(stitch_path)
        except Exception as exec:
            logging.error("ERROR run STITCHING file {}!".format(file_list))
            raise Exception(str(exec))

    src_ds = gdal.Open(stitch_path)
    outputname = "{outdir}/cut.{fi}.{da}.tif".format(
        outdir=output_path, fi = product, da= date)
    extent = [gt_out[0], gt_out[3]+gt_out[5]*ySize,
        gt_out[0]+gt_out[1]*xSize, gt_out[3]]
    if not os.path.exists(outputname):
        try:
            gdal.Warp(outputname, 
                    src_ds, 
                    dstSRS=dstSRS, 
                    xRes=gt_out[1], 
                    yRes=gt_out[5],
                    creationOptions = ['COMPRESS=LZW'],
                    outputBounds=extent, 
                    format = outformat)
            src_ds = None
        except Exception as exec:
            logging.error("ERROR run REPROJECT file {} to {}!".format(stitch_path, output_path))
            raise Exception(str(exec))
    if not save_stitch_file:
        os.remove(stitch_path)