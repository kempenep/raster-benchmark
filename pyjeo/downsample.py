# -*- coding: utf-8 -*-
import os
import timeit
import pandas as pd
import pyjeo as pj

wd = os.getcwd()
catalog = os.path.join('data', 'LC08_L1TP_190024_20200418_20200822_02_T1')
rasters = os.listdir(catalog)
rasters = [r for r in rasters if r.endswith(('.TIF'))]
rasters = [os.path.join(wd, catalog, r) for r in rasters]

### raster stack
band_names = ["B1", "B10", "B11", "B2", "B3", "B4", "B5", "B6", "B7", "B9"]

ras = []
jim = pj.Jim()
for i, path in enumerate(rasters):
    jim.geometry.stackBand(pj.Jim(path))
jim.properties.setDimension(band_names, 'band')

### crop

# minx, miny, maxx, maxy
area = [598500, 5682100, 727500, 5781000]
# ulx, uly, lrx, lry
bbox = [598500, 5781000, 727500, 5682100]

t_list = [None] * 10
for i in range(10):
    tic = timeit.default_timer()

    pj.geometry.warp(jim, t_srs = 'epsg:32633', dx = 90, dy = 90, resample = 'average')

    toc = timeit.default_timer()
    t_list[i] = round(toc - tic, 2)


df = {'task': ['downsample'] * 10, 'package': ['pyjeo'] * 10,
      'time': t_list}
df = pd.DataFrame.from_dict(df)
if not os.path.isdir('results'): os.mkdir('results')
savepath = os.path.join('results', 'downsample-pyjeo.csv')
df.to_csv(savepath, index = False, decimal = ',', sep = ';')
