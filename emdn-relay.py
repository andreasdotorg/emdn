import zmq
import emdn
import sys

def main():
    context = zmq.Context()
    receiver  = context.socket(zmq.PULL)
    receiver.bind("tcp://*:8500")
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:9500")
    rejected = context.socket(zmq.PUB)
    rejected.bind("tcp://*:9600")

    while True:
        data = receiver.recv()
        try:
            emdn.verify(data)
            publisher.send(data)
        except Exception as e:
            print e
            rejected.send(data)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
