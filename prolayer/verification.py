from hashlib import *
from time import sleep

def sync_blocks(blockchain):
    for i in range(1,len(blockchain)):
        if blockchain[i].prevHash == blockchain[i-1].calcHash():
            continue
        else:
            return i, False

    return 0, True


def verify_block(block):

    check_1 = sha256((str(str(block.data)+str(block.nonce)+str(block.timeStamp)+str(block.prevHash))).encode('utf-8')).hexdigest()
    sleep(5)
    check_2 = sha256((str(str(block.data)+str(block.nonce)+str(block.timeStamp)+str(block.prevHash))).encode('utf-8')).hexdigest()

    return check_1==check_2


def verfiy_merkle(block):
    votedata=block.votedata
    if len(votedata) == 0:
        return []
    if len(votedata) == 1:
        return [sha256(str(votedata[0]).encode()).hexdigest()]
    vote_hashes = [sha256(str(vote).encode()).hexdigest() for vote in votedata]
    if len(vote_hashes) % 2 == 1:
        vote_hashes.append(vote_hashes[-1])
    while len(vote_hashes) > 1:
        new_hashes = []
        for i in range(0, len(vote_hashes), 2):
            if i == len(vote_hashes) - 1:
                new_hashes.append(vote_hashes[i])
            else:
                concatenated = vote_hashes[i] + vote_hashes[i+1]
                new_hash = sha256(concatenated.encode()).hexdigest()
                new_hashes.append(new_hash)  # 将新节点添加到存储所有节点的列表中
        vote_hashes = new_hashes
    if vote_hashes[-1]==block.merkle:
        flag=0
        print("votedata is all right!")
    else:
        flag=1
        print("data may be changed")
        vote_hashes = [sha256(str(vote).encode()).hexdigest() for vote in votedata]
        different_indices=find_different_indices(vote_hashes,block.tree)
        print("There is error in the vote location:",end='')
        print(different_indices)
    return flag==0

def find_different_indices(list1, list2):
    different_indices = []
    for i, (item1, item2) in enumerate(zip(list1, list2)):
        if item1 != item2:
            different_indices.append(i)
    return different_indices