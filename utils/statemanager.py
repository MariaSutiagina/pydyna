from utils.constants import DB_FILENAME
from utils.environment import Environment
from utils.singleton import MetaSingleton
from utils.crypt import password_encrypt, password_decrypt
import random
import string
import json


class StateManager(metaclass=MetaSingleton):
    def _gen_password(self):
        return ''.join(random.choices(list(string.ascii_uppercase), k=8))

    def save_state_enc(self, data:str):
        db = Environment().db
        password = self._gen_password()
        enc_data = password_encrypt(data.encode(), password)
        query = 'replace into hero(password,data) values(?, ?)'        
        cursor = db.execute(query,(password, enc_data))
        db.conn.commit()

        return password

    def finalize_state(self, password:str):
        db = Environment().db
        query = f"update hero set password=NULL where password='{password}'"        
        cursor = db.execute(query)
        db.conn.commit()


    def load_state(self, password:str):
        db = Environment().db
        query = f"select data from hero where password='{password}'"
        cursor = db.query(query)
        for row in cursor:
            enc_data = row['data']
            data = password_decrypt(enc_data, password)
            return data.decode()

        query = f"select data from hero where password is NULL"
        cursor = db.query(query)
        for row in cursor:
            enc_data = row['data']
            try:
                data = password_decrypt(enc_data, password)
                o = json.loads(data)
                return data
            except:
                pass

                



        
        

