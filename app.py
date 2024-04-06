from datalayer.blockchain import Blockchain

# --libraries

# --project files

# --frequency of mining of blocks seconds
BLOCK_TIME_LIMIT = 20


# --inline methode that runs parallel to the program

def main():
    # --Blockchain initialized and Genesis block added
    EVoting = Blockchain(b"\x02Ed\xc1\xe7\xe1", 1, 1000)
    Blockchain.display(EVoting)



    print(EVoting)
    return


if __name__ == '__main__':
    main()
