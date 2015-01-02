#!/usr/bin/python

from decimal import Decimal
import glob
import re
import numpy as np
from matplotlib import pyplot as plt


def main():

    # Build dict of voltages and their corresponding files
    filenames = glob.glob('./i_*.lems.dat')
    file_dict = {}
    for name in filenames:
        v_match = re.match("\./i_(.*)\.lems\.dat", name)
        voltage = v_match.group(1)
        voltage = voltage.replace("min", "-")
        voltage = Decimal(voltage)
        file_dict[voltage] = name

    v_arr = []
    ih = []
    il = []

    print "voltage (mV)   i_lowest (A)   i_highest (A)"

    # Find highest, lowest, and steady-state current from each file
    voltages = file_dict.keys()
    voltages.sort()
    for voltage in voltages:
        i_highest = None
        i_lowest = 10000
        i_steady = None

        i_file = open(file_dict[voltage], "r")

        for line in i_file:
            columns = line.split()

            i = float(columns[1])

            if i < i_lowest:
                i_lowest = i;

            if i > i_highest:
                i_highest = i;

        print "{0:>12}{1:>15E}{2:>15E}".format(voltage, i_lowest, i_highest)

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

