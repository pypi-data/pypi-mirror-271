
from .bio_tools import *
from habitatsuitability.hsi_raster.raster import Raster

from .visualization import gaussian_dist_random_graph
from .fun import *
from habitatsuitability.hsi_raster.flusstools_geotools_functions import create_raster


def threshold_list_creator(bins_count=None, decimals=2, zero=True, bin_size=None):
    """
    Creates a list of upper limits (included) of bin thresholds
        :param bins_count: int number of Bins between 0 and 1
        :param decimals: number of decimal points of the bin threshold (default decimal=2 ex. 0.01)
        :param zero: boolean if true adds zero bin at the beginning
        :param bin_size: float of size of bin
        :return bin_thresholds: list of threshold values for bins example bin_thresholds = [0, 0.25, .5, .75, 1]
    """
    if bins_count == None and bin_size == None:
        print("Error:function requires bins_count or bin_size input ")
        return 1
    bin_thresholds = [] # establish variable
    if zero: # if true adds zero as first list variable
        bin_thresholds.append(0)
    if bin_size is None:
        bin_size = 1 / bins_count # establishes step size
    if bins_count is None:
        bins_count = int(1/bin_size)
    # loop to create requested quantity of thresholds
    for i in range(bins_count):
        bin_thresholds.append(round(bin_size * (1 + i), decimals))  # adds threshold which is rounded to fit decimal requirments
    print("Created thresholds parameters list with a step size of ", bin_size)
    return bin_thresholds


def calculate_threshold_pixels(chsi_raster_path, bin_thresholds,convert_to_area=False):
    """
    Calculates the amount of pixels in each bin
            :param chsi_raster_path: string location of chsi raster
            :param bin_thresholds: list threshold values which is upper limit of bin and is included in bin  ex. bin_thresholds = [0.25, .5, .75, 1]
            :param convert_to_area=False: Boolean if true converts pixels into actual area
            :return pixel_per_threshold: list of [thresholds,pixels in thresholds] and sum added to the end
    """
    unit_area=1
    chsi_raster = Raster(chsi_raster_path)  # open the chsi raster from class
    if convert_to_area:
        geo_info = chsi_raster.geo_transformation
        pixelWidth = geo_info[1]
        pixelHeight = geo_info[5]
        unit_area=None
        unit_area=abs(pixelWidth*pixelHeight)
    pixels_prev = np.sum(np.less(chsi_raster.array, 0) * 1)*unit_area # establishes prev pixel variable by removing any values less than 0
    pixel_per_threshold = []  # establishes pixel variable
    # loop over bin_thresholds inputs ex. [0.25,0.5,0.75,1.0]
    for thresh in bin_thresholds:
        # extract pixels where the physical habitat quality is higher than the user threshold value
        habitat_pixels = np.less_equal(chsi_raster.array, thresh) * 1

        sum_pixels = np.sum(habitat_pixels)*unit_area # calculates number of pixels by summing values
        # creates list of upper threshold and their quantity of pixels *upper limit included, lower excluded
        pixel_per_threshold.append([thresh, sum_pixels - pixels_prev])  # appends to thresholds to list

        # setting subtraction for next loop
        pixels_prev = sum_pixels
    pixel_per_threshold.append(["sum", sum_pixels])  # adds total area in last list item
    return pixel_per_threshold


def mann_u_test(bio_data_path,rand_data_directory):
    """
    Runs Mann Whitney U Test
        :param bio_data_path: string file location of bio data HSI values csv
        :param rand_data_path: string file location of random data directory
        :return stats.mannwhitneyu: p value and statistic (null hypothesis is that the sets are the same)

    """
    print("Running Mann-Whitney U test")
    # Import bio data
    directory = os.fsencode(rand_data_directory)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            break

    rand_data_path = rand_data_directory + "\\" + filename
    print("Mann_U test conducted with",rand_data_path)
    bio_data_list = csv_import_coords_to_list(bio_data_path, only=0)
    # Import random data
    rand_data_list = csv_import_coords_to_list(rand_data_path, only=0)

    if len(bio_data_list) == len(rand_data_list):
        print("Checked that Bio and Random data have same length of", len(bio_data_list))
    else:
        print("Error: Bio and Random data do not have same Length ({} vs.{})".format(len(bio_data_list),
                                                                                     len(rand_data_list)))
        return 1
    print("P value <.05 means Bio Data is different from Random")
    return stats.mannwhitneyu(x=bio_data_list, y=rand_data_list, alternative='two-sided')


def forage_ratio_test(chsi_raster_path, bin_thresholds, bio_data_path, decimals=4, area=None,utilization=None, bio_data_list=None):
    """
    Evaluates forage ratio for each bin
        :param chsi_raster_path: string location of chsi raster
        :param bin_thresholds: list threshold values which is upper limit of bin and is included in bin ex. bin_thresholds = [0.25, .5, .75, 1]
        :param bio_data_path: string file location of bio data HSI values csv
        :param decimals: int number of decimal points of the bin threshold (default decimal=4 ex. 0.0001)
        :param area:list of int for each bin (default None, only add if doing repeated forage ratios ex.random data)
        :param utilization:list of [bin threshold , #of data points in threshold] for each bin (default None,
        *only add if doing repeated forage ratios or are not using csv path ex.random data)
        :param bio_data_list: list of bio data from coordinates( default: none )* add to avoid using csv file
        :return bin_forage: list of forage results for each bin
    """
    if area == None: # if None generates area:* used for speeding up forage ratio test data generation
        area = calculate_threshold_pixels(chsi_raster_path, bin_thresholds)
    if utilization == None: # if None generates utilization: * used for importing utilization
        utilization = catagorize_CHSI(bin_thresholds,bio_data_path=bio_data_path,  bio_data_list=bio_data_list)

    bin_forage = []  # establishes variable
    # looping over bins
    for i in range(len(area) - 1):
        # generating forage ratio
        area_percent = area[i][1] / area[len(area) - 1][1]  # Area%=Area_bin/Total Area
        ut_percent = utilization[i][1] / utilization[len(area) - 1][1]  # Utilization=Count_bin/Total Count
        if area_percent == 0:
            forage_ratio = 0
        else:
            forage_ratio = round(ut_percent / area_percent, decimals)  # Forage Ratio = %U/%A

        bin_forage.append(forage_ratio) # adds forage ratio to bin forage list

    return bin_forage

def random_forage_test(random_data_hsi_directory, chsi_raster_path, bin_thresholds,area_input=None,plot_gaussian=False):
    """
    Evaluates Forage Ratio for Random data with mean,std and 95% confidence intervals
        :param random_data_hsi_directory: string location of random hsi data folder
        :param chsi_raster_path: string location of chsi raster
        :param bin_thresholds: list threshold values which is upper limit of bin and is included in bin
        ex. bin_thresholds = [0.25, .5, .75, 1]
        :param area_input:list of int for each bin (default None, only add if doing repeated forage ratios ex.random data)
        :param plot_gaussian: boolean if true creates gaussian distribution plot using median stdev forage ratio bin
        :return fr_results: list of forage ratio results per bin
        :return stats: list of stats per bin [mean,std,upper 95% confidence interval,lower 95% confidence interval]
        """

    print("Evaluating random datasets using the forage ratio test")
    directory = os.fsencode(random_data_hsi_directory)
    filename_list = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            filename_list.append(filename)
            continue
        else:
            continue
    fr_results = []
    if area_input is None:
        area_input = calculate_threshold_pixels(chsi_raster_path, bin_thresholds)
    count=0
    percent_counter=0
    total_count=len(filename_list)
    display_percent_count=round(total_count/10) # displays every 10%
    for rand_filename in filename_list:
        count+=1
        # print(rand_filename)
        if (count == display_percent_count):
            print("{:.1%} of the random data sets evaluated using the forage ratio test".format((count+display_percent_count*percent_counter)/total_count))
            count = 0
            percent_counter+= 1

        rand_fr_results = forage_ratio_test(chsi_raster_path, bin_thresholds,
                                            random_data_hsi_directory + "\\" + rand_filename, area=area_input)
        rand_fr_results.insert(0, rand_filename)
        fr_results.append(rand_fr_results)

    # forage ratio stats
    stats = []
    mean = ["Mean"]
    std = ["Standard Deviation"]
    upper_conf = ["Upper 95% Confidence Limit"]
    lower_conf = ["Lower 95% Confidence Limit"]
    rand_dataset_qnt = ["# of Random data sets used for Statistics"]
    n_datapoints_per_dataset = ["# of points used per data set"]

    n_datapoints_per_dataset.append(len(csv_import_coords_to_list(random_data_hsi_directory + "\\" + rand_filename)))
    rand_dataset_qnt.append(len(filename_list))
    # Looping over bins
    for i in range(len(bin_thresholds)):
        fr_per_bin = []
        # Looping over Datasets
        for fr_list in fr_results:
            fr_per_bin.append(fr_list[i + 1])
            # establishing values
        mean_value = statistics.mean(fr_per_bin)
        std_value = round(statistics.stdev(fr_per_bin),4)

        # adding to list
        mean.append(mean_value)
        std.append(std_value)
        upper_conf.append(mean_value + (2 * std_value))
        lower_conf.append(mean_value - (2 * std_value))

    # stats Final Product

    stats.append(["Thresholds"]+bin_thresholds)
    stats.append(mean)
    stats.append(std)
    stats.append(upper_conf)
    stats.append(lower_conf)
    stats.append(rand_dataset_qnt)

    # uses median standard deviation to establish upper and lower 95% confidence interval
    if len(std) % 2 == 0: # median value is averaged if even which, if guarantees odd number for indexing to work
        start = 1
    else:
        start =2
    median_std = statistics.median(std[start:])
    std_index = std.index(median_std)

    median_mean=round(mean[std_index],3)
    fr_thresholds = [median_mean+ 2 * median_std, median_mean - 2 * median_std]  # list of upper and lower forage ratio thresholds
    if plot_gaussian:
        #creating gaussian distribution graph
        print("Creating Guassian Distribution plot with 95% confidence interval of {} to {} ".format(fr_thresholds[1],fr_thresholds[0]))
        gaussian_bin=[]
        for gaus_list in fr_results:
            gaussian_bin.append(gaus_list[std_index + 1])
        gaussian_dist_random_graph(gaussian_bin, fr_thresholds) # plots gaussian curve
    return fr_results, stats, fr_thresholds,median_std

def habitat_quality_from_threshold_generator(tif_input_path,tif_output_path,bin_thresholds):
    """
    creates a habitat tif file from threshold list and tif file with lower values being better habitat
        :param tif_input_path: string location of tif raster
        :param tif_output_path: string location of outputh path for habitat tif raster
        :param bin_thresholds: list threshold values which is upper limit of bin and is included in bin  ex. bin_thresholds = [0.25, .5, .75, 1]

    """
    print("Generating habitat tif with thresholds of,",bin_thresholds)
    # establishing raster array and geo transformation from geo tif
    raster = Raster(tif_input_path)  # calling raster class
    tif_array = raster.array  # raster class array
    geo_info = raster.geo_transformation  # raster class transformation
    epsg=raster.epsg

    #converting array to habitat
    non_nan_pixels = np.greater_equal(tif_array, 0) * 1 # non nan mask
    habitat_pixels = np.empty(tif_array.shape) # empty array with required shape
    #loop over habitat
    for thresh in bin_thresholds:
        tif_habitat_addition = np.less_equal(tif_array, thresh) * 1
        habitat_pixels = np.add(habitat_pixels,tif_habitat_addition)
    habitat_pixels_sin_nan=np.multiply(habitat_pixels, non_nan_pixels)
    create_raster(tif_output_path, raster_array=habitat_pixels_sin_nan, epsg=epsg,rdtype= gdal.GDT_Byte, geo_info=geo_info, nan_val=0)
    print("Succesfuly created tif for Habitat Evaluation in ", tif_output_path)
    return 0
def bin_resolution_check(bin_interval=None,observation_data_path=None,n_observations=None):
    """
    Checks and or creates bin resolution through the bin step size.
    :param bin_interval: float user selected bin interval
    :param observation_data_path: string file location of observation data
    :param n_observations:int number of observations
    """
    if n_observations == None:
        if observation_data_path == None:
            print("Error:function requires observation_data_path or n_observation")
            return 1
        n_observations = len(csv_import_coords_to_list(observation_data_path, only=0))
    bin_size_check = 100 / (10 ** len(str(int(n_observations))))
    if bin_size_check == 1:
        bin_size_check = .2
    if bin_size_check > 1:
        print("Error:Insufficient observations")
        return 1
    if bin_interval == None:
        print("HSI bin step size resolution of {} was chosen based on the {} available observations".format(bin_size_check,n_observations))
        return bin_size_check
    if bin_interval<bin_size_check:
        print("HSI bin step size resolution of {} was overridden to {} based on the {} available observations. A smaller step size would increase the error".format(
            bin_interval,bin_size_check, n_observations))
        return bin_size_check
    return bin_interval


