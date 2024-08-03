def encrypt(key, message):
    message = list(map(ord, message))
    n, e = key[0], key[1] 
    def encrypt_character(character):
        return str(pow(character, e, n))
    return ' '.join(list(map(encrypt_character, message)))
