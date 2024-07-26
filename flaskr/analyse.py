import string
from password_strength import PasswordPolicy
from flask import current_app, g
from .initdb import get_db
from .actions import decrypt

policy = PasswordPolicy.from_names(
    length=10,            # min length: 10
    uppercase=1,          # need min. 1 uppercase letters
    numbers=3             # need min. 3 digits
)

def check_strength(password):
    # Check the strength of a password using password-strength library
    policy_result = policy.test(password)
    if len(policy_result) == 0:
        return "strong"
    elif len(policy_result) < 2:
        return "moderate"
    else:
        return "weak"

def analyse_passwords():
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
            return []

        temp = []
        passwords = {}
        for row in table:
            cipher_dict = {
                'cipher_text': row[2],
                'salt': row[3],
                'iv': row[4]
            }
            decrypted_password = decrypt(cipher_dict, current_app.config['SECRET_KEY'])
            strength = check_strength(decrypted_password)
            is_unique = "Yes" if decrypted_password not in passwords else "No"
            passwords[decrypted_password] = True
            temp.append((row[0], row[1], decrypted_password, strength, is_unique, row[5]))

    return temp