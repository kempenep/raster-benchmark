# -*- coding: utf-8 -*-
import os
import timeit
import pyjeo as pj

wd = os.getcwd()
catalog = os.path.join('data', 'LC08_L1TP_190024_20200418_20200822_02_T1')
rasters = os.listdir(catalog)
rasters = [r for r in rasters if r.endswith(('.TIF'))]
rasters = [os.path.join(wd, catalog, r) for r in rasters]

### raster stack
band_names = ["B1", "B10", "B11", "B2", "B3", "B4", "B5", "B6", "B7", "B9"]

jim = pj.Jim()
for i, path in enumerate(rasters):
    jim.geometry.stackBand(pj.Jim(path))
jim.properties.setDimension(band_names, 'band')

### write

t_list = [None] * 10
stack_file = 'stack.TIF'
for i in range(10):
    tic = timeit.default_timer()

    jim.io.write(stac_file, co = ['COMPRESS=LZW'])

    toc = timeit.default_timer()
    t_list[i] = round(toc - tic, 2)


df = {'task': ['write'] * 10, 'package': ['pyjeo'] * 10, 'time': t_list}
df = pd.DataFrame.from_dict(df)
if not os.path.isdir('results'): os.mkdir('results')
savepath = os.path.join('results', 'write-pyjeo.csv')
df.to_csv(savepath, index = False, decimal = ',', sep = ';')
