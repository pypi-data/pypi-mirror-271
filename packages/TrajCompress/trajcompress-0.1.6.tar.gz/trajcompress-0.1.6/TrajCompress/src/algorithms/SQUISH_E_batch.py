#how to use this file :
# read txt from 'data' folder
# the code concerning input is line 223
# txt is like "lat lon time\n" note the delimeter
# the code concerning output is line 228
import sys
import math
#import ../Zhou/Sttrace
import heapq
#from heapq import _siftup, _siftdown, heapify
import bisect
import os
#from DOTS import get_MeanErr
# sys.path.append("..")
#from test1 import test1
from ..basic_notion.DistFunc import synchronized_euclidean_distance
from ..basic_notion.Point import Point
from ..basic_notion.LineSimplify import LineSimplify
from .. import basic_notion as utils_copy




class SQUPoint(Point):
    def __init__(self, x:  float, y:  float, t:  float, id: int,succ=None , pred=None,pi=0):
        self._id = id
        super().__init__(x,y,t)
        self._pred=pred
        self._succ=succ
        self._pi=pi
        self.weight=float('inf')
    def __lt__(self, other):
        return True
    def get_pred(self) :
        return self._pred

    def get_succ(self) :#$ check the -> code may be wrong
        return self._succ

    def get_id(self) -> int:
        return self._id
    def set_succ(self,succ):
        self._succ=succ
    def set_pred(self,pred):
        self._pred=pred

    def set_pi(self,pi):
        self._pi=pi

    def get_pi(self) -> int:
        return self._pi

class SQU_Alg(LineSimplify):#init_beta
    def __init__(self,init_beta=10,lam=10,miu=500):
        super().__init__()
        self.simplified_track=[]
        self.beta= init_beta
        self.lam = lam
        self.miu = miu
        self.q=[]
        self.startPoint=None
        self.tmp=None#this is made to save the latest point with inf weight
    def add_point(self, x: float, y: float, t: float = None, convert=True, id :int = None,succ = None,pred = None,pi:int = 0):
        """
        :param x: horizontal coordinate, e.g., lon
        :param y: vertical coordinate, e.g., lat
        :param t: time stamp
        :param convert: convert lat-lon to x-y-z Cartesian coordinate system -- needed if calculate distance later
        """
        p = SQUPoint(x, y, t,id,succ,pred,pi)
        #self, x:  float, y:  float, t:  float, id: int,succ=None , pred=None,pi=0):
        if convert:
            p.latlon2cartesian()

        self._trace.append(p)

    @staticmethod
    def set_priority(point,weight,q):
        # try:
        heapq.heappush(q, (weight, point))
        # except:
        #     heapq.heappush(q, (weight+0.01*k, point))
        #     k+=1

    def adjust_priority(self,point,q):#here is a little different from the persudo code
        # find the index of the point then update it and shift up(the inf weight point is handled in other way)
        if point.get_succ() and point.get_succ():
            p=point.get_pi()+synchronized_euclidean_distance(point.get_pred(),point,point.get_succ())
            #print("this weight ,p,len,point",point.weight,p,len(q),point,self.q)
            a=round(p,5)
            #i=bisect.bisect_left(q,(point.weight,point))
            i=q.index((point.weight,point))

            #print('find i',i)

            point.weight=a#I compare the weight in the bisect function  and use round to avoid the inaccuracy of float
            q[i]=(a,point)
            #print("suc i,len", i, len(q), self.q)
            if p>point.weight:
            #if  value is increased just shiftup the point
                heapq._siftup(q, i)
            elif p<point.weight:
                heapq._siftdown(q, 0, i)

            #self.set_priority(point,p,q)

    def reduce(self,q):
        #print("Before_reduce",len(q))
        _,pj=heapq.heappop(self.q)
        #print("after_pop", len(q))
        suc = pj.get_succ()
        pred = pj.get_pred()
        suc.set_pi(max(suc._pi, pj._pi))
        pred.set_pi(max(pred._pi, pj._pi))
        suc.set_pred(pred)
        pred.set_succ(suc)
        #remove the pj and make the pred and suc conncted
        if pred.get_pred():
            self.adjust_priority(pred, q)
        if pred.get_succ():
            self.adjust_priority(suc, q)

        #print("After_reduce", len(q))

    def Main_alg(self):
        inList = self.get_trace()
        for i in range(len(inList)):
            #print('i,beta',i,self.beta)
            if i/self.lam >=self.beta:
                self.beta+=1
            self.tmp=inList[i]
            if i > 1:
                a=synchronized_euclidean_distance(inList[i - 2], inList[i - 1], inList[i])
                self.set_priority(inList[i-1],round(a,5),self.q)
                inList[i - 1].weight = round(a,5)
            elif i==0:
                self.set_priority(inList[0],float('inf'),self.q)
                self.startPoint=inList[0]

                #if i==1 then do nothing  it is saved in tmp
            #here is different from the persudo code the article gives
            if i>=1:
                inList[i-1].set_succ(inList[i])
                inList[i].set_pred(inList[i-1])

                #self.adjust_priority(inList[i],self.q)

            if len(self.q)==self.beta:
                self.reduce(self.q)

        self.q.append((float('inf'),self.tmp))
        #print("####################################### the second stage")
        p,_=self.q[0]

        while p<self.miu:
            self.reduce(self.q)#$
            p=self.q[0][0]


        return self.form_trace()#in the priority queue lies points

    def form_trace(self):

        p=self.startPoint
        outList = [p]
        while p.get_succ():
            p=p.get_succ()
            outList.append(p)
        return outList


    def load_from_txt(self, filepath, time_include=False,delimter=","):
        if not os.path.exists(filepath):
            print("Please check if file exists AT ", filepath)
            exit()

        with open(filepath, "r") as rf:
            lines = rf.readlines()
            id = 0
            for line in lines:
                #id=0
                line = line.rstrip()
                if line and line[0] != '#':
                    if time_include:
                        lat, lon, ts = line.split(delimter)
                        self.add_point(float(lon), float(lat), float(ts),id=id)
                        id+=1
def get_MeanErr(point_list,output_point_list):
    Err=0.0
    start_index=0
    end_index=len(output_point_list)-1

    while(start_index<end_index):
        pointA_id=int(output_point_list[start_index].get_id())
        pointB_id=int(output_point_list[start_index+1].get_id())
        #print("first interval",pointA_id,pointB_id)
        id=pointA_id+1
        while(id<pointB_id):
            Err+=synchronized_euclidean_distance(output_point_list[start_index],point_list[id],output_point_list[start_index+1])
            id+=1
            #print("Err,id",Err,id)

        start_index+=1

    return Err / len(point_list)
        #return Err

# SQU_E = SQU_Alg(lam=1,miu=100)
# SQU_E.load_from_txt("..//data//test_with_time.txt",time_include=True,delimter=" ")
# #print('aaa', SQU_E._trace[90]._cx,SQU_E._trace[90]._x)
# outList = SQU_E.Main_alg()
#
# err=get_MeanErr(SQU_E.get_trace(),outList)
# print(len(outList),err)
# ol=[]
# for i in outList:
#     ol.append(i._id)




def SQU_Once(lam,miu,toFile=False):#

    SQU_E = SQU_Alg(lam=lam, miu=miu)
    SQU_E.load_from_txt("Sample.txt", time_include=True, delimter=" ")
    # print('load in', SQU_E._trace[90]._cx,SQU_E._trace[90]._x)
    outNum = SQU_E.Main_alg()
    # print(outNum)
    if toFile:
        f = open("SQUISH-E_output.txt", 'w')
        for i in outNum:
            f.write(str(i.get_y())+" ")
            f.write(str(i.get_x())+" ")
            f.write(str(i.get_time())+" ")
            f.write('\n')
        f.close()
    return len(outNum)/len(SQU_E._trace),get_MeanErr(SQU_E._trace,outNum)


def SQUISH_one_traj(pointList,arg_tup):
    lam,lam=arg_tup
    SQU_E = SQU_Alg(lam=lam, miu=lam)
    SQU_E._trace=pointList
    # change_to_local_points(pointList)
    outNum = SQU_E.Main_alg()
    return outNum


def SQUISH_batch(orig_list_of_Points, arg_tup):
    compressed_list_of_Points = []
    for traj in orig_list_of_Points:
        traj=change_to_local_points(traj)# also latlon2cartesian
        compressed_list_of_Points.append(SQUISH_one_traj(traj, arg_tup))
    # print('DOTS_batch ',len(orig_list_of_Points),' have done')
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
    for enu,i in enumerate(input_list):
        local_point=SQUPoint(i.get_x(),i.get_y(),i.get_time(),enu) # pkg.module.class
        local_point.latlon2cartesian()
        output_list.append(local_point)
    return output_list





# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '5,10'")
# argps = parser.parse_args()
# lam,miu = eval(argps.args)
#
# SQU_Once(lam=lam,miu=miu,toFile=True)####the one that saves its output


# ########################################## to draw two plots to show the effect of the alg #####################################
# x=list(np.linspace(1,7,10))
# ERR=[]
# compressionRate=[]

# for i in x:
#     k,w=SQU_Once(i,0)
#     compressionRate.append(k)
#     ERR.append(w)


# import matplotlib.pyplot as plt
# plt.figure(figsize=(7,7))
# plt.subplot(2,1,1)
# plt.plot(x,compressionRate,"b*")
# plt.title('μ = 0 ; λ from 1 to 7 minimize SED error ensuring the compression ratio of λ')
# plt.xlabel("λ")
# plt.ylabel("CompressionRate")
# plt.subplot(2,1,2)
# plt.plot(x,ERR,"r-")
# plt.xlabel("λ")
# plt.ylabel("mean_SED error")
# #plt.legend()
# plt.show()



# x=list(np.linspace(10,300,10))
# ERR=[]
# compressionRate=[]

# for i in x:
#     k,w=SQU_Once(1,i)
#     compressionRate.append(k)
#     ERR.append(w)


# import matplotlib.pyplot as plt
# plt.figure(figsize=(7,7))
# plt.subplot(2,1,1)
# plt.plot(x,compressionRate,"b*")
# plt.title('λ = 1 ; μ from 10 to 300 maximizes compression ratio while keeping SED error under μ')
# plt.xlabel("μ")
# plt.ylabel("CompressionRate")
# plt.subplot(2,1,2)
# plt.plot(x,ERR,"r-")
# plt.xlabel("μ")
# plt.ylabel("mean_SED error")
# #plt.legend()
# plt.show()




