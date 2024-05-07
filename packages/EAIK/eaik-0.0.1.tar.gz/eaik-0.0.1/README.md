# EAIK: A Toolbox for Efficient Analytical Inverse Kinematics
This is a preliminary version of the implementation of the EAIK toolbox. The functionality is currently limited and will be extended during the next weeks! Keep updated to not miss out!
See our [Project page](https://https://eaik.cps.tum.de/) fore further information.

## Overview
The problem of calculating the inverse kinematics appears for any manipulator with arbitrary degrees of freedom.
This problem might have exactly one, multiple, infinite, or no solution at all depending on the number of joints, their types, and their respective placement ( i.e., the manipulator's joint configuration).

Due to this characteristic of the inverse kinematic problem, the existence of a closed-form solution is not guaranteed.
Current methods for general closed-form derivation comprise the above-mentioned requirements in their final solution (given a solvable manipulator) but suffer from complex setup procedures.
With this toolbox, we propose a method for automatic inverse kinematic derivation.
We exploit intersecting and parallel axes to remodel a manipulator's kinematic chain.

This allows us for a hard-coded decomposition of its inverse kinematics into pre-solved subproblems.
This approach surpasses current analytical methods in terms of usability and derivation speed without compromising on computation time or the completeness of the overall solution set.

## Credits
See our [Project page](https://https://eaik.cps.tum.de/) fore further information.

We adopt the solutions and overall canonical subproblem set from [Elias et al.](https://arxiv.org/abs/2211.05737).
Check out their publication and [implementation](https://github.com/rpiRobotics/ik-geo). 

## Example
We currently provide support for CSV files containing the homogeneous transformations of each joint in zero-pose with respect to the basis, as well as [ROS URDF](http://wiki.ros.org/urdf) files.

#### URDF
```
import numpy as np
import random

from eaik.IK_URDF import Robot

def test_urdf(path, batch_size):

    bot = Robot(path)

    # Example desired pose
    test_angles = []
    for i in range(batch_size):
        rand_angles = np.array([random.random(), random.random(), random.random(), random.random(), random.random(), random.random()])
        rand_angles *= 2*np.pi
        test_angles.append(rand_angles)
    poses = []
    for angles in test_angles:
       poses.append(bot.fwdKin(angles))

    for pose in poses:
        ik_solution = bot.IK(pose)
        
test_urdf("../tests/UR5.urdf", 100)
```

#### CSV

```
from eaik.IK_CSV import Robot
import numpy as np
import csv

def load_test_csv(path):
    bot = Robot(path, False)

    total_num_ls = 0
    error_sum = 0
    total_num_analytic = 0
    num_no_solution = 0
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        T01 = None
        T02 = None
        T03 = None
        T04 = None
        T05 = None
        T06 = None

        for row in reader:
            T06 = np.array([[np.float64(row['6-T00']), np.float64(row['6-T01']), np.float64(row['6-T02']), np.float64(row['6-T03'])],
                            [np.float64(row['6-T10']), np.float64(row['6-T11']), np.float64(row['6-T12']), np.float64(row['6-T13'])], 
                            [np.float64(row['6-T20']), np.float64(row['6-T21']), np.float64(row['6-T22']), np.float64(row['6-T23'])],
                            [np.float64(row['6-T30']), np.float64(row['6-T31']), np.float64(row['6-T32']), np.float64(row['6-T33'])]])
            
            
            ik_solutions = bot.IK(T06)


load_test_csv("./tests/robot_1.csv")

```