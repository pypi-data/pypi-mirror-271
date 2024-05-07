# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 17:48:15 2022

@author: Administrator
"""
import math

    
def cacl_distance(points):
    distance=[]
    for i in range(1, len(points)):
        distance.append(math.sqrt(math.pow(points[i].get_x()-points[i-1].get_x(),2)+math.pow(points[i].get_y() - points[i - 1].get_y(), 2)))
    return distance

def cacl_angle(points):
    anglee=[]
    for i in range(1,len(points)):
        lat_diff = points[i].get_x() - points[i-1].get_x()
        lon_diff = points[i].get_y() - points[i-1].get_y()
        anglee.append(math.atan2(lon_diff,lat_diff))
    return anglee

def Dead_Reckoning(points,eps):
    n=len(points)
    max_d = 0
    start_idx = 0
    d=cacl_distance(points)
    anglee=cacl_angle(points)
    simplifindex=[]
    simplifindex.append(0)
    for i in range(2, n):
        max_d = max_d + abs(d[i - 1] * math.sin(anglee[i - 1] - anglee[start_idx]))
        if abs(max_d)>eps:
            max_d =0
            simplifindex.append(i-1)
            start_idx=i-1
    if simplifindex[len(simplifindex)-1]!=n-1:
        simplifindex.append(n-1)
    simplified_points = [points[x] for x in simplifindex]
    return simplified_points

def Dead_Reckoning_batch(orig_list_of_Points,epsilon):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        compressed_list_of_Points.append(Dead_Reckoning(traj,epsilon))
    print('Dead_Reckoning_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points

