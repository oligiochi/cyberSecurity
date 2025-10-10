# in sql/union/test2.py
from ..util.Inj import Inj

import binascii
import time

inj = Inj('http://web-17.challs.olicyber.it')
dictionary = '0123456789abcdef'
timestart=time.time()
for i in range(1,10000):
    inj.time(i)
timeend=time.time()
print(f"Time taken for 10k requests: {timeend-timestart} seconds")
print("average time per request: {} seconds".format((timeend-timestart)/10000))