from hashlib import *
import time
from threading import Thread, Lock, current_thread
import csv
import pickle
import sys
import os
import math


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)



DIFFICULTY = 3


BLOCK_TIME_LIMIT = 3


class Blockchain:

    MAX_VOTES_PER_BLOCK = 50

    def __init__(self, vote_activity_id, initiator_puk, max_votes, max_days, votefile_path, new_chain=True, chain=None):
        if chain is None:
            chain = []
        self.chain = chain
        if new_chain:
            self.chain_folder = self.create_chain_folder(vote_activity_id, max_votes, max_days, initiator_puk)
        else:
            self.chain_folder = self.identify_existing_chain_folder()
        # self.load_blockchain() #该函数有问题，会报错genesis没有append
        self.votefile_path = votefile_path
        self.max_votes = max_votes
        self.max_days = max_days # Convert days to seconds
        # self.start_time = time.time()
        if new_chain == False:
            return
        self.add_genesis(vote_activity_id, initiator_puk)
        print(f'[{current_thread().name}] Blockchain initialized')

    def create_chain_folder(self, vote_activity_id, max_votes, max_days, initiator_puk):
        identifier = f"{vote_activity_id}-{max_votes}-{max_days}-{initiator_puk}"
        folder_name = f"chain_{identifier}"
        folder_path = os.path.join(PROJECT_PATH, 'records/chains', folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path


    def identify_existing_chain_folder(self):
        chains_path = os.path.join(PROJECT_PATH, 'records/chains')
        if not os.path.exists(chains_path):
            print("No chain directories found. Creating a new chain.")
            return None  # Return None if no directories exist yet

        # Get all directories within the chains path
        try:
            directories = [os.path.join(chains_path, d) for d in os.listdir(chains_path) if os.path.isdir(os.path.join(chains_path, d))]
            # Find the most recently modified directory
            latest_folder = max(directories, key=os.path.getmtime)
            print(f"Using existing chain folder: {latest_folder}")
            return latest_folder
        except ValueError:
            print("Error finding the most recently modified chain directory.")
            return None

    # --genesis block creation has nothing to do with blockchain class,
    # --..but has to be created when blockchain is initialized
    def add_genesis(self, vote_activity_id, initiator_puk):
        genesis = GenesisBlock(vote_activity_id, initiator_puk)
        self.chain.append(genesis)
        # Save the genesis block in the designated chain folder
        genesis_file_path = os.path.join(self.chain_folder, 'GenesisBlock.dat')

        #  之后可能要改
        with open(genesis_file_path, 'wb') as genfile:
            pickle.dump(genesis, genfile)
        print(f'[{current_thread().name}] Genesis block added to {genesis_file_path}')

    def set_votefile_path(self, path):
        self.votefile_path = path

    '''可能有bug，还没用过这个函数'''
    @staticmethod
    def display_dat(self):
        # --print the information of blocks of the blockchain in the console
        data_file_path = os.path.join(self.chain_folder, 'blockchain.dat')
        
        try:
            with open(data_file_path, 'rb') as blockfile:
                while True:
                    try:
                        data = pickle.load(blockfile)
                        # Print all data of a block
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
            print(f'File not found: {data_file_path}')


    def display(self):
        for block in self.chain:
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


    def update_votepool2(self, n):

        input_file = self.votefile_path
        output_file = self.votefile_path
        # 如果输出文件与输入文件相同，则使用临时文件
        if output_file == input_file:
            temp_file = 'temp_output.csv'
        else:
            temp_file = output_file

        with open(input_file, 'r', newline='') as csv_in, open(temp_file, 'w', newline='') as csv_out:
            reader = csv.reader(csv_in)
            writer = csv.writer(csv_out)

            # 跳过前n行
            for _ in range(n):
                next(reader, None)

                # 写入剩余的行
            for row in reader:
                writer.writerow(row)

                # 如果输出文件与输入文件相同，则替换原始文件
        if output_file == input_file:
            # 先删除原始文件，防止替换失败（例如，如果新文件与旧文件大小不同）
            try:
                os.remove(input_file)
            except FileNotFoundError:
                pass
                # 然后重命名临时文件为原始文件名
            os.rename(temp_file, input_file)

            # 使用示例

    def is_votepool_empty(self):
        my_path = self.votefile_path
        # The file is considered empty if it doesn't exist or has no content
        return not os.path.isfile(my_path) or os.stat(my_path).st_size == 0


    def total_votes_in_chain(self):
        total_votes = sum(block.number_of_votes for block in self.chain)
        return total_votes

    def mine_if_needed(self):
        while True:
            # Check if the total votes in the chain reached max_votes
            if self.total_votes_in_chain() >= self.max_votes:
                print(f"[{current_thread().name}] Maximum number of votes reached. Stopping the mining thread.")
                self.display()
                return

            # # Check if the elapsed time has exceeded max_days
            # if self.elapsed_time_exceeded():
            #     votefile_path = self.votefile_path
            #     os.remove(votefile_path)
            #     print(f"[{current_thread().name}] Maximum time exceeded. Stopping the mining thread.")
            #     break

            if self.should_mine():
                if os.path.exists(self.votefile_path) == False:
                    print("this votefile has been deleted")
                    break
                total_votes = self.count_total_votes_in_pool()
                blocks_to_mine, votes_per_block = self.calculate_block_distribution(total_votes)

                while total_votes > 0 and blocks_to_mine > 0 and self.total_votes_in_chain() < self.max_votes:
                    votes_per_block = min(Blockchain.MAX_VOTES_PER_BLOCK, votes_per_block, total_votes, self.max_votes-self.total_votes_in_chain())
                    print(f"[{current_thread().name}] Mining a block with {votes_per_block} votes...")

                    new_block = Block()
                    new_block.mineblock(self, votes_per_block)

                    total_votes = self.count_total_votes_in_pool()  # Update the total votes after mining a block
                    blocks_to_mine -= 1  # Decrement the number of blocks to mine

                    print(f"[{current_thread().name}] Block mined. {total_votes} votes remaining, {blocks_to_mine} blocks to mine.")
            else:
                time.sleep(BLOCK_TIME_LIMIT)
                # Uncomment if need add votes
                # append_random_votes(self.votefile_path, num_votes=10)
                print(f"[{current_thread().name}] No mining needed at this time.")


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
                count = sum(1 for row in csvreader if any(row))  # Sum the rows to get the total count
        except (IOError, IndexError):
            print(f"[{current_thread().name}] Error reading votefile.csv")
        return count

    def calculate_block_distribution(self, total_votes):
        if len(self.chain) >= 3:
            min_blocks = 1
        else:
            min_blocks = 2
        blocks_needed = min_blocks
        if total_votes > min_blocks * Blockchain.MAX_VOTES_PER_BLOCK:
            votes_per_block = Blockchain.MAX_VOTES_PER_BLOCK
            extra_blocks = math.ceil((total_votes - min_blocks * Blockchain.MAX_VOTES_PER_BLOCK) / votes_per_block)
            blocks_needed += extra_blocks
        else:
            votes_per_block = math.ceil(total_votes / min_blocks)
        return blocks_needed, votes_per_block



class Block:

    def __init__(self, height=0, votes=0, merkle='0',  timeStamp=0, prevHash='0', representative_pow=0, hash='Genesis'):

        self.height = height  # len(Blockchain.chain-1)
        self.votedata = []  # loadvote()
        self.votecount = []  # loadvote()
        self.number_of_votes = votes  # votecount per block
        self.merkle = merkle  # calculateMerkleRoot()
        self.DIFFICULTY = DIFFICULTY  # cryptographic difficulty
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


    def load_data(self, blockchain_instance, votes_per_block):
        votelist = []
        votecount = {}

        count = 0
        try:
            with open(blockchain_instance.votefile_path, 'r', newline='', encoding='UTF-8') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    if count >= votes_per_block:
                        break  # Stop reading once the required number of votes is loaded

                    # Ensure we only extract the expected three values, handle extra values
                    try:
                        voter_pub_key, candidate, timestamp = row[:3]
                    except ValueError as e:
                        print(f"[{current_thread().name}] Error unpacking row: {row} - {e}")
                        continue

                    votelist.append({'Voter Public Key': voter_pub_key.strip(), 'Candidate': candidate.strip(), 'TimeStamp': timestamp.strip()})

                    # Count votes per candidate
                    if candidate in votecount:
                        votecount[candidate] += 1
                    else:
                        votecount[candidate] = 1

                    count += 1

        except (IOError, IndexError) as e:
            print(f'[{current_thread().name}] Error reading votefile.csv: {e}')

        # finally:
        #     if count > 0:
        #         blockchain_instance.update_votepool(votelist)  # Ensure this updates the file correctly, removing only processed votes

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


        while len(vote_hashes) > 1:
            if len(vote_hashes) % 2 == 1:
                vote_hashes.append(vote_hashes[-1])  # Duplicate the last hash if the number is odd

            new_hashes = []
            for i in range(0, len(vote_hashes), 2):
                concatenated = vote_hashes[i] + vote_hashes[i + 1]
                new_hash = sha256(concatenated.encode()).hexdigest()
                new_hashes.append(new_hash)

            vote_hashes = new_hashes

        return vote_hashes[0]  # Return the Merkle root and all nodes

    def mineblock(self, blockchain_instance, votes_per_block):


        self.height = len(blockchain_instance.chain)
        self.prevHash = blockchain_instance.chain[-1].hash if self.height > 0 else '0'

        self.votedata, self.votecount, self.number_of_votes = Block.load_data(self, blockchain_instance, votes_per_block)


        blockchain_instance.update_votepool2(self.number_of_votes)

        self.merkle = self.merkleRoot()


        self.DIFFICULTY = DIFFICULTY
        self.timeStamp = time.time()

        self.nonce = self.representative_pow()


        self.hash = self.calcHash()

        blockchain_instance.chain.append(self)
        chain_file_path = os.path.join(blockchain_instance.chain_folder, f'block-{self.height}.dat')
        with open(chain_file_path, 'wb') as file:
            pickle.dump(self, file)

        return self  # Return the mined block



class GenesisBlock(Block):
    def __init__(self, vote_activity_id, initiator_puk, version="v1.0"):
        super().__init__()  # 调用父类的构造函数
        self.vote_activity_id = vote_activity_id
        self.initiator_puk = initiator_puk
        self.version = version
        self.timeStamp = time.time()
        self.hash = self.calcHash()


    def calcHash(self):
        print(self.vote_activity_id)
        print(str(self.timeStamp))
        print(str(self.initiator_puk))
        print(str(self.version))
        return sha256((str(self.vote_activity_id) + str(self.timeStamp) + str(self.initiator_puk) + str(self.version)).encode('utf-8')).hexdigest()

if __name__ == '__main__':
    print(PROJECT_PATH)