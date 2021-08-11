from hashlib import sha256
import json
import time
from flask import Flask,request
import requests


class Block:
    def __init__(self,index,transaction,timestamp,previous_hash): #construira nuestro objeto
        self.index = index #numero de bloque
        self.transaction = transaction #transaccion
        self.timestamp=timestamp #tiempo
        self.previous_hash=previous_hash

    def compute_hash(self):
        block_string = json.dumps(self.__dict__,sort_keys=True) #convierte el bloque en una cadena de texto
        return sha256(block_string.encode()).hexdigest() #crear nuestro hash

class Blockchain:
    difficulty=2
    def __init__(self):
        self.unconfirmed_transaction=[] #bloques pendientes
        self.chain=[] #bloques en la cadena
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block=Block(0,[],time.time(),"0"*64)
        genesis_block.hash=genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1] #devuelve el ultimo bloque


    def print_block(self,n):
        if(len(self.chain)<n):
            return
        else:
            block = self.chain[n]
            return ' index: {}\n Transactions: {}\n Timestamp: {}\n PreviousHash: {}\n'.format(block.index,block.transaction,block.timestamp,block.previous_hash)


    def proof_of_work(self,block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*Blockchain.difficulty):
            block.nonce+=1
            computed_hash=block.compute_hash()
        return computed_hash

    def add_block(self,block,proof):
        previous_hash=self.last_block.hash
        if(previous_hash!=block.previous_hash):
            return False
        if not self.is_valid_proof(block,proof):
            return False
        block.hash=proof
        self.chain.append(block)
        return True

    def is_valid_proof(self,block,block_hash):
        return (block_hash.startswith('0'*Blockchain.difficulty) and block_hash==block.compute_hash())


    def new_transaction(self,transaction):
        self.unconfirmed_transaction.append(transaction)

    def mine(self):
        if not self.unconfirmed_transaction:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index-1,transaction=self.unconfirmed_transaction,timestamp=time.time(),previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block,proof)
        self.unconfirmed_transaction=[]
        return new_block.index

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/new_transaction',methods=['POST'])
def new_transaction():
    tx_data=request.get_json()
    require_fields= ["author","content"]
    for field in require_fields:
        if not tx_data.get(field):
            return "Datos invalidos",404
    tx_data["timestamp"]=time.time()
    blockchain.new_transaction(tx_data)
    return "Exito",201
@app.route('/chain',methods=['GET'])
def get_chain():
    chain_data=[]
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
        return json.dumps({"length":len(chain_data),
                           "chain":chain_data})

@app.route('/mine',methods=['GET'])
def mine_unconfirmed_transaction():
    result=blockchain.mine()
    if not result:
        return "No hay nada que minar"
    return "Block#{} minado".format(result)

@app.route('/pending_tx',methods=['POST'])
def pending_transaction():
    return json.dumps(blockchain.unconfirmed_transaction)

app.run(port=8000)

