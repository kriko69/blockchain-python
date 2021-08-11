from Backend.Blockchain.Blockchain import Blockchain
from Backend.Blockchain.Block import GENESIS_DATA
import pytest
def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain=Blockchain()
    data='test-data'
    blockchain.add_block(data)
    assert blockchain.chain[-1].data==data

@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    return blockchain


def test_is_valid_chain(blockchain_three_blocks):

    Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_is_valid_chain_bad_genesis_block(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash='evil-hash'
    with pytest.raises(Exception,match='the genesis block must be invalid'): #mismo error que se pone en raise Exception
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_replace_chain(blockchain_three_blocks):
    blockchain=Blockchain() #blockchain solo con genesis
    blockchain.replace_chain(blockchain_three_blocks.chain) #como blockchain_three_blocks es mas lago lo reemplaza
    assert blockchain.chain == blockchain_three_blocks.chain #comprobando que paso la longitud

def test_replace_chain_not_longer(blockchain_three_blocks):
    blockchain=Blockchain() #blockchain solo con genesis
    with pytest.raises(Exception,match='Cannot replace. The incoming chain must be longer'): #mismo error que se pone en raise Exception
        blockchain_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(blockchain_three_blocks):
    blockchain=Blockchain() #blockchain solo con genesis
    blockchain_three_blocks.chain[1].hash='evil-hash' #cambiando el hash a un bloque para que sea una cadena mala
    with pytest.raises(Exception,match='Cannot replace.Incoming chain is invalid'): #mismo error que se pone en raise Exception
        blockchain.replace_chain(blockchain_three_blocks.chain)