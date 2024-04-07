import csv
import random
import os

# Replace with your actual votefile path
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
votefile_path = os.path.join(PROJECT_PATH, 'applayer', 'votefile.csv')

def append_random_votes(votefile_path, num_votes=10):
    candidates = ['Candidate A', 'Candidate B', 'Candidate C', 'Candidate D']
    voters = ['Voter1', 'Voter2', 'Voter3', 'Voter4']

    with open(votefile_path, 'a', newline='', encoding='UTF-8') as file:
        csv_writer = csv.writer(file)
        for _ in range(num_votes):
            voter = random.choice(voters)
            candidate = random.choice(candidates)
            timestamp = random.randint(1650000000, 1659999999)
            csv_writer.writerow([voter, candidate, timestamp])

if __name__ == "__main__":
    append_random_votes(votefile_path)