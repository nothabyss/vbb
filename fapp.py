import os
import pickle
import re
import shutil
import sys
from threading import Thread

from flask import *
import datalayer.enc as enc
from datalayer.blockchain2 import Blockchain
from vbb.ftools import find_blockchain_filename, msg2java
from vbb.prolayer.verification import sync_blocks, verfiy_merkle, verify_block

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
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id, 'chains')
    chain = []
    #load Genesis block
    Genesis_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/GenesisBlock.dat')
    with open(Genesis_file_path, 'rb') as file:
        Genesis_block = pickle.load(file)
        Genesis_dict = {
            'height': Genesis_block.height,
            'votedata': Genesis_block.votedata,
            'votecount': Genesis_block.votecount,
            'number_of_votes': Genesis_block.number_of_votes,
            'merkle': Genesis_block.merkle,
            'difficulty': Genesis_block.DIFFICULTY,
            'timeStamp': Genesis_block.timeStamp,
            'prevHash': Genesis_block.prevHash,
            'hash': Genesis_block.hash,
            'nonce': Genesis_block.nonce
        }
        json_Genesis = json.dumps(Genesis_dict)
    chain.append(json_Genesis)
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




@app.route('/data/load_Genesis', methods=['POST'])
def load_Genesis():
    # blockchain_name = request.form.get('blockchain_name')  # 获取名为'name'的参数值
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH,  blockchain_id, 'chains')
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

@app.route('/protocol/delete_csv', methods=['POST'])
def delete_csv():
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id, 'vote_pool')
    completed_csv = os.path.join(PROJECT_PATH, f'records/vote_pool/{blockchain_name}')

    if os.path.exists(completed_csv):  # 检查路径是否存在
        if os.stat(completed_csv).st_size == 0:
            os.remove(completed_csv)
            print (f"{completed_csv}  deleted")
            return make_response("Success", 200)
        else:
            return make_response("Not_empty", 201)
    else:
        print(f"{completed_csv}  not found")
        return make_response("Error", 201)

@app.route('/protocol/delete_chain', methods=['POST'])
def delete_a_voting_activity():
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id, 'chains')
    chain_folder_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}')
    if os.path.exists(chain_folder_path) and os.path.isdir(chain_folder_path):  # 检查路径是否存在且为文件夹
        shutil.rmtree(chain_folder_path)
        print (f"{chain_folder_path} folder deleted")
        return make_response("Success", 200)
    else:
        print(f"{chain_folder_path} folder not found or not a directory")
        return make_response("Error", 201)

@app.route('/protocol/syn_blocks', methods=['POST'])
def syn_blocks():
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id, 'chains')
    chain = []
    #load Genesis block
    Genesis_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/GenesisBlock.dat')
    with open(Genesis_file_path, 'rb') as file:
        Genesis_block = pickle.load(file)
    chain.append(Genesis_block)
    i = 1
    while True:
        chain_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/block-{i}.dat')
        try:
            with open(chain_file_path, 'rb') as file:
                block = pickle.load(file)
                chain.append(block)
                i += 1
        except FileNotFoundError:
                break

    # 去掉'chain_'
    input_str = blockchain_name.replace('chain_', '')
    # 用'-'作为分隔符来拆分字符串
    attributes = input_str.split('-')
    # 逐个读取每个数值
    reload_blockchain = Blockchain(attributes[0], attributes[3], attributes[1], attributes[2], None, False, chain)
    index, flag = sync_blocks(reload_blockchain)
    if flag == True:
        result = "Success"
        response = make_response(result, 200)
    else:
        result = str(index)
        response = make_response(result, 201)
    return response

@app.route('/protocol/verify_blocks', methods=['POST'])
def verify_blocks():
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id, 'chains')
    chain = []
    #load Genesis block
    Genesis_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/GenesisBlock.dat')
    with open(Genesis_file_path, 'rb') as file:
        Genesis_block = pickle.load(file)
    chain.append(Genesis_block)
    i = 1
    while True:
        chain_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/block-{i}.dat')
        try:
            with open(chain_file_path, 'rb') as file:
                block = pickle.load(file)
                chain.append(block)
                i += 1
        except FileNotFoundError:
                break

    response = None
    for block in chain:
        result = verify_block(block)
        if result == 0:
            result = "Error"
            response = make_response(result, 200)
            break
        else:
            response = make_response("Success", 201)
    return response

@app.route('/protocol/verify_merkles', methods=['POST'])
def verify_merkles():
    blockchain_id = request.form.get('blockchain_id')  # 获取名为'name'的参数值
    blockchain_name = find_blockchain_filename(PROJECT_PATH, blockchain_id, 'chains')
    chain = []
    #load Genesis block
    Genesis_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/GenesisBlock.dat')
    with open(Genesis_file_path, 'rb') as file:
        Genesis_block = pickle.load(file)
    chain.append(Genesis_block)
    i = 1
    while True:
        chain_file_path = os.path.join(PROJECT_PATH, f'records/chains/{blockchain_name}/block-{i}.dat')
        try:
            with open(chain_file_path, 'rb') as file:
                block = pickle.load(file)
                chain.append(block)
                i += 1
        except FileNotFoundError:
                break

    response = None
    for block in chain:
        result = verfiy_merkle(block)
        if result == 0:
            result = "Error"
            response = make_response(result, 200)
            break
        else:
            response = make_response("Success", 201)
    return response

if __name__ == '__main__':
    # a = find_blockchain_filename(PROJECT_PATH,  200)
    # print(a)
    # print(PROJECT_PATH)
    # print(sys.path)
    # sys.path.append(PROJECT_PATH)
    # print(sys.path)
    app.run(host="0.0.0.0", port=5000)