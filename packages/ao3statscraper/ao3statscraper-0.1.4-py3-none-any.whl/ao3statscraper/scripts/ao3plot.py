#!python3

import argparse


def _parse_plotter_args():
    """
    Setup argument parser and read cmdline args.
    """

    parser = argparse.ArgumentParser(
        prog="ao3plot",
        description="Plot your AO3 statistics based on data you downloaded beforehand using the AO3StatScraper.",
        epilog="""
By default, this program will run a dialogue and ask you what to plot.
Alternately, you can skip this dialogue by using the -t or the -i flags.
""",
    )

    parser.add_argument(
        "-n",
        "-np",
        "--no-prettify",
        action="store_true",
        default=False,
        dest="no_pretty",
        help="Avoid any prettifycations, and only do a bare-bones plot.",
    )

    parser.add_argument(
        "-t",
        "-ts",
        "-u",
        "--total",
        "--totalstats",
        "--user",
        "--userstats",
        action="store_true",
        default=False,
        dest="user",
        help="plot the total user statistics.",
    )

    parser.add_argument(
        "-i",
        "-id",
        "--id",
        "--ID",
        action="store",
        type=int,
        nargs=1,
        default=-1,
        dest="work_id",
        help="plot work with AO3 ID `WORK_ID`.",
    )

    args = parser.parse_args()

    return args


def ao3plot():
    """
    Plot your AO3 statistics based on data you downloaded beforehand using the
    AO3StatScraper. By default, this program will run a dialogue and ask you
    what to plot. Alternately, you can skip this dialogue by using the -t or
    the -i flags.
    """

    from ..plotting import plot_total_stats, plot_work_stats
    from ..configuration import Config
    from ..statsdata import WorkStatsData, TotStatsData
    from ..utils import clear_terminal

    # Setup
    args = _parse_plotter_args()
    conf = Config()
    conf.plotting.prettify = not args.no_pretty

    # Get and check list of dump files.
    tsfiles = TotStatsData.get_dump_file_list(conf)
    wsfiles = WorkStatsData.get_dump_file_list(conf)

    if len(tsfiles) == 0:
        print("Error: Found no total stats files.")
        quit()
    if len(tsfiles) == 1:
        print("Error: Found only 1 total stats file.")
        quit()
    if len(wsfiles) == 0:
        print("Error: Found no work stats files.")
        quit()
    if len(wsfiles) == 1:
        print("Error: Found only 1 work stats file.")
        quit()

    if args.user:
        # Plot user data only
        plot_total_stats(tsfiles, conf)
        quit()
    if args.work_id != -1:
        # argparse returns ID as a list.
        workID = args.work_id[0]
        plot_work_stats(wsfiles, workID, conf)
        quit()

    # If user hasn't specified what to run with cmdline flags,
    # run the dialogue.

    ts_last = TotStatsData(conf, source=tsfiles[-1])
    ws_last = WorkStatsData(conf, source=wsfiles[-1])

    # extract list of work names
    work_data = ws_last.data
    purged = work_data.drop_duplicates(["ID"], ignore_index=True)

    # print out the list of works
    clear_terminal()
    print("Select what work (or total stats) to plot by selecting a number.")
    print("[0] Total Statistics")
    i = 1
    for entry in purged["Title"]:
        print(f"[{i}]", entry)
        i += 1

    # Get what to plot
    index_str = input("Select number to plot: ")
    try:
        index = int(index_str)
    except ValueError:
        print("Invalid input.")
        quit()

    if index == 0:
        plot_total_stats(tsfiles, conf)
        quit()
    else:
        ID = purged["ID"].at[index - 1]
        plot_work_stats(wsfiles, ID, conf)
        quit()


if __name__ == "__main__":
    ao3plot()
