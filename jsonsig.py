import simplejson as json
import pysodium
import base64

def sign_json(message, pk, sk):
    try:
        del message['sender']
    except KeyError:
        True
    try:
        del message['signature']
    except KeyError:
        True

    canonicalized = json.dumps(message, separators=(',', ':'), sort_keys=True)
    signature = pysodium.crypto_sign_detached(canonicalized, sk)
    message['sender'] = base64.b64encode(pk)
    message['signature'] = base64.b64encode(signature)

    return message

def check_json_signature(message):
    message = message.copy()
    sender = message['sender']
    del message['sender']
    signature = message['signature']
    del message['signature']

    canonicalized = json.dumps(message, separators=(',', ':'), sort_keys=True)
    return pysodium.crypto_sign_verify_detached(base64.b64decode(signature), canonicalized, base64.b64decode(sender))

