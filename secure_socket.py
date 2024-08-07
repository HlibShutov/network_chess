import socket
from encrypt import encrypt
from decrypt import decrypt
from hashlib import md5

class Secure_socket(socket.socket):
    def send_message(self, message, reciever_public_key):
        message = encrypt(reciever_public_key, message)
        self.send(bytes("message:" + message, "utf-8"))

    def send_move(self, message, private_key):
        sign = encrypt(private_key, md5(message.encode()).hexdigest())
        self.send(bytes(f"{message},{sign}", "utf-8"))

    def recieve(self, length, private_key, opponent_public_key):
        message = self.recv(length).decode()
        message_type = "message" if message[:8] == "message:" else "move"
        if message_type == "message":
            message = message[8:]
            message = decrypt(private_key, message)
        else:
            message, sign = ','.join(message.split(',')[:-1]), message.split(',')[-1] 
            decrypted_sign = decrypt(opponent_public_key, sign)
            if md5(message.encode()).hexdigest() != decrypted_sign: print('sign does not match')

        return {"message_content": message, "message_type": message_type}

    def accept(self, public_key):
        fd, address = self._accept()
        client_socket = Secure_socket(self.family, self.type, self.proto, fileno=fd)

        client_socket.send(bytes(' '.join(list(map(str, public_key))), 'utf-8'))
        client_public_key = client_socket.recv(124).decode()
        client_public_key = list(map(int, client_public_key.split(' ')))

        return client_socket, address, client_public_key

    def connect(self, address, public_key):
        super().connect(address)

        client_public_key = self.recv(124).decode()
        client_public_key = list(map(int, client_public_key.split(' ')))
        self.send(bytes(' '.join(list(map(str, public_key))), 'utf-8'))

        return client_public_key
