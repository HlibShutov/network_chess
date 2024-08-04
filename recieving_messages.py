from decrypt import decrypt
def recieve(key, client):
    message = list(map(int, client.recv(256).decode().split(' ')))
    print(f'{client.getpeername()[0]}:{client.getpeername()[1]} -', decrypt(key, message))
