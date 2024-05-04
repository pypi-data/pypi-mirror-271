# import seaborn
import matplotlib.pyplot as plt


def set_matplotlib_theme(ZOOM=2, figsize=(8.8, 5.43)):
    # seaborn.set_theme(style="ticks", font="Times New Roman")

    plt.rc('font', size=6.5*ZOOM)  # controls default text sizes
    plt.rc('axes', titlesize=6.5*ZOOM)  # fontsize of the axes title
    plt.rc('axes', labelsize=6.5*ZOOM)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=5.5*ZOOM)  # fontsize of the tick labels. For text with subscripts, use 7*ZOOM
    plt.rc('ytick', labelsize=5.5*ZOOM)  # fontsize of the tick labels
    plt.rc('legend', fontsize=6*ZOOM)  # legend fontsize
    plt.rc('figure', titlesize=7*ZOOM)  # fontsize of the figure title
    plt.rc('axes', linewidth=0.75)
    plt.rc('xtick.major', size=2*ZOOM)  # fontsize of the tick labels
    plt.rc('ytick.major', size=2*ZOOM)  # fontsize of the tick labels
    plt.rcParams.update({"font.family": "serif",
                         # "text.usetex": True,
                        "font.serif": ['Times New Roman'],
                        "axes.formatter.min_exponent": 3,  # Below 1000 => plain text
                         "axes.grid": True,
                        "grid.linewidth": 0.25,
                        'xtick.major.width': 0.6,
                        'ytick.major.width': 0.6,
                        'xtick.minor.width': 0.4,
                        'ytick.minor.width': 0.4})
    plt.rc('figure', figsize=(figsize[0]/2.54*ZOOM, figsize[1]/2.54*ZOOM))
    plt.rc('figure', autolayout=True)
    plt.rc('legend', labelspacing=0.1)
    # plt.rc('grid', visible=True)
    plt.rcParams['axes.axisbelow'] = True
    plt.rcParams['savefig.format'] = 'pdf'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'