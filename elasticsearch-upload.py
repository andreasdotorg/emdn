import zlib
import zmq
import requests

elasticsearch_url="http://localhost:9200/emdn/message"

def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    subscriber.connect('tcp://firehose.elite-market-data.net:9500')
    subscriber.setsockopt(zmq.SUBSCRIBE, "")

    while True:
        market_json = zlib.decompress(subscriber.recv())
        requests.post(elasticsearch_url, market_json)

if __name__ == '__main__':
    main()
