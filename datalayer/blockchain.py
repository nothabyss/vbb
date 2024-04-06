#--libraries
from hashlib import *
import time
from threading import Thread
import csv
import pickle
import os


#--project files
from . import enc
from prolayer import verification as ver

#--<<Global variables>>

#--cryptographic difficulty
DIFFICULTY = 2

#--frequency of mining of blocks seconds
BLOCK_TIME_LIMIT = 20

#--path of project files
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
votefile_path = os.path.join(PROJECT_PATH, 'applayer', 'votefile.csv')





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

    def __init__(self,vote_activity_id, initiator_puk, max_nums):
        self.add_genesis(vote_activity_id, initiator_puk, max_nums)
        print('Blockchain initialized')


    #--genesis block creation has nothing to do with blockchain class,
    #--..but has to be created when blockchain is initialized
    def add_genesis(self, vote_activity_id, initiator_puk, max_nums):
        genesis = GenesisBlock(vote_activity_id, initiator_puk, max_nums)
        self.chain.append(genesis)
        #--genesis block created7/hain data file
        with open('applayer/temp/blockchain.dat', 'wb') as genfile:
            pickle.dump(genesis, genfile)
        print("Genesis block added")



    # @staticmethod
    # def display(EVoting):
    #     #--print the information of blocks of the blockchain in the console
    #     try:
    #         with open(PROJECT_PATH + '/applayer/temp/blockchain.dat','rb') as blockfile:
    #             while True:
    #                 try:
    #                     data = pickle.load(blockfile)
                
    #                     #--print all data of a block
    #                     print("Block Height: ", data.height)
    #                     print("Data in block: ", data.votedata)
    #                     print("Total in block: ", data.votecount)
    #                     print("Number of votes: ",data.number_of_votes)
    #                     print("Merkle root: ", data.merkle)
    #                     print("Difficulty: ", data.DIFFICULTY)
    #                     print("Time stamp: ", data.timeStamp)
    #                     print("Previous hash: ", data.prevHash)
    #                     print("Block Hash: ", data.hash)
    #                     print("Nonce: ", data.nonce, '\n\t\t|\n\t\t|')
    #                 except EOFError:
    #                     break  # End of file reached
    #     except FileNotFoundError:
    #         print("\n.\n.\n.\n<<<File not found!!>>>")
    @staticmethod
    def display(EVoting):
        for block in Blockchain.chain:
            print("Block Height: ", block.height)
            print("Data in block: ", block.votedata)
            print("Total in block: ", block.votecount)
            print("Number of votes: ", block.number_of_votes)
            print("Merkle root: ", block.merkle)
            print("Difficulty: ", block.DIFFICULTY)
            print("Time stamp: ", block.timeStamp)
            print("Previous hash: ", block.prevHash)
            print("Block Hash: ", block.hash)
            print("Nonce: ", block.nonce, '\n\t\t|\n\t\t|')


    #--to clear up the votepool after a block has been mined...
    #如果文件不存在则创建新文件。'w+'模式表示可读写，如果文件已存在则清空文件内容
    @staticmethod
    def update_votepool(processed_votedata):
        try:
            
            # Open and read the existing votes from the vote pool
            with open(votefile_path, 'r', newline='', encoding='UTF-8') as file:
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
            with open(votefile_path, 'w', newline='', encoding='UTF-8') as file:
                
                csv.writer(file).writerows(remaining_votes)

        except Exception as e:
            print(f"Error updating votefile.csv: {e}")

    @staticmethod
    def is_votepool_empty():
        my_path = votefile_path
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
            if len(str(index))==1:
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
    

    @staticmethod
    def mine_if_needed():
        while True:
            if Blockchain.should_mine():
                print("Mining a new block...")
                new_block = Block()
                new_block.mineblock()  # Assumes mineblock() will handle block creation and voting data loading

                # Now the vote pool should be updated only if new_block actually contains votes
                # if new_block.number_of_votes > 0:
                #     Blockchain.update_votepool(new_block.votedata)

            # Sleep to prevent continuous loop without pause unless you have a triggering event to mine
            else:
                time.sleep(BLOCK_TIME_LIMIT)
                print("no vote update")
              

    @staticmethod
    def should_mine():
        total_votes = Blockchain.count_total_votes_in_pool()
        
        # Don't mine if there are no votes to process
        if total_votes == 0:
            return False

        blocks_needed, votes_per_block = Blockchain.calculate_block_distribution(total_votes, max_votes_per_block=500)
        
        # Mine only if we need more blocks to accommodate the votes
        return len(Blockchain.chain) < blocks_needed + 1  # +1 for genesis block
        
    @staticmethod
    def count_total_votes_in_pool():
        count = 0
        try:
            with open(votefile_path, 'r', newline='', encoding='UTF-8') as votepool:
                csvreader = csv.reader(votepool)
                count = sum(1 for row in csvreader)  # Sum the rows to get the total count
        except (IOError, IndexError):
            print("Error reading votefile.csv")
        return count
    
    @staticmethod
    def calculate_block_distribution(total_votes, max_votes_per_block=500):
        # Set a minimum of 4 blocks
        min_blocks = 4

        # Calculate the number of additional blocks needed for excess votes
        extra_blocks = max(0, (total_votes - min_blocks * max_votes_per_block + max_votes_per_block - 1) // max_votes_per_block)

        # The total number of blocks needed is the sum of minimum blocks and extra blocks
        blocks_needed = min_blocks + extra_blocks

        # Determine the number of votes per block to distribute them as equally as possible
        # If total votes are less than or equal to the capacity of 4 blocks, spread them evenly
        if total_votes <= min_blocks * max_votes_per_block:
            votes_per_block = (total_votes + min_blocks - 1) // min_blocks
        else:
            # Otherwise, use the maximum votes per block for the extra blocks
            votes_per_block = max_votes_per_block

        return blocks_needed, votes_per_block
    


class Block:

    """
    The basic structure of block that will be created when the block is generated
    the data in the block will be updated later and block will be mined then.
    """

    def __init__(self, height = 0, votes = 0 ,merkle = '0',timeStamp = 0,prevHash = '0', representative_pow = 0, hash = 'Genesis'):
        self.height = height                    #len(Blockchain.chain-1)
        self.votedata = []                      #loadvote()
        self.votecount = []                     #loadvote()
        self.number_of_votes = votes            #votecount per block
        self.merkle = merkle                    #calculateMerkleRoot()
        self.DIFFICULTY = DIFFICULTY            #cryptography difficulty
        self.timeStamp = time.time()                   #time()
        self.prevHash = prevHash                #previous block hash
        self.nonce = representative_pow                        #proof of work function will find nonce
        self.hash = hash                        #hash of the current block
    #--The HEART OF BLOCKCHAIN - 'Proof-of-Work' function

    def representative_pow(self,zero=DIFFICULTY):
        self.nonce=0
        while(sha256(self.calcHash().encode('utf-8')).hexdigest()[:zero]!='0'*zero):

            self.nonce+=1
        return self.nonce

    #--calculate hash of a given block
    def calcHash(self):
        return sha256((str(str(self.merkle)+str(self.timeStamp)+str(self.nonce)+str(self.prevHash))).encode('utf-8')).hexdigest()

    """
    the vote data from the temporary pool will be loaded into the block
    and after successful loading of data, the pool will be cleared and
    will be reset for the next bunch of transactions
    """

    # @staticmethod
    # def loadvote():
    #     votelist = []
    #     votecount = 0
    #     try:
    #         with open('votefile.csv', mode = 'r', encoding='UTF-8') as votepool:
    #             csvreader = csv.reader(votepool)
    #             for row in csvreader:
    #                 votelist.append({'Voter Public Key':row[0], 'Candidate':row[1],'TimeStamp':row[2]})
    #                 votecount+=1
    #         return votelist,votecount
    #
    #     except(IOError,IndexError):
    #         pass
    #
    #     finally:
    #         print("data loaded in block")
    #         print("Updating unconfirmed vote pool...")
    #         print (Blockchain.update_votepool())
    @staticmethod
    def load_data(votes_per_block):
        votelist = []
        votecount = {}
        count = 0
        try:
            with open(votefile_path, 'r', newline='', encoding='UTF-8') as votepool:
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
            print("Error reading votefile.csv:", e)

        finally:
            print(f"{count} votes loaded in block")
            if count > 0:
                Blockchain.update_votepool(votelist)  # Ensure this updates the file correctly, removing only processed votes

        return votelist, votecount, count

    #--create a merkle tree of vote transactions and return the merkle root of the tree
    def merkleRoot(self):
        return 'congrats'

    #--fill the block with data and append the block in the blockchain
    def mineblock(self):
        total_votes = Blockchain.count_total_votes_in_pool()
        blocks_needed, votes_per_block = Blockchain.calculate_block_distribution(total_votes, max_votes_per_block=500)

        # Set the height and previous hash for the new block
        self.height = len(Blockchain.chain)
        self.prevHash = Blockchain.chain[-1].hash if self.height > 0 else '0'

        # Load vote data and count into the block
        self.votedata, self.votecount, self.number_of_votes = Block.load_data(votes_per_block)
        Blockchain.update_votepool(self.votedata)

        # Calculate the Merkle root for the vote data (you'll need to implement this function)
        self.merkle = self.merkleRoot()

        # Set the block's difficulty and timestamp
        self.DIFFICULTY = DIFFICULTY
        self.timeStamp = time.time()

        # Perform the proof-of-work to find the nonce
        self.nonce = self.representative_pow()

        # Calculate the block's hash with the nonce found
        self.hash = self.calcHash()

        # Append the mined block to the blockchain
        Blockchain.chain.append(self)

        Blockchain.display(self)

        return self  # Return the mined block


class GenesisBlock(Block):
    def __init__(self, vote_activity_id, initiator_puk, max_nums, version = "v1.0"):
        super().__init__()  # 调用父类的构造函数
        self.vote_activity_id = vote_activity_id
        self.initiator_puk = initiator_puk
        self.version = version
        self.max_nums = max_nums
        self.hash = self.calcHash()
        self.timeStamp = time.time()
    def calcHash(self):
        return sha256((str(str(self.vote_activity_id) + str(self.timeStamp) + str(self.initiator_puk) + str(self.version))).encode(
            'utf-8')).hexdigest()

# To run the mining check in a separate thread
def run_mining_scheduler():
    mining_thread = Thread(target=Blockchain.mine_if_needed)
    mining_thread.start()

# Call this function at the start of your program
run_mining_scheduler()
