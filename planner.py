# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self):
        timeStep = 0.03
        trajectory = []
        # Parabola
        for x in range(0, int(1.5/timeStep)):
          trajectory.append([x*timeStep, (timeStep*x)**2])

        # Sigmoid
        #for x in range(0, int(2.5 / timeStep)):
        #    trajectory.append([x * timeStep, 2 / (1 + 2.71828 ** (-2 * x * timeStep)) - 1])
        
        print(f"First point: {trajectory[0]}")
        print(f"Last point: {trajectory[-1]}")
        print(f"Total points: {len(trajectory)}")

        return trajectory
        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        # return 

