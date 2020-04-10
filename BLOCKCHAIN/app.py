from blockchainObj.Blockchain import Blockchain
import json

from uuid import uuid4
from flask import Flask, jsonify, request, render_template

def create_app():
    # Instantiate our Node
    APP = Flask(__name__)

    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    blockchain = Blockchain()

    @APP.route('/', methods=['GET'])
    def root():
        f = open("BLOCKCHAIN/my_id.txt", "r")
        users = f.read()
        f.close()
        return render_template('base.html', title='Home', users=users)
    

    @APP.route('/mine', methods=['POST'])
    def mine():
        # Run the proof of work algorithm to get the next proof
        # proof = blockchain.proof_of_work()

        # TODO: GET PROOF FROM CLIENT
        # data is a dictionary with the POST variables
        data = request.get_json()

        # Check that 'proof', and 'id' are present
        if 'proof' not in data or 'id' not in data:
            response = {'message': 'Must contain "proof" and "id"'}
            return jsonify(response), 400

        proof = data['proof']

        # Determine if the proof is valid
        last_block = blockchain.last_block
        last_block_string = json.dumps(last_block, sort_keys=True)

        if blockchain.valid_proof(last_block_string, proof):
            blockchain.new_transaction(sender="0", recipient=data["id"].strip(), amount=1)

            # Forge the new Block by adding it to the chain with the proof
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)


            response = {
                'message': "New Block Forged",
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
            }
            return jsonify(response), 200
        else:
            response = {'message': 'Invalid proof'}
            return jsonify(response), 200


    @APP.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            # TODO: Return the chain and its current length
            'length': len(blockchain.chain),
            'chain': blockchain.chain
        }
        return jsonify(response), 200


    @APP.route('/last_block', methods=['GET'])
    def get_last_block():
        response = {
            'last_block': blockchain.last_block
        }
        return jsonify(response), 200

    @APP.route('/transactions/add_user', methods=['POST'])
    def add_user():
        users = request.get_json()

        return render_template('base.html', title='Home', users=users)

    @APP.route('/transactions/new', methods=['POST'])
    def new_transaction():
        values = dict()
        values['sender'], values['recipient'], values['amount'] = sorted([request.values['sender'],
                                                                          request.values['recipient'],
                                                                          request.values['amount']])
        print(values)
        f = open("BLOCKCHAIN/my_id.txt", "r")
        users = f.read()
        f.close()
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing Values', 400

        index = blockchain.new_transaction(values["sender"],
                                        values["recipient"],
                                        values["amount"])

        response = {'message': f"Transaction will be added to Block {index}"}
        # return jsonify(response), 200
        return render_template('transactions.html', title='Home', response=response, users=users)


    # Run the program on port 5000
    # if __name__ == '__main__':
    #     app.run(host='0.0.0.0', port=5000)
    return APP