import hashlib
import random

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


def base6toint(s):
    result=0
    for i in s:
        result=result*6+i
    return result

def computeEnd(start, reduceFunc):
    for func in reduceFunc:
        start=func(myHash(start))
    return start

def getBytes(bytes, mask):
    result=[]
    for m in mask:
        result.append(bytes[m])
    return result

def reduce(bytes, mask):
    bytes=getBytes(bytes, mask)
    result=""
    for i in range(bytes[0]%4+2): #number of words taken (2, 3, 4 or 5)
        result+=lines[(bytes[i*2+1]*256+bytes[i*2+2])%len(lines)]
    return result



def generateRT(width, length):
    result=[]
    reduceFunctions=[]
    for _ in range(width):
        mask=(random.choices(range(32), k=11))
        reduceFunctions.append(lambda x: reduce(x, mask))
    for i in range(length):
        start=reduce(myHash(str(i)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) #start is a pseudo-random word from the dictionary
        end=computeEnd(start, reduceFunctions)
        result.append((start, end))
    return (result, reduceFunctions)

def lookup(hash, rainbowTable):
    pairs, reduceFunctions=rainbowTable
    for i in range(len(reduceFunctions)-1, -1, -1):
        candidate=hash
        for func in reduceFunctions[:-i]:
            candidate=func(candidate)
            for start, end in pairs:
                if end==candidate:
                    return start
            candidate=myHash(candidate)
    return None


result, func=generateRT(10, 10)

print(result)

start, end=result[-1]

find=computeEnd(start, func[:5])
print(find, myHash(find))

print(lookup(myHash(find), (result, func)))

