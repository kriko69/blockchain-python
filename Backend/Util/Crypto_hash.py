import hashlib
import json

def stringify(data):
    return json.dumps(data) #retorna la data limpia

def crypto_hash(*args):
    """return a sha-256 hash of the given data"""
    stringifield_args=map(stringify,args) #doy formato a los argumentos
    #print(f"stringifield_args: {stringifield_args}") #todo convertido a direccion de memoria
    joined_data=''.join(stringifield_args) #uno todos los argumentos
    #print(f"joined_data: {joined_data}")
    return hashlib.sha256(joined_data.encode('UTF-8')).hexdigest() #hexdigest hace que de 256 caracteres se represente en 64

def main():
    #data='hola'
    #print(data.encode('UTF-8'))
    print(f"crypto_hash('uno','2',['A',2.58,True]): {crypto_hash('uno','2',['A',2.58,True])}")

if __name__ == '__main__':
    main()

