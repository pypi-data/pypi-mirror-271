from .src.List_Points_2_List_Points import choose_compression_method
from .utils.get_sample import get_sample


# from TrajCompress.src.List_Points_2_List_Points import choose_compression_method
# from TrajCompress.utils.get_sample import get_sample

# if __name__ == '__main__':
#     from types import SimpleNamespace
#     orig_list_of_Points = get_sample()
#     breakpoint()



#     parser.add_argument("--alg",default='OPERB', help="name of the py file like 'bottom-up'")
#     parser.add_argument("--args",default='100',help="describe the args of the algs, just for record, like '90'")
    
#     args = parser.parse_args()

#     # Convert argparse.Namespace to a simpler types.SimpleNamespace
#     config = SimpleNamespace(alg=args.alg, args=args.args)
    
#     print('orig_list_of_Points:', orig_list_of_Points)
#     choose_compression_method(config, orig_list_of_Points)
#     # Do something with compressed_points...
#     # assert compressed_points[0][0]
#     # parser.add_argument("--alg",default='RLTS', help="name of the py file like 'bottom-up'")
#     config = SimpleNamespace(alg=args.alg, args=args.args)

#     for i,o in zip(orig_list_of_Points,compressed_points):
#         print(len(i),len(o))


#     print('done')

#     '''
#     cd /home/chenghao/mk_pkg_compression/TrajCompress/
#     python __init__.py
#     '''