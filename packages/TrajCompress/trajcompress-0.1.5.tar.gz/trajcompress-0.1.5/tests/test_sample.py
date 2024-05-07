import argparse
import unittest
from types import SimpleNamespace
import TrajCompress
import time
import pandas as pd



class TestTrajCompression(unittest.TestCase):

    def setUp(self):
        # 这里调用get_sample来获取测试数据
        self.orig_list_of_Points = TrajCompress.get_sample()
        assert len(self.orig_list_of_Points) > 0 and len(self.orig_list_of_Points[0]) > 0,\
            f'you should have at least one traj in Sample.txt'

    def test_compression(self):
        # parser = argparse.ArgumentParser()
        # parser.add_argument("--alg", default='Angular', help="name of the compression algorithm")
        # parser.add_argument("--args", default='3', help="algorithm specific arguments")
        # args = parser.parse_args()

        # config = SimpleNamespace(alg=args.alg, args=args.args)
        methods2args = {
            'OpeningWindow': '15',
            'Uniform': '5',
            'Dead_Reckoning': '2.9e-5',
            'TD_TR': '2e-6',
            'interval': '0.05',
            'Angular': '0.1',
            'bottom_up': '20',
            'threshold': '3,3',
            'STTrace': '50',
            'DP': '15',
            'DOTS': '1.2,0.8',
            'SQUISH_E': '2,1',
            'OPERB': '100'
        }
        results = []


        for name,args in methods2args.items():
            is_ordered=True
            config = SimpleNamespace(alg=name, args=args)


            start_time = time.time()
            compressed_points = TrajCompress.choose_compression_method(config, self.orig_list_of_Points)

            for i, o in zip(self.orig_list_of_Points, compressed_points):
                print(f"Original: {len(i)}, Compressed: {len(o)}")
                self.assertTrue(len(o) <= len(i))

            duration = time.time() - start_time
            for L_orig,L_comp in zip(self.orig_list_of_Points, compressed_points):
                if self._is_ordered_subsequence(L_orig,L_comp) is False:
                    is_ordered=False
                # self.assertTrue(self._is_ordered_subsequence(L_orig,L_comp),
                #                 f"Algorithm {name} failed to maintain order with args {args}")


            compression_rate = sum(len(o) for o in compressed_points) / sum(len(i) for i in self.orig_list_of_Points)
            results.append({
                'Algorithm': name,
                'Parameters': args,
                'Compression Rate': compression_rate,
                'Duration (seconds)': duration,
                'Is Ordered': is_ordered
            })
            print(f"{name} with args {args}: Duration = {duration:.2f} seconds, Is Ordered: {is_ordered}")



        # Write results to a CSV file
        with open('compression_results.csv', 'w', newline='') as file:
            result_df=pd.DataFrame(results)
            print(result_df)
            writer = result_df.to_csv(file, index=False)


        # check the points are in the same order, and they exist in the original traj
    @staticmethod
    def _is_ordered_subsequence(original, compressed):
        it = iter(original)
        last_time = None
        for comp_point in compressed:
            orig_point = next((x for x in it if abs(x.get_time() - comp_point.get_time())<1e-6), None)
            if orig_point is None:
                print(f"Point {comp_point} not found in original traj")
                return False  
            comp_time = comp_point.get_time()
            if last_time is not None and comp_time <= last_time:
                return False  # 如果时间不是递增的，返回False
            last_time = comp_time
        return True


        

if __name__ == '__main__':
    unittest.main()
