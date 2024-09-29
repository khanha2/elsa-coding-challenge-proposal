import sys
import os

from receivers import record_results_receiver

if __name__ == '__main__':
    try:
        record_results_receiver.start()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
