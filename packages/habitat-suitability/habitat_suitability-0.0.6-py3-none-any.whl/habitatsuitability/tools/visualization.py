from .bio_tools import catagorize_CHSI, directory_creator
from .fun import *


def hsi_forage_plot(hsi, fr, regression_formular=False, graph_directory=os.path.abspath("") + "\\generated_graphs"):
    """
           Creates a hsi vs. forage ratio plot
           :param hsi: list of hsi values signifying upper threshold of hsi interval
           :param fr: list forage ratio values for the hsi bins
           :param regression_formular: optional to write out regression formular in text if true
           :param graph_directory: path to graph directory of graphs (default graph_directory= os.path.abspath("") + "\\generated_graphs")
           :return none
           """
    y_est = np.polyfit(hsi, fr, 2)
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.scatter(hsi, fr)
    plt.plot(hsi, np.polyval(y_est, hsi))
    plt.xlabel("hsi", fontsize=18)
    plt.ylabel("forage ratio", fontsize=18)
    plt.title(f'Forage ratio vs hsi', fontsize=20)
    directory_creator(graph_directory)  # creates directory if missing

    if regression_formular:

        graph_path = os.path.join(graph_directory, "hsi_forage_regformular.png")
        textstr = '\n'.join((
            "2nd order polynomial regression",
            "fr={}+{}*hsi+{}*hsi^2".format(round(y_est[2], 1), round(y_est[1], 1), round(y_est[0], 1)
                                           )))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)

    else:
        graph_path = os.path.join(graph_directory, "hsi_forage.png")
    ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable='box')

    plt.savefig(graph_path)


def binning_hsi_forage_plot(hsi, fr, hsi_thresh, habitat=False,
                            graph_directory=os.path.abspath("") + "\\generated_graphs"):
    """
       Creates a hsi vs. forage ratio plot with the binning defined
       :param hsi: list of hsi values signifying upper threshold of hsi interval
       :param fr: list forage ratio values for the hsi bins
       :param hsi_thresh: list hsi thresholds which define the bins
       :param habitat: optional text description of habitat bin color description (default false text describes intervals)
       :param graph_directory: path to graph directory of graphs (default graph_directory= os.path.abspath("") + "\\generated_graphs")
       :return none
       """
    y_est = np.polyfit(hsi, fr, 2)
    fig = plt.figure()
    ax = fig.add_subplot()
    # ax.set_xlim([0, 1])
    # ax.set_ylim([0, max(fr)])
    plt.scatter(hsi, fr)
    plt.plot(hsi, np.polyval(y_est, hsi))
    plt.xlabel("hsi", fontsize=18)
    plt.ylabel("forage ratio", fontsize=18)
    plt.title(f'Forage ratio vs hsi binning', fontsize=20)
    plt.axvline(x=hsi_thresh[1], color='g', linestyle='-')
    plt.axvline(x=hsi_thresh[0], color='r', linestyle='-')

    directory_creator(graph_directory)  # creates directory if missing

    # plt.show()
    if habitat:
        textstr = '\n'.join((
            "Habitat Binning",
            "Green- Preferred Habitat", "Gray- Neutral Habitat", "Red- Avoided Habitat"
        ))
        graph_path = os.path.join(graph_directory, "hsi_forage_binning_habitat_label.png")
    else:
        textstr = '\n'.join((
            "HSI Binning",
            "Upper CI HSI 95%= {}".format(round(hsi_thresh[0], 2)),
            "Lower CI HSI 95%= {}".format(round(hsi_thresh[1], 2))))
        graph_path = os.path.join(graph_directory, "hsi_forage_binning.png")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable='box')
    x = hsi
    ax.axvspan(0, hsi_thresh[0], alpha=0.5, color='red')
    ax.axvspan(hsi_thresh[0], hsi_thresh[1], alpha=0.5, color='gray')
    ax.axvspan(hsi_thresh[1], 1, alpha=0.5, color='green')

    # plt.savefig("hsi_forage.png")
    plt.savefig(graph_path)


def fr_conf_interval_hsi_forage_plot(hsi, fr, fr_interval, graph_directory=os.path.abspath("") + "\\generated_graphs"):
    """
      Creates a gaussian distribution plot with the forage ratio random data
      :param gaussian_data_list: list of forage ratio values for hsi bin
      :param fr_limits: list of upper and lower forage 95% confidence interval limit
      """
    y_est = np.polyfit(hsi, fr, 2)
    fig = plt.figure()
    ax = fig.add_subplot()
    # ax.set_xlim([0,1])
    # ax.set_ylim([0, max(fr)])

    x = hsi

    ax.fill_between(x, 0, fr_interval[1],
                    facecolor='red', alpha=0.5)
    ax.fill_between(x, fr_interval[1], fr_interval[0],
                    facecolor='gray', alpha=0.5)
    ax.fill_between(x, fr_interval[0], max(fr),
                    facecolor='green', alpha=0.5)
    plt.scatter(hsi, fr)
    plt.plot(hsi, np.polyval(y_est, hsi))
    plt.xlabel("hsi", fontsize=18)
    plt.ylabel("forage ratio", fontsize=18)
    plt.title(f'Forage ratio vs hsi with 95% CI', fontsize=20)
    # plt.show()
    plt.axhline(y=fr_interval[0], xmin=0, xmax=1, color='g', linestyle='-')
    plt.axhline(y=fr_interval[1], xmin=0, xmax=1, color='r', linestyle='-')

    textstr = '\n'.join((
        "FR 95% CI",
        "Upper CI 95%= {}".format(round(fr_interval[0], 1)),
        "Lower CI 95%= {}".format(round(fr_interval[1], 1))
    ))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    directory_creator(graph_directory)  # creates directory if missing
    graph_path = os.path.join(graph_directory, "conf_interval_hsi_forage.png")
    ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable='box')

    # plt.savefig("hsi_forage.png")
    plt.savefig(graph_path)


def gaussian_dist_random_graph(gaussian_data_list, fr_limits,
                               graph_directory=os.path.abspath("") + "\\generated_graphs"):
    """
    Creates a gaussian distribution plot with the forage ratio random data
    :param gaussian_data_list: list of forage ratio values for hsi bin
    :param fr_limits: list of upper and lower forage 95% confidence interval limit
    :param graph_directory: path to graph directory of graphs (default graph_directory= os.path.abspath("") + "\\generated_graphs")
    :return none
    """
    stdev = (fr_limits[0] - 1) / 2
    forage_value_classification = np.arange(fr_limits[1] - 2 * stdev, fr_limits[0] + 2 * stdev, .04)
    fig = plt.figure()
    ax = fig.add_subplot()

    count = catagorize_CHSI(forage_value_classification, bio_data_list=gaussian_data_list)

    directory_creator(graph_directory)  # creates directory if missing
    graph_path = os.path.join(graph_directory, "randomdataset_gaussian_distribution.png")
    sum = count[-1]
    percent = []

    for i in count[:-1]:
        percent.append(i[1] / sum[1])

    fr_upper95 = fr_limits[0]

    fr_lower95 = fr_limits[1]

    plt.plot(forage_value_classification, percent, 'o')
    plt.ylabel("probability density", fontsize=18)
    plt.xlabel("forage ratio", fontsize=18)

    plt.axvline(x=fr_upper95, color='g', linestyle='-')
    plt.axvline(x=fr_lower95, color='r', linestyle='-')
    plt.title(f'Randomdata gaussian distribution', fontsize=20)
    ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable='box')
    plt.savefig(graph_path)
    return 0


# def hsi_paramter_graph(coordinate_csv_path, parameters, hsi_parameter_tif_inputs):
#     Hsi_vel = [0, 0.1, 0.1, 0.2, 0.5, 1, 1, 0.5, 0.2, 0.1, 0, 0]
#     vel = [0, 0, 0.35, 0.85, 1.25, 1.55, 2.95, 3.25, 3.85, 4.45, 4.65, 9.71099]
#
#     hsi_depth = [0, 0, 0.1, 0.2, 0.5, 1, 1, 0.5, 0.2, 0.1, 0, 0]
#     depth = [0, 0.25, 0.45, 0.65, 0.75, 0.95, 1.85, 2.15, 2.55, 2.85, 3.35, 7.13959]
#     hsi_substrate = [0, 0, 1, 1, 0, 0]
#     substrate = [0, 32, 32, 195, 195, 384]
#     hsi = [Hsi_vel, hsi_depth, hsi_substrate]
#     param_val = [vel, depth, substrate]
#
#     coordinates = csv_import_coords_to_list(coordinate_csv_path)
#     coord_quant = int(len(coordinates))
#     i = 1
#     par_quant = int(len(parameters))
#     for par in parameters:
#         hsi_n_value = np.empty([2, coord_quant])
#
#         # parameter hsi
#         parameter_hsi_tif_path = hsi_parameter_tif_inputs[par]
#         hsi_n_value[0, :] = tif_coordinate_value(parameter_hsi_tif_path, coordinates, with_coords=False)
#         print("Created hsi values list from {} hsi tif dataset in".format(par))
#         # parameter value
#         parameter_value_tif_path = hsi_parameter_value_inputs[par]
#         hsi_n_value[1, :] = tif_coordinate_value(parameter_value_tif_path, coordinates, with_coords=False)
#         print("Created parameter values list from {} tif dataset in".format(par))
#         # save hsi and parameter value as csv
#         output_csv_path = parameter_hsi_directory + "{}_hsi_y_value.csv".format(par)
#
#         max = np.amax(hsi_n_value[1, :])
#         print("max parameter value", max)
#         min = np.min(hsi_n_value[1, :])
#         print("max parameter value", min)
#
#         # forage_ratio_test(parameter_value_tif_path, range(min,max,.01),output_csv_path)
#         # interrupting y value based on x value
#
#         # plot
#         plt.subplot(1, par_quant, i)
#         plt.plot(hsi_n_value[1, :], hsi_n_value[0, :], 'o')
#         # plt.plot(param_val[i-1],hsi[i-1])
#         plt.ylabel("hsi value", fontsize=18)
#         plt.xlabel(x_units[i - 1], fontsize=18)
#         # plt.title(f'{parameters_label[i-1]} hsi curve',fontsize=20)
#         plt.title(f'{par} hsi curve', fontsize=20)
#         i += 1
#     plt.tight_layout()
#     plt.show()
#     return


# def utilization_vs_hsi(bio_data_path, bins,):
#     count = catagorize_CHSI(bio_data_path, bins)
#     sum = count[-1]
#     percent = []
#     percent_prev = 0
#
#     for i in count[:-1]:
#         percent.append((i[1] / sum[1]) * 100 + percent_prev)
#         percent_prev = i[1] / sum[1] * 100 + percent_prev
#         # percent.append((i[1] / sum[1]) * 100)
#     # plt.plot(bins, percent,'o')
#     plt.xlim(0, 1.1)
#     plt.bar(bins, percent, width=.01)
#     plt.ylabel("Cumulative utilization %", fontsize=18)
#     plt.xlabel("hsi", fontsize=18)
#
#     plt.title(f'Cumulative utilization vs. hsi', fontsize=20)
#     plt.tight_layout()
#     plt.show()
#     return






