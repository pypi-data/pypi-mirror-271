try:
    import os
    import logging
    import random
    import shutil
    import string
except ImportError:
    print("ERROR: Cannot import basic Python libraries.")

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("ERROR: Cannot import SciPy libraries.")

try:
    import json
except ImportError:
    print("ERROR: Cannot import json package.")

try:
    import scipy.stats as stats
except ImportError:
    print("ERROR: Cannot import scipy package.")

try:
    import bisect
except ImportError:
    print("ERROR: Cannot import bisect package.")

try:
    import csv
except ImportError:
    print("ERROR: Cannot import csv package.")

try:
    import statistics
except ImportError:
    print("ERROR: Cannot import statistics package.")

try:
    from osgeo import gdal
except ImportError:
    print("ERROR: Cannot import osgeo gdal package.")

try:
    from time import perf_counter
except ImportError:
    print("ERROR: Cannot import time package.")
try:
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.neighbors import kneighbors_graph
except ImportError:
    print("ERROR: Cannot import sklearn package.")

try:
    import matplotlib.pyplot as plt
except:
    print("ERROR: Cannot import matplotlip package.")

nan_value = -99.0  # do not change to zero due to zero being an acceptable value for hsi


# parameter dict used for reading json

par_dict_abreviations = ["u", "h", "d", "o1", "o2", "o3", "o4", "o5"]

cache_folder = os.path.abspath("") + "\\__cache__\\"

header = ["Value", "X", "Y"]
headerXY = ["X", "Y"]

# *Config modified from Sebastian Schwindt's https://github.com/Ecohydraulics/Exercise-geco
