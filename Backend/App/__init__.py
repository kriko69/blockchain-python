from flask import Flask, jsonify

from Backend.Blockchain.Blockchain import Blockchain
app=Flask(__name__)
blockchain= Blockchain()


for i in range(3):
    blockchain.add_block(i)
@app.route('/test')
def test():
    return 'test'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def blockchain_mine():
    data='data-test'
    blockchain.add_block(data)
    return jsonify(blockchain.chain[-1].to_json())



app.run(port=5000)
