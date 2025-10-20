# This script converts the laser scan data
import numpy as np
import matplotlib.pyplot as plt
from utilities import FileReader
from utilities import Logger
from math import sin, cos, isfinite
import subprocess

# Copied from motions.py
CIRCLE=0; SPIRAL=1; ACC_LINE=2
motion_types=['circle', 'spiral', 'line']
motion_type = ACC_LINE
filename = 'lab_1_prt_6/laser_content_'+str(motion_types[motion_type])+'.csv'
#headers, values=FileReader(filename).read_file() 

read_headers=False

table=[]
headers=[]
with open(filename, 'r') as file:
    # Skip the header line
    
    if not read_headers:
        for line in file:
            values=line.strip().split(',')

            for val in values:
                if val=='':
                    break
                headers.append(val.strip())

            read_headers=True
            break
    
    next(file)
    
    # Read each line and extract values
    for line in file:

        # laser data has weird formatting, so we need to clean it up
        line = line.replace("array('f',", "").replace(")", "").replace("]", "").replace("[", "").strip()
        values = line.strip().split(',')
        
        row=[]                
        
        for val in values:
            if val=='':
                break
            row.append(float(val.strip()))

        table.append(row)

ranges = table[:][:-2]
angle_increment = table[0][-2]
laser_time = table[0][-1]

# Set up a new logger to save the modified data
laser_logger=Logger('laser_modified_'+str(motion_types[motion_type])+'.csv', headers=["x", "y", "stamp"])

# First row of data
i = 1

# Convert polar to Cartesian and log the new values
for j in range(len(ranges[0])-1):
    if not isfinite(ranges[i][j]):
        continue
    x = ranges[i][j] * cos(angle_increment * j)
    y = ranges[i][j] * sin(angle_increment * j)
            
    log_data = [x, y, laser_time]  #,angle_increment * i, laser_time
    laser_logger.log_values(log_data)

# Now plot the modified data using the plotting script
subprocess.run(["python3", "filePlotter.py", "--files", 'laser_modified_'+str(motion_types[motion_type])+'.csv'])
