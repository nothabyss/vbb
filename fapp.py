import os
import pickle
import re
import sys
from threading import Thread

from flask import *
import datalayer.enc as enc
from datalayer.blockchain2 import Blockchain

app=Flask("block")
app.config.from_object(app.config)

# @app.route("/")
# def hello():
#     return "hello world"
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.join(PROJECT_PATH, 'vbb')
@app.route('/enc/keys')
def keys():
    data = enc.rsakeys()
    response = make_response(jsonify(data), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
@app.route('/enc/hash_public_key', methods=['POST'])
def hash_public_key():
    public_key = request.form.get('public_key')  # 获取名为'name'的参数值
    hash_pk = enc.hash_public_key(public_key)
    response = make_response(jsonify(hash_pk), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/mine', methods=['POST'])
def get_post_body():
    body = request.get_data()
    return body

@app.route('/submit_vote', methods=['POST'])
def submit_vote():


    data = request.json

    vote_activity_id = data.get('vote_activity_id')
    max_time = data.get('max_time')
    max_votes = data.get('max_votes')
    creator_public_key = data.get('creator_public_key')
    file_path = data.get('file_path')
    # 在这里执行相关操作，比如保存投票信息到数据库
    voting_activity = Blockchain(creator_public_key, vote_activity_id, max_votes, max_time, file_path)

    response = {
        'message': 'Vote submitted successfully',
        'vote_activity_id': vote_activity_id,
        'max_time': max_time,
        'max_votes': max_votes,
        'creator_public_key': creator_public_key
    }

    return jsonify(response)
@app.route('/data/load_blockchain', methods=['POST'])
def load_blockchain():

    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id)
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
    response = make_response(chain, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

def find_id(folder_name):
    match = re.search(r'chain_(\d+)', folder_name)

    if match:
        number_after_chain = match.group(1)
        return number_after_chain
    else:
        # print("cannot find the blockchain, please check your name")
        return 0
def find_blockchain_filename(root_dir,  id):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            # 判断文件夹名称是否包含特定字符串
            if  str(id) == find_id(dirname):
                # 找到含有特定字符串的文件夹，然后输出文件夹名字
                return dirname

@app.route('/data/load_Genesis', methods=['POST'])
def load_Genesis():
    # blockchain_name = request.form.get('blockchain_name')  # 获取名为'name'的参数值
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH,  blockchain_id)
    chain = []
    chain_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/GenesisBlock.dat')
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
    except FileNotFoundError:
        response = {
            'error': "cannot find GenesisBlock"
        }
        return response
    response = make_response(json_block, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/protocol/verify', methods=['POST'])
def verify():
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id)
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
    response = make_response(chain, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    # a = find_blockchain_filename(PROJECT_PATH,  200)
    # print(a)
    # print(PROJECT_PATH)
    # print(sys.path)
    # sys.path.append(PROJECT_PATH)
    # print(sys.path)
    app.run(host="0.0.0.0", port=5000)