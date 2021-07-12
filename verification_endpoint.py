from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)

    #Check if signature is valid
    result = False #Should only be true if signature validates
    
    if 'sig' in content and 'payload' in content and 'platform' in content['payload']:
      sig = content['sig']
      payload_platform = content['payload']['platform']
      payload_pk = content['payload']['pk']
      payload = json.dumps(content['payload'])

      if payload_platform == 'Ethereum':
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == payload_pk:
            result = True

      elif payload_platform == 'Algorand':
        if algosdk.util.verify_bytes(payload.encode('utf-8'), sig, payload_pk):
            result = True

    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
