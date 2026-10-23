import hashlib
import random
import pickle

import time

#precomputed values to generate the password length, that follows the proportion of possible 1, 2 and 3 word passwords

#there are 7776 possible 1 word passwords, 60.466.176 possible 2 word passwords, and, using only 2 dice to determine the last word, 2.176.782.336 possible 3 word passwords.
#there are 2.237.256.288 possible words in total, and most of them are 3 word passwords, so a good reduction function should generate more 3 word passwords
#that proportion is then scaled to fit 4 bytes of information (4.294.967.296 possible values)
#as an example, 0,000347% of passwords have only one word, so 0,000347% of 4.294.967.296 (14.927,957) bit combinations should be allocated to one word password 
#given a password length n, Threshold(n)=P(len(password)<=n)*2^32
TWO_WORD_THRESHOLD=14927
THREE_WORD_THRESHOLD=116094721

DICEWARE_LENGTH=7776


random.seed(42)

with open("diceware.txt", "r") as f:
    lines=f.readlines()

lines=[line.strip() for line in lines]

def myHash(s):
    hash_object = hashlib.sha256()
    hash_object.update(b"GBC083")
    hash_object.update(s.encode('utf-8'))
    #return hash_object.hexdigest()
    return hash_object.digest()

def computeEnd(start, reduceMasks):
    for mask in reduceMasks:
        start=reduce(myHash(start), mask)
    return start

def reduce(bytes, mask):
    lenByte=bytes[mask[0]]+256*bytes[mask[1]]+65536*bytes[mask[2]]+16777216*bytes[mask[3]] #acts like converting a base 256 number into base 10
    result=lines[(bytes[mask[4]]*256+bytes[mask[5]])%DICEWARE_LENGTH] #generate first word
    if(lenByte>TWO_WORD_THRESHOLD): #checks if another word is needed
        result+=lines[(bytes[mask[6]]*256+bytes[mask[7]])%DICEWARE_LENGTH]
        if(lenByte>THREE_WORD_THRESHOLD):
            result+=lines[(bytes[mask[8]]*256+bytes[mask[9]])%36] #only two dice used for a possible third word
    return result

def generateRT(width, length):
    reduceMasks=[]
    for _ in range(width):
        reduceMasks.append(random.choices(range(32), k=10))
    with open("reduceMasks.pkl", "wb") as f:
        pickle.dump(reduceMasks, f)
    with open("rainbow_table.txt", "a") as f:
        for i in range(length):
            start=reduce(myHash(str(i)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) #start is a pseudo-random word from the dictionary
            end=computeEnd(start, reduceMasks)
            f.write(f"{start} {end}\n")
    return

start_time = time.time()
for _ in range(2):
    generateRT(10000, 10000)
print((time.time() - start_time)/2)