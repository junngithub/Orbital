from Crypto.Cipher import AES 
from Crypto.Util import Padding
import hashlib
import os
import base64
from binascii import hexlify, unhexlify
 

def to_pad(string):
    return Padding.pad(string, 16, style="x923")

def to_unpad(string):
    return Padding.unpad(string, 16, style="x923")

def encrypt(password, key):
    salt = os.urandom(AES.block_size)
    iv = os.urandom(AES.block_size)
    private_key = hashlib.blake2b(key.encode(), salt=salt, digest_size=32).digest()
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(to_pad(password.encode()))
    return {
        'cipher_text': cipher_text.hex(),
        'salt': salt.hex(),
        'iv' : iv.hex()
    }

def decrypt(cipher_dict, key):
    salt = unhexlify(cipher_dict['salt'])
    cipher_text = unhexlify(cipher_dict['cipher_text'])
    iv = unhexlify(cipher_dict['iv'])
    private_key = hashlib.blake2b(key.encode(), salt=salt, digest_size=32).digest()
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    text = to_unpad(cipher.decrypt(cipher_text))
    return text.decode()