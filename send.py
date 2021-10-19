import requests

size = 0

for x in range(1000):
    print(requests.get("http://3.85.230.162/"))
    size += int(requests.get("http://3.85.230.162/").headers['content-length'])*2

print(size)