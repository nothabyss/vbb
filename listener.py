'''
1. 每隔几秒进行监听，检测有几个投票池子，即有几个.csv文件，一个投票活动对应一个csv文件。
2. 为每个csv文件创建一个blockchain对象，进行挖矿
3. 挖完矿的dat文件，命名好（可以先用创建时间进行命名），专门有一个文件夹存放dat文件，可以先按日期对该文件夹进行命名。
4. 如果某一个投票活动达到了预定的总票数，挖矿完毕，释放该对象，结束线程。如果超过了指定时间，释放对象，结束该线程。
'''
import os
import time

from datalayer.blockchain3 import Blockchain, run_mining_scheduler

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

votefile_path = os.path.join(PROJECT_PATH, 'vbbNew', 'applayer', 'vote_pool')


def count_csv_files(votefile_path):
    csv_files = [file for file in os.listdir(votefile_path) if file.endswith('.csv')]
    return csv_files

def listening():
    num_csv_files = count_csv_files(votefile_path)
    print(f"Number of csv files in directory: {num_csv_files}")
    time.sleep(5)  # 每隔5秒检测一次

def main():

    csv_files = count_csv_files(votefile_path)
    print(csv_files)
    for i in range(len(csv_files)):
        voting_activity = Blockchain(b"\x02Ed\xc1\xe7\xe1", i, 20)
        # 读取csv文件名，作为输入参数
        run_mining_scheduler(os.path.join(votefile_path, csv_files[i]))

if __name__ == '__main__':
    main()