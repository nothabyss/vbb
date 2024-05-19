#--libraries
from hashlib import *
from time import time
import pickle

#--project files
import datalayer.enc as enc
from applayer import aes as aes


class vote:
    count = 0

    def __init__(self,hiddenvoterid,candidateID,voterpubkey):
        #--voterid hashed with PIN (ZKP)
        self.hiddenvoterid = hiddenvoterid
        self.candidate = candidateID
        self.voterpubkey = voterpubkey
        self.time = time()
        self.votedata = [self.hiddenvoterid, self.candidate, self.time]


    #--returns the voter's public key in pickle object as a byte value
    def get_voter_pk(self):
        return pickle.dumps(self.voterpubkey)


    #--vote gets a digital signature by voter's private key and gets signed by admin public key
    def encryptvote(self):
        """
        the data of the vote (in the votedata list) will be first hashed by SHA-256
        and then, the data will be converted into bytes and signed by voter's private key
        and that hashed signature will be appended with votedata itself
        """
        self.votedata.append(enc.sign(voterkeys['sk'], bytes(sha256(str('---'.join(str(x) for x in self.votedata)).encode('utf-8')).hexdigest(),'utf-8')))

        """
        now that whole data (the new votedata list) will be encrypted by AES encryption
        and the shared key of AES will be encrypted with admin's public key
        this data will be broadcasted and saved into the unconfirmed votepool and will be added in the block
        """
        voterpk = self.get_voter_pk()

        #--byte value of voter public key pickle object is converted to string
        #--then added to list
        return [str(voterpk)[2:-1], str(aes.encrypt('***'.join(str(i) for i in self.votedata), voterkeys['aeskey']))[2:-1], str(enc.encrypt(Blockchain.adminpub, voterkeys['aeskey']))[2:-1]]

    #--keep track of no. of votes
    @classmethod
    def inc_votecount(cls):
        cls.count+=1

    @classmethod
    def get_votecount(cls):
        #--return the current number of votes
        return cls.count
