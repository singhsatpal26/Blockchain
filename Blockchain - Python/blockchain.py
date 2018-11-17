# Module 1 - Create a Blockchain

import datetime
import hashlib
import json
from flask import Flask,jsonify                                    #jsonify is used to convert the data into json format for sending it to get and post

# Part 1 - Building a Blockchain

# Since we need to  create a lot of blockchains, we create a class. 

class Blockchain:                                                  
    
    def __init__(self):
        
         # initialise the blockchain's chain.
        self.chain=[]

        # creating the GENESIS BLOCK (THE FIRST BLOCK OG THE BLOCKCHAIN).                                     
        self.create_block(proof = 1 , previous_hash = '0')  
        
    
    def create_block(self, proof , previous_hash):
        
        block = { 'index'         : len(self.chain) + 1,
                  'timestamp'     : str(datetime.datetime.now()),
                  'proof'         : proof ,
                  'previous_hash' : previous_hash
                 }
        
        self.chain.append(block)
        
        return block
    
    
    def proof_of_work(self,block):
        
        new_proof=1
        check_proof = False
        
        while check_proof is False :
            
            block['proof'] = new_proof
            encoded_block = json.dumps(block, sort_keys = True).encode()
            hash_operation = hashlib.sha256(encoded_block).hexdigest()
            
            if hash_operation[:4]=="0000":
                check_proof = True
                
            else :
                new_proof +=1
                
        return new_proof
    
    def get_previous_block(self):
        return self.chain[len(self.chain)-1]
    
    
    def hash(self,block):
        
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    def is_chain_valid(self, chain):
        
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            hash_operation=self.hash(block)
            if hash_operation[:4] != "0000":
                return False
            
            previous_block = block
            
            block_index +=1
            
        return True
    
#   Part 2 - Mining our Blockchain
        
#   Creating our app
app = Flask(__name__)

#   Creating a Blockchain
blockchain = Blockchain()

#   Mining a new block
@app.route('/mine_block' , methods = [ 'GET' ])
def mine_block():
    previous_block = blockchain.get_previous_block
    previous_hash = blockchain.hash(previous_block)
    proof = 1
    block = blockchain.create_block(proof, previous_hash)
    new_proof = blockchain.proof_of_work(block)
    block['proof'] = new_proof
    response = { 'message' : 'THE BLOCK HAS BEEN SUCCESSFULLY MINED',
                 'index' : block['index'],
                 'timestamp' : block['timestamp'],
                 'proof' : block['proof'],
                 'previous_hash' : block['previous_hash']
                 }
    
    return jsonify(response),200

# Getting the full blockchain
    
@app.route('/get_chain' , methods = [ 'GET' ])
def get_chain():
    response = {'chain' : blockchain.chain , 
                'length' : len(blockchain.chain)
                }
    return jsonify(response), 200
                    
                
