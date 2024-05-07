# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 13:35:51 2022

@author: lenovo
"""
from .. import basic_notion as utils_copy
import math

class Point(object):
    def __init__(self,lat,lon,time):
        self.lat = lat
        self.lon = lon
        self.time = time

def cacl_angle(p1:Point,p2:Point):
    lat_diff = p2.lat - p1.lat
    lon_diff = p2.lon - p1.lon
    return math.atan2(lon_diff, lat_diff)

def safe_oriten(res_b:Point,res_c:Point,points_c:Point,points_d:Point,points_e:Point):
    angle_res_bc = cacl_angle(res_b, res_c)
    angle_de = cacl_angle(points_d, points_e)
    angle_res_bc_de = angle_de - angle_res_bc
    angle_points_cd = cacl_angle(points_c, points_d)
    angle_points_cd_de = angle_de - angle_points_cd
    if abs(angle_res_bc_de) > ori_threshold or abs(angle_points_cd_de) > ori_threshold:
        return False
    else:
        return True
    
def cacl_distance(p1:Point,p2:Point): 
    earth_r = 6371010
    degree2radian = math.pi / 180  # Assume the given lat/lon is in degree, while the cos/sin requires radian
    lat1, lon1 = p1.lat, p1.lon
    lat2, lon2 = p2.lat, p2.lon
    diff_lat, diff_lon = lat2 - lat1, lon2 - lon1
    a = (math.sin(diff_lat * degree2radian / 2))**2 + math.cos(lat1 * degree2radian) * math.cos(lat2 * degree2radian) * ((math.sin(diff_lon * degree2radian / 2))**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return earth_r * c

def cacl_speed(a:Point,b:Point):
    return cacl_distance(a,b)/max(1e-6,(b.time-a.time))

def safe_speed(res_b:Point,res_c:Point,points_c:Point,points_d:Point,points_e:Point):
    res_speed=cacl_speed(res_b,res_c)
    points_speed=cacl_speed(points_c,points_d)
    max_res_distance = (points_e.time - points_d.time)*(res_speed + speed_threshold)
    min_res_distance = (points_e.time - points_d.time)*(res_speed - speed_threshold)
    max_points_distance = (points_e.time - points_d.time)*(points_speed + speed_threshold)
    min_points_distance = (points_e.time - points_d.time)*(points_speed - speed_threshold)
    distance_de = cacl_distance(points_d, points_e)
    if (distance_de <= max_res_distance and distance_de >= min_res_distance and distance_de <= max_points_distance and distance_de >= min_points_distance):
        return True
    else:
        return False

def threshold(points,threshold_tup):
    result=[]
    global speed_threshold,ori_threshold
    speed_threshold, ori_threshold=threshold_tup
    result.append(points[0])
    result.append(points[1])
    if len(points)>2:
        for i in range(2,len(points)-1): ## really careless ,zx!
            if(safe_speed(result[len(result)-2],result[len(result)-1],points[i-2],points[i-1],points[i])\
                and safe_oriten(result[len(result)-2],result[len(result)-1],points[i-2],points[i-1],points[i])):
                continue
            else:
                result.append(points[i])
        result.append(points[len(points)-1])# 最后一行没问题，但是前面的在len=2的时候，会重复
    elif len(points)==2:
        pass
        # result.append(points[len(points)-1])
    else:
        assert len(points)!=1,'len(points) should not be 1'
    return change_to_util_points(result)

def threshold_batch(orig_list_of_Points, threshold_tup):
    compressed_list_of_Points = []
    # orig_list_of_Points=list(map(change_to_local_points,compressed_list_of_Points))
    for traj in orig_list_of_Points:
        traj=change_to_local_points(traj)
        compressed_list_of_Points.append(threshold(traj, threshold_tup))
    # print('OPW_batch ',len(orig_list_of_Points),' have done')
    # return list(map(change_to_util_points,compressed_list_of_Points))
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
# points=[]
# #print("请输入速度误差阈值、角度误差阈值，中间用逗号分割")
# # speed_threshold,ori_threshold = eval(input(
# #     "\请输入速度误差阈值、角度误差阈值，中间用逗号分割,enter to defalut '0.5,0.5" ) or '0.5,0.5')
