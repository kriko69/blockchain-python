import time
from Backend.Util.Crypto_hash import crypto_hash
from Backend.Config import MINE_RATE
from Backend.Util.Hex_to_binary import hex_to_binary
#informacion que tendra el genesis block
GENESIS_DATA={
    'timestamp':1,
    'last_hash':'genesis_last_hash',
    'hash':'genesis_hash',
    'data':[],
    'difficulty':3,
    'nonce':'genesis_nonce'
}

class Block:


    #constructor
    def __init__(self,timestamp,last_hash,hash,data,difficulty,nonce):
        self.data=data #informacion
        self.timestamp=timestamp #tiempo
        self.last_hash=last_hash #anterior hash
        self.hash=hash #hash del bloque
        self.difficulty=difficulty #dificultad
        self.nonce=nonce

    #representation es como el tostring()
    def __repr__(self):
        return(
            'Block('
            f'Timestamp: {self.timestamp}, '
            f'Last-hash: {self.last_hash}, '
            f'Hash: {self.hash}, '
            f'Data: {self.data}, '
            f'Difficulty: {self.difficulty}, '
            f'Nonce: {self.nonce})'
        )

    def __eq__(self, other): #compara si un bloque es igual a otro bloque al usar == or != se invoca esta funcion
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary  of its attributes
        """
        return self.__dict__
    @staticmethod #un metodo estaico no necesita self y la forma de llamar al metodo es desde la misma clase
    def mine_block(last_block, data):
        """
        Prepara el blowue para unirlo a la cadena
        Retorna el bloque con los datos necesarios
        """
        timestamp = time.time()*1000000000 #con esto ponemos el time en nanosegundos
        #print('seconds:{0:.0f}'.format(timestamp*1000000000))
        last_hash = last_block.hash
        difficulty=Block.adjust_difficulty(last_block,timestamp)
        nonce=0
        hash = crypto_hash(timestamp,last_hash,data,difficulty,nonce) #creando el hash con toda la data,last hash y el tiempo
        while hex_to_binary(hash)[0:difficulty] != '0'*difficulty:
            nonce+=1
            timestamp=time.time()*1000000000 #actualizando el tiempo porque esto puede tardar
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data,difficulty,nonce)

    @staticmethod
    def genesis():
        """
        generate genesis block
        """
        #return Block(
        #   timestamp=GENESIS_DATA['timestamp'],
        #   last_hash=GENESIS_DATA['last_hash'],
        #   hash=GENESIS_DATA['hash'],
        #   data=GENESIS_DATA['data']
        #)

        #**GENESIS_DATA lee todos los datos del diccionario
        return Block(**GENESIS_DATA)


    @staticmethod
    def adjust_difficulty(last_block,new_timestamp):
        """
        Calculate th adjusted difficulty  according to the MINE_RATE.
        Increase the difficulty for quickly mine blocks
        Decrease the difficulty for slowly mine blocks
        """
        if(new_timestamp-last_block.timestamp)<MINE_RATE:
            return last_block.difficulty+1
        if (last_block.difficulty-1)>0: #verifica que no sea negativo
            return last_block.difficulty-1
        return 1 #por defecto  sies negativo
    @staticmethod
    def is_valid_block(last_block,block):
        """
        validate block by enforcing the following rules:
        - the block must have the proper last_block reference
        - the block  must meet  the proof of work  requirement
        - the difficulty must only adjust by 1
        - the hash must  be valid combination of the block fields
        """
        if block.last_hash != last_block.hash: #validacion del hash
            raise Exception('The block last_hash must be incorrect')
        if hex_to_binary(block.hash)[0:block.difficulty]!='0'*block.difficulty: #validacion de la prueba de trabajo
            raise Exception('The proof of requeriment  was not meet')
        if abs(last_block.difficulty-block.difficulty)>1: #validacion del ajuste de dificultad del PoW
            raise Exception('The block hash must only adjust by 1')

        reconstruction_hash=crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )
        if block.hash!=reconstruction_hash: #validacion del hash propio con los datos del bloque
            raise Exception('The block difficulty must be incorrect')

def main():

    """genesis_block=Block.genesis() #asi se llama a los metodos estaticos de la clase
    block=Block.mine_block(genesis_block,'hola')
    print(block)"""
    genesis_block = Block.genesis()
    bad_block=Block.mine_block(Block.genesis(),'chris')
    #bad_block.last_hash='evil-data'
    try:
        Block.is_valid_block(genesis_block,bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')


if __name__ == '__main__': #solo si es main se ejecuta
    main()
