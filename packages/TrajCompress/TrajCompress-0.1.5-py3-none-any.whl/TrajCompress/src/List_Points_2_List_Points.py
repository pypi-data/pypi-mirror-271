
import os
import sys
import argparse
from types import SimpleNamespace

# def setup_environment():
#     """
#     Set up the environment for the script.
#     """
#     # Optionally, change the current working directory to the script directory
#     origional_dir = os.getcwd()
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     os.chdir(script_dir)

#     # Append necessary paths to sys.path
#     sys.path.append(os.path.join(script_dir,'..', '..', 'Zhou'))
#     sys.path.append(os.path.join(script_dir,'..', '..', 'Zhu'))
#     sys.path.append(os.path.join(script_dir,'..', '..', 'Liu'))

#     os.chdir(origional_dir)
#     # print('L22 after set',sys.path)

# def setup_environment_l2l():
#     """
#     Set up the environment for the script.
#     """
#     # Optionally, change the current working directory to the script directory
#     origional_dir = os.getcwd()
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     os.chdir(script_dir)

#     # Append necessary paths to sys.path
#     sys.path.append(os.path.join(script_dir,'..', '..', 'Zhou'))
#     sys.path.append(os.path.join(script_dir,'..', '..', 'Zhu'))
#     sys.path.append(os.path.join(script_dir,'..', '..', 'Liu'))

#     os.chdir(origional_dir)
#     print('L22 after set',sys.path)

def choose_compression_method(config, orig_list_of_Points):
    """
    Choose a compression method based on the given configuration.
    """
    # setup_environment_l2l()
    # print('l2l L45',sys.path)
    # import .algrithms.Angular_batch as Angular_b
    # import .algrithms.bottom_up_batch as bottom_up_b
    # import .algrithms.Dead_Reckoning_batch as Dead_Reckoning_b
    # import .algrithms.DP_batch as DP_b
    # import .algrithms.DOTS_batch as DOTS_b
    # import .algrithms.interval_batch as interval_b
    # import .algrithms.OpeningWindow_batch as OPW_b
    # import .algrithms.OPERB_batch as OPERB_b
    # import .algrithms.STTrace_batch as STTrace_b
    # import .algrithms.SQUISH_E_batch as SQUISH_E_b
    # import .algrithms.TD_TR_batch as TD_TR_b
    # import .algrithms.threshold_batch as threshold_b
    # import .algrithms.Uniform_batch as Uniform_b

    from .algorithms import Angular_batch as Angular_b
    from .algorithms import bottom_up_batch as bottom_up_b
    from .algorithms import Dead_Reckoning_batch as Dead_Reckoning_b
    from .algorithms import DP_batch as DP_b
    from .algorithms import DOTS_batch as DOTS_b
    from .algorithms import interval_batch as interval_b
    from .algorithms import OpeningWindow_batch as OPW_b
    from .algorithms import OPERB_batch as OPERB_b
    from .algorithms import STTrace_batch as STTrace_b
    from .algorithms import SQUISH_E_batch as SQUISH_E_b
    from .algorithms import TD_TR_batch as TD_TR_b
    from .algorithms import threshold_batch as threshold_b
    from .algorithms import Uniform_batch as Uniform_b
    
    alg = config.alg
    args = config.args
    implemented_algs=['OpeningWindow','Uniform','Dead_Reckoning','TD_TR','interval',
                  'Angular','bottom_up','threshold','STTrace','DP','DOTS','SQUISH_E',
                  'OPERB',]#'RLTS'
    assert alg in implemented_algs, f'{alg} not in the implemented_algs:{implemented_algs}'


    if alg == 'OpeningWindow':
        compressed_list_of_Points = OPW_b.OPW_batch(orig_list_of_Points, epsilon=float(args))
    if alg == 'Uniform':
        compressed_list_of_Points = Uniform_b.Uniform_batch(orig_list_of_Points, uniform=float(args))
    if alg == 'Dead_Reckoning':
        compressed_list_of_Points = Dead_Reckoning_b.Dead_Reckoning_batch(orig_list_of_Points, epsilon=float(args))
    if alg == 'TD_TR':
        compressed_list_of_Points = TD_TR_b.TD_TR_batch(orig_list_of_Points, Dmax=float(args))
    if alg == 'interval':
        compressed_list_of_Points = interval_b.interval_batch(orig_list_of_Points, epsilon=float(args))
    if alg == 'Angular':
        compressed_list_of_Points = Angular_b.Angular_batch(orig_list_of_Points, error_t=eval(args))
    if alg=='bottom_up':
        compressed_list_of_Points=bottom_up_b.bottom_up_batch(orig_list_of_Points,max_error=float(args))
    if alg=='threshold':
        compressed_list_of_Points=threshold_b.threshold_batch(orig_list_of_Points,threshold_tup=eval(args))
    if alg=='STTrace':
        compressed_list_of_Points=STTrace_b.STTrace_batch(orig_list_of_Points,cmp_ratio=int(float(args)))
    if alg=='DP':
        compressed_list_of_Points=DP_b.DP_batch(orig_list_of_Points,Dmax=float(args))
    if alg=='DOTS':
        compressed_list_of_Points=DOTS_b.DOTS_batch(orig_list_of_Points,arg_tup=eval(args))
    if alg=='SQUISH_E':
        compressed_list_of_Points=SQUISH_E_b.SQUISH_batch(orig_list_of_Points,arg_tup=eval(args))
    if alg=='OPERB':
        compressed_list_of_Points=OPERB_b.OPERB_batch(orig_list_of_Points,max_error=eval(args))
    if alg=='RLTS':

        print('this is not included in this package for it have much more dependencies, especailly about specific version of tensorflow')

        sys.path.append('/home/chenghao/RLTS')
        sys.path.append('/home/chenghao/RLTS/online-rlts')#TODO
        import list_Point_io
        import Point
        import os
        origional_dir = os.getcwd()
        os.chdir('/home/chenghao/RLTS/online-rlts')
        config.list_of_trajs=orig_list_of_Points#[:20000]#TODO
        
        compressed_trajectories=list_Point_io.run_trajectory_compression(config)
        compressed_list_of_Points=[[Point.Point(point_info[0],point_info[1],point_info[2])for point_info in sub_traj] for sub_traj in compressed_trajectories]
        # compressed_list_of_Points=[Point.Point(la,lo,time) for la,lo,time in compressed_trajectories]
        os.chdir(origional_dir)

    return compressed_list_of_Points

def get_sample(): #TODO, move this to utils
    # Get the directory where the script file is located
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # Setup environment
    # print('before',sys.path)
    # setup_environment_l2l()
    # print('after',sys.path)
    # Assume orig_list_of_Points is provided or loaded somewhere
    orig_list_of_Points = []  # Your list of points
    # Choose compression method
    import utils_copy
    this_traj=[]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', '..', 'Liu', 'Sample.txt')
    with open(file_path) as f:
    # with open ('Sample.txt') as f:
        for line in f:
            a,o,t=list(map(eval,line.split()))
            this_traj.append(utils_copy.Point.Point(a,o,t))
    orig_list_of_Points.append(this_traj)
    orig_list_of_Points.append(this_traj[:20])
    return orig_list_of_Points

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--alg",default='OPERB', help="name of the py file like 'bottom-up'")
    # parser.add_argument("--args",default='100',help="describe the args of the algs, just for record, like '90'")
    
    parser.add_argument("--alg",default='RLTS', help="name of the py file like 'bottom-up'")
    parser.add_argument("--args",default="/home/chenghao/RLTS/online-rlts/save_1211_06/1.4023512414981615e-05_ratio_0.6/",help="describe the args of the algs, just for record, like '90'")

    # parser.add_argument("--alg",default='SQUISH_E', help="name of the py file like 'bottom-up'")
    # # parser.add_argument("goal_folder",defalult='../Zhou', help="Path to input file like '../Zhou/'")
    # parser.add_argument("--args",default='1.2,2',help="describe the args of the algs, just for record, like '90'")
    

    # parser.add_argument("--alg",default='STTrace', help="name of the py file like 'bottom-up'")
    # # parser.add_argument("goal_folder",defalult='../Zhou', help="Path to input file like '../Zhou/'")
    # parser.add_argument("--args",default='54',help="describe the args of the algs, just for record, like '90'")
    

    args = parser.parse_args()

    # Convert argparse.Namespace to a simpler types.SimpleNamespace
    config = SimpleNamespace(alg=args.alg, args=args.args)
    # if RLTS:
    if not hasattr(config, 'ratio'):
        print(' you need to specify the compression ratio you want  (default 0.6)')
        config.ratio=float(input() or 0.6) 
    
    orig_list_of_Points=get_sample()
    # print(sys.path)
    compressed_points = choose_compression_method(config, orig_list_of_Points)
    # Do something with compressed_points...
    # assert compressed_points[0][0]
    for i,o in zip(orig_list_of_Points,compressed_points):
        print(len(i),len(o))


'''
python /home/user/ZCH/compression_GMVAE_STVEC/gmvae_compression_batch/0/l2l.py --alg OPERB --args 100

'''