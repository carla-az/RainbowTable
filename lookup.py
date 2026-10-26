import pickle
from genTable import myHash, reduce
import random

def generateRandomPassword(words, length):
    return "".join(random.choices(words, k=length))

def load():
    with open("reduceMasks12kBY188K.pkl", "rb") as f:
        reduceMasks=pickle.load(f)
    pairs=[]
    with open("rainbow_table12kBY188K.txt", "r") as f:
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

with open("diceware.txt", "r") as f:
    lines=[line.strip() for line in f.readlines()]

NUMBER_OF_TRIES=100000

miss=0
#1 word password
for line in lines:
    start=lookup(myHash(line), rt)
    if start is None:
        miss+=1

print(miss,"misses out of 7776 possibilities")


miss=0
wordMisses=[]
#2 word password
for _ in range(NUMBER_OF_TRIES):
    input=generateRandomPassword(lines, 2)
    start=lookup(myHash(input), rt)
    wordMisses.append(input)
    if start is None:
        miss+=1

print(miss,"misses out of 100.000 tries\nWords missed:")
print(wordMisses)



miss=0
wordMisses=[]
#3 word password
for _ in range(NUMBER_OF_TRIES):
    input=generateRandomPassword(lines, 2)
    start=lookup(myHash(input), rt)
    wordMisses.append(input)
    if start is None:
        miss+=1

print(miss,"misses out of 100.000 tries\nWords missed:")
print(wordMisses)
