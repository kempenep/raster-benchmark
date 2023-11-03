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

jim = pj.Jim(rasters[5])
jim.geometry.stackBand(pj.Jim(rasters[6]))
jim.properties.setDimension(['red', 'nir'], 'band')
#todo: check if needed
jim.pixops.convert('GDT_Float32')

### extract

t_list = [None] * 10
for i in range(10):
    tic = timeit.default_timer()

    ndvi = pj.pixops.NDVI(jim, red = 'red', nir = 'nir')

    toc = timeit.default_timer()
    t_list[i] = round(toc - tic, 2)


df = {'task': ['ndvi'] * 10, 'package': ['pyjeo'] * 10, 'time': t_list}
df = pd.DataFrame.from_dict(df)
if not os.path.isdir('results'): os.mkdir('results')
savepath = os.path.join('results', 'ndvi-pyjeo.csv')
df.to_csv(savepath, index = False, decimal = ',', sep = ';')
