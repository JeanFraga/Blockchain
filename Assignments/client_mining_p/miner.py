import hashlib
import json
from time import time
from uuid import uuid4
import requests
import sys

from flask import Flask, jsonify, request

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    print('Mining has started')
    block_string = json.dumps(block[-1], sort_keys=True)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
    print(f"Minning has found a working proof in {proof}")
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return True or False
    return guess_hash[:4] == "000000"

app = Flask(__name__)

genesis_block = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
block = []

@app.route('/last_block', methods=['GET'])
def last_block():
    if len(block) > 0:
        block_string = json.dumps(block[-1], sort_keys=True)
        guess = f'{block_string}{proof}'.encode()
        current_hash = hashlib.sha256(guess).hexdigest()
    else:
        current_hash = genesis_block
    block = {
        'block': current_hash
    }
    return jsonify(block), 200

@app.route('/mine', methods=['POST'])
def mine():
    block = request.get_json()
    block['']


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("Blockchain/Assignments/client_mining_p/my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # new_proof = ???
        new_proof = data['block']

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        coins = 0
        if data['message'] == 'New Block Forged':
            coins += 1
