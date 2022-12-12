# For timestamp
import datetime

# Calculating the hash in order to add digital fingerprints to the blocks
import hashlib

# To store data in the blockchain
import json
import time

#from random import random
import random

# main chain
chain = []

# selfish miner's chain 
selfish_chain = []

# honest miner's chain
honest_chain = []

# fraction of maximum hash power owned by selfish miner 0.49 
#(ref :- Blockchain Mining with Multiple Selfish Miners)
#γ = 0, the threshold for success of block-withholding behavior is α ≥33 %
alpha = random.uniform(0.33,0.49)

# fraction of honest miners that build on selfish miner block in a tie.
gamma = 0.00


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


def broadcast(x):
 x['BrF'] = True
 x['AccF'] = True
 if(x['BrF'] == True & x['AccF'] == True):
  x['BAF'] = True
 return x['previous_hash'] , x['timestamp']

def runsimulation(iter):
    hmblocks = 0
    hmorphans = 0
    smblocks = 0
    smorphans = 0

    for _ in range(1, iter):

        # SM chain is always longer than HM chain because otherwise SM switches to HM chain(main chain)
        assert len(selfish_chain) >= len(honest_chain)

        # SM will never risk more than one block to a tie
        assert len(selfish_chain) != len(honest_chain) or len(selfish_chain) < 2

        if(random.random() < alpha):

            selfishB =mine_selfish_block()
            
            if (len(selfish_chain) > 0) and (len(selfish_chain) == len(honest_chain)):
                # SM publishes its chain to resolve tie.
                if(selfishB!= None):
                 selfish_chain.append(selfishB)
                
                 s_previous_hash , s_timestamp = broadcast(selfishB) 

                 chain.extend(selfish_chain[:])
                 smblocks += len(selfish_chain)
                 hmorphans += len(honest_chain)
                del honest_chain[:]
                del selfish_chain[:]
                
               

            else:
                # SM mines selfishly
                assert (len(selfish_chain) == 0 and len(honest_chain) == 0) or len(selfish_chain) > len(honest_chain)
                
                if(selfishB!= None):
                 selfish_chain.append(selfishB)
                 time.sleep(3)


                
        else:
            #HM found a block

            honestB =mine_honest_block()

            if len(selfish_chain) == 0:
                # HM publishes and SM builds on top
                assert len(honest_chain) == 0
                if(honestB!= None):
                 honest_chain.append(honestB)
                
                 h_previous_hash , h_timestamp = broadcast(honestB)

                 chain.extend(honest_chain[:])
                 hmblocks += len(honest_chain)
                 smorphans += len(selfish_chain)
                del honest_chain[:]
                del selfish_chain[:]

                

            elif (len(selfish_chain) == len(honest_chain) and random.random() < gamma):
                # In case of a tie, a fraction of HM may build on SM's chain
                # and this gets the longest published chain
                assert len(honest_chain) == 1
                smblocks += len(selfish_chain)
                hmorphans += len(honest_chain)
                del honest_chain[:]
                del selfish_chain[:]

                if(honestB!= None):
                 honest_chain.append(honestB)
               

            else:
                # HM builds on its own chain.
                if(honestB!= None):
                 honest_chain.append(honestB)

                if len(selfish_chain) == len(honest_chain) + 1:
                    # If SMs chain is longer by exactly 1,
                    # SM will publish his longer chain.
                    if(honestB!= None):
                     h_previous_hash , h_timestamp = broadcast(honestB)

                     chain.extend(selfish_chain[:])
                     smblocks += len(selfish_chain)
                     hmorphans += len(honest_chain)
                    del honest_chain[:]
                    del selfish_chain[:]


                if len(honest_chain) > len(selfish_chain):
                    # if HM has longer chain, SM switches to it.
                    if(honestB!= None):
                     h_previous_hash , h_timestamp = broadcast(honestB)

                     chain.extend(honest_chain[:])
                     hmblocks += len(honest_chain)
                     smorphans += len(selfish_chain)
                    del honest_chain[:]
                    del selfish_chain[:]
          

    print("Iterations: %d, alpha: %f, gamma: %f" % (iter, alpha, gamma))
    print("SM %d blocks, HM %d blocks"
            % (smblocks, hmblocks ))
    print(" Orphans: SM %d, HM %d "
            % (smorphans, hmorphans))

    print(" still contested: SM %d, HM %d"
            % (len(selfish_chain), len(honest_chain)))


runsimulation(100)

print(len(chain))



