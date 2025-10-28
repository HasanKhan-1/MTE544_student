from math import atan2, asin, sqrt

M_PI=3.1415926535

class Logger:
    
    def __init__(self, filename, headers=["e", "e_dot", "e_int", "stamp"]):
        
        self.filename = filename

        with open(self.filename, 'w') as file:
            
            header_str=""

            for header in headers:
                header_str+=header
                header_str+=", "
            
            header_str+="\n"
            
            file.write(header_str)


    def log_values(self, values_list):

        with open(self.filename, 'a') as file:
            
            vals_str=""
            
            for value in values_list:
                vals_str+=f"{value}, "
            
            vals_str+="\n"
            
            file.write(vals_str)
            

    def save_log(self):
        pass

class FileReader:
    def __init__(self, filename):
        
        self.filename = filename
        
        
    def read_file(self):
        
        read_headers=False

        table=[]
        headers=[]
        with open(self.filename, 'r') as file:

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
                values = line.strip().split(',')
                
                row=[]                
                
                for val in values:
                    if val=='':
                        break
                    row.append(float(val.strip()))

                table.append(row)
        
        return headers, table
    
    

# CHECK Part 3: Implement the conversion from Quaternion to Euler Angles
def euler_from_quaternion(quat):
    """
    Convert quaternion (w in last place) to euler roll, pitch, yaw.
    quat = [x, y, z, w]
    """

    # Extract the components of the quaternion
    x,y,z,w = quat

    # Yaw (z-axis rotation)
    yaw = atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y**2 + z**2))

    return yaw


#CHECK Part 4: Implement the calculation of the linear error
def calculate_linear_error(current_pose, goal_pose):
        
    # Accept either [x,y] or [[x,y], ...] shapes for goal_pose
    if isinstance(goal_pose, (list, tuple)) and len(goal_pose) > 0 and isinstance(goal_pose[0], (list, tuple)):
        gp = goal_pose[0]
    else:
        gp = goal_pose

    dx = gp[0] - current_pose[0]
    dy = gp[1] - current_pose[1]

    error_linear = sqrt(dx*dx + dy*dy)

    return error_linear

#CHECK Part 4: Implement the calculation of the angular error
def calculate_angular_error(current_pose, goal_pose):

    # Normalize goal shape like in linear error
    if isinstance(goal_pose, (list, tuple)) and len(goal_pose) > 0 and isinstance(goal_pose[0], (list, tuple)):
        gp = goal_pose[0]
    else:
        gp = goal_pose

    dx = gp[0] - current_pose[0]
    dy = gp[1] - current_pose[1]

    desired_theta = atan2(dy, dx)
    current_theta = current_pose[2]

    error_angular = desired_theta - current_theta

    # Wrap into [-π, π]
    while error_angular > M_PI:
        error_angular -= 2*M_PI
    while error_angular < -M_PI:
        error_angular += 2*M_PI
    
    return error_angular
