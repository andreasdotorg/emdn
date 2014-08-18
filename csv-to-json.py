import simplejson as json
import zmq
import sys
import base64
import zlib
from jsonsig import *

fieldnames = "buyPrice,sellPrice,demand,demandLevel,stationStock,stationStockLevel,categoryName,itemName,stationName,timestamp".split(',')

(pk, sk) = pysodium.crypto_sign_keypair()

context = zmq.Context()
socket  = context.socket(zmq.SUB)
socket.connect("tcp://firehose.elite-market-data.net:9050")
socket.setsockopt(zmq.SUBSCRIBE, "")
publisher = context.socket(zmq.PUSH)
publisher.connect("tcp://collector.elite-market-data.net:8500")

while True:
    data      = socket.recv()
    values    = data.split(',')
    
    message   = dict(zip(fieldnames, values))
    message['timestamp'] = message['timestamp']+"+00:00"
    for field in ['buyPrice', 'sellPrice']:
        message[field] = float(message[field])
    for field in ['demand', 'demandLevel', 'stationStock', 'stationStockLevel']:
        message[field] = int(message[field])

    envelope  = {'version': '0.1', 'type': 'marketquote', 'message': message}
    envelope = sign_json(envelope, pk, sk)

    jsonstring = json.dumps(envelope, separators=(',', ':'), sort_keys=True)
    print jsonstring
    publisher.send(zlib.compress(jsonstring))

    sys.stdout.flush()
