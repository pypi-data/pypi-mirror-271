from habitatsuitability.hsi_raster.flusstools_geotools_functions import create_raster
from .fun import *
from habitatsuitability.hsi_raster.raster import Raster

def catagorize_CHSI(bin_thresholds,bio_data_path=None,bio_data_list=None):
    """
    Categorizes bio data and puts it into the corresponding bin
        :param bio_data_path: string file location of bio data HSI values csv
        :param bin_thresholds: list threshold values which is upper limit of bin and is included in bin
        :param bio_data_list: list of values from coordinate location example: hsi (default: None)
        ex. bin_thresholds = [0.25, .5, .75, 1]
        :return bins: list of [threshold value upper limit, # of data points in bin]
        """
    # Import CSV
    if bio_data_list is None:
        if bio_data_path is None:
            print("Error: function needs either a path or a list input")
            return 1
        else:
            bio_data_list = csv_import_coords_to_list(bio_data_path, only=0)
    bio_length = len(bio_data_list)
    bio_data_list.sort()

    bins = []
    for thresh in bin_thresholds:
        position = bisect.bisect(bio_data_list, thresh)
        threshold = bio_data_list[:position]
        # Creates list of upper threshold and amount of values
        bin = [thresh, len(threshold)]

        bins.append(bin)
        bio_data_list = bio_data_list[position:]
        # print(bio_data_list)
    bins.append(["Sum", bio_length])

    return bins

def wetted_area_generator(depth_input_tif = None,chsi_input_tif=None, save_tif=False,raster_variable = "chsi+depth"):
    """
    Creates wetted area using depth tif, has option to save tif wetted area
    :param depth_input_tif:string file location string of chsi tif location
    :param chsi_input_tif:string file location string of chsi tif location
    :save_tif:boolean if true saves a tif of wetted area
    :raster_variable: string (default = "depth) for chsi_tif input requires raster_variable="chsi"
    :return wetted_area_pixels: raster with values 1 being wetted area and 0 being dry
    :return depth_raster.geo_transformation: geo information from depth raster

    """
    if depth_input_tif is None and chsi_input_tif is None:
        print("Error: depth and or chis tif path needs to be input")
        return 1


    if raster_variable == "chsi+depth":
        if depth_input_tif is None or chsi_input_tif is None:
            print("Error: depth and chsi tif path needs to be input for raster_variable == chsi+depth")
            return 1

        depth_raster = Raster(depth_input_tif) #depth tif to raster
        chsi_raster = Raster(chsi_input_tif)   #chsi tif to raster

        wetted_area_pixels_depth = np.greater(depth_raster.array, 0) * 1 # extract pixels where the depth is greater than 0
        wetted_area_pixels_chsi = np.greater_equal(chsi_raster.array, 0) * 1 # extract pixels where the chsi is not Nan (equal or greater than zero)
        wetted_area_pixels = wetted_area_pixels_chsi * wetted_area_pixels_depth
        geo_information = chsi_raster.geo_transformation
        raster_epsg = chsi_raster.epsg
    elif raster_variable == "chsi":
        if chsi_input_tif is None:
            print("Error: chsi tif path needs tif path input for raster_variable == chsi")
            return 1
        chsi_raster = Raster(chsi_input_tif)
        wetted_area_pixels = np.greater_equal(chsi_raster.array, 0) * 1 # extract pixels where the chsi is not Nan (equal or greater than zero)
        geo_information=chsi_raster.geo_transformation
        raster_epsg=chsi_raster.epsg
    elif raster_variable == "depth":
        if depth_input_tif is None:
            print("Error depth tif path needs tif path input for raster_variable == depth")
            return 1
        depth_raster = Raster(depth_input_tif)
        wetted_area_pixels = np.greater(depth_raster.array, 0) * 1# extract pixels where the depth is greater than 0
        geo_information = depth_raster.geo_transformation
        raster_epsg = depth_raster.epsg
    else:
        print("Unknown variable input {} needs to be either 'depth' or 'chsi'".format(raster_variable))
    if save_tif:
        raster_shp_file_name = os.path.abspath("") + "\\habitat\\wetted_area.tif"
        create_raster(raster_shp_file_name,
                          raster_array=wetted_area_pixels,
                          epsg=raster_epsg,
                          nan_val= 0,
                          geo_info=geo_information)
        print("Created wetted area tif file in", raster_shp_file_name)

    return wetted_area_pixels, geo_information


def random_w_area_coords_generator(hsi_tif_path,random_points_quantity,depth_tif_path=None ,rows=None, cols=None, transform=None,
                                   hsi_array=None):
    """
    Creates random data set of coordinates inside wetted area
        :param hsi_tif_path: string file location string of hsi tif location
        :param random_points_quantity: integer number of how many random points need to be created in data set
        :param cols: list of int of the showing column index of pixels (default= None)
        :param rows: list of int of the showing row index of pixels (default= None)
        :param transform: list geo transformation data of hsi raster None (default= None)
        :param hsi_array: np array of hsi values from hsi raster (default= None)
        :return coords:list of [hsi,x coord,y coord]
    """
    if hsi_array is None or transform is None:
        hsi_raster = Raster(hsi_tif_path)
        hsi_array = hsi_raster.array
        transform = hsi_raster.geo_transformation
    if rows is None or cols is None:

        wetted_area_pixels, transform = wetted_area_generator(depth_input_tif = depth_tif_path, chsi_input_tif = hsi_tif_path, raster_variable = "chsi+depth")
        rows, cols = np.where(wetted_area_pixels == 1)

    if transform[2] or transform[4] != 0:
        print("The tif to coordinate value can only function properly when the tif does not have a rotation")
        return 1
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    coords = []
    i = 0
    while i < random_points_quantity - 1:
        i += 1
        random_index = np.random.randint(0, len(rows) - 1)
        xCoord = ((cols[random_index]+0.5) * pixelWidth) + xOrigin
        yCoord = ((rows[random_index]+0.5) * pixelHeight) + yOrigin
        # nan value check
        if np.isnan(hsi_array[rows[random_index]][cols[random_index]]):
            random_points_quantity += 1
        else:
            coords.append([hsi_array[rows[random_index]][cols[random_index]], xCoord, yCoord])

    return coords


def tif_test_data_creator(tifs, percent):
    """
    Creates a tif sample data with a percentage of the real data
    :param tifs: dictionary of string file location of all the data variable inputs example:velocity, depth tif location
    :param percent: float decimal number of percent of data
    :return none
    """
    # loops over variables in tifs dictionary
    for t in tifs:
        # setting filename from dictionary
        file_name = tifs[t]

        # opening tif file with gdal
        tif = gdal.Open(file_name)  # opens tiff to be used with gdal

        # finding geo transfrom data and getting array
        geo_transform = tif.GetGeoTransform()
        raster_array = tif.GetRasterBand(1).ReadAsArray()

        # setting new array length to get percentage of raster
        array_length = round(np.size(raster_array, 0) * percent)

        # taking a percentage of raster
        new_raster_array = raster_array[1:array_length]

        # modifiying string name to create name with additiong of test data tag
        file_name_new = file_name.replace(".tif", "_TestData.tif")

        # saving tif
        geotools.create_raster(file_name_new, new_raster_array, geo_info=geo_transform)

        print("Made Test data set in ", file_name_new)
    return 0


def csv_import_coords_to_list(coordinate_csv_path, only=None):
    """
    Imports Csv files to list
           :param coordinate_csv_path:string file location of csv file location of coordinates
           :param only: int of row number to isolate one row return only
           :return coordinates: list of coordinates *normaly None if not designated
           """
    # panda import reading csv file
    df = pd.read_csv(coordinate_csv_path)

    # converting panda imports to list
    coordinates = df.values.tolist()

    # if a integer return only that integer row position only = 0 would return the first row
    if only != None:
        # checks to see if value is integer
        if type(only) == int:
            Value = []
            for item in coordinates:
                Value.append(item[only])
            return Value
        else:
            print("Error: {} Not a valid integer input for only".format(type(only)))

    return coordinates


def tif_coordinate_value(tif_path, coordinates,with_coords=True):
    """
    Converts coordinates to chsi value using tif raster
    :param tif_path:string file location of tif
    :param coordinates: list of coordinates  *must have same epsg as tif can not have rotation!
    :param with_coords: boolean returns list of values and coordinates if true (default with_coords= true) else just tif value
    :return pixel_values
    Uses modified code from https://gis.stackexchange.com/questions/221292/retrieve-pixel-value-with-geographic-coordinate-as-input-with-gdal
    """

    # trying open gdal
    try:
        # opening Gdal
        dataset = gdal.Open(tif_path)
        band = dataset.GetRasterBand(1)
        transform = dataset.GetGeoTransform()

        # establishing Variables
        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        if transform[2] or transform[4] != 0:
            print("The tif to coordinate value can only function properly when the tif does not have a rotation")
            return 1

        xOrigin = transform[0]
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = -transform[5]

        data = band.ReadAsArray(0, 0, cols, rows)
    except:
        print("Something went wrong with opening Tif file, ", tif_path)
        return 1

    pixel_values = []  # list of value and coordinates
    value = []  # list for results of only value

    # looping over coordinates

    i = 0  # establishing i
    while i < len(coordinates):

        # extracting coordinate list form lists by i
        point = coordinates[i]
        # converting Coordinates to row and col of tif array
        col = int((point[0] - xOrigin) / pixelWidth)
        row = int((yOrigin - point[1]) / pixelHeight)

        # creating lists
        try:
            if with_coords:
                pixel_values.append([data[row][col], point[0], point[1]])  # lists of [Tif value,x coord,y coord]
            else:
                pixel_values.append(data[row][col])  # lists of Tif values
            if data[row][col] == nan_value:
                print("Nan value detected skipping point", point)
            else:
                value.append(data[row][col])  # lists of [x coord,y coord]
        except:
            print(
                "Error with retrieving of tif value for coordinate data point ({},{}), skipping point".format(point[0],
                                                                                                              point[1]))

        i += 1  # adding +1 to add to count for while loop
    return pixel_values


def stats_generator(data_path, column_position=0, name=None):
    """
    Creates statistics for data from csv file column
    :param data_path: string of file location
    :param column_position: int column of data position (default 0)
    :param name: string optional name input of dataset
    """
    value = csv_import_coords_to_list(data_path, only=column_position)

    if name == None:
        name = data_path.split(os.sep)[-1]
    if len(value) > 2:
        # Calculating Statistics of Tif Value
        stats = {
            "name": name,
            "entries": len(value),
            "mean": statistics.mean(value),
            "std": statistics.stdev(value),
            "variance": statistics.variance(value)
        }
    else:
        print("Insufficent Points for Stats")
        stats = {
            "name": "Blank",
            "entries": len(value),
            "mean": "Insufficent Points for Stats",
            "std": "Insufficent Points for Stats",
            "variance": "Insufficent Points for Stats"
        }
    return stats
def directory_creator(directory_path):
    """
    Checks if folder exist and if not creates one
    :param data_path: string of file location
    :return none
    """
    if not os.path.isdir(directory_path):
        try:
            os.makedirs(directory_path)
        except:
            print("Error:Unable to create directory with the path ",directory_path)
            return 1
    return 0





