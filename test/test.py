import json
import os
import pickle

from flask import jsonify

blockchain_name = "13aaee7dc8fc47201fb4ec60e53ff3ced373fba0fad0f977c6919e84785f0c"

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




def find_blockchain_filename(root_dir, target_substring):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            # 判断文件夹名称是否包含特定字符串
            if target_substring in dirname:
                # 找到含有特定字符串的文件夹，然后输出文件夹名字
                return dirname

blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_name)


def main():
    chain = []
    i = 1
    while True:
        chain_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/block-{i}.dat')
        try:
            with open(chain_file_path, 'rb') as file:
                block = pickle.load(file)
                block_dict = {
                    'height': block.height,
                    'votedata': block.votedata,
                    'votecount': block.votecount,
                    'number_of_votes': block.number_of_votes,
                    'merkle': block.merkle,
                    'difficulty': block.DIFFICULTY,
                    'timeStamp': block.timeStamp,
                    'prevHash': block.prevHash,
                    'hash': block.hash,
                    'nonce': block.nonce
                }

                json_block = json.dumps(block_dict)
                chain.append(json_block)
                i += 1
        except FileNotFoundError:
            break
    chain = jsonify(chain)
    print(chain)


if __name__ == '__main__':
    main()

