from threading import Thread

from flask import *
import datalayer.enc as enc
from vbb.datalayer.blockchain import Blockchain

app=Flask("block")
app.config.from_object(app.config)

# @app.route("/")
# def hello():
#     return "hello world"
def run_mining_scheduler(blockchain_instance):
    mining_thread = Thread(target=blockchain_instance.mine_if_needed)
    # mining_thread.start()
    return mining_thread

@app.route('/enc/keys')
def index():
    data = enc.rsakeys()
    response = make_response(jsonify(data), 200)
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
    thread = run_mining_scheduler(voting_activity)
    thread.start()
    thread.join()

    response = {
        'message': 'Vote submitted successfully',
        'vote_activity_id': vote_activity_id,
        'max_time': max_time,
        'max_votes': max_votes,
        'creator_public_key': creator_public_key
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()