# -*- coding: utf-8 -*-
"""
uniform batch form
"""
# class Point(object):
#     def __init__(self):
#         self.lat = 0
#         self.lon = 0
#         self.time = 0
#     def gpsreader(filename):         #读数据 存入points
#         file=open(filename,'r')
#         for n,line in enumerate(file):
#             if not line:
#                 break
#             li=line.split(" ")
#             point=Point()
#             point.lat =float(li[0])
#             point.lon = float(li[1])
#             point.time = float(li[2].strip())
#             points.append(point)
#         points.pop()
#         # print('reader:len(points)',len(points))
#         return

def Uniform(points,uniform):         #判断轨迹点是否应被保留，并返回保留点在Points中对应的下标
    simplified=[]             #下标保存
    originalIndex=0
    while(True):
        if originalIndex >= len(points)-1:
            break
        else:
            simplified.append(int(originalIndex))
            originalIndex = originalIndex + uniform## ?? why add a epsilon
    simplified.append(len(points)-1)
    simplified_points=[points[x] for x in simplified]
    return simplified_points

def Uniform_batch(orig_list_of_Points,uniform):
    compressed_list_of_Points=[]
    for traj in orig_list_of_Points:
        compressed_list_of_Points.append(Uniform(traj,uniform))
    print('Uniform_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points

# points=[]                         #初始数据
# filename='Sample.txt'
#
# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '5'")
# argps = parser.parse_args()
# epsilon = eval(argps.args)
#
# # epsilon=eval(input("epsilon please or default 5") or '5')      #键入阈值
# # epsilon=5                          #这里假设阈值为5
# # ##############################not a thershold at all! just a simple skip, skip 5 and choose one for example
# save_filename='Uniform_output.txt'
# Point.gpsreader(filename)
# cmp_buffer = Point.Uniform(epsilon)  #最终结果集合
# fd=open(save_filename,'w')          #写入并输出结果
#
# assert len(cmp_buffer)<=len(points) ,'seems reverse compressed'
#
# for i in range(len(cmp_buffer)):
#     fd.write("{} {} {}\n".format(points[cmp_buffer[i]].lat,points[cmp_buffer[i]].lon,points[cmp_buffer[i]].time))
# fd.close()

