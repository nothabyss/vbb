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
output_path = os.path.join(PROJECT_PATH, 'vbb', 'records', 'dat_files')

if not os.path.exists(output_path):
    os.makedirs(output_path)

lock = Lock()
processed_files = set()

def count_csv_files(votefile_path):
    csv_files = [file for file in os.listdir(votefile_path) if file.endswith('.csv')]
    return csv_files

def worker(blockchain_instance, output_file, csv_file):
    blockchain_instance.mine_if_needed()
    blockchain_instance.save_to_file(output_file)
    
    # Cleanup: Remove empty CSV files after processing
    lock.acquire()
    if os.stat(output_file.replace('.dat', '.csv')).st_size == 0:
        os.remove(output_file.replace('.dat', '.csv'))
        print(f"Removed empty CSV file: {csv_file}")
    lock.release()

def monitor_directory():
    while True:
        csv_files = count_csv_files(votefile_path)
        
        for csv_file in csv_files:
            lock.acquire()
            if csv_file not in processed_files:
                processed_files.add(csv_file)
                lock.release()
                
                file_path = os.path.join(votefile_path, csv_file)
                print("Processing:", csv_file)

                # Use a default configuration for Blockchain
                vote_id = "default_vote_id"
                max_votes = 30  # Default maximum votes
                max_days = 7  # Default maximum days
                public_key = "default_public_key"

                # Create a Blockchain object
                blockchain_instance = Blockchain(vote_id, public_key, max_votes, max_days, file_path)
                output_file = os.path.join(output_path, f"{time.strftime('%Y%m%d-%H%M%S')}-{csv_file.replace('.csv', '.dat')}")
                print(f"Blockchain object created: {blockchain_instance}")
                print(f"Chain: {blockchain_instance.chain}")

                # Start a thread for mining
                mining_thread = Thread(target=worker, args=(blockchain_instance, output_file, csv_file))
                mining_thread.start()
            else:
                lock.release()

        time.sleep(3)  # Check for new files every 3 seconds

def main():
    monitor_thread = Thread(target=monitor_directory)
    monitor_thread.start()
    monitor_thread.join()

if __name__ == '__main__':
    main()