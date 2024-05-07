# -*- coding: utf-8 -*-
"""
Created on Wed May 18 20:04:54 2022

@author: lenovo
"""

import math
import pickle

from .. import basic_notion as utils_copy

class Point(object):
    def __init__(self,lat,lon,time):
        self.lat = lat
        self.lon = lon
        self.time = time
    
        
class GPSPointWithSED(object):
    def __init__(self,point,sed):
        self.point = point
        self.sed=sed
        
#计算SED
def perpendicular_euclidean_dist(start_point: Point, mid_point: Point, end_point: Point):
    start_x,start_y,start_z = start_point.lat,start_point.lon,start_point.time
    end_x,end_y,end_z=end_point.lat,end_point.lon,end_point.time
    mid_x,mid_y,mid_z=mid_point.lat,mid_point.lon,mid_point.time	

    if any(val is None for val in [start_x, start_y, start_z, end_x, end_y, end_z, mid_x, mid_y, mid_z]):	
        print("Distance calculation needs coordinate coversion from lat/lon to Cartesian one") 
        exit()
    eps=1e-5
    vec_start_mid = (mid_x-start_x+eps , mid_y-start_y+eps , mid_z-start_z+eps)
    vec_start_end =(end_x-start_x+eps , end_y-start_y+eps , end_z-start_z+eps)

    if vec_start_end[0]==0 and vec_start_end[1]== 0:
        print('start and End points are the same one!')
        exit()	
	
    projected_x = start_x+ vec_start_mid[2] // vec_start_end[2] * vec_start_end[0]	
    projected_y = start_y+ vec_start_mid[2] // vec_start_end[2] * vec_start_end[1]	
    return math.sqrt((projected_x-mid_x)**2 + (projected_y -mid_y)**2)	


#需要注意的是：这里用户指定内存大小为cmp_ratio，但实际要多一个点的空间，这样才能计算buffer中最后一个点的SED
def STTrace(points,cmp_ratio):      #参数为用户指定的内存大小，这里简作为点的个数处理
    max_buffer_size = cmp_ratio  
    buffer = []                #buffer是最终结果集合
    buffer.append(GPSPointWithSED(points[0], 0))
   
    if max_buffer_size > 2:
        
        buffer.append(GPSPointWithSED(points[1], 0))
        for i in range(2,len(points)) :
            buffer.append(GPSPointWithSED(points[i], 0))
            # Compute SED for previous point
            segment_start = buffer[len(buffer) - 3].point
            segment_end = buffer[len(buffer) - 1].point
            buffer[len(buffer) - 2].sed = perpendicular_euclidean_dist(segment_start, buffer[len(buffer) - 2].point, segment_end)
            
         
            # Buffer full, remove a point
            if len(buffer) > max_buffer_size:   
                to_remove = max_buffer_size       #应删掉点的下标
                for buf in range(1,max_buffer_size):
                    if to_remove is max_buffer_size or buffer[buf].sed < buffer[to_remove].sed:
                        to_remove = buf
                if to_remove - 1 > 0:
                    buffer[to_remove - 1].sed = perpendicular_euclidean_dist(buffer[to_remove - 2].point, buffer[to_remove - 1].point, buffer[to_remove + 1].point)
                if to_remove + 1 < len(buffer) - 1:
                    buffer[to_remove + 1].sed = perpendicular_euclidean_dist(buffer[to_remove - 1].point, buffer[to_remove + 1].point, buffer[to_remove + 2].point)
                del buffer[to_remove]
        # i += 1#why +=1 ? what is i?
    else:
        buffer.append(GPSPointWithSED(points[len(points) - 1], 0))
    return change_to_util_points([i.point for i in buffer])


def STTrace_batch(orig_list_of_Points,cmp_ratio):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        traj=change_to_local_points(traj)
        compressed_list_of_Points.append(STTrace(traj,cmp_ratio))
    # print('OPW_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points


# import utils_copy
def change_to_util_points(input_list):
    '''
    change current Point class to util class,
    list of points
    '''
    output_list=[]
    for i in input_list:
        util_point=utils_copy.Point.Point(i.lat,i.lon,i.time) # pkg.module.class
        output_list.append(util_point)
    return output_list

def change_to_local_points(input_list):
    '''
    change util Point class to local Point class
    '''
    output_list=[]
    for i in input_list:
        local_point=Point(i.get_x(),i.get_y(),i.get_time()) # pkg.module.class
        output_list.append(local_point)
    return output_list

# #主程序
# # print('主程序')
# points=[]         #原数据集合
# file=open('Sample.txt','r')    #读数据 存入points
# for n,line in enumerate(file):
#     if not line:
#         break
#     li=line.split(" ")
#     point=Point()
#     point.lat =float(li[0])
#     point.lon = float(li[1])
#     point.time = float(li[2].strip())
#     points.append(point)
#
# # cmp_ratio = eval(input('number of points reserved (default 20: just enter)') or '20')     #用户指定的内存大小约束
# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '20'")
# argps = parser.parse_args()
# cmp_ratio = int(eval(argps.args))#150#$#eval(input('max_error default 0.7') or '0.7')
# # print(max_error)
#
# cmp_buffer = STTrace(cmp_ratio)  #最终结果集合
# # print('line 101!!!!!!!!!')
# fd=open(r"STTrace_output.txt",'w')
# for i in range(len(cmp_buffer)):
#     fd.write("{} {} {}\n".format(cmp_buffer[i].point.lat,cmp_buffer[i].point.lon,cmp_buffer[i].point.time))
# fd.close()

