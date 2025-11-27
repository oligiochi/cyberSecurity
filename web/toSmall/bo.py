import random, hashlib

username = "ciao6"
seed = int(hashlib.sha256(username.encode()).hexdigest(), 16)

random.seed(seed)

A = [random.randint(0, 4000) for _ in range(10)]
B = [random.randint(0, 4000) for _ in range(5)]

print("A =", A)
print("B =", B)
