#!/usr/bin/python

import re
import numpy as np
from matplotlib import pyplot as plt


def main():

    # list of files to process
    files = [
        "i_min100.lems.dat",
        "i_min80.lems.dat",
        "i_min60.lems.dat",
        "i_min40.lems.dat",
        "i_min20.lems.dat",
        "i_0.lems.dat",
        "i_20.lems.dat",
        "i_40.lems.dat",
        "i_60.lems.dat",
        "i_80.lems.dat",
        "i_100.lems.dat"
    ]

    v_arr = []
    ih = []
    il = []

    print "voltage\ti_lowest\ti_highest"

    # Find highest, lowest, and steady-state current from each file
    for f in files:
        i_highest = None
        i_lowest = 10000
        i_steady = None

        v_match = re.match("i_(.*)\.lems\.dat", f)
        voltage = v_match.group(1)
        voltage = voltage.replace("min", "-")

        i_file = open(f, "r")

        for line in i_file:
            columns = line.split()

            i = float(columns[1])

            if i < i_lowest:
                i_lowest = i;

            if i > i_highest:
                i_highest = i;

        print str(voltage) + "\t" + str(i_lowest) + "\t" + str(i_highest)

        v_arr.append(float(voltage));
        ih.append(float(i_highest));
        il.append(float(i_lowest));

    x=np.array(v_arr)
    y=np.array(ih)
    plt.figure(1)
    plt.subplot(211)
    plt.plot(x,y)

    y=np.array(il)
    plt.subplot(212)
    plt.plot(x,y)

    plt.show()



if __name__ == '__main__':
    main()

