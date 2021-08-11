from Backend.Blockchain.Block import Block #importando la clase block

#esta importacion ya no es necesario porque los metodos son estaticos,
#si estuvieran fuera de la clase block si seria necesario.
#from Block import genesis,mine_block

class Blockchain:

    #constructor
    def __init__(self):
        self.chain=[Block.genesis()] #agrega el bloque genesis

    #agrega bloues a la cadena
    def add_block(self,data):
        #last_block = self.chain[-1] #el ultimo bloque
        self.chain.append(Block.mine_block(self.chain[-1],data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self,chain):
        """
        replace the local chain with the incoming one  if the following applies:
            -the incoming chain is longer that the local one
            -the incoming chain is formetted properly
            *self is the local chain and chain is the incoming chain
        """
        if len(chain)<= len(self.chain): #si la cadena que entra es mas corta no se reemplaza
            raise Exception('Cannot replace. The incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace.Incoming chain is invalid: {e}')

        self.chain=chain


    def to_json(self):
        """
        Serialize the blockchain into  a list of blocks.
        """
        serialized_chain=[]
        for block in self.chain:
            serialized_chain.append(block.to_json())

        return serialized_chain
    @staticmethod
    def is_valid_chain(chain):

        """
        Validate de incoming chain.
        Enforce the following  rules  of the blokchain:
        -the chain must start with genesis block
        -block must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception('the genesis block must be invalid')

        for i in range(1,len(chain)):
            block=chain[i]
            last_block=chain[i-1]
            Block.is_valid_block(last_block,block)


def main():
    blockchain=Blockchain()
    blockchain.add_block('hola1')
    blockchain.add_block('hola2')
    print(blockchain)
    #print(f'Blockchain.py __name__: {__name__}') #para saber que es el main

if __name__ == '__main__': #solo si es main se ejecuta
    main()