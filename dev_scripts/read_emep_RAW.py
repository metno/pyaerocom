import os
import iris

base_dir = "/lustre/storeB/project/fou/kl/emep/ModelRuns/2016_REPORTING/Trend_runs/3245.trends"

if not os.path.isdir(base_dir):
    raise IOError("Path not found...")

ftype = ".nc"
opt_str_mask = "day"
var = "AOD_550nm"

paths = []
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(ftype) and opt_str_mask in file:
            paths.append(os.path.join(root, file))
                
for path in paths:
    print(path)


c = iris.Constraint(cube_func=lambda c: c.var_name == var)
cube = iris.load_cube(paths[0], c)

print(cube.var_name)

import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt

cube.attributes["projection"]

