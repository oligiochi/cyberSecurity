from sql_w.util.Inj import Inj
import binascii
import time

inj = Inj('http://web-17.challs.olicyber.it')
dictionary = '0123456789abcdef'
r=inj.time('1')
print(r)
timestart=time.time()
for i in range(1,100):
    inj.time(i)
timeend=time.time()
print(f"Time taken for 10k requests: {timeend-timestart} seconds")
print("average time per request: {} seconds".format((timeend-timestart)/100))