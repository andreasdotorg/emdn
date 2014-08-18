import simplejson
import jsonsig
import iso8601
import datetime
import pytz
import zlib

def verify(message):
    market_json = zlib.decompress(message)
    verify_decompressed(market_json)

def verify_decompressed(market_json):
    market_data = simplejson.loads(market_json)
    verify_parsed(market_data)

def verify_parsed(market_data):
    if not jsonsig.check_json_signature(market_data):
        raise ValueError("Bad signature!")
    if not len(market_data) == 5:
        raise ValueError("Wrong number of fields in envelope!")
    if not market_data['version'] == "0.1":
        raise ValueError("Unknown protocol version!")
    if not market_data['type'] == "marketquote":
        raise ValueError("Unknown message type!")
    message = market_data['message']
    if not len(message) == 10:
        raise ValueError("Wrong number of fields in message!")
    for field in ['buyPrice', 'sellPrice']:
        if not isinstance(message[field], float):
            raise ValueError("Field %s not of type float!" % field)
    for field in ['demand', 'demandLevel', 'stationStock', 'stationStockLevel']:
        if not isinstance(message[field], int):
            raise ValueError("Field %s not of type int!" % field)
    for field in ['categoryName', 'itemName', 'stationName']:
        if not isinstance(message[field], str):
            raise ValueError("Field %s not of type string!" % field)
    timestamp = iso8601.parse_date(message['timestamp'])
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    if abs((timestamp - now).total_seconds()) > 300:
        raise ValueError("Data not current!")
    
