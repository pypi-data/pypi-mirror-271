
from habitatsuitability.tools.fun import *
from osgeo import osr
import os
from habitatsuitability.config import par_dict_abreviations
from habitatsuitability.hsi_raster.hsi_raster_fun import get_hsi_curve, combine_hsi_rasters, get_hsi_raster
from habitatsuitability.hsi_raster.raster import Raster
from habitatsuitability.tools import binning
from habitatsuitability.tools.bio_evaluation_fun import bin_resolution_check, threshold_list_creator, \
    calculate_threshold_pixels, forage_ratio_test, random_forage_test, habitat_quality_from_threshold_generator,mann_u_test
from habitatsuitability.tools.bio_tools import directory_creator, csv_import_coords_to_list, catagorize_CHSI
from habitatsuitability.tools.bioverification_fun import tif_coordinate_value_csv, random_data_hsi
from habitatsuitability.tools.input_data_testing import wetted_area_coordinate_check
from habitatsuitability.tools.visualization import hsi_forage_plot, fr_conf_interval_hsi_forage_plot, \
    binning_hsi_forage_plot

from habitatsuitability.tools import input_data_testing

@cache
@log_actions
def run_hsi_raster_generator(parameters = None,parameter_hsicurve_json_dict=None,tifs_dictionary = None,
         hsi_output_dir= os.path.abspath("") + "\\hsi_raster_tifs\\",par_dict=None):
    """
        Generates HSI rasters for each parameter using parameter tif input,json_hsc_curve.Then calclates a combined HSI raster with the HSI raster.
        :param parameters: list of string input parameters ex. ["velocity","depth","substrate"]
        :param parameter_hsicurve_json_dict: dictionary of parameters and their corresponing json files which contain the parameter hsi curve
        ex. paramaterhsicurve_json_dict = dict(velocity=velocity_hsicurve_json_path,depth=depth_hsicurve_json_path,substrate=substrate_hsicurve_json_path,other=other_hsicurve_json_path)
        :param tifs_dictionary: dictionary of parameters with their corresponding tif path
        ex. tif_inputs = {"velocity": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_velocity.tif",
                  "depth": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_depth.tif",
                  "substrate": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_substrate.tif"}
        :param hsi_output_dir: output directory for hsi tifs (default hsi_output_dir= os.path.abspath("") + "\\hsi_raster_tifs\\")
        :param par_dict = dictionary of parameters and the abreviations optional input otherwise it is generated with parameter list and config  par_dict_abreviations
                ex.par_dict = {"velocity": "u","depth": "h","substrate": "d","other": "o"}
        :return: None
        *function modified from Sebastian Schwindt's https://github.com/Ecohydraulics/Exercise-geco
        """
    directory_creator(hsi_output_dir)  # creates directory if missing for hsi output
    if par_dict is None: # par dict creation if missing
        par_dict={} #establish dictionary
        for p in range(len(parameters)):
            par_dict[parameters[p]]=par_dict_abreviations[p]

    print("Starting the creation of the hsi raster")
    hsi_curve = get_hsi_curve(par_dict,parameter_hsicurve_json_dict , parameters=parameters)
    # create HSI rasters for all parameters considered and store the Raster objects in a dictionary
    eco_rasters = {}
    for par in parameters:
        hsi_par_curve = [list(hsi_curve[par][par_dict[par]]),
                         list(hsi_curve[par]["HSI"])]
        print("Creating Hsi Tif for {} parameter".format(par))
        print(hsi_curve[par])
        eco_rasters.update({par: get_hsi_raster(tif_dir=tifs_dictionary[par], hsi_curve=hsi_par_curve)})
        eco_rasters[par].save(hsi_output_dir + "hsi_%s.tif" % par)
# get and save chsi raster
    chsi_raster = combine_hsi_rasters(raster_list=list(eco_rasters.values()),
                                      method="geometric_mean")
    print("Made combined raster")

    chsi_raster.save(hsi_output_dir + "chsi.tif")
    return 0

def run_bioverifier_observation_chsi_analysis(
        # mandatory
        observation_coordinate_csv_path=None,
        # optional
        chsi_tif_path=os.path.abspath("") + "\\hsi_raster_tifs\\chsi.tif",
        depth_tif_path=os.path.abspath("") + "\\hsi_raster_tifs\\hsi_depth.tif",

        random_datasets_quantity=10000,
        random_data_directory=os.path.abspath("") + "\\randomdatasets\\",
        observation_chsi_directory=os.path.abspath("") + "\\observation_chsi\\",
        wetted_area_test=True,
        coordinate_to_chsi_raster_value=True,
        generate_random_data_sets=True
):
    """
           Finds chsi value for each observation location,filters valid points, generates randomly picked datasets
           #mandatory
           :param observation_coordinate_csv_path:input path csv file of xy coordinates observation data
           #optional changes
           :param chsi_tif_path:input path tif file of chsi tif file. Saved by default from create_hsi-raster in (default:chsi_tif_path=os.path.abspath("") + "\\hsi_raster_tifs\\chsi.tif",)
           :param depth_tif_path:input path tif file of depth tif file. Saved by default from create_hsi-raster in (default:depth_tif_path=os.path.abspath("") + "\\hsi_raster_tifs\\hsi_depth.tif",)
           :param random_datasets_quantity:quantity of randomdatasets to be created (default:random_datasets_quantity=10000)
           :param random_data_directory:output directory path of random datasets(default:random_data_directory=os.path.abspath("") + "\\randomdatasets\\")
           :param observation_chsi_directory:output directory path of chsi observation data(default:observation_chsi_directory=os.path.abspath("") + "\\observation_chsi\\")
           :param wetted_area_test:bool enable wetted area test to include only valid observation coordinates (default:wetted_area_test=True)
           :param coordinate_to_chsi_raster_value:bool finds chsi value for each xy observation coordinate (default:coordinate_to_chsi_raster_value=True)
           :param generate_random_data_sets:bool generates random data sets(default:generate_random_data_sets=True)
           :return: None
           """

    if observation_coordinate_csv_path is None or not os.path.isfile(observation_coordinate_csv_path):
        print("Error:Function needs valid input for observation_coordinate_csv_path."
              "Either none selected or path is wrong")
        return 1

    # Random Data
    directory_creator(random_data_directory)  # creates directory if missing

    # Import of Coordinates
    print("Starting the bioverification")
    coordinates = csv_import_coords_to_list(observation_coordinate_csv_path)

    if wetted_area_test:

        new_coordinate_csv_path, coordinates_list = wetted_area_coordinate_check(observation_coordinate_csv_path,
                                                                                 chsi_input_tif=chsi_tif_path,
                                                                                 depth_input_tif=depth_tif_path,
                                                                                 raster_variable="chsi+depth")
        coordinates_list.insert(0, headerXY)
        coordinates = coordinates_list

    else:
        new_coordinate_csv_path = observation_coordinate_csv_path
    data_points_quantity = len(coordinates)

    if coordinate_to_chsi_raster_value:
        directory_creator(observation_chsi_directory)  # creates directory if missing
        chsi_output_csv_path = os.path.join(observation_chsi_directory, "observation_chsi_data.csv")
        tif_coordinate_value_csv(chsi_tif_path, new_coordinate_csv_path, chsi_output_csv_path)
        print("Creating bio dataset in", chsi_output_csv_path)

    if generate_random_data_sets:
        # clean folder of potential other runs
        filelist = [f for f in os.listdir(random_data_directory) if f.endswith(".csv")]
        for f in filelist:
            os.remove(os.path.join(random_data_directory, f))

        print("Removed {} csv files in {}".format(len(filelist), random_data_directory))
        # create new set of random data sets
        random_data_hsi(random_data_directory, chsi_tif_path, random_datasets_quantity, data_points_quantity,
                        depth_tif_path=depth_tif_path)
    print("Completed bioverification and the creation of randomly picked data sets")
    return 0
def run_hsi_habitat_evaluation(
         bio_data_path=os.path.abspath("")+"\\observation_chsi\\observation_chsi_data.csv",
         bin_resolution=None,
         bootstrap_binning=True,
         custom_binning=False,
         custom_bin_thresholds=None,
         print_random_forage_results =True,
         agglomerativeclustering_binning=False,
         resolution_check=True,
         random_data_hsi_directory=os.path.abspath("") + "\\randomdatasets\\",
         chsi_raster_path = os.path.abspath("") + "\\hsi_raster_tifs\\chsi.tif",
         results_analysis_directory=os.path.abspath("") + "\\binning_analysis_results\\"):
    """
    Habitat binning uses the chsi and observation data to distinguish habitat quality in the form of chis thresholds bootstrap binning,
    generates habitat quality tifs, creates results analysis,and gives flexibility for custom binning options.

    #mandatory inputs
    :param bin_resolution: float decimal number giving the resolution bin size for the bootstrap binning analysis
    decimal options (0.25,0.2,0.1,0.05,0.04,0.02,0.01) needs to be a factor of 1, larger bin has less uncertainity but has lower resolution

    #optional inputs (if bioverifier_observation_chsi_analysis and hsi_raster_generator outputs were run on default
    :param bio_data_path: path of chsi observation data (default:random_data_hsi_directory=os.path.abspath("") + "\\randomdatasets\\")
    :param chsi_raster_path:path of chsi tif raster (default:chsi_raster_path = os.path.abspath("") + "\\hsi_raster_tifs\\chsi.tif")
    :param random_data_hsi_directory:directory path for random hsi data (default:random_data_hsi_directory=os.path.abspath("") + "\\randomdatasets\\")
    :param custom_bin_thresholds: list of custom bin thresholds ex.[.25,.5,.75,1], only generates if custom_binning is true

    #optional outputs
    :param results_analysis_directory:
    #options
    :param bootstrap_binning:bool enables bootstrap binning  (default:True)
    :param custom_binning:bool enables custom binning instead of bootstrap binning, if true needs custom_bin_threshold input (default:False)
    :param resolution_check:bool enables check of resolution prior to analysis and corrects if resolution bin size below minimum threshold(default:True)
    :param print_random_forage_results:bool creates csv file with random datasets forage ratio results  (default:True)
    :param agglomerativeclustering_binning:bool enables further categorization of bootstrap binning thresholds with agglomerative clustering results in 5 bins(default:False)

    """
    #inputs
    directory_creator(results_analysis_directory)  # creates directory if missing

    # forage ratio inputs
    csv_results_path = os.path.join(results_analysis_directory, "observation_fr_results.csv")
    csv_randforagedata_path = os.path.join(results_analysis_directory, "randomdata_fr_results.csv")

    # habitat outputs
    habitat_tif_output_path=os.path.join(results_analysis_directory, "evaluated_habitat.tif")
    habitat_results_path = os.path.join(results_analysis_directory, "evaluated_habitat_results.csv")

    # resolution check
    print("Starting the bio data evaluation")
    if resolution_check:
        bin_size = bin_resolution_check(bin_interval=bin_resolution,observation_data_path=bio_data_path)
    else:
        bin_size=bin_resolution
    bin_thresholds = threshold_list_creator(bin_size= bin_size)

    area_input = calculate_threshold_pixels(chsi_raster_path, bin_thresholds) #creates list of area per bin
    # biodata
    mann_u_stats = mann_u_test(bio_data_path,random_data_hsi_directory)
    print(mann_u_stats)

    bio_forage_ratio_results = forage_ratio_test(chsi_raster_path, bin_thresholds, bio_data_path, area=area_input)
    hsi_forage_plot(bin_thresholds,bio_forage_ratio_results)
    hsi_forage_plot(bin_thresholds, bio_forage_ratio_results,regression_formular=True)
    bio_forage_ratio_results.insert(0, "BioData")
    print("Forage Ratio results:", bio_forage_ratio_results)


    # Binning
    if custom_binning:
        hsi_fr_thresholds = custom_bin_thresholds
        habitat_rand_fr_results, habitat_rand_random_fr_stats, habitat_rand_fr_thresholds, habitat_rand_median_std = random_forage_test(
            random_data_hsi_directory,chsi_raster_path, hsi_fr_thresholds)

    elif bootstrap_binning:
        # Random Data
        fr_results, random_fr_stats, fr_thresholds,median_std = random_forage_test(random_data_hsi_directory, chsi_raster_path, bin_thresholds, area_input=area_input,plot_gaussian=True)
        print(random_fr_stats)
        if median_std > 0.4:
            resolution_warning="Warning:Resolution binsize of {} is too small. Run bio_evaluation again and choose a bigger number!".format(bin_size)
            print(resolution_warning)
        else:
            resolution_warning = None
        # Printing to csv
        print("bin", bin_thresholds)
        print("forage", bio_forage_ratio_results)
        fr_conf_interval_hsi_forage_plot(bin_thresholds, bio_forage_ratio_results[1:], fr_thresholds)
        myFile = open(csv_results_path, 'w')
        writer = csv.writer(myFile)

        header3 = ["Entries", "Thresholds Bins Forage Ratios"]
        writer.writerow(header3)
        header2 = ["Name"] + bin_thresholds[1:]
        writer.writerow(header2)
        writer.writerow(bio_forage_ratio_results)
        writer.writerow(["Random Forage Ratio Stats"])
        for stats in random_fr_stats:
            writer.writerow(stats)

        writer.writerow(["Mann Whintey U Test Results"])
        try:
            writer.writerow(["pvalue", mann_u_stats[1]])
        except:
            writer.writerow(["pvalue", "Error"])
        myFile.close()

        if print_random_forage_results:
            myFile = open(csv_randforagedata_path, 'w')
            writer = csv.writer(myFile)
            header3 = ["Entries", "Thresholds Bins Forage Ratios"]
            writer.writerow(header3)
            header2 = ["Name"] + bin_thresholds[1:]
            writer.writerow(header2)
            for item in fr_results:
                writer.writerow(item)
            myFile.close()
        print("Binning 3 bins using bootstrapping")
        hsi_fr_thresholds = binning.fr_to_hsi(bio_forage_ratio_results[1:], bin_thresholds, fr_thresholds)
        print("Bootstrap Binning was successful, hsi boundaries of neutral habitat is ", hsi_fr_thresholds)
        binning_hsi_forage_plot(bin_thresholds, bio_forage_ratio_results[1:], hsi_fr_thresholds)
        binning_hsi_forage_plot(bin_thresholds, bio_forage_ratio_results[1:], hsi_fr_thresholds,habitat=True)
        if agglomerativeclustering_binning:
            print("Agglomerative clustering not available, may show up in future release")
            #print("Further binning into 5 using agglomerative clustering")
            #binning.algomerative_clustering_5bins(hsi_fr_thresholds, bio_forage_ratio_results[1:], bin_thresholds)
        #hsi_fr_thresholds.append(1)
        #print("Evaluated habitat thresholds are",hsi_fr_thresholds)

    else:
        print("Error: No binning method selected")
        return 1
    # generates a habitat tif
    bin_habitat_output_path = habitat_tif_output_path.replace(".tif", "_{}bins.tif".format(len(hsi_fr_thresholds)))
    habitat_quality_from_threshold_generator(chsi_raster_path, bin_habitat_output_path, hsi_fr_thresholds)
    # generates habitat information
    habitat_area = calculate_threshold_pixels(chsi_raster_path, hsi_fr_thresholds, convert_to_area=True)
    habitat_utilization = catagorize_CHSI(hsi_fr_thresholds, bio_data_path=bio_data_path)
    habitat_forage = forage_ratio_test(chsi_raster_path, hsi_fr_thresholds, bio_data_path, area=habitat_area)

    # retrieve units
    chsi_raster = Raster(chsi_raster_path)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(chsi_raster.epsg)
    area_unit = "square %s" % str(srs.GetLinearUnitsName())
    #printing csv
    area=[]
    thresholds=[]
    ut=[]
    bin_habitat_results_path = habitat_results_path.replace(".csv", "_{}bins.csv".format(len(hsi_fr_thresholds)))
    myFile = open(bin_habitat_results_path, 'w')
    writer = csv.writer(myFile)
    writer.writerow(["Habitat Evaluation Results"])
    if resolution_warning is not None:
        writer.writerow([resolution_warning])

    for i in habitat_area:
        thresholds.append(i[0])
        area.append(i[1])
    writer.writerow(["Thresholds"]+thresholds)
    writer.writerow(["Area {}".format(area_unit)]+area)
    for u in habitat_utilization:
        ut.append(u[1])
    writer.writerow(["Redds"]+ut)
    writer.writerow(["Bin Forage Ratio"] + habitat_forage)
    writer.writerow(["Random Generated data Forage Ratio Stats "])
    if custom_binning:
        for stats in habitat_rand_random_fr_stats:
            writer.writerow(stats)

    myFile.close()
    print("Created csv for Habitat Evaluation Results in,",bin_habitat_results_path)

    print("Completed bio_evaulation and habitat binning")
    return 0

def run_complete_hsi_habitat_binning(
        # mandatory inputs
        tifs_dictionary=None,  # Input test +create_hsi_raster
        parameters=None,  # create_hsi_raster
        depth_tif_path=None,
        parameter_hsicurve_json_dict=None,
        observation_coordinate_csv_path=None,  # bioverification

        bin_resolution=None,  # bio_evaluation
        # create_chsi_raster optional
        par_dict=None,
        hsi_output_dir=os.path.abspath("") + "\\hsi_raster_tifs\\",
        random_datasets_quantity=10000,
        # bioverification optional
        chsi_tif_path=os.path.abspath("") + "\\hsi_raster_tifs\\chsi.tif",  # used in bio_evaluation

        random_data_directory=os.path.abspath("") + "\\randomdatasets\\",  # used in bio_evaluation
        observation_chsi_directory=os.path.abspath("") + "\\observation_chsi\\",  # used in bio_evaluation
        wetted_area_test=True,
        coordinate_to_chsi_raster_value=True,
        generate_random_data_sets=True,

        # bio_evaluation optional
        bootstrap_binning=True,
        custom_binning=False, custom_bin_thresholds=None,
        print_random_forage_results=True,
        agglomerativeclustering_binning=False,
        resolution_check=True,
        random_data_hsi_directory=os.path.abspath("") + "\\randomdatasets\\",

        results_analysis_directory=os.path.abspath("") + "\\binning_analysis_results\\"):
    """
        Runs the complete process for CHSI creation,observation data evaluation,random data generation,Habitat Binning, and analysis. Runs raster_input_check,hsi_raster_generator
        ,bioverifier_observation_chsi_analysis, and habitat_binning in order.


         #mandatory inputs
            #hsi_raster_generator
                :param parameters: list of string input parameters ex. ["velocity","depth","substrate"]
                :param parameter_hsicurve_json_dict: dictionary of parameters and their corresponding json files which contain the parameter hsi curve
                ex. parameter_hsicurve_json_dict = dict(velocity=velocity_hsicurve_json_path,depth=depth_hsicurve_json_path,substrate=substrate_hsicurve_json_path,other=other_hsicurve_json_path)
                :param tifs_dictionary: dictionary of parameters with their corresponding tif path
                ex. tif_inputs = {"velocity": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_velocity.tif",
                "depth": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_depth.tif",
                "substrate": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_substrate.tif"}

            #bioverifier_observation_chsi_analysis
                :param observation_coordinate_csv_path:input path csv file of xy coordinates observation data

            #habitat_binning
                :param bin_resolution: float decimal number giving the resolution bin size for the bootstrap binning analysis
                decimal options (0.25,0.2,0.1,0.05,0.04,0.02,0.01) needs to be a factor of 1, larger bin has less uncertainity but has lower resolution

        #optional changes
            #hsi_raster_generator
                :param hsi_output_dir: output directory for hsi tifs (default hsi_output_dir= os.path.abspath("") + "\\hsi_raster_tifs\\")
            :param par_dict = dictionary of parameters and the abreviations optional input otherwise it is generated with parameter list and config  par_dict_abreviations
                ex.par_dict = {"velocity": "u","depth": "h","substrate": "d","other": "o"}

            #bioverifier_observation_chsi_analysis

               #optional input changes for bioverifier_observation_chsi_analysis
               :param chsi_tif_path:input path tif file of chsi tif file. Saved by default from create_hsi-raster in (default:chsi_tif_path=os.path.abspath("") + "\\hsi_raster_tifs\\chsi.tif",)
               :param depth_tif_path:input path tif file of depth tif file. Saved by default from create_hsi-raster in (default:depth_tif_path=os.path.abspath("") + "\\hsi_raster_tifs\\hsi_depth.tif",)
               :param random_datasets_quantity:quantity of randomdatasets to be created (default:random_datasets_quantity=10000)
               :param random_data_directory:output directory path of random datasets(default:random_data_directory=os.path.abspath("") + "\\randomdatasets\\")

               #optional output changes bioverifier_observation_chsi_analysis
               :param observation_chsi_directory:output directory path of chsi observation data(default:observation_chsi_directory=os.path.abspath("") + "\\observation_chsi\\")

                #options for bioverifier_observation_chsi_analysis
                :param wetted_area_test:bool enable wetted area test to include only valid observation coordinates (default:wetted_area_test=True)
                :param coordinate_to_chsi_raster_value:bool finds chsi value for each xy observation coordinate (default:coordinate_to_chsi_raster_value=True)
                :param generate_random_data_sets:bool generates random data sets(default:generate_random_data_sets=True)
            #habitat_binning
                #optional input changes for habitat_binning
                    :param random_data_hsi_directory: (default:)
                    :param custom_bin_thresholds: list of custom bin thresholds ex.[.25,.5,.75,1], only generates if custom_binning is true
                #optional outputs for habitat_binning
                    :param results_analysis_directory:
                #options for habitat_binning
                    :param bootstrap_binning:bool enables bootstrap binning  (default:True)
                    :param custom_binning:bool enables custom binning instead of bootstrap binning, if true needs custom_bin_threshold input (default:False)
                    :param resolution_check:bool enables check of resolution prior to analysis and corrects if resolution bin size below minimum threshold(default:True)
                    :param print_random_forage_results:bool creates csv file with random datasets forage ratio results  (default:True)
                    :param agglomerativeclustering_binning:bool enables further categorization of bootstrap binning thresholds with agglomerative clustering results in 5 bins(default:False)
    """
    # input testing of tif files to confirm same geo information (size, origin,extent...)
    input_data_testing.raster_input_check(tifs_dictionary)

    # Creates hsi parameter and combined hsi tif files
    run_hsi_raster_generator(parameters=parameters, hsi_output_dir=hsi_output_dir,
                                        tifs_dictionary=tifs_dictionary,
                                        parameter_hsicurve_json_dict=parameter_hsicurve_json_dict,par_dict=par_dict)
    # Converts location data into hsi values by comparing coordinates with hsi raster and creats randomly picked data sets
    run_bioverifier_observation_chsi_analysis(
        observation_coordinate_csv_path=observation_coordinate_csv_path,
        random_datasets_quantity=random_datasets_quantity,
        chsi_tif_path=chsi_tif_path,
        depth_tif_path=depth_tif_path,
        random_data_directory=random_data_directory,
        observation_chsi_directory=observation_chsi_directory,
        wetted_area_test=wetted_area_test,
        coordinate_to_chsi_raster_value=coordinate_to_chsi_raster_value,
        generate_random_data_sets=generate_random_data_sets)

    # evaluating perfomance of hsi raster versus bio coordinate data and creating hsi habitat bins
    run_hsi_habitat_evaluation(
                                   bin_resolution=bin_resolution, bootstrap_binning=bootstrap_binning,
                                   custom_binning=custom_binning, custom_bin_thresholds=custom_bin_thresholds,
                                   print_random_forage_results=print_random_forage_results,
                                   agglomerativeclustering_binning=agglomerativeclustering_binning,
                                   resolution_check=resolution_check,
                                   random_data_hsi_directory=random_data_hsi_directory,
                                   chsi_raster_path=chsi_tif_path,
                                   results_analysis_directory=results_analysis_directory)
    return 0


if __name__ == '__main__':
    # define global variables for the main() function

    t0 = perf_counter()
    # json files path
    velocity_hsicurve_json_path = os.path.abspath("") + "\\input_files\\fish_hsc_json\\_example_velocity_hsi.json"
    depth_hsicurve_json_path = os.path.abspath("") + "\\input_files\\fish_hsc_json\\_example_depth_hsi.json"
    substrate_hsicurve_json_path = os.path.abspath("") + "\\input_files\\fish_hsc_json\\_example_substrate_hsi.json"
    other_hsicurve_json_path = None
    parameter_hsicurve_json_dict = dict(
        velocity=velocity_hsicurve_json_path,
        depth=depth_hsicurve_json_path,
        substrate=substrate_hsicurve_json_path,
        other=other_hsicurve_json_path)
    tif_inputs = {"velocity": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_velocity.tif",
                  "depth": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_depth.tif",
                  "substrate": os.path.abspath("") + "\\input_files\\input_parameter_tifs\\example_substrate.tif"}

    run_complete_hsi_habitat_binning(tifs_dictionary=tif_inputs,  # Input test +create_hsi_raster
                                     parameters=["velocity", "depth", "substrate"],  # create_hsi_raster
                                     parameter_hsicurve_json_dict=parameter_hsicurve_json_dict,
                                     # bioverification
                                     depth_tif_path=tif_inputs["depth"],
                                     observation_coordinate_csv_path=os.path.abspath(
                                         "") + "\\input_files\\input_bioverification_files\\example_observation_data.csv",

                                     bin_resolution=0.04,random_datasets_quantity=1000)  # habitat_binning)
    t1 = perf_counter()
    print("Time elapsed: " + str(t1 - t0))
