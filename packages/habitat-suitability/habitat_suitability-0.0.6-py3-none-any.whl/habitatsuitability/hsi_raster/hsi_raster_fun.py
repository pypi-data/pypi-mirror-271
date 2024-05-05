from habitatsuitability.tools.fun import *
from .raster_hsi import HSIRaster, Raster



def combine_hsi_rasters(raster_list, method="geometric_mean"):
    """
    Combine HSI rasters into combined Habitat Suitability Index (cHSI) Rasters
    :param raster_list: list of HSIRasters (HSI)
    :param method: string (default="geometric_mean", alt="product)
    :return HSIRaster: contains float pixel values
    *Function origin from Sebastian Schwindt's https://github.com/Ecohydraulics/Exercise-geco
    """
    if method is "geometric_mean":
        power = 1.0 / float(raster_list.__len__())


    else:
        # supposedly method is "product"
        power = 1.0

    chsi_raster = Raster(cache_folder + "chsi_start.tif",
                         raster_array=np.ones(raster_list[0].array.shape),
                         epsg=raster_list[0].epsg,
                         geo_info=raster_list[0].geo_transformation)
    for ras in raster_list:
        print(ras.array.shape)
        chsi_raster = chsi_raster * ras

    return chsi_raster ** power


def get_hsi_curve(par_dict, json_dict, parameters):
    """
    Retrieve HSI curves from fish json file for a specific life stage and a set of parameters
    :param json_dict: dictionary of strings (directory and name of json file containing HSI curves)
    :param parameters: list (may contain "velocity", "depth", and/or "grain_size")
    :param par_dict:dictionary of parameters list and their abreviation
    :return curve_data: dictionary of life stage specific HSI curves as pd.DataFrame for requested parameters;
                        for example: curve_data["velocity"]["HSI"]
*Function origin from Sebastian Schwindt's https://github.com/Ecohydraulics/Exercise-geco
    """

    curve_data = {}
    # iterate through parameter list (e.g., ["velocity", "depth"])
    for par in parameters:
        # create a void list to store pairs of parameter-HSI values as nested lists
        json_file = json_dict[par]
        print("file_location", json_file)
        # instantiate output dictionary
        file_info = read_json(json_file)
        # instantiate output dictionary
        par_pairs = []
        # iterate through the length of parameter-HSI curves in the JSON file
        for i in range(0, file_info.__len__()):
            # if the parameter is not empty (i.e., __len__ > 0), append the parameter-HSI (e.g., [u_value, HSI_value]) pair as nested list
            if str(file_info[i]["HSI"]).__len__() > 0:
                try:

                    # only append data pairs if both parameter and HSI are numeric (floats)
                    par_pairs.append([float(file_info[i][par_dict[par]]),
                                      float(file_info[i]["HSI"])])

                except ValueError:
                    logging.warning("Invalid HSI curve entry for {0} in parameter {1}.".format(par))
        # add the nested parameter pair list as pandas DataFrame to the curve_data dictionary
        curve_data.update({par: pd.DataFrame(par_pairs, columns=[par_dict[par], "HSI"])})
    return curve_data


def get_hsi_raster(tif_dir, hsi_curve):
    """
    Calculate and return Habitat Suitability Index Rasters
    :param tif_dir: string of directory and name of  a tif file with parameter values (e.g., depth in m)
    :param hsi_curve: nested list of [[par-values], [HSI-values]], where
                            [par-values] (e.g., velocity values) and
                            [HSI-values] must have the same length.
    :return hsi_raster: Raster with HSI values
    *Function origin from Sebastian Schwindt's https://github.com/Ecohydraulics/Exercise-geco
    """
    return HSIRaster(tif_dir, hsi_curve)

# *Modified from Sebastian Schwindt's https://github.com/Ecohydraulics/Exercise-geco
