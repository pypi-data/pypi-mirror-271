# import utils_copy

import os
from TrajCompress.src import basic_notion

def get_sample():
    orig_list_of_Points = []  
    this_traj=[]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f'you are getting sample from {script_dir}, using __file__:{__file__}')
    file_path = os.path.join(script_dir, '..', 'assets', 'Sample.txt')
    with open(file_path) as f:
        for line in f:
            a,o,t=list(map(eval,line.split()))
            this_traj.append(basic_notion.Point.Point(a,o,t))
    orig_list_of_Points.append(this_traj)
    orig_list_of_Points.append(this_traj[:20])
    return orig_list_of_Points