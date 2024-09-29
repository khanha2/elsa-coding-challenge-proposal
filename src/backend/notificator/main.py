import sys
import os

from receivers import message_broadcasting_receiver

if __name__ == '__main__':
    try:
        message_broadcasting_receiver.start()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
