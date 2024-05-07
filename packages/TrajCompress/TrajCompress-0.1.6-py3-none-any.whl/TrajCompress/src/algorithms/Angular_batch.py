# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 18:41:38 2022

@author: Administrator
"""
import math
# import utils_copy
from .. import basic_notion as utils_copy

PI = 3.1415926


class Point(object):
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.time = 0
    # def gpsreader(filename):         #读数据 存入points
    #     file=open(filename,'r')
    #     for n,line in enumerate(file):
    #         if not line:
    #             break
    #         li=line.split(" ")
    #         point=Point()
    #         point.lat =float(li[0])
    #         point.lon = float(li[1])
    #         point.time = float(li[2].strip())
    #         P.append(point)
    #     # P.pop()#???? why pop --jijivski
    #     return

    def Standardization(a):
        if a<0:
            a=a+2*PI
        if a>=2*PI:
            a=a-2*PI
        return a

    def AngularDeviation(P,i):
        d1 = math.atan2(P[i].lon-P[i-1].lon,P[i].lat-P[i-1].lat)
        d2 = math.atan2(P[i+1].lon-P[i].lon,P[i+1].lat-P[i].lat)
        deviation = min(abs(d2-d1),2*PI-abs(d2-d1))
        if d1 >=0:
            if(d2>=d1+PI or d2<=d1):
                return -deviation
        else:
            if(d2>d1-PI and d2<d1):
                return -deviation
        return deviation

def Angular(points,error_t):# input is a list of util Points
    P = []
    R = []

    for i in points[1:]:
        temppoint = Point()
        temppoint.lon = i.get_x()
        temppoint.lat = i.get_y()
        temppoint.time = i.get_time()
        P.append(temppoint)


    R.append(0)
    deviation=0
    for i in range(1,len(P)-1):
        deviation = deviation +Point.AngularDeviation(P,i)
        if(abs(deviation)>error_t):
            R.append(i)
            deviation = 0

    R.append(len(P)-1)
    return [points[x] for x in R] # to util points

def change_to_points(input_list):
    output_list=[]
    for i in input_list:
        util_point=utils_copy.Point.Point(i.x,i.y,i.time) # pkg.module.class
        output_list.append(util_point)
    return output_list


def Angular_batch(orig_list_of_Points,error_t):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        compressed_list_of_Points.append(Angular(traj,error_t))
    print('Angular_batch_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points



# def fast_way(DUPLICATES):
#     return list(set(DUPLICATES))
def fast_way(DUPLICATES):
    return DUPLICATES
    # return list(set(DUPLICATES))


# error = PI/4
# error_t = error/2
# filename='Sample.txt'
# save_filename='Angular_output.txt'
#
# # with open(filename) as f:
# #     print(f.readline())
#     # print('f[0]',f[0])
#
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '3.1415926/4,3.1415926/8'")
# argps = parser.parse_args()
#
# # speed_threshold,ori_threshold = eval(argps.args)
# error,error_t=eval(argps.args)
#
# # print(error,error_t)
#

# print('haha',len(cmp_buffer))
# fd=open(save_filename,'w')          #写入并输出结果
# for i in range(len(cmp_buffer)):
#     fd.write("{} {} {}\n".format(P[cmp_buffer[i]].lat,P[cmp_buffer[i]].lon,P[cmp_buffer[i]].time))
# fd.close()
