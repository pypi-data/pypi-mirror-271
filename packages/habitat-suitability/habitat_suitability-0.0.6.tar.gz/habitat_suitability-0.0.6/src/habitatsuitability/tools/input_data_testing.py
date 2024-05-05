
from .bio_tools import *
from .fun import *
from .bio_tools import wetted_area_generator

def wetted_area_coordinate_check(coords_csv_path, chsi_input_tif=None, depth_input_tif=None, raster_variable="chsi"):
    """
    Checks if coordinates are within wetted area
            :param coords_csv_path:string file location of folder for coordinate csv file format "X","Y"
            :param tif_path:string file location string of shapefile of tif file optional depth and chsi tif input
            :raster_variable: string (default = "depth) for chsi_tif input requires raster_variable= "chsi"
            :return coords_csv_path_in: string path of printed csv files with only coordinates inside area of shapefile
            :return coords_in list of [x,y] coordinates  with only coordinates inside area of shapefile
    """
    wetted_area_pixels, transform = wetted_area_generator(chsi_input_tif=chsi_input_tif,depth_input_tif=depth_input_tif, raster_variable=raster_variable)
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]
    print("Checking if coordinates are within Wetted Area")

    # import shapefile and coordinates
    try:
        coordinates= csv_import_coords_to_list(coords_csv_path)
    except:
        # exception if there is problems importing
        print("Problem importing csv file")
        return 1

    # establishes lists of coordinates and points
    coords_out=[]
    coords_in=[]

    #count for printing messages every set points
    count=0
    for point in coordinates:
        col = int((point[0] - xOrigin) / pixelWidth)
        row = int((yOrigin - point[1]) / pixelHeight)


        # checks if point is inside wetted area

        if col >= 0 and row >= 0 and wetted_area_pixels[row][col] == 1:
            # if inside adds coords and points to in lists
            coords_in.append([point[0], point[1]])
        else:
            # if not inside adds to out lists
            coords_out.append([point[0], point[1]])

            # prints to console if point is not within bounds of wetted area
            print("Coord {} not in extent of area".format(point))
            # printing for user to see progress of point checking
        count += 1
        if (count % 100 == 0):  # Printing every 100 counts
            print("Checking point {}/{}".format(count, len(coordinates)))


    # sets header


    # establish string path of in and out csv location
    coords_csv_path_in = coords_csv_path.replace(".csv", "_inside_WettedArea.csv")
    coords_csv_path_out = coords_csv_path.replace(".csv", "_outside_WettedArea.csv")

    # adds header to coordinate list

    coords_in.insert(0, headerXY)
    coords_out.insert(0, headerXY)

    # create csv file

    np.savetxt(coords_csv_path_in, coords_in, delimiter=", ", fmt='% s')
    np.savetxt(coords_csv_path_out, coords_out, delimiter=", ", fmt='% s')


    if (len(coords_in)) == 0:
        print("No coordinates inside bounds, check data and coordinates projection in QGIS")
        return 1

    # prints results of number of coordinates in and out of shapefile
    print("Out of the {} coordinates, {} are inside and {} are outside the bounds. Check the values outside. {}"
          .format(len(coordinates),len(coords_in[1:]),len(coords_out[1:]),coords_csv_path_out))


    return coords_csv_path_in, coords_in[1:]

def raster_input_check(tifs):
    """
        Checks if geo data of all tifs are the same

        param tifs: Dictionary of input variables and their string tif location
        return: 0
    """
    shape=[]
    geo_information=[]
    epsgs=[]
    for tif_var in tifs:
        print("Checking", tif_var, "tif")

        input_raster = Raster(tifs[tif_var])
        shape.append(np.shape(input_raster.array))
        geo_information.append(input_raster.geo_transformation)
        epsgs.append(input_raster.epsg)

    #checking if geo data is the same
    if all(i == epsgs[0] for i in epsgs):
        print("All epsgs are the same",epsgs[0])
    else:
        print("Epsgs are different", epsgs)

    if all(i == shape[0] for i in shape):
        print("Array Dimensions are the same", shape[0])
    else:
        print("Array Dimensions are different", shape)


    if all(i == geo_information[0] for i in geo_information):
        print("All geo information are the same", geo_information[0])
    else:
        print("Error: Geo Information is different", geo_information)
        for o in range(len(geo_information)):
            if any(i[o] != geo_information[0][o] for i in geo_information):
                print("difference in the {} position of geo information {}".format(o,geo_information[0][o]))
        return 1
    return 0




