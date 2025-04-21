import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/barenbo/Desktop/Code/robot/lab2/install/py_pubsub'
