# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:02:31 2022

@author: lenovo
"""


import math
import os
import sys

from ..basic_notion import Point

class GPSPointWithSED(object):
    def __init__(self,point,sed):
        self.point = point
        self.sed=sed

def synchronized_euclidean_distance(start_point: Point, mid_point: Point, end_point: Point) -> float:

    
    start_x, start_y, start_z = start_point.get_cx(), start_point.get_cy(), start_point.get_cz()
    end_x, end_y, end_z = end_point.get_cx(), end_point.get_cy(), end_point.get_cz()
    mid_x, mid_y, mid_z = mid_point.get_cx(), mid_point.get_cy(), mid_point.get_cz()

    if any(val is None for val in [start_x, start_y, start_z, end_x, end_y, end_z, mid_x, mid_y, mid_z]):
        print("Distance calculation needs coordinate coversion from lat/lon to Cartesian one")
        sys.exit()

    start_t, end_t, mid_t = start_point.get_time(), end_point.get_time(), mid_point.get_time()

    if start_t is None or end_t is None or mid_t is None:
        print('Time stamp is missing from input!')
        sys.exit()

    if start_t <= mid_t <= end_t:
        project_ratio = (mid_t - start_t) / (end_t - start_t+0.0000001)

        projected_x = start_x + project_ratio * (end_x - start_x)
        projected_y = start_y + project_ratio * (end_y - start_y)
        projected_z = start_z + project_ratio * (end_z - start_z)

        return math.sqrt((projected_x - mid_x) ** 2 + (projected_y - mid_y) ** 2 + (projected_z - mid_z) ** 2)
    else:
        print("Please check the time stamps of input!")
        sys.exit()

def bottom_up(points,max_error):
    for p in points:
        p.latlon2cartesian()

    res=[]
    res.append(GPSPointWithSED(points[0], float('inf')))     
    res.append(GPSPointWithSED(points[1], 0))
    for i in range(2,len(points)) :
        res.append(GPSPointWithSED(points[i], 0))
        # Compute SED for previous point
        segment_start = res[len(res) - 3].point
        segment_end = res[len(res)-1].point
        res[len(res) - 2].sed = synchronized_euclidean_distance(segment_start, res[len(res) - 2].point, segment_end)
    res.append(GPSPointWithSED(points[len(points)-1], float('inf')))
    while True:
        to_remove = 1    
        for buf in range(1,len(res)-1):
            if res[buf].sed < res[to_remove].sed:
               to_remove = buf
        if res[to_remove].sed<=max_error:
            if to_remove - 1 > 0:
                res[to_remove - 1].sed = synchronized_euclidean_distance(res[to_remove - 2].point, res[to_remove - 1].point, res[to_remove + 1].point)
            if to_remove + 1 < len(res) - 1:
                res[to_remove + 1].sed = synchronized_euclidean_distance(res[to_remove - 1].point, res[to_remove + 1].point, res[to_remove + 2].point)
            del res[to_remove]
        else:
            break
    return [i.point for i in res]


def bottom_up_batch(orig_list_of_Points,max_error):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        compressed_list_of_Points.append(bottom_up(traj,max_error))
    # print('OPW_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points



# result = bottom_up(max_error)


#
# points=[]
# # print(os.getcwd())
# # print(sys.argv[0])
# # print('open?')
#
# file=open('Sample.txt','r')
# # file=open('../Zhou/Sample.txt','r')
#
# # print('open!')
# for n,line in enumerate(file):
#     if not line:
#         break
#     li=line.split(" ")
#     point=Point(float(li[0]),float(li[1]),float(li[2].strip()))
#     point.latlon2cartesian()
#     points.append(point)
#
# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '90'")
# argps = parser.parse_args()
# max_error = int(eval(argps.args))#150#$#eval(input('max_error default 0.7') or '0.7')
# # print(max_error)
# result = bottom_up(max_error)
#
# fd=open(r"bottom-up_output.txt",'w')
# for i in range(len(result)):
#     fd.write("{} {} {}\n".format(result[i].point._x,result[i].point._y,int(result[i].point._t)))
# fd.close()
# print("压缩比：{}".format(len(result)/len(points)))


