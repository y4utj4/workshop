#!/usr/bin/python3
import argparse
import csv
import sys
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main():
    # setup arguments
    parser = argparse.ArgumentParser(description='Put description here')
    parser.add_argument('-i', '--infile', help='input file for script to process')
    args = parser.parse_args()


    red_action = []
    red_dates = []
    blue_action = []
    blue_dates = []

    with open(args.infile, 'r') as csv_file:
        r = csv.reader(csv_file, delimiter=',')
        next(r)
        for lines in r:
            red_action.append(lines[0])
            red_dates.append(lines[1])
            blue_action.append(lines[2])
            blue_dates.append(lines[3])
    blue_action = filter(None, blue_action)
    blue_dates = filter(None, blue_dates)

    red_dates = [datetime.strptime(d, "%m/%d/%Y %H:%M:%S") for d in red_dates]
    blue_dates = [datetime.strptime(d, "%m/%d/%Y %H:%M:%S") for d in blue_dates]

    levels = np.tile([-1,1,-3,3,-5,5,-7,7,-9,9,-11,11, -13,13],
                 int(np.ceil(len(red_dates)/6)))[:len(red_dates)]
    blue_levels = np.tile([-2,2,-4,4,-6,6,-8,8],
                 int(np.ceil(len(red_dates)/6)))[:len(red_dates)]

    matplotlib.rcParams['font.size'] = 9.5
    plt.style.use('dark_background')
    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(18, 8), constrained_layout=True)

    ax.set_title("Internal Pentest Timeline", fontsize=20)
    ax.set_xlabel('Date', fontsize=20)

    markerline, stemline, baseline = ax.stem(red_dates, levels,
                                             linefmt="#FFFFFF", basefmt="white",
                                             use_line_collection=True)
    
    plt.setp(markerline, mec="k", mfc="w", zorder=3)
    
    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(red_dates)))
    
    # annotate lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
 
    for d, l, r, va in zip(red_dates, levels, red_action, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                    textcoords="offset points", va=va, ha="center", 
                    bbox=dict(boxstyle="round", fc=("#b30000"), ec=("black")))

    for d, l, r, va in zip(blue_dates, blue_levels, blue_action, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                    textcoords="offset points", va=va, ha="center", 
                    bbox=dict(boxstyle="round", fc=("#006b8f"), ec=("black")))

    # format xaxis with 1 day intervals
    ax.get_xaxis().set_major_locator(mdates.DayLocator(interval=1))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%m %d"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    
    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)
    
    ax.margins(y=0.1)
    plt.show()
if __name__ == '__main__':
    main()
