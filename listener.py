'''
1. 每隔几秒进行监听，检测有几个投票池子，即有几个.csv文件，一个投票活动对应一个csv文件。
2. 为每个csv文件创建一个blockchain对象，进行挖矿
3. 挖完矿的dat文件，命名好（可以先用创建时间进行命名），专门有一个文件夹存放dat文件，可以先按日期对该文件夹进行命名。
4. 如果某一个投票活动达到了预定的总票数，挖矿完毕，释放该对象，结束线程。如果超过了指定时间，释放对象，结束该线程。
'''
import os
import time
from threading import Thread, Lock
from datalayer.blockchain2 import Blockchain

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
votefile_path = os.path.join(PROJECT_PATH, 'vbb', 'records', 'vote_pool')


processed_files = set()

def count_csv_files(votefile_path):
    csv_files = [file for file in os.listdir(votefile_path) if file.endswith('.csv')]
    return csv_files

def worker(blockchain_instance):
    blockchain_instance.mine_if_needed()
    # votefile_path = blockchain_instance.votefile_path
    # if os.stat(votefile_path).st_size == 0:
    #     os.remove(votefile_path)
    # Cleanup: Remove empty CSV files after processing
    # lock.acquire()
    # lock.release()

def main():

    while True:
        csv_files = count_csv_files(votefile_path)
        
        for csv_file in csv_files:

            if csv_file not in processed_files:
                processed_files.add(csv_file)

                file_path = os.path.join(votefile_path, csv_file)
                print(csv_file)
                # 解析文件名
                file_parts = csv_file.replace('.csv', '').split('-')
                vote_id = file_parts[0]
                max_votes = int(file_parts[1])
                max_days = int(file_parts[2])
                public_key = file_parts[3]
                print("Processing:", csv_file)


                # Create a Blockchain object
                blockchain_instance = Blockchain(vote_id, public_key, max_votes, max_days, file_path)
                # Start a thread for mining
                mining_thread = Thread(target=worker, args=(blockchain_instance,))
                mining_thread.start()
            else:
                continue
        print("***************************")
        time.sleep(20)  # Check for new files every 20 seconds



if __name__ == '__main__':
    main()