from .bio_tools import *
from .fun import *



def tif_coordinate_value_csv(tif_path, coordinate_csv_path, output_csv_path):
    """
    Finds HSI value from CHSI Raster using XY Coordinates
    :param tif_path: string file location of chsi tif location
    :param coordinate_csv_path: string file location string of coordinates in X,Y location
    :param output_csv_path: string file location where new csv file should be saved
    :return stats: dictionary of hsi statistics
    """
    # import coordinates from csv file
    coordinates = csv_import_coords_to_list(coordinate_csv_path)

    # converts coordinates to chsi value
    value_with_coordinates = tif_coordinate_value(tif_path, coordinates)

    # csv printing

    value_with_coordinates.insert(0, header)  # adding header

    np.savetxt(output_csv_path,
               value_with_coordinates,
               delimiter=", ",
               fmt='% s')
    return output_csv_path


def random_data_hsi(output_folder_csv_path, hsi_tif_path, random_dataset_quantity,
                    data_points_quantity, depth_tif_path=None):
    """
    Creates HSI random data set using wetted area
                :param output_folder_csv_path: string file location of folder for output RandomDataCoordsHSI csv file
                :param hsi_tif_path:string file location string of chsi tif location
                :param depth_tif_path:string file location string of depth tif location
                :param random_dataset_quantity: integer number of how many random data sets should be created
                :param data_points_quantity: integer number of how many random points need to be created in each data set
                :return stats_list: list of dictionaries of statistics of the created random data points


        """
    print("Creating randomly picked data sets using raster in ", output_folder_csv_path)
    # finding eligible pixels from tif for generation of random data coordinates
    if depth_tif_path is not None:
        wetted_area_pixels, transform = wetted_area_generator(depth_input_tif=depth_tif_path,
                                                              chsi_input_tif=hsi_tif_path, raster_variable="chsi+depth")
    else:
        wetted_area_pixels, transform = wetted_area_generator(chsi_input_tif=hsi_tif_path, raster_variable="chsi")
    # list of rows and cols integers where pixels are eligible for random data
    rows, cols = np.where(wetted_area_pixels == 1)
    print("# of pixels available for random generated data", len(rows))

    # establishing raster array and geo transformation from geo tif
    hsi_raster = Raster(hsi_tif_path)  # calling raster class
    hsi_array = hsi_raster.array  # raster class array
    transform = hsi_raster.geo_transformation  # raster class transformation

    random_dataset_quantity_digits = len(
        str(random_dataset_quantity))  # generates integers for digits in quanity of data sets to add zeros to name later

    # loops over amount of random data sets established in random_dataset_quantity
    count = 0
    percent_counter = 0
    total_count = random_dataset_quantity
    display_percent_count = round(total_count / 10)  # displays every 10%
    for i in range(random_dataset_quantity):
        count += 1
        # generates random coordinate data set using function
        value_with_coordinates = random_w_area_coords_generator(hsi_tif_path, data_points_quantity, rows=rows,
                                                                cols=cols, transform=transform, hsi_array=hsi_array)

        # adds value, X and Y to top of list for csv file
        value_with_coordinates.insert(0, header)

        # printing csv file
        #   generating name digit with filled in zeros ex. random_dataset_quantity =100. str_i= 5 with zeros = 005
        str_i = str(i)
        str_i = str_i.zfill(random_dataset_quantity_digits)
        #   creates csv path with added set number
        output_csv_path = os.path.join(output_folder_csv_path, "RandomCoordsHSIset_{}.csv".format(str_i))
        # output_csv_path = output_folder_csv_path + "RandomCoordsHSIset_{}.csv".format(str_i)
        # print("Creating random dataset in ", output_csv_path)
        #   generating csv file
        np.savetxt(output_csv_path,
                   value_with_coordinates,
                   delimiter=", ",
                   fmt='% s')

        if (count == display_percent_count):
            print("{:.1%} of {} random data sets generated".format(
                ((count + display_percent_count * percent_counter) / total_count), total_count))
            count = 0
            percent_counter += 1

    return 0






