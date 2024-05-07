# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 13:43:50 2022

@author: Administrator
"""
import math
# import utils_copy
from .. import basic_notion as utils_copy
#import numpy
class Interval:
    str="20081106231922"
    R=[]
    save_path=None
    averagerate=0
    class Point:
        def __init__(self):
            #instance fields found by Java to Python Converter:
            self.x = 0
            self.y = 0
            self.time = None
            self.num = 0
    #将角度约束在[0,2pi]之间
    def Standardization(a):
        if a<0:
            a=a+2*math.pi
        if a>=2*math.pi:
            a=a-2*math.pi
        return a 
    #定义区间
    class Range:
        def __init__(self):
            #instance fields found by Java to Python Converter:
            self.left = 0
            self.right = 0
    #给出一个角度的规范化后的扇形区域
    def Fan(d,error):
        range=Interval().Range()
        range.left=Interval.Standardization(d+error)
        range.right=Interval.Standardization(d-error)
        return range
    #判断两个区间是否有交集，True代表无交集
    def notInt(ComSub,range):
        if(ComSub.left<ComSub.right):  #ComSub的区间跨（0，1）方向
            if(range.left>range.right):
                if(range.right>ComSub.left and range.left<ComSub.right):
                    return True
        else:           #ComSub的区间不跨（0，1）方向
            if(range.left<range.right):
                if(ComSub.right>range.left and ComSub.left<range.right):
                    return True
            elif(range.left<ComSub.right or range.right>ComSub.left):
                return True
        return False
    #判断方向是否在区间内
    def isInt1(inter,direction):
        if inter.left<inter.right:
            if(direction<=inter.left)or(direction>=inter.right):
                return True
        else:
            if(direction<=inter.left)and(direction>=inter.right):
                return True
        return False
    #求交集（r1的范围小于r2）
    def Intersection(r1, r2):
        intersection=Interval.Range()
        if(r1.left<r1.right):#r1跨（0,1）
            if(r2.left<=r1.left)or(r2.left>=r1.right):#交叉
                intersection.left = r2.left
                intersection.right = r1.right
            elif((r2.right<=r1.left)or(r2.right>=r1.right)):#交叉
                intersection.left = r1.left
                intersection.right = r2.right
            else:#不交叉，r2包含了r1
                intersection.left = r1.left
                intersection.right = r1.right
        else:
            if((r2.left<=r1.left)and(r2.left>=r1.right)):
                intersection.left = r2.left
                intersection.right = r1.right 
            elif((r2.right<=r1.left)and(r2.right>=r1.right)):
                intersection.left = r1.left
                intersection.right = r2.right 
            else:
                intersection.left = r1.left
                intersection.right = r1.right 
        return intersection

def change_to_points(input_list):
    output_list=[]
    for i in input_list:
        util_point=utils_copy.Point.Point(i.x,i.y,i.time) # pkg.module.class
        output_list.append(util_point)
    return output_list
    # self.x = 0
    # self.y = 0
    # self.time = None
def one(Points_list,error=8):
    # error=math.pi*2.5#这里给定阈值为pi*2.5
    p=[]
    R=[]

    for i in Points_list:
        temppoint=Interval.Point()
        temppoint.x=i.get_x()
        temppoint.y=i.get_y()
        temppoint.time=i.get_time()
        p.append(temppoint)

    R.append(p[0])
    #计算p0p1方向
    direction12=Interval.Standardization(math.atan2(p[1].y-p[0].y, p[1].x-p[0].x))
    ComSub=Interval.Fan(direction12,error)
    s=0
    directsum=0
    for i in range(1,len(p)-1):
        direct=Interval.Standardization(math.atan2(p[i+1].y-p[i].y, p[i+1].x-p[0].x))
        interval=Interval.Fan(direct,error)
        if(Interval.notInt(ComSub, interval)==True):
            R.append(p[i])
            ComSub=interval
            s=i
        else:
            ComSub=Interval.Intersection(ComSub,interval)
            directsum=Interval.Standardization(math.atan2(p[i+1].y-p[s].y, p[i+1].x-p[s].x))
            if(Interval.isInt1(ComSub,directsum)==False):
                R.append(p[i])
                ComSub=interval
                s=i
    R.append(p[len(p)-1])
    T=len(p)
    T1=len(R)
    # print("compression rate:"+str((T1)/T))


    return change_to_points(R)

def interval_batch(orig_list_of_Points,epsilon):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        compressed_list_of_Points.append(one(traj,epsilon))
    # print('OPW_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points


# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '7.85'(which is approximately the result of  3.1415926*2.5)")
# argps = parser.parse_args()
# error_parse = eval(argps.args)
#
# output_point_list=one(error=error_parse)
# fd=open(r"interval_output.txt",'w')
# for point in output_point_list:
#     fd.write("{} {} {}\n".format(point.x,point.y,point.time))
# fd.close()

