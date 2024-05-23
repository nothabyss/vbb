from hashlib import *
import time
from threading import Thread, Lock, current_thread
import csv
import pickle
import sys
import os
import math

#--project files
from . import enc
from prolayer import verification as ver

#--<<Global variables>>

#--cryptographic difficulty
DIFFICULTY = 3

#--frequency of mining of blocks seconds
BLOCK_TIME_LIMIT = 20

#--path of project files
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)

from votetest import append_random_votes

# votefile_path = os.path.join(PROJECT_PATH, 'applayer', 'votefile.csv')
maxb = 0 
lock = Lock()

class Blockchain:
    chain = []

    def __init__(self, vote_activity_id, initiator_puk, max_nums, votefile_path):
        self.votefile_path = votefile_path
        self.add_genesis(vote_activity_id, initiator_puk, max_nums)
        print(f'[{current_thread().name}] Blockchain initialized')

    def add_genesis(self, vote_activity_id, initiator_puk, max_nums):
        genesis = GenesisBlock(vote_activity_id, initiator_puk, max_nums)
        global maxb
        maxb = max_nums
        self.chain.append(genesis)
        with open('applayer/temp/blockchain.dat', 'wb') as genfile:
            pickle.dump(genesis, genfile)
        print(f'[{current_thread().name}] Genesis block added')

    def set_votefile_path(self, path):
        self.votefile_path = path

    @staticmethod
    def display():
        for block in Blockchain.chain:
            print(f'[{current_thread().name}] Block Height: {block.height}')
            print(f'[{current_thread().name}] Data in block: {block.votedata}')
            print(f'[{current_thread().name}] Total in block: {block.votecount}')
            print(f'[{current_thread().name}] Number of votes: {block.number_of_votes}')
            print(f'[{current_thread().name}] Merkle root: {block.merkle}')
            print(f'[{current_thread().name}] Difficulty: {block.DIFFICULTY}')
            print(f'[{current_thread().name}] Time stamp: {block.timeStamp}')
            print(f'[{current_thread().name}] Previous hash: {block.prevHash}')
            print(f'[{current_thread().name}] Block Hash: {block.hash}')
            print(f'[{current_thread().name}] Nonce: {block.nonce}\n\t\t|\n\t\t|')

    def update_votepool(self, processed_votedata):
        try:
            with open(self.votefile_path, 'r', newline='', encoding='UTF-8') as file:
                existing_votes = list(csv.reader(file))
            processed_rows = [
                [vote['Voter Public Key'].strip(), vote['Candidate'].strip(), vote['TimeStamp'].strip()]
                for vote in processed_votedata
            ]
            existing_votes = [[item.strip() for item in row] for row in existing_votes]
            remaining_votes = [vote for vote in existing_votes if vote not in processed_rows]
            with open(self.votefile_path, 'w', newline='', encoding='UTF-8') as file:
                csv.writer(file).writerows(remaining_votes)
        except Exception as e:
            print(f'[{current_thread().name}] Error updating votefile.csv: {e}')

    def is_votepool_empty(self):
        my_path = self.votefile_path
        return not os.path.isfile(my_path) or os.stat(my_path).st_size == 0

    def mine_if_needed(self):
        while True:
            if self.should_mine():
                total_votes = self.count_total_votes_in_pool()
                blocks_to_mine, _ = self.calculate_block_distribution(total_votes)

                while total_votes > 0 and blocks_to_mine > 0:
                    votes_per_block = math.ceil(total_votes / blocks_to_mine)
                    print(f'[{current_thread().name}] Mining a block with {votes_per_block} votes...')

                    # Perform mining outside the critical section
                    new_block = Block()
                    new_block.mineblock(self, votes_per_block)

                    # Acquire the lock before updating shared resources
                    with lock:
                        print(f'[{current_thread().name}] acquired the lock')
                        Blockchain.chain.append(new_block)
                        self.update_votepool(new_block.votedata)
                        total_votes = self.count_total_votes_in_pool()
                        blocks_to_mine -= 1
                        print(f'[{current_thread().name}] released the lock')

                    print(f'[{current_thread().name}] Block mined. {total_votes} votes remaining, {blocks_to_mine} blocks to mine.')
            else:
                time.sleep(BLOCK_TIME_LIMIT)
                print(f'[{current_thread().name}] No mining needed at this time.')

    def should_mine(self):
        total_votes = self.count_total_votes_in_pool()
        blocks_needed, _ = self.calculate_block_distribution(total_votes)
        return total_votes > 0 or (len(self.chain) - 1 < blocks_needed)

    def count_total_votes_in_pool(self):
        count = 0
        try:
            with open(self.votefile_path, 'r', newline='', encoding='UTF-8') as votepool:
                csvreader = csv.reader(votepool)
                count = sum(1 for row in csvreader)
        except (IOError, IndexError):
            print(f'[{current_thread().name}] Error reading votefile.csv')
        return count

    def calculate_block_distribution(self, total_votes):
        if len(self.chain) >= 3:
            min_blocks = 1
        else:
            min_blocks = 2
        blocks_needed = min_blocks
        if total_votes > min_blocks * maxb:
            votes_per_block = maxb
            extra_blocks = math.ceil((total_votes - min_blocks * maxb) / votes_per_block)
            blocks_needed += extra_blocks
        else:
            votes_per_block = math.ceil(total_votes / min_blocks)
        return blocks_needed, votes_per_block

class Block:
    def __init__(self, height=0, votes=0, merkle='0', tree=None, timeStamp=0, prevHash='0', representative_pow=0, hash='Genesis'):
        if tree is None:
            tree = []
        self.height = height
        self.votedata = []
        self.votecount = []
        self.number_of_votes = votes
        self.tree = tree
        self.merkle = merkle
        self.DIFFICULTY = DIFFICULTY
        self.timeStamp = time.time()
        self.prevHash = prevHash
        self.nonce = representative_pow
        self.hash = hash

    def representative_pow(self, zero=DIFFICULTY):
        self.nonce = 0
        while (sha256(self.calcHash().encode('utf-8')).hexdigest()[:zero] != '0' * zero):
            self.nonce += 1
        return self.nonce

    def calcHash(self):
        return sha256((str(self.merkle) + str(self.timeStamp) + str(self.nonce) + str(self.prevHash)).encode('utf-8')).hexdigest()

    @staticmethod
    def load_data(blockchain_instance, votes_per_block):
        votelist = []
        votecount = {}
        count = 0
        try:
            with open(blockchain_instance.votefile_path, 'r', newline='', encoding='UTF-8') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    if count >= votes_per_block:
                        break
                    voter_pub_key, candidate, timestamp = row
                    votelist.append({'Voter Public Key': voter_pub_key, 'Candidate': candidate, 'TimeStamp': timestamp})
                    if candidate in votecount:
                        votecount[candidate] += 1
                    else:
                        votecount[candidate] = 1
                    count += 1
        except (IOError, IndexError) as e:
            print(f'[{current_thread().name}] Error reading votefile.csv: {e}')
        finally:
            if count > 0:
                blockchain_instance.update_votepool(votelist)
        return votelist, votecount, count

    def merkleRoot(self):
        votedata = self.votedata
        if len(votedata) == 0:
            return '', []
        if len(votedata) == 1:
            hash_value = sha256(str(votedata[0]).encode()).hexdigest()
            return hash_value, [hash_value]
        vote_hashes = [sha256(str(vote).encode()).hexdigest() for vote in votedata]
        all_hashes = vote_hashes.copy()
        while len(vote_hashes) > 1:
            if len(vote_hashes) % 2 == 1:
                vote_hashes.append(vote_hashes[-1])
            new_hashes = []
            for i in range(0, len(vote_hashes), 2):
                concatenated = vote_hashes[i] + vote_hashes[i + 1]
                new_hash = sha256(concatenated.encode()).hexdigest()
                new_hashes.append(new_hash)
            all_hashes.extend(new_hashes)
            vote_hashes = new_hashes
        return vote_hashes[0], all_hashes

    def mineblock(self, blockchain_instance, votes_per_block):
        self.height = len(Blockchain.chain)
        self.prevHash = Blockchain.chain[-1].hash if self.height > 0 else '0'
        self.votedata, self.votecount, self.number_of_votes = Block.load_data(blockchain_instance, votes_per_block)
        self.merkle, self.tree = self.merkleRoot()
        self.DIFFICULTY = DIFFICULTY
        self.timeStamp = time.time()
        self.nonce = self.representative_pow()
        self.hash = self.calcHash()
        if blockchain_instance.count_total_votes_in_pool() == 0:
            Blockchain.display()
        return self

class GenesisBlock(Block):
    def __init__(self, vote_activity_id, initiator_puk, max_nums, version="v1.0"):
        super().__init__()
        self.vote_activity_id = vote_activity_id
        self.initiator_puk = initiator_puk
        self.version = version
        self.max_nums = max_nums
        self.hash = self.calcHash()
        self.timeStamp = time.time()

    def calcHash(self):
        return sha256((str(self.vote_activity_id) + str(self.timeStamp) + str(self.initiator_puk) + str(self.version)).encode('utf-8')).hexdigest()
