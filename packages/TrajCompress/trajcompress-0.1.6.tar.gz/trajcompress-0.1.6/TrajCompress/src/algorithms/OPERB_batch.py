import math
# class Point(object):
#     def __init__(self):
#         self._x = 0
#         self._y = 0
#         self._t = 0

#把两个点变成一个有向线段
class GPSLine():				    
    def __init__(self,startPoint,endPoint):
        self.length=getDistanceOfP_P(startPoint._x, startPoint._y, endPoint._x, endPoint._y)
        self.angle=getAngleOfVector(startPoint._x, startPoint._y, endPoint._x, endPoint._y)             
    

def rad(d):
    return d * math.pi / 180
	
#两点距离	
def getDistanceOfP_P(lat1, lon1, lat2, lon2):#wei du ,jing du 			
	radLat1 = rad(lat1)
	radLat2 = rad(lat2)
	dw = radLat1 - radLat2 # 纬度
	dj = rad(lon1) - rad(lon2) 
	s = 2 * math.asin(math.sqrt(
				math.pow(math.sin(dw / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(dj / 2), 2)))
	s = s * 6378137.0
	return s
    # checked wondering the lat and lon, the sequence here,
	

#有向线段的角度
import pdb

def getAngleOfVector(latS,  lonS,  latE,  lonE):
    try:
        if math.isclose(latS, latE, abs_tol=1e-8) and math.isclose(lonS, lonE, abs_tol=1e-8):
            return 0
        elif math.isclose(latS, latE, abs_tol=1e-8) and lonS < lonE:
            return 0
        elif math.isclose(latS, latE, abs_tol=1e-8) and lonS > lonE:
            return math.pi
        elif latS < latE and math.isclose(lonS, lonE, abs_tol=1e-8):
            return math.pi / 2
        elif latS > latE and math.isclose(lonS, lonE, abs_tol=1e-8):
            return 3.0 * math.pi/ 2
        high = getDistanceOfP_P(latE, lonE, latS, lonE)
        length = getDistanceOfP_P(latS, lonS, latE, lonE)
        if math.isclose(length, 0, abs_tol=1e-8):
            return 0
        
        angle = math.atan(high / length)       #in [0 pi/2]
        if latS > latE and lonS < lonE:
            angle = math.pi - angle          # in [pi/2, pi)
        if latS > latE and lonS > lonE:
            angle = math.pi + angle          #in [pi, 3pi/2)
        if latS < latE and lonS > lonE:
            angle = 2 * math.pi - angle      #in [3pi/2, 2pi)
        return angle
    except Exception as e:
        pdb.set_trace()

#点弦距离		
def getDistanceOfP_L(Rline, line):
    r = Rline.length
    angle1 = Rline.angle
    angle2 = line.angle
    if r == 0:
        return 0
    sita = getIncludedAngle(angle1, angle2)
    dis = r * math.sin(sita)
    return abs(dis)


#两个角度的差值
def getIncludedAngle( angle1, angle2):
    '''Included angles (∠). Given two directed line segments
    L1 =
    # » PsPe1 and L2 =
    # » PsPe2 with the same start point Ps,
    the included angle from L1 to L2, denoted as ∠(L1, L2), is
    L2.θ−L1.θ. For convenience, we also represent the included
    angle ∠(L1, L2) as ∠Pe1 PsPe2
    .'''
    theta = angle2 - angle1

    # if theta > math.pi:
	#     theta = -2 * math.pi + theta
    # if theta < -math.pi:
	#     theta = 2 * math.pi + theta       
    return theta

#Fitting Function中的f()函数
def f(Rline,lline):
    angle_diff=Rline.angle-lline.angle 
    if -2*math.pi<angle_diff and angle_diff<=-1.5*math.pi:
        return 1
    elif -math.pi<=angle_diff and angle_diff<=-0.5*math.pi:
        return 1
    elif  0<=angle_diff and angle_diff<=0.5*math.pi:
        return 1
    elif  math.pi<=angle_diff and angle_diff<1.5*math.pi:
        return 1
    else: 
        return -1
 

import copy
#fitting function函数F
def fittingFunction(points,start , i , lline , error):
    '''
    '''
    lline=copy.deepcopy(lline)
    Rline=GPSLine(points[start],points[i])
    j = int(Rline.length * 2/error - 0.5)+1
    value=j*error/2
    if Rline.length - lline.length<=error/4:
        lline=lline
    elif Rline.length>error/4 and lline.length==0:
        lline.length=value
        lline.angle=Rline.angle
    else:
        lline.length=value
        ascin_raw=getDistanceOfP_L(Rline,lline)/value
        if ascin_raw<=-1 or ascin_raw>=1:
            print('out of bound')
            ascin_raw = min(max(ascin_raw, -0.99), 0.99)
        # special variables
        # angle:1.2113205463421615
        # length:87.28782494224896
        # lline
        # <__main__.GPSLine object at 0x7f9690718b20>
        # special variables
        # angle:2.962579479887357
        # length:85.0
        # value
        # 85.0
        # maybe
        lline.angle=lline.angle+f(Rline,lline)*math.asin(ascin_raw)/j
    return lline
        
        
def getActivePoint(points,start,active,lline,error):
    '''
    逻辑是,根据一个圆 来判断是否在一个叫做active zone的范围内，得到不在这个范围内的点
    输入输出的目的是 下一个不再内的点（如果没点了就是-1） 然后就是是否能被加进去到当前的R的位置
    下一个active的点（如果没有了就是-1，然后这里是否能被归到前一个轨迹内）
    太抽象了，
    '''
    i=active+1
    if i>=len(points):
        return -1,False
    flag=True
    Rlinei=GPSLine(points[start],points[i])
    Rlinea=GPSLine(points[start],points[active])
    n=len(points)
    while Rlinei.length-lline.length<=error/4 and i<=n and i-start<4*100000:

        if getDistanceOfP_L(Rlinei,lline)>error/2 or getDistanceOfP_L(Rlinei,Rlinea)>error:
            flag=False
            # print(f'{i}th point be the new active')
            break
        i+=1
        if i>=len(points):
            return i,False
        # Lline.append(lline)# ?? what is it
        # print(f'{i}th point is is okay with the traj start {start} to {active}')
        Rlinei=GPSLine(points[start],points[i])
        # Rlinea=GPSLine(points[start],points[active])

        # 两种出去的情况： 
        # 1 if里面的break 就是说能fit，
        # 2 应该是上面while，主要的方法是 Rlinei.length-lline.length>error/4 超过这个圆 
    if getDistanceOfP_L(Rlinei,lline)>error/2 and lline.length>0:
        flag=False
    if i==len(points):
        i=-1  
    return i,flag

     
def OPERB(points,error):
    
    # global Lline
    Lline=[]

    res=[]   
    Lline.append(GPSLine(points[0],points[0]))
    end_bk=0
    end=0
    res.append(points[end])

    active,flag=getActivePoint(points,0,0,Lline[0],error)
    while active!=-1 and active<len(points)-1:
        # print('after add the new active:',active,end=' ')
        start=end 
        Lline.append(fittingFunction(points,start,active,Lline[len(Lline)-1],error))
        active,flag=getActivePoint(points,start,active,Lline[len(Lline)-1],error)
        while active!=-1 and active<len(points)-1 and flag==True:
            
            # 0.5 的时候直接跳过了这里的循环, 不断的添加0号点, active ++, flag=False
                # 需要更新？ 有进入循环的吗
            # 4的时候 直接 active -1 ，falg=True
                # 需要加入最后一个点
            Lline.append(fittingFunction(points,start,active,Lline[len(Lline)-1],error))
            end=active
            # print('L153')# this means the new active line contribute to the La, while the active and start 
            # print('inside new active:',active)


            # 61th point is is okay with the traj start 32 to 32
            # L153
            # inside new active: 61
            # 63th point is is okay with the traj start 32 to 61
            # 64th point is is okay with the traj start 32 to 61
            # 65th point is is okay with the traj start 32 to 61
            # L153
            # inside new active: 65
            # 67th point is is okay with the traj start 32 to 65
            # 68th point is is okay with the traj start 32 to 65
            # 69th point is is okay with the traj start 32 to 65
            # 70th point is is okay with the traj start 32 to 65
            # L153
            # inside new active: 70
            # 72th point is is okay with the traj start 32 to 70
            # 73th point is is okay with the traj start 32 to 70
            # 74th point is is okay with the traj start 32 to 70

            #from above the active Line La is changing, debug finished


            active,flag=getActivePoint(points,start,active,Lline[len(Lline)-1],error)
        
        if flag is False:
            end=active
            # if end==-1:
            #     end=
        
        # if end==end_bk:
        #     # active !=-1 but falg=False, can not fit in, so increase the end, 
        #     # meaning end is add to the compressed traj
        #     end+=1 
        end=min(end,len(points)-1)
        if points[end].get_time()<=res[-1].get_time():
            continue
        res.append(points[end])
        # print('res_id:',end)
        # end_bk=end  

    if end<len(points)-1:
        res.append(points[len(points)-1])

    return list(res)

    

# def test_GPSLine():
#     start = Point()
#     start._x, start._y = 0, 0
#     end = Point()
#     end._x, end._y = 1, 1
#     gps_line = GPSLine(start, end)
#     assert gps_line.length > 0, "Length should be positive"
#     assert 0 <= gps_line.angle <= 2 * math.pi, "Angle should be in range [0, 2π]"

# def test_getDistanceOfP_P():
#     assert getDistanceOfP_P(0, 0, 1, 1) > 0, "Distance should be positive"

# def test_getAngleOfVector():
#     assert 0 <= getAngleOfVector(0, 0, 1, 1) <= 2 * math.pi, "Angle should be in range [0, 2π]"

# Add more tests as needed
import tqdm


# if __name__=='__main__':
#     _run=True
#     if _run:
        # points=[]
        # Lline=[]
        # res=[]      
        # file=open('Sample.txt','r')    
        # for n,line in enumerate(file):
        #     if not line:
        #         break
        #     li=line.split(" ")
        #     point=Point()
        #     point._x =float(li[0])
        #     point._y = float(li[1])
        #     point._t = float(li[2].strip())
        #     points.append(point)
        # file.close()
import tqdm
def OPERB_batch(orig_list_of_Points,max_error):
    compressed_list_of_Points=[]
    for traj in tqdm.tqdm(orig_list_of_Points):
        compressed_list_of_Points.append(OPERB(traj,max_error))
    # print('OPW_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points
        # print(f'points before compression {len(points)}')
        # print(f'points after compression {len(res)}')
        # fd=open(r"OPERBoutput.txt",'w')
        # for i in range(len(res)):
        #     fd.write("{} {} {}\n".format(res[i]._x,res[i]._y,res[i]._t))
        # fd.close()
        # print("compression ratio {}".format(len(res)/len(points)))


# Run tests
    # test_GPSLine()
    # test_getDistanceOfP_P()
    # test_getAngleOfVector()
