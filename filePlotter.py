# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

import matplotlib.pyplot as plt
from utilities import FileReader
from utilities import Logger

# This function is modified for laser data currently, regular code commented out
def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file() 
    time_list=[]
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    #for i in range(0, len(headers) - 1):
    #    plt.plot(time_list, [lin[i] for lin in values], label= headers[i]+ " spiral")
    #plt.plot([lin[0] for lin in values], [lin[1] for lin in values])
    
    x = [row[0] for row in values]
    y = [row[1] for row in values]
    plt.plot(x, y, marker = 'o', label="x-y coordinates line")

    
    plt.legend()
    plt.grid()
    plt.title(filename)
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.show()
    
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)
