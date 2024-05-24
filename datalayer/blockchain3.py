#--libraries
#--libraries
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
    #--holds the info of chain of blocks as objects
    chain = []
    
    # adminpriv,adminpub = enc.rsakeys() # 获得公钥和私钥
    #--administrator public/private key pair generated along with the blockchain initialization.
    #--the public key of admin will be used to encrypt the vote data for confidentiality
    #公钥用来加密投票信息
    # with open('temp/Adminkeys.txt', 'wb') as adminkeyfile:
    #     pickle._dump(adminpriv,adminkeyfile)
    #     pickle._dump(adminpub,adminkeyfile)

    def __init__(self, vote_activity_id, initiator_puk, max_nums, votefile_path):
        self.votefile_path = votefile_path
        self.add_genesis(vote_activity_id, initiator_puk, max_nums)
        print(f'[{current_thread().name}] Blockchain initialized')

    #--genesis block creation has nothing to do with blockchain class,
    #--..but has to be created when blockchain is initialized
    def add_genesis(self, vote_activity_id, initiator_puk, max_nums):
        genesis = GenesisBlock(vote_activity_id, initiator_puk, max_nums)
        global maxb
        maxb = max_nums
        self.chain.append(genesis)
        #--genesis block created7/hain data file
        with open('applayer/temp/blockchain.dat', 'wb') as genfile:
            pickle.dump(genesis, genfile)
        print(f'[{current_thread().name}] Genesis block added')
        
    def set_votefile_path(self, path):
        self.votefile_path = path

    @staticmethod
    def display_dat():
        #--print the information of blocks of the blockchain in the console
        try:
            with open(PROJECT_PATH + '/applayer/temp/blockchain.dat', 'rb') as blockfile:
                while True:
                    try:
                        data = pickle.load(blockfile)
                        #--print all data of a block
                        print(f'[{current_thread().name}] Block Height: {data.height}')
                        print(f'[{current_thread().name}] Data in block: {data.votedata}')
                        print(f'[{current_thread().name}] Total in block: {data.votecount}')
                        print(f'[{current_thread().name}] Number of votes: {data.number_of_votes}')
                        print(f'[{current_thread().name}] Merkle root: {data.merkle}')
                        print(f'[{current_thread().name}] Difficulty: {data.DIFFICULTY}')
                        print(f'[{current_thread().name}] Time stamp: {data.timeStamp}')
                        print(f'[{current_thread().name}] Previous hash: {data.prevHash}')
                        print(f'[{current_thread().name}] Block Hash: {data.hash}')
                        print(f'[{current_thread().name}] Nonce: {data.nonce}\n\t\t|\n\t\t|')
                    except EOFError:
                        break  # End of file reached
        except FileNotFoundError:
            print(f'\n.\n.\n.\n<<<File not found!!>>>')

    @staticmethod
    def display():
        for block in Blockchain.chain:
            print(f'[{current_thread().name}] Block Height: {block.height}')
            print(f'[{current_thread().name}] Data in block: {block.votedata}')
            print(f'[{current_thread().name}] Total in block: {block.votecount}')
            print(f'[{current_thread().name}] Number of votes: {block.number_of_votes}')
            print(f'[{current_thread().name}] Merkle root: {block.merkle}')
            # print(f'[{current_thread().name}] Merkle tree: {block.tree}') 先不要在区块里放tree了
            print(f'[{current_thread().name}] Difficulty: {block.DIFFICULTY}')
            print(f'[{current_thread().name}] Time stamp: {block.timeStamp}')
            print(f'[{current_thread().name}] Previous hash: {block.prevHash}')
            print(f'[{current_thread().name}] Block Hash: {block.hash}')
            print(f'[{current_thread().name}] Nonce: {block.nonce}\n\t\t|\n\t\t|')

    #--to clear up the votepool after a block has been mined...
    #如果文件不存在则创建新文件。'w+'模式表示可读写，如果文件已存在则清空文件内容
    def update_votepool(self, processed_votedata):
        try:
            # Open and read the existing votes from the vote pool
            with open(self.votefile_path, 'r', newline='', encoding='UTF-8') as file:
                existing_votes = list(csv.reader(file))

            # Convert each vote in processed_votedata to its CSV row format for comparison
            processed_rows = [
                [vote['Voter Public Key'].strip(), vote['Candidate'].strip(), vote['TimeStamp'].strip()]
                for vote in processed_votedata
            ]

            # Strip whitespace from existing_votes for accurate comparison
            existing_votes = [[item.strip() for item in row] for row in existing_votes]

            # Filter out the processed votes from existing_votes
            remaining_votes = [vote for vote in existing_votes if vote not in processed_rows]

            # Write the unprocessed votes back to the vote pool
            with open(self.votefile_path, 'w', newline='', encoding='UTF-8') as file:
                csv.writer(file).writerows(remaining_votes)

        except Exception as e:
            print(f'[{current_thread().name}] Error updating votefile.csv: {e}')

    def is_votepool_empty(self):
        my_path = self.votefile_path
        # The file is considered empty if it doesn't exist or has no content
        return not os.path.isfile(my_path) or os.stat(my_path).st_size == 0

    """
    After regular intervals, we need to verify that the blockchain
    is indeed valid at all points. And no data has been tampered - EVEN IN ONE SINGLE COPY
    (if not for the whole network).
    We do that by verifying the chain of block hashes.
    """
    '每间隔一定的时间，验证区块链有没有别篡改'
    @classmethod
    def verify_chain(cls):
        index, conclusion = ver.sync_blocks(cls.chain)
        if not conclusion:
            if len(str(index)) == 1:
                error_msg ="""+-----------------------------------------+
|                                         |
| Somebody messed up at Block number - {}  |
|                                         |
+-----------------------------------------+""".format(index)
            else:
                error_msg ="""+-----------------------------------------+
|                                         |
| Somebody messed up at Block number - {} |
|                                         |
+-----------------------------------------+""".format(index)

            raise Exception(error_msg)

        return True

    def mine_if_needed(self):
        while True:
            if self.should_mine():
                total_votes = self.count_total_votes_in_pool()
                blocks_to_mine, _ = self.calculate_block_distribution(total_votes)

                # while total_votes > 0 and blocks_to_mine > 0:
                #     votes_per_block = math.ceil(total_votes / blocks_to_mine)
                #     print(f'[{current_thread().name}] Mining a block with {votes_per_block} votes...')
                #
                #     # Acquire the lock before mining
                #     with lock:
                #         new_block = Block()
                #         new_block.mineblock(self, votes_per_block)
                #
                #         total_votes = self.count_total_votes_in_pool()  # Update the total votes after mining a block
                #         blocks_to_mine -= 1  # Decrement the number of blocks to mine
                #
                #     print(f'[{current_thread().name}] Block mined. {total_votes} votes remaining, {blocks_to_mine} blocks to mine.')
                while total_votes > 0 and blocks_to_mine > 0:
                    votes_per_block = math.ceil(total_votes / blocks_to_mine)
                    print(f"Mining a block with {votes_per_block} votes...")

                    new_block = Block()
                    new_block.mineblock(self, votes_per_block)

                    total_votes = Blockchain.count_total_votes_in_pool(self)  # Update the total votes after mining a block
                    blocks_to_mine -= 1  # Decrement the number of blocks to mine

                    print(f'[{current_thread().name}] Block mined. {total_votes} votes remaining, {blocks_to_mine} blocks to mine.')
            else:
                time.sleep(BLOCK_TIME_LIMIT)
                #uncomment if need add votes
                #append_random_votes(self.votefile_path, num_votes=10)
                print(f'[{current_thread().name}] No mining needed at this time.')

    def should_mine(self):
        total_votes = self.count_total_votes_in_pool()
        blocks_needed, _ = self.calculate_block_distribution(total_votes)

        # Check if there are enough votes to mine and if the blockchain doesn't already have the necessary blocks
        return total_votes > 0 or (len(self.chain) - 1 < blocks_needed)

    def count_total_votes_in_pool(self):
        count = 0
        try:
            with open(self.votefile_path, 'r', newline='', encoding='UTF-8') as votepool:
                csvreader = csv.reader(votepool)
                count = sum(1 for row in csvreader)  # Sum the rows to get the total count
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
    """
    The basic structure of block that will be created when the block is generated
    the data in the block will be updated later and block will be mined then.
    """
    def __init__(self, height=0, votes=0, merkle='0', tree=None, timeStamp=0, prevHash='0', representative_pow=0, hash='Genesis'):
        if tree is None:
            tree = []
        self.height = height  # len(Blockchain.chain-1)
        self.votedata = []  # loadvote()
        self.votecount = []  # loadvote()
        self.number_of_votes = votes  # votecount per block
        self.tree = tree
        self.merkle = merkle  # calculateMerkleRoot()
        self.DIFFICULTY = DIFFICULTY  # cryptography difficulty
        self.timeStamp = time.time()  # time()
        self.prevHash = prevHash  # previous block hash
        self.nonce = representative_pow  # proof of work function will find nonce
        self.hash = hash  # hash of the current block

    #--The HEART OF BLOCKCHAIN - 'Proof-of-Work' function
    def representative_pow(self, zero=DIFFICULTY):
        self.nonce = 0
        while (sha256(self.calcHash().encode('utf-8')).hexdigest()[:zero] != '0' * zero):
            self.nonce += 1
        return self.nonce

    #--calculate hash of a given block
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
                        break  # Stop reading once the required number of votes is loaded

                    voter_pub_key, candidate, timestamp = row
                    votelist.append({'Voter Public Key': voter_pub_key, 'Candidate': candidate, 'TimeStamp': timestamp})
                    
                    # Count votes per candidate
                    if candidate in votecount:
                        votecount[candidate] += 1
                    else:
                        votecount[candidate] = 1

                    count += 1

        except (IOError, IndexError) as e:
            print(f'[{current_thread().name}] Error reading votefile.csv: {e}')

        finally:
            if count > 0:
                blockchain_instance.update_votepool(votelist)  # Ensure this updates the file correctly, removing only processed votes

        return votelist, votecount, count

    #--create a merkle tree of vote transactions and return the merkle root of the tree
    def merkleRoot(self):
        votedata = self.votedata
        if len(votedata) == 0:
            return '', []  # Return empty values if no vote data
        if len(votedata) == 1:
            hash_value = sha256(str(votedata[0]).encode()).hexdigest()
            return hash_value, [hash_value]

        vote_hashes = [sha256(str(vote).encode()).hexdigest() for vote in votedata]
        all_hashes = vote_hashes.copy()  # Store all nodes in a list

        while len(vote_hashes) > 1:
            if len(vote_hashes) % 2 == 1:
                vote_hashes.append(vote_hashes[-1])  # Duplicate the last hash if the number is odd
            
            new_hashes = []
            for i in range(0, len(vote_hashes), 2):
                concatenated = vote_hashes[i] + vote_hashes[i + 1]
                new_hash = sha256(concatenated.encode()).hexdigest()
                new_hashes.append(new_hash)
            all_hashes.extend(new_hashes)  # Add new nodes to the list
            vote_hashes = new_hashes

        return vote_hashes[0], all_hashes  # Return the Merkle root and all nodes

    def mineblock(self, blockchain_instance, votes_per_block):
        # Assume that the total votes and blocks needed are already calculated

        # Set the height and previous hash for the new block
        self.height = len(Blockchain.chain)
        self.prevHash = Blockchain.chain[-1].hash if self.height > 0 else '0'

        # Load vote data and count into the block based on votes_per_block
        self.votedata, self.votecount, self.number_of_votes = Block.load_data(blockchain_instance, votes_per_block)

        # Update the vote pool by removing the votes that are now loaded into the block
        blockchain_instance.update_votepool(self.votedata)

        # Calculate the Merkle root for the vote data (implement this function if necessary)
        self.merkle, self.tree = self.merkleRoot()

        # Set the block's difficulty and timestamp
        self.DIFFICULTY = DIFFICULTY
        self.timeStamp = time.time()

        # Perform the proof-of-work to find the nonce
        self.nonce = self.representative_pow()

        # Calculate the block's hash with the nonce found
        self.hash = self.calcHash()

        Blockchain.chain.append(self)
        if blockchain_instance.count_total_votes_in_pool() == 0:
            Blockchain.display()
        # Append the mined block to the blockchain
        return self  # Return the mined block

class GenesisBlock(Block):
    def __init__(self, vote_activity_id, initiator_puk, max_nums, version="v1.0"):
        super().__init__()  # 调用父类的构造函数
        self.vote_activity_id = vote_activity_id
        self.initiator_puk = initiator_puk
        self.version = version
        self.max_nums = max_nums
        self.hash = self.calcHash()
        self.timeStamp = time.time()

    def calcHash(self):
        return sha256((str(self.vote_activity_id) + str(self.timeStamp) + str(self.initiator_puk) + str(self.version)).encode('utf-8')).hexdigest()
