#!/usr/bin/python

import argparse
import numpy as np
from matplotlib import pyplot as plt

def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="A script that plots current data from a LEMS simulation")

    parser.add_argument('currentFile', type=str, metavar='<tab-separated data file containing time and current values>',
                        help='Name of the file containing time/current data')

    return parser.parse_args()


def main():

    args = process_args()


    i_file = open(args.currentFile, "r")

    t_array = []
    i_array = []
    # Process the inf files
    for line in i_file:
        columns = line.split()

        t = float(columns[0])
        i = float(columns[1])

        t_array.append(t)
        i_array.append(i)

    x=np.array(t_array)
    y=np.array(i_array)
    plt.figure(1)
    plt.subplot(111)
    plt.plot(x,y)

    plt.show()


if __name__ == '__main__':
    main()

