# For timestamp
import datetime

# Calculating the hash in order to add digital fingerprints to the blocks
import hashlib

# To store data in the blockchain
import json

from random import random
import time
import re

# main chain
chain = []

# selfish miner's chain 
selfish_chain = []

# honest miner's chain
honest_chain = []

# fraction of hash power owned by selfish miner
#alpha = 0.35

# fraction of honest miners that build on selfish miner block in a tie.
#gamma = 0.00

class GenesisBlock:

# This function is created to create the very first block(genesis block) and set its hash to "0"
 def __init__(self):
  self.a = self.create_block(proof=1, previous_hash='0')
  chain.append(self.a)


# This function is created to create genesis block
 def create_block(self, proof, previous_hash):
  block = {'index': len(chain) + 1,
    'timestamp': str(datetime.datetime.now()),
    'proof': proof,
    'previous_hash': previous_hash,
  #  broadcast flag
    'BrF' : True,
  #  acceptance flag
    'AccF' : True,
  #  block acceptance flag
    'BAF' : True}
  return block
 

# This function is created to display the previous block in the chain
 def print_previous_block(self):
  return chain[-1]


# This is the function for proof of work and used to successfully mine the block 
 def proof_of_work(self, previous_proof):
  new_proof = 1
  check_proof = False
  
  while check_proof is False:
   hash_operation = hashlib.sha256(
    str(new_proof**2 - previous_proof**2).encode()).hexdigest()
   if hash_operation[:5] == '00000':
    check_proof = True
   else:
    new_proof += 1
    
  return new_proof


 def hash(self, block):
  encoded_block = json.dumps(block, sort_keys=True).encode()
  return hashlib.sha256(encoded_block).hexdigest()


class SelfishBlock:

 def create_block(self, proof, previous_hash):
  block = {'index': len(chain) + len(selfish_chain) + 1,
    'timestamp': str(datetime.datetime.now()),
    'proof': proof,
    'previous_hash': previous_hash,
    'BrF' : False,
    'AccF' : False,
    'BAF' : False}
  return block
 

 def print_previous_block(self):
    if (len(selfish_chain) == 0):
        return chain[-1]
    else:
        return selfish_chain[-1]

 
 def proof_of_work(self, previous_proof):
  new_proof = 1
  check_proof = False
  
  while check_proof is False:
   hash_operation = hashlib.sha256(
    str(new_proof**2 - previous_proof**2).encode()).hexdigest()
   if hash_operation[:5] == '00000':
    check_proof = True
   else:
    new_proof += 1
    
  return new_proof


 def hash(self, block):
  encoded_block = json.dumps(block, sort_keys=True).encode()
  return hashlib.sha256(encoded_block).hexdigest()


class HonestBlock:

 def create_block(self, proof, previous_hash):
  block = {'index': len(chain) + len(honest_chain) + 1,
    'timestamp': str(datetime.datetime.now()),
    'proof': proof,
    'previous_hash': previous_hash,
    'BrF' : False,
    'AccF' : False,
    'BAF' : False}
  return block
 

 def print_previous_block(self):
    if (len(honest_chain) == 0):
        return chain[-1]
    else:
        return honest_chain[-1]

 
 def proof_of_work(self, previous_proof):
  new_proof = 1
  check_proof = False
  
  while check_proof is False:
   hash_operation = hashlib.sha256(
    str(new_proof**2 - previous_proof**2).encode()).hexdigest()
   if hash_operation[:5] == '00000':
    check_proof = True
   else:
    new_proof += 1
    
  return new_proof


 def hash(self, block):
  encoded_block = json.dumps(block, sort_keys=True).encode()
  return hashlib.sha256(encoded_block).hexdigest()



# Create the objects of the classes
genesis_block = GenesisBlock()
selfish_block = SelfishBlock()
honest_block = HonestBlock()

def mine_selfish_block():
 previous_block = selfish_block.print_previous_block()
 if(previous_block['BAF']):
  previous_proof = previous_block['proof']
  proof = selfish_block.proof_of_work(previous_proof)
  previous_hash = selfish_block.hash(previous_block)
  sblock = selfish_block.create_block(proof, previous_hash)
  return sblock 

def mine_honest_block():
 previous_block = honest_block.print_previous_block()
 if(previous_block['BAF']):
  previous_proof = previous_block['proof']
  proof = honest_block.proof_of_work(previous_proof)
  previous_hash = honest_block.hash(previous_block)
  hblock = honest_block.create_block(proof, previous_hash)
  return hblock

#mine_genesis_block()

def broadcast(x):
 x['BrF'] = True
 return x['previous_hash'] , x['timestamp']
  

def runsimulation(iter):
    hmblocks = 0
    hmorphans = 0
    smblocks = 0
    smorphans = 0

    for _ in range(1, iter):
        
            # SM found a block

            selfishB = mine_selfish_block()
            
            time.sleep(3)
        
            #HM found a block

            honestB = mine_honest_block()


            h_previous_hash , h_timestamp = broadcast(honestB)
            
            s_previous_hash , s_timestamp = broadcast(selfishB)

            if(h_previous_hash == s_previous_hash):
              print("***********Accidental fork occurs****************")
              max_timestamp = max(h_timestamp,s_timestamp)
              print(max_timestamp)
              
              if(honestB['timestamp'] == max_timestamp):
                honestB['AccF'] = True
                if(honestB['AccF'] == True & honestB['BrF'] == True) :
                  honestB['BAF'] = True
                chain.append(honestB)
                hmblocks += 1
                smorphans += 1
              
              if(selfishB['timestamp'] == max_timestamp):
                selfishB['AccF'] = True
                if(selfishB['AccF'] == True & selfishB['BrF'] == True) :
                  selfishB['BAF'] = True
                chain.append(selfishB)
                smblocks += 1
                hmorphans += 1
          

    print("Iterations: %d" % (iter))
    print("SM %d blocks, HM %d blocks, ratio %f" % (smblocks, hmblocks, smblocks / float(smblocks + hmblocks)))
    print("Orphans: SM %d, HM %d, orphan ratio %f; SM: %f, HM: %f" % (smorphans, hmorphans,
               (smorphans + hmorphans) / float(smblocks + hmblocks + smorphans + hmorphans),
               smorphans / float(smblocks + smorphans), hmorphans / float(hmblocks + hmorphans)))
  

runsimulation(100)

print(len(chain))




