import time

from datalayer.blockchain import Blockchain

# --libraries

# --project files

# --frequency of mining of blocks seconds
BLOCK_TIME_LIMIT = 20


# --inline methode that runs parallel to the program

def main():
    # --Blockchain initialized and Genesis block added
    time1 = time.time()
    EVoting1 = Blockchain(1, b"\x02Ed\xc1\xe7\xe1", 20)
    # EVoting1.display()
    time2 = time.time()
    duration = time2 - time1
    print("...................")
    print(duration)
    return


if __name__ == '__main__':
    main()
