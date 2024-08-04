from encrypt import encrypt
def send(key, client):
    while True:
        message = input()
        message = encrypt(key, message)
        client.send(bytes("message:" + message, "utf-8"))
