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
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
PROJECT_PATH = os.path.dirname(current_dir_path)





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

    def __init__(self,vote_activity_id, initiator_puk):
        self.add_genesis(vote_activity_id, initiator_puk)
        print('Blockchain initialized')


    #--genesis block creation has nothing to do with blockchain class,
    #--..but has to be created when blockchain is initialized
    def add_genesis(self, vote_activity_id, initiator_puk):
        genesis = GenesisBlock(vote_activity_id, initiator_puk)
        self.chain.append(genesis)
        #--genesis block created7/hain data file
        with open('temp/blockchain.dat', 'wb') as genfile:
            pickle.dump(genesis, genfile)
        print("Genesis block added")



    @staticmethod
    def display(EVoting):
        #--print the information of blocks of the blockchain in the console
        try:
            with open(PROJECT_PATH + '/applayer/temp/blockchain.dat','rb') as blockfile:
                while True:
                    try:
                        data = pickle.load(blockfile)

                        #--print all data of a block
                        print("Block Height: ", data.height)
                        print("Data in block: ", data.votedata)
                        print("Total in block: ", data.votecount)
                        print("Number of votes: ",data.number_of_votes)
                        print("Merkle root: ", data.merkle)
                        print("Difficulty: ", data.DIFFICULTY)
                        print("Time stamp: ", data.timeStamp)
                        print("Previous hash: ", data.prevHash)
                        print("Block Hash: ", data.hash)
                        print("Nonce: ", data.nonce, '\n\t\t|\n\t\t|')
                    except EOFError:
                        break  # End of file reached
        except FileNotFoundError:
            print("\n.\n.\n.\n<<<File not found!!>>>")


    @staticmethod
    #--to clear up the votepool after a block has been mined...
    #如果文件不存在则创建新文件。'w+'模式表示可读写，如果文件已存在则清空文件内容
    def update_votepool():
        try:
            votefile = open('votefile.csv','w+')
            votefile.close()

        except Exception as e:
            print("Some error occured: ", e)
        return "Done"

    @staticmethod
    def is_votepool_empty():
        my_path = PROJECT_PATH + '/temp/votefile.csv'
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
            # Check conditions for mining a new block
            if len(Blockchain.chain) == 1 or Blockchain.should_mine():
                print("Mining a new block...")
                new_block = Block()
                new_block.mineblock()  # Assumes mineblock() adds the block to the chain
                
            # Wait for a specified interval before checking again
            time.sleep(BLOCK_TIME_LIMIT)

    @staticmethod
    def should_mine():
        # Always mine until there are at least 4 blocks
        if len(Blockchain.chain) < 4:
            return True
        # Beyond that, only mine if there are votes to process
        return not Blockchain.is_votepool_empty()
    


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
    def load_data():
        votelist = []
        votecount = []
        count = 0
        try:
            with open('votefile.csv', mode = 'r', encoding='UTF-8') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    # votedata是一个字典，包含候选人的键和值
                    # votelist.append({'Voter Public Key':row[0], 'Vote Data':row[1],'Key':row[2]})/
                    votelist.append({'Voter Public Key':row[0], 'Candidate':row[1], 'TimeStamp':row[2]})
                    candidate_exists = False
                    candidate_name = row[1]
                    count += 1
                    # if len(votelist) == 0:
                    #     votecount.append({'Candidate':row[1], 'total':})
                    for candidate in votecount:
                        if candidate['Candidate'] == candidate_name:
                            candidate['total'] += 1
                            candidate_exists = True
                            break
                    if not candidate_exists:
                        votecount.append({'Candidate': candidate_name, 'total': 1})
                    # votecount的键为vote data的键，然后值加1
        except(IOError,IndexError):
            pass

        finally:
            print("data loaded in block")
            print("Updating unconfirmed vote pool...")
            print (Blockchain.update_votepool())
        return votelist, votecount, count

    #--create a merkle tree of vote transactions and return the merkle root of the tree
    def merkleRoot(self):
        return 'congrats'

    #--fill the block with data and append the block in the blockchain
    def mineblock(self):
        # Set the height and previous hash for the new block
        self.height = len(Blockchain.chain)
        self.prevHash = Blockchain.chain[-1].hash if self.height > 0 else '0'

        # Load vote data and count into the block
        self.votedata, self.votecount, self.number_of_votes = Block.load_data()

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
    def __init__(self, vote_activity_id, initiator_puk, version = "v1.0"):
        super().__init__()  # 调用父类的构造函数
        self.vote_activity_id = vote_activity_id
        self.initiator_puk = initiator_puk
        self.version = version
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
