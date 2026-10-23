import pickle
from genTable import myHash, reduce
import random

def generateRandomPassword(words, length):
    return "".join(random.choices(words, k=length))

def load():
    with open("reduceMasks.pkl", "rb") as f:
        reduceMasks=pickle.load(f)
    pairs=[]
    with open("rainbow_table.txt", "r") as f:
        for line in f.readlines():
            start, end=line.strip().split()
            pairs.append((start, end))
    return pairs, reduceMasks

def lookup(hash, rainbowTable):
    pairs, reduceMasks=rainbowTable
    for i in range(len(reduceMasks)-1, -1, -1):
        candidate=hash
        for mask in reduceMasks[:-i]:
            candidate=reduce(candidate, mask)
            for start, end in pairs:
                if end==candidate:
                    return start
            candidate=myHash(candidate)
    return None

rt=load()
print(lookup(myHash("teste"), rt))

with open("diceware.txt", "r") as f:
    lines=[line.strip() for line in f.readlines()]


for _ in range(10):
    password=generateRandomPassword(lines, 3)
    print(f"Password: {password}\nLookup:{lookup(myHash(password), rt)}")
