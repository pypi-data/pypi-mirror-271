#how to use this file :
# read txt from 'data' folder
#the code concering input and output is in line 299 and line 316
# txt is like "lat lon time\n" note the delimeter
import sys
import math
# sys.path.append("..")
#from test1 import test1
from ..basic_notion import DistFunc
from ..basic_notion.Point import Point
from ..basic_notion import LineSimplify
from .. import basic_notion as utils_copy

# import numpy as np



class DotPoint(Point):
    def __init__(self, x:  float, y:  float, t:  float, id: int):
        self._id = id
        super().__init__(x,y,t)
    def cals(self,sx,sx2,sy,sy2,sz,sz2,st,st2,sxt,syt,szt):
        sx += self.get_cx()
        sy += self.get_cy()
        sz += self.get_cz()
        st += self.get_time()
        sx2 += self.get_cx()**2
        sy2 += self.get_cy()**2
        sz2 += self.get_cz()**2
        st2 += self.get_time()**2
        sxt += self.get_cx()*self.get_time()
        syt += self.get_cy()*self.get_time()
        szt += self.get_cz()*self.get_time()

        self._sx = sx
        self._sy = sy
        self._sz = sz
        self._st = st

        self._sx2 = sx2
        self._sy2 = sy2
        self._sz2 = sz2
        self._st2 = st2

        self._sxt = sxt
        self._syt = syt
        self._szt = szt

        return sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt

    def get_sx(self) -> float:
        return self._sx

    def get_sx2(self) -> float:
        return self._sx2

    def get_sy(self) -> float:
        return self._sy

    def get_sy2(self) -> float:
        return self._sy2

    def get_sz(self) -> float:
        return self._sz

    def get_sz2(self) -> float:
        return self._sz2

    def get_st(self) -> float:
        return self._st

    def get_st2(self) -> float:
        return self._st2

    def get_sxt(self) -> float:
        return self._sxt

    def get_syt(self) -> float:
        return self._syt

    def get_szt(self) -> float:
        return self._szt

    def get_id(self) -> int:
        return self._id


# DOTS=DotsSimplify()


def addPoint(yi, n, pList):  # yi means epsilon # n* yi  is the bound #$ replace

    j = 0
    k = 0
    # $v=[[(0,-1,0)]]#v[k]=[(id,orderOfParent,point:(with property: x,y,time,id,cx,cy,cz,st,st2,sx,sx2,sy,sy2,sz,sz2,sxt,syt,szt))]#order指父节点在上一层的相对位置
    # 换成类 下面的参数全部都要改 plist[j].getbalabla   balabala

    sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt = (0 for i in range(11))
    sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt = pList[0].cals(sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt)
    v = [[(0, -1, pList[0])]]
    already = 0
    outPointList = [0]
    flag=0
    while j < len(pList) - 1:
        # 创建新的一层并填满
        k += 1  # k means the generation
        v.append([])  # v(k+1) a mepty gen
        termk = []  # record the order of term point
        #sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt = (0 for i in range(11))

        while j < len(pList) - 1:  # pointList# lon lat time id
            # 新进来的点编号j
            j += 1
            if flag==0:#if flag==0
                sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt = pList[j].cals(sx, sx2, sy, sy2, sz, sz2, st, st2, sxt,
                                                                              syt, szt)

            else:
                flag=0

            for i, pi in enumerate(v[k - 1]):

                if i in termk:
                    # print('termi,k',k,i,pi)
                    continue
                else:

                    p = LISSED(pi[2], pList[j])#easy_name
                    if p < yi:
                        v[k].append((pList[j].get_id(), i, pList[j]))  # $plist 直接给弄好 元素是dotpoint

                        break  # for
                    if p > n * yi:  # and n not in termk:origin the name need to be checked
                        termk.append(i)
                        #print('termk',termk)

            # if len(termk) >= len(v[k - 1]):  # 建好一层
            if len(v[k]) == 0 or len(termk) >= len(v[k - 1]):  # 建好一层

                if len(v[k]) == 0:
                    # if len(termk)==0:
                    #i = -1  # 其实这里应该考虑取最小的#￥
                    # print('len(termk)==0==v[k-1]')
                    i=min(range(len(v[k-1])),key=lambda x: LISSED(v[k-1][x][2],pList[j]))
                    v[k].append((pList[j].get_id(), i, pList[j]))
                #print('建好一层',v[k])
                v[k] = Minimize(v[k - 1], v[k])
                #print('建and 修好一层',v[k])
                List, already = TryToDecode(v, already)
                #print('List,already',List,already)
                outPointList.extend(List)
                j -= 1
                flag=1#if 1 this point need to be dismissed form sx
                break

    endlist = [v[k][-1][0]]
    paridx = v[k][-1][1]
    while k-1>already:
        paridx = v[k-1][paridx][1] #pList[endlist[-1]] is a DOTSPOINT obj
        # endlist.append(v[k-1][paridx][0])
        endlist.append(v[k - 1][min(len(v[k - 1]) - 1, paridx)][0])
        k-=1
    endlist.reverse()
    outPointList.extend(endlist)
    #print("outPointList,endlist")

    if outPointList[-1] != j:  # $here need the trackback
        outPointList.append(j)


    return outPointList


def TryToDecode(v, already):
    '''
    already 指之前已经完成输出的层的编号
    v也许可以考虑切片？
    '''
    List = []
    live = []

    for i in range(len(v) - already - 1):  # $
        live.append([0 for _ in range(len(v[i + already + 1]))])

    # live.append([1 for _ in range(len(v[-1]))])
    live[-1] = [1 for _ in range(len(live[-1]))]
    # print('try Decode,inilive',live)#$

    k = len(v) - already - 2
    d = 0
    for m in range(k, d, -1):  # m is the alyer of live
        for n, pj in enumerate(live[m]):
            if pj:
                live[m - 1][v[m + already + 1][n][1]] = 1
    m = d

    # print('try Decode,inilive2',live)#$

    def checkIfSingle(layer):
        sum = 0
        for n, i in enumerate(layer):
            sum += i
        if sum == 1:
            return True, n
        else:
            return False, -1

    m = already + 1
    while m < len(v):
        if not checkIfSingle(live[m - already - 1])[0]:  # m 是层数（对应的v
            break
        else:
            # print('checkIfSingle:live,m,already',live,m,already,checkIfSingle(live[m-already-1]))
            p = checkIfSingle(live[m - already - 1])[1]
            List.append(v[m][p][0])
            m += 1  # 很奇怪之前这里怎么跑的
    return List, already + len(List)

    # return outPointList, already


# termk=[]
def LISSED(i, j):#由于sx全部是在这个点之前的 所以 用还没有更新过的sx来计算

    if i.get_id()+1>=j.get_id():
        return 0
    else:
        eps= 1e-8
        eps2=1e-12
        c1 = (i.get_cx()*j.get_time()-j.get_cx()*i.get_time()+eps2)/(j.get_time()-i.get_time()+eps)
        c2 = (j.get_cx()-i.get_cx()+eps2)/(j.get_time()-i.get_time()+eps)
        c3 = (i.get_cy()*j.get_time()-j.get_cy()*i.get_time()+eps2)/(j.get_time()-i.get_time()+eps)
        c4 = (j.get_cy()-i.get_cy()+eps2)/(j.get_time()-i.get_time()+eps)
        c5 = (i.get_cz()*j.get_time()-j.get_cz()*i.get_time()+eps2)/(j.get_time()-i.get_time()+eps)
        c6 = (j.get_cz()-i.get_cz()+eps2)/(j.get_time()-i.get_time()+eps)

        dsx = j.get_sx()-j.get_cx()-i.get_sx()
        dsx2 = j.get_sx2() - j.get_cx()**2 - i.get_sx2()
        dsy = j.get_sy() - j.get_cy() - i.get_sy()
        dsy2 = j.get_sy2() - j.get_cy()**2 - i.get_sy2()
        dsz = j.get_sz() - j.get_cz() - i.get_sz()
        dsz2 = j.get_sz2() - j.get_cz()**2 - i.get_sz2()
        dsxt = j.get_sxt() - j.get_cx()*j.get_time() - i.get_sxt()
        dsyt = j.get_syt() - j.get_cy()*j.get_time() - i.get_syt()
        dszt = j.get_szt() - j.get_cz()*j.get_time() - i.get_szt()
        dst = j.get_st() - j.get_time() - i.get_st()
        dst2 = j.get_st2() - j.get_time()**2 - i.get_st2()
        LISSED = (c1**2+c3**2+c5**2)*(j.get_id()-i.get_id()-1)+\
            (c2**2+c4**2+c6**2)*(dst2)+\
             2*(c1*c2+c3*c4+c5*c6)*dst+\
             dsx2+dsy2+dsz2+\
            -2*c1*dsx-2*c3*dsy-2*c5*dsz+\
            -2*c2*dsxt-2*c4*dsyt-2*c6*dszt
        #print(i.get_id(),j.get_id(),LISSED)
    return LISSED


# def LISSED_DAG(i,j,pList):
#     sum=0
# #     if j-i==1:
# #         return sum
#     #a=time.time()
#     #print('LISSED',i,j)
#     for p in range(i+1,j):
#         sum+=getSed(pList[i],pList[j],pList[p])**2#$check the name
#     #print(time.time()-a)
#     return sum

def Minimize(par,child):#v[k]=[(idOfSelf,orderOfParent,dotspoint)]
    """
    不存具体的经纬度了 只存点位不知道好不好
    """
    for enu,i in enumerate(child):
        minLISSED=float("inf")#np.inf
        minParNum=0
        for n,j in enumerate(par):

            k=LISSED(j[2],i[2])
            if k<minLISSED:
                minParNum=n
                minLISSED=k

        # child[enu]=(i[0],minParNum,par[minParNum][2])
        i=(i[0],minParNum,par[minParNum][2])

    return child

# def formPoint(plist):
#     usefulList = []
#     # sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt = (0 for i in range(11))
#     # startTime = plist[0][2]
#     startTime=0
#     # last_time=0
#     for i in plist:
#         # if i[2]==last_time:
#         #     continue
#         # last_time=i[2]
#         a = DotPoint(i[0],i[1],i[2]-startTime,i[3])
#         a.latlon2cartesian()  # a have cx cy cz, t ,id  property
#         # sx+=a.get_cx()
#         # sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt, szt = a.update(sx, sx2, sy, sy2, sz, sz2, st, st2, sxt, syt,
#         #                                                              szt)
#         usefulList.append(a)
#     return startTime,usefulList

# import utils_copy
def change_to_util_points(input_list):
    '''
    change current Point class to util class,
    list of points
    '''
    output_list=[]
    for i in input_list:
        util_point=utils_copy.Point.Point(i.get_x(),i.get_y(),i.get_time()) # pkg.module.class
        output_list.append(util_point)
    return output_list

def change_to_local_points(input_list):
    '''
    change util Point class to local Point class
    '''
    output_list=[]
    for enu,i in enumerate(input_list):
        local_point=DotPoint(i.get_x(),i.get_y(),i.get_time(),enu)
        local_point.latlon2cartesian()
        output_list.append(local_point)
    return output_list
####################################################main#############################################################

def out_pois(traj):
    pass
    # for i in traj:
    #     print(i.get_x(),i.get_y(),i.get_time())

flag=0
def DOTS_one_traj(pointList,arg_tup):
    global flag
    yi,n=arg_tup
    outNum = addPoint(yi=yi, n=n, pList=pointList) #like[0,3,5,12,16....]
    if flag==0:

        # print('L337')
        out_pois([pointList[i] for i in outNum])

    # print(yi,n,'outnum',outNum)
    outNum2=[]
    for i in outNum:
        if  i>0 and pointList[i].get_time()==pointList[i-1].get_time():
            print('duplicates!')
            continue
        if i > 0 and pointList[i].get_time() < pointList[i - 1].get_time():
            print('error!')
            continue
        outNum2.append(pointList[i]) # line [point[0],point[3],point[5],....]
    # outNum2 = [pointList[i] for i in outNum]
    outNum2=change_to_util_points(outNum2)
    if flag==0:
        # print('L348')
        out_pois(outNum2)
        flag=1

    return outNum2



def DOTS_batch(orig_list_of_Points, arg_tup):
    compressed_list_of_Points = []
    for enu,traj in enumerate(orig_list_of_Points):
        traj=change_to_local_points(traj)# also latlon2cartesian
        if enu==0:
            # print('input')
            out_pois(traj)
        compressed_list_of_Points.append(DOTS_one_traj(traj, arg_tup))
        if enu==0:
            # print('output')
            out_pois(compressed_list_of_Points[0])
            # 但是这里 输出的时候会少一点
    # print('DOTS_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points

# pointList=[]
# data=open('Sample.txt','r')
# for n,line in enumerate(data):
#     lines=line.split(' ')
#     longitude=float(lines[0])
#     latitude=float(lines[1])
#     timef=float(lines[2].strip())
#     pointList.append((longitude,latitude,int(timef),n))
# startTime,pointList=formPoint(pointList)
# ####################################DOTS here addPoint means the DOTS algrithm
# # yi means epislon (the tolerance of ISSED )
# # n means  if Local SSED between new point and a typical point P is n times larger than episilon
# # then we think it is impossible that new point's parent point is before P
#
# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
#                                  "in the specific file, like '10,2'")
# argps = parser.parse_args()
# yi,n = eval(argps.args)
#
#
# outNum = addPoint(yi=yi, n=n, pList=pointList) #like[0,3,5,12,16....]
# outNum = [pointList[i] for i in outNum]#line [point[0],point[3],point[5],....]
#
# # print(f"compression rate is {round(len(outNum)/len(pointList),2)}")
#
# #####################################write file
# f = open("DOTS_output.txt", 'w')
# for i in range(len(outNum)):
#     if i>0 and outNum[i].get_time()==outNum[i-1].get_time():
#         # print('duplicates!')
#         continue
#     if i > 0 and outNum[i].get_time() < outNum[i - 1].get_time():
#         print('error!')
#         continue
#     f.write(str(outNum[i].get_x())+" ")
#     f.write(str(outNum[i].get_y())+" ")
#     f.write(str(outNum[i].get_time()+startTime)+" ")
#     f.write('\n')
# f.close()



# the following aims to check the lissed
# for i in range(10):
#     p=DotPoint(0,0,i,i)
#     p._cy=(i-5)*2
#     p._cx=(i%2)*2
#     p._cz=0
#     pointList.append(p)

# for i in pointList:
#
#     print('id cx cy cz time',i.get_id(),i.get_cx(),i.get_cy(),i.get_cz(),i.get_time())
#     if i.get_id()>20:
#         break
#print(pointList[0],pointList[0].get_time(),pointList[2].get_cx())


#outPointList = addPoint(1000,2,pointList)
# print(len(outPointList),outPointList)

########################################draw the picture################################################
#这里为了画图
# def get_MeanErr(point_list,output_point_list):
#     Err=0

#     start_index=0
#     end_index=len(output_point_list)-1

#     while(start_index<end_index):        #遍历所有关键点
#         #选取两相邻关键点
#         pointA_id=int(output_point_list[start_index].get_id())
#         pointB_id=int(output_point_list[start_index+1].get_id())

#         id=pointA_id+1        #工作指针,用于遍历非关键点
#         while(id<pointB_id):        #遍历两关键点之间的非关键点
#             Err+=DistFunc.synchronized_euclidean_distance(output_point_list[start_index],point_list[id],output_point_list[start_index+1])
#             id+=1

#         start_index+=1

#     return Err / len(point_list)


# def DOTS(yi,n,pointList):
#     outNum=addPoint(yi,n,pointList)
#     output_point_list=[pointList[i] for i in outNum]
#     get_MeanErr(pointList,output_point_list)
#     #print(len(output_point_list))
#     return len(output_point_list)/len(pointList),get_MeanErr(pointList,output_point_list)


# if __name__ == 'main':
#     x=list(range(200,2000,200))+list(range(2000,6000,500))
#     ERR=[]
#     compressionRate=[]
#     x=list(range(200,2000,200))+list(range(2000,6000,500))
#     for i in x:
#         k,w=DOTS(i,1.5,pointList)
#         compressionRate.append(k)
#         ERR.append(w)
#         #print(i)

#     print('DOTsPic')
#     import matplotlib.pyplot as plt
#     plt.subplot(2,1,1)
#     plt.plot(x,compressionRate,"b*")

#     plt.xlabel("epsilon")
#     plt.ylabel("CompressionRate")
#     plt.subplot(2,1,2)
#     plt.plot(x,ERR,"r-")
#     plt.xlabel("epsilon")
#     plt.ylabel("SED error")
#     #plt.legend()
#     plt.show()
