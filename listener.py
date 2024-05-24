'''
1. 每隔几秒进行监听，检测有几个投票池子，即有几个.csv文件，一个投票活动对应一个csv文件。
2. 为每个csv文件创建一个blockchain对象，进行挖矿
3. 挖完矿的dat文件，命名好（可以先用创建时间进行命名），专门有一个文件夹存放dat文件，可以先按日期对该文件夹进行命名。
4. 如果某一个投票活动达到了预定的总票数，挖矿完毕，释放该对象，结束线程。如果超过了指定时间，释放对象，结束该线程。
'''
import os
import time
from threading import Thread
from datalayer.blockchain2 import Blockchain

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
votefile_path = os.path.join(PROJECT_PATH, 'vbb', 'applayer', 'vote_pool')

def count_csv_files(votefile_path):
    csv_files = [file for file in os.listdir(votefile_path) if file.endswith('.csv')]
    return csv_files

def run_mining_scheduler(blockchain_instance):
    mining_thread = Thread(target=blockchain_instance.mine_if_needed)
    # mining_thread.start()
    return mining_thread

# def process_csv_file(file_path, index):
#     # Create a Blockchain object
#     voting_activity = Blockchain(b"\x02Ed\xc1\xe7\xe1", index, 20, file_path)
#     run_mining_scheduler(voting_activity)

def main():
    csv_files = count_csv_files(votefile_path)
    print(csv_files)
    threads = []

    for i, csv_file in enumerate(csv_files):
        file_path = os.path.join(votefile_path, csv_file)
        print(csv_file)
        # thread = Thread(target=process_csv_file, args=(file_path, i))
        voting_activity = Blockchain(b"\x02Ed\xc1\xe7\xe1", i, 200, 7, file_path)
        thread = run_mining_scheduler(voting_activity)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()