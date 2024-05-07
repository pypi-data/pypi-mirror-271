# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:02:09 2022

@author: Administrator
"""
import math
#point:x(lon),y(lat),t(tamp)
def Rad(d):
    return d * math.pi / 180

class Point:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.time = 0
        self.id=0

def cacl_SED(pointS,pointE,pointM):
    radLonS = Rad(pointS.get_x())
    radLonM = Rad(pointM.get_x())
    radLonE = Rad(pointE.get_x())
    radLatS = Rad(pointS.get_y())
    radLatM = Rad(pointM.get_y())
    radLatE = Rad(pointE.get_y())
    numerator = pointM.get_time() - pointS.get_time()             #算tm-ts (分子)
    denominator = pointE.get_time() - pointS.get_time()           #算te-ts (分母)
    if(denominator==0):
        time_ratio =0
    else:
        time_ratio =numerator/denominator
    #分母（te-ts ）若为0，说明e,s两点时间戳t相同，则有te=ts=tm，则比值为1?否则计算分数的值
    lat = radLatS + (radLatE - radLatS)*time_ratio      #计算m’点的维度
    lon = radLonS + (radLonE - radLonS)*time_ratio   #计算m’点的经度
    lat_diff = lat - radLatM                   #计算m-m’的经度差
    lon_diff = lon - radLonM                #计算m-m’的经度差
    return math.sqrt(lat_diff*lat_diff + lon_diff*lon_diff)  #计算经纬度差的平方和的算术平方根


def TD_TR(point_list,output_point_list,Dmax):
    if len(point_list)<2:
        return 0
    start_index=0
    end_index=len(point_list)-1

    #起止点必定是关键点,但是作为递归程序此步引入了冗余数据,后期必须去除
    output_point_list.append(point_list[start_index])
    output_point_list.append(point_list[end_index])

    if start_index<end_index:
        index=start_index+1        #工作指针,遍历除起止点外的所有点
        max_vertical_dist=0        #路径中离弦最远的距离
        key_point_index=0        #路径中离弦最远的点,即划分点

        while(index<end_index):
            cur_vertical_dist=cacl_SED(point_list[start_index],point_list[end_index],point_list[index])
            if cur_vertical_dist>max_vertical_dist:
                max_vertical_dist=cur_vertical_dist
                key_point_index=index        #记录划分点
            index+=1

        #递归划分路径
        if max_vertical_dist>=Dmax:
            TD_TR(point_list[start_index:key_point_index],output_point_list,Dmax)
            TD_TR(point_list[key_point_index:end_index],output_point_list,Dmax)

#主程序
# point_list=[]
# output_point_list=[]

# #将待处理的数据写入
# fd=open(r"Sample.txt",'r')
# idx=0
# for line in fd:
#     line=line.strip()
#     longitude=float(line.split(" ")[0])
#     latitude=float(line.split(" ")[1])
#     time=float(line.split(" ")[2])
#     point_list.append((longitude,latitude,time,idx))
#     idx += 1  # did not use the point calss ,but just
# fd.close()


# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '0.00045'")
# argps = parser.parse_args()
# Dmax = eval(argps.args)#0.00045#0.0000008#

def TD_TR_one_traj(point_list,Dmax):
    Poi_to_num={}
    for enu,i in enumerate(point_list):
        Poi_to_num[i]=enu
    output_point_list=[]
    TD_TR(point_list,output_point_list,Dmax=Dmax)

    output_point_list=list(set(output_point_list))        #去除递归引入的冗余数据
    output_point_list=sorted(output_point_list,key=lambda x:Poi_to_num[x])

    # 按照time排序,--但是后面面对重复的点需要单向处理
    # 好吧 这里的递归是完全不按照顺序的，考虑增加一个id变量来重新排序
    # print(output_point_list)
    return output_point_list

def TD_TR_batch(orig_list_of_Points,Dmax):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        compressed_list_of_Points.append(TD_TR_one_traj(traj,Dmax))
    # print('TD_TR_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points
