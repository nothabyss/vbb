# Blockchain Voting System Listener Explanation

## Overview
The listener in the blockchain voting system is designed to monitor a specified directory for CSV files, which represent voting pools. Each CSV file corresponds to a unique voting activity. The listener ensures that for each voting activity, a blockchain is initiated, mining processes are managed, and resources are appropriately released when conditions are met.

## How It Works
1. **Monitoring CSV Files**:
   - The listener continuously checks the `vbb/records/vote_pool` directory for CSV files.
   - Each CSV file represents a separate voting activity, with its name containing critical parameters like maximum votes, duration, and a unique identifier.

2. **Blockchain Initialization**:
   - For each new CSV file detected, a new blockchain instance is created.
   - The blockchain manages the voting data encapsulated in the CSV file, including creating blocks through a mining process.

3. **Mining Process**:
   - A separate thread is spawned for each blockchain instance to handle the mining process.
   - Mining involves validating new votes, creating new blocks, and ensuring the integrity of the blockchain through cryptographic methods.

4. **Termination Conditions**:
   - Each blockchain instance operates under specific constraints, such as a maximum number of votes or a time limit.
   - Once these conditions are met, the thread managing the blockchain terminates, ensuring that resources are efficiently utilized and released.

5. **Data Management**:
   - After mining, the resulting blockchain data (stored in `.dat` files) is organized within the `vbb/records/chains` directory, often categorized by date or other relevant metadata.
   - If a CSV file is depleted (i.e., all votes are processed), it is automatically removed from the directory to prevent reprocessing.


## Running the Listener
To run the listener, ensure that you have Python installed on your machine and the necessary project files are correctly set up.

**Run the Script**:
   - Execute the listener by typing:
     ```
     python listener2.py
     ```