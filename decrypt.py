def decrypt(key, message):
    message = list(map(int, message.split()))
    n, d = key[0], key[1] 
    def decrypt_character(character):
        return pow(character, d, n)
    decrypted_message = list(map(decrypt_character, message))
    decrypted_message = list(map(chr, decrypted_message))
    return ''.join(decrypted_message)
