from uuid import uuid4
from blockchainObj.Blockchain import Blockchain

from flask import Flask, jsonify, request

def create_app():
    # Instantiate our Node
    APP = Flask(__name__)

    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    blockchain = Blockchain()


    @APP.route('/mine', methods=['GET'])
    def mine():
        # Run the proof of work algorithm to get the next proof
        proof = blockchain.proof_of_work()

        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

        return jsonify(response), 200


    @APP.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            # TODO: Return the chain and its current length
            'length': len(blockchain.chain),
            'chain': blockchain.chain
        }
        return jsonify(response), 200


    # Run the program on port 5000
    # if __name__ == '__main__':
    #     app.run(host='0.0.0.0', port=5000)
    return APP