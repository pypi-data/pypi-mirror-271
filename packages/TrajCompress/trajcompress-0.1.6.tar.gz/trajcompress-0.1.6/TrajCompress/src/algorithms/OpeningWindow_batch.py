'''
batch mode OpeningWindow,
'''
import math
from ..basic_notion.DistFunc import synchronized_euclidean_distance
from ..basic_notion.Point import Point
from ..basic_notion.LineSimplify import LineSimplify

points = []

def gpsreader(filename):
    with open(filename) as fin:
        lines = fin.readlines()
        for line in lines:
            data = line.strip().split()
            point = Point(float(data[0]), float(data[1]), float(data[2]))
            point.latlon2cartesian()
            points.append(point)

def gpsreader_batch(filename):
    '''
    goal from is
    [],[],[]
"TRIP_ID","CALL_TYPE","ORIGIN_CALL","ORIGIN_STAND","TAXI_ID","TIMESTAMP","DAY_TYPE","MISSING_DATA","POLYLINE"
"1372636858620000589","C","","","20000589","1372636858","A","False","[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]"
"1372637303620000596","B","","7","20000596","1372637303","A","False","[[-8.639847,41.159826],[-8.640351,41.159871],[-8.642196,41.160114],[-8.644455,41.160492],[-8.646921,41.160951],[-8.649999,41.161491],[-8.653167,41.162031],[-8.656434,41.16258],[-8.660178,41.163192],[-8.663112,41.163687],[-8.666235,41.1642],[-8.669169,41.164704],[-8.670852,41.165136],[-8.670942,41.166576],[-8.66961,41.167962],[-8.668098,41.168988],[-8.66664,41.170005],[-8.665767,41.170635],[-8.66574,41.170671]]"
    '''
    with open(filename) as fin:
        lines = fin.readlines()
        for line in lines:
            data = line.strip().split()
            point = Point(float(data[0]), float(data[1]), float(data[2]))
            point.latlon2cartesian()
            points.append(point)


from timeout_decorator import timeout


# # @timeout(18000)
# def OPW(points,epsilon):
#     if len(points) < 3:
#         return points
#     # print(f'len(points),points',len(points),points)
#     print(f'len(points)',len(points))

#     for p in points:
#         p.latlon2cartesian()
#     e = 0
#     originalIndex = 0
#     simplified = [originalIndex]

#     e = originalIndex + 2
#     while e < len(points):
#         i = originalIndex + 1
#         condOPW = True
#         while i < e and condOPW:
#             if synchronized_euclidean_distance(points[originalIndex],
#                                                points[i], points[e]) > epsilon:
#                 condOPW = False
#             else:
#                 i += 1
#         if not condOPW:
#             originalIndex = i
#             simplified.append(originalIndex)
#             e = originalIndex + 2
#         else:
#             e += 1
#     if simplified[-1]!=len(points)-1:
#         simplified.append(len(points) - 1)
#     simplified_points=[points[x] for x in simplified]
#     return simplified_points


def OPW(points,epsilon):
    if len(points) < 3:
        return points
    # print(f'len(points),points',len(points),points)
    # print(f'len(points)',len(points))

    for p in points:
        p.latlon2cartesian()
    e = 0
    originalIndex = 0
    simplified = [originalIndex]

    e = originalIndex + 2
    while e < len(points):
        i = originalIndex + 1
        condOPW = True
        while i < e and condOPW:
            if synchronized_euclidean_distance(points[originalIndex],
                                               points[i], points[e]) > epsilon:
                condOPW = False
            else:
                i += 1
        if not condOPW:
            originalIndex = i
            simplified.append(originalIndex)
            e = originalIndex + 2
        else:
            e += 1
    if simplified[-1]!=len(points)-1:
        simplified.append(len(points) - 1)
    simplified_points=[points[x] for x in simplified]
    return simplified_points


def OPW_unlimit(points,epsilon):
    if len(points) < 3:
        return points
    # print(f'len(points),points',len(points),points)
    print(f'len(points)',len(points))

    for p in points:
        p.latlon2cartesian()
    e = 0
    originalIndex = 0
    simplified = [originalIndex]

    e = originalIndex + 2
    while e < len(points):
        i = originalIndex + 1
        condOPW = True
        while i < e and condOPW:
            if synchronized_euclidean_distance(points[originalIndex],
                                               points[i], points[e]) > epsilon:
                condOPW = False
            else:
                i += 1
        if not condOPW:
            originalIndex = i
            simplified.append(originalIndex)
            e = originalIndex + 2
        else:
            e += 1
    if simplified[-1]!=len(points)-1:
        simplified.append(len(points) - 1)
    simplified_points=[points[x] for x in simplified]
    return simplified_points



def OPW_detail(points,epsilon):
    if len(points) < 3:
        return points
    # print(f'len(points),points',len(points),points)
    print(f'len(points)',len(points))

    for p in points:
        p.latlon2cartesian()
    print(f'transform to cartesian done')
    e = 0
    originalIndex = 0
    simplified = [originalIndex]

    e = originalIndex + 2
    while e < len(points):
        i = originalIndex + 1
        condOPW = True
        while i < e and condOPW:
            if synchronized_euclidean_distance(points[originalIndex],
                                               points[i], points[e]) > epsilon:
                condOPW = False
                print(f'   L131,e:{e},i:{i}')

            else:
                i += 1
                print(f'L136 i:{i},e:{e}')

        if not condOPW:
            originalIndex = i
            simplified.append(originalIndex)
            e = originalIndex + 2
            print(f'L139 originalIndex:{originalIndex},e:{e}')
        else:
            e += 1
            print(f'L141 e:{e}')
    if simplified[-1]!=len(points)-1:
        simplified.append(len(points) - 1)
    simplified_points=[points[x] for x in simplified]
    return simplified_points



import tqdm

def OPW_batch(orig_list_of_Points,epsilon):
    compressed_list_of_Points=[]
    for traj in tqdm.tqdm(orig_list_of_Points):
        try:
            # compressed_list_of_Points.append(OPW(traj[:5000],epsilon))
            # compressed_list_of_Points.append(OPW(traj[:2000],epsilon))

            compressed_list_of_Points.append(OPW(traj,epsilon))

        except Exception as e:
            print('OPW_batch error:',e)
            import pdb
            pdb.set_trace()
    # print('OPW_batch ',len(orig_list_of_Points),' have done')
    return compressed_list_of_Points



if __name__ == '__main__':
    ## for I use command line to exec the py file,so the name will be __main__, if use import will be okay

    filename = 'Sample.txt'#input("Enter file name: ")
    epsilon = 8#float(input("Enter value of epsilon: "))
    save_filename = 'OpeningWindow_output.txt'#input("Enter name for output file: ")
    gpsreader(filename)
    cmp_index = OPW(points,epsilon)
    with open(save_filename, "w") as s_fp:
        for i in cmp_index:
            s_fp.write(f"{points[i].get_x()} {points[i].get_y()} {int(points[i].get_time())}\n")
        # s_fp.write(f"{timeuse / 1000000.0}\n")
    # print(epsilon,':',round(len(cmp_index)/len(points),2))

    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument("args", help="describe the args of the algs ,just for record ,need to change " \
    #                                  "in the specific file, like '0.0008'")
    # argps = parser.parse_args()
    # epsilon = eval(argps.args)
    # filename = 'Sample.txt'#input("Enter file name: ")
    # # epsilon = 0.0008#float(input("Enter value of epsilon: "))
    # save_filename = 'OpeningWindow_output.txt'#input("Enter name for output file: ")
    # gpsreader(filename)
    # cmp_index = OPW(points,epsilon)
    # with open(save_filename, "w") as s_fp:
    #     for i in cmp_index:
    #         s_fp.write(f"{points[i].get_x()} {points[i].get_y()} {int(points[i].get_time())}\n")
    # # print(epsilon,':',round(len(cmp_index)/len(points),2))











