def send(key, client):
    while True:
        message = input()
        client.send_message(message, key)
