# -*- coding: utf-8 -*-
"""
Created on Sat May 21 17:05:52 2022

@author: lenovo
"""

import math

def Rad(d):
    return d * math.pi / 180

def Geodist(point1,point2):
    radLat1 = Rad(point1.get_y())
    radLat2 = Rad(point2.get_y())
    delta_lon = Rad(point1.get_x()- point2.get_x())
    top_1 = math.cos(radLat2) * math.sin(delta_lon)
    top_2 = math.cos(radLat1) * math.sin(radLat2) - math.sin(radLat1) * math.cos(radLat2) * math.cos(delta_lon)
    top = math.sqrt(top_1 * top_1 + top_2 * top_2)
    bottom = math.sin(radLat1) * math.sin(radLat2) + math.cos(radLat1) * math.cos(radLat2) * math.cos(delta_lon)
    delta_sigma = math.atan2(top, bottom)
    distance = delta_sigma * 6378137.0

    return round(distance,3)

#点弦距离
def get_vertical_dist(pointA,pointB,pointX):
    a=math.fabs(Geodist(pointA,pointB))

    #当弦两端重合时,点到弦的距离变为点间距离
    if a==0:
        return math.fabs(Geodist(pointA,pointX))

    b=math.fabs(Geodist(pointA,pointX))
    c=math.fabs(Geodist(pointB,pointX))
    p=(a+b+c)/2
    S=math.sqrt(math.fabs(p*(p-a)*(p-b)*(p-c)))

    vertical_dist=S*2/a

    return vertical_dist

#递归压缩
def DP_compress(point_list,output_point_list,Dmax):
    start_index=0
    end_index=len(point_list)-1
    assert len(point_list)>1, f'len(point_list) is {len(point_list)},'
    output_point_list.append(point_list[start_index])
    output_point_list.append(point_list[end_index])

    if start_index<end_index:
        index=start_index+1        #工作指针,遍历除起止点外的所有点
        max_vertical_dist=0        #路径中离弦最远的距离
        key_point_index=0        #路径中离弦最远的点,即划分点

        while(index<end_index):
            cur_vertical_dist=get_vertical_dist(point_list[start_index],point_list[end_index],point_list[index])
            if cur_vertical_dist>max_vertical_dist:
                max_vertical_dist=cur_vertical_dist
                key_point_index=index        #记录划分点
            index+=1

        #递归划分路径
        if max_vertical_dist>=Dmax:
            if start_index+1<key_point_index:
                DP_compress(point_list[start_index:key_point_index],output_point_list,Dmax)
            if key_point_index + 1 < end_index:
                DP_compress(point_list[key_point_index:end_index],output_point_list,Dmax)


def DP_one_traj(point_list,Dmax):
    Poi_to_num={}
    for enu,i in enumerate(point_list):
        Poi_to_num[i]=enu
    output_point_list=[]
    DP_compress(point_list,output_point_list,Dmax=Dmax)

    output_point_list=list(set(output_point_list))        #去除递归引入的冗余数据
    output_point_list=sorted(output_point_list,key=lambda x:Poi_to_num[x])

    # 按照time排序,--但是后面面对重复的点需要单向处理
    # 好吧 这里的递归是完全不按照顺序的，考虑增加一个id变量来重新排序
    # print(output_point_list)
    return output_point_list

def DP_batch(orig_list_of_Points,Dmax):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        compressed_list_of_Points.append(DP_one_traj(traj,Dmax))
    # print('TD_TR_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points


# #平均误差
# def get_MeanErr(point_list,output_point_list):
#     Err=0
#
#     start_index=0
#     end_index=len(output_point_list)-1
#
#     while(start_index<end_index):        #遍历所有关键点
#         #选取两相邻关键点
#         pointA_id=int(output_point_list[start_index][2])
#         pointB_id=int(output_point_list[start_index+1][2])
#
#         id=pointA_id+1        #工作指针,用于遍历非关键点
#         while(id<pointB_id):        #遍历两关键点之间的非关键点
#             Err+=get_vertical_dist(output_point_list[start_index],output_point_list[start_index+1],point_list[id])
#             id+=1
#
#         start_index+=1
#
#     return Err/len(point_list)

#主程序
# point_list=[]
# output_point_list=[]
# times=[]
# #将处理后的数据写入内存
# fd=open(r"Sample.txt",'r')
# id=0
# for line in fd:
#     line=line.strip()
#     # id=int(line.split(",")[0])
#
#     longitude=float(line.split(" ")[0])
#     latitude=float(line.split(" ")[1])
#     point_list.append((longitude,latitude,id))
#     id += 1
#     time=float(line.split(" ")[2])
#     times.append(int(float(time)))
# fd.close()
#
# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '8'")
# argps = parser.parse_args()
# # speed_threshold,ori_threshold = eval(argps.args)
# Dmax=int(eval(argps.args))
#
# DP_compress(point_list,output_point_list,Dmax=Dmax)
#
# output_point_list=list(set(output_point_list))        #去除递归引入的冗余数据
# output_point_list=sorted(output_point_list,key=lambda x:x[2])        #按照id排序
#
# #将压缩数据写入输出文件
# fd=open(r"DP_output.txt",'w')
# for point in output_point_list:
#     fd.write("{} {} {}\n".format(point[0],point[1],times[point[2]]))
# fd.close()

# print("compression rate={}/{}={}".format(len(point_list),len(output_point_list),len(output_point_list)/len(point_list)))
# print("mean error:{}".format(get_MeanErr(point_list,output_point_list)))
