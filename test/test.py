import re
def find_id(id, folder_name):
    match = re.search(r'chain_(\d+)', folder_name)

    if match:
        number_after_chain = match.group(1)
        return id
    else:
        print("cannot find the blockchain, please check your name")
        return 0