from Crypto.Cipher import AES 
from Crypto.Util import Padding
import hashlib
import os
from binascii import unhexlify
from .initdb import get_db
from flask import current_app, g
 

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

def get_all():
    dbconn = get_db()
    with dbconn.cursor() as cur:
        SQL = '''
            SELECT w.website, a.email, a.pw, a.salt, a.iv, a.id
            FROM website w
            INNER JOIN pw a ON a.pw_id = w.id AND w.website_id = %s
            ORDER by w.id
        '''
        table = cur.execute(SQL, (g.user[0],)).fetchall()
        if not table:
            table = "None"
        else:
            temp = [None] * len(table)
            i = 0
            for row in table:
                cipher_dict = {
                    'cipher_text' : row[2],
                    'salt' : row[3],
                    'iv' : row[4]    
                }
                temp[i] = (row[0], row[1], decrypt(cipher_dict, current_app.config['SECRET_KEY']), row[5])
                i += 1
            table = temp
    return table