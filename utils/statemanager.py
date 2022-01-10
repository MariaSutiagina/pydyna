from utils.constants import DB_FILENAME
from utils.environment import Environment
from utils.singleton import MetaSingleton
from utils.crypt import password_encrypt, password_decrypt
import random
import string
import json

# реализует сохранение и загрузку из базы sqlite состояния игры
class StateManager(metaclass=MetaSingleton):
    def _gen_password(self):
        return ''.join(random.choices(list(string.ascii_uppercase), k=8))
    
    # сохраняет состояние игры, переданное в параметре data
    def save_state_enc(self, data:str):
        # подключение к базе берем из окружения (реализуется объектом Environment)
        db = Environment().db
        # генерим пароль длины 8 из случайного набор латинских символов
        password = self._gen_password()

        # шивруем этим паролем состояние игры
        enc_data = password_encrypt(data.encode(), password)

        # пишем состояние игры в таблицу hero базы
        query = 'replace into hero(password,data) values(?, ?)'        
        cursor = db.execute(query,(password, enc_data))
        db.conn.commit()
        
        # пароль возвращаем, для последующей демонстрации игроку
        return password

    # загружаем состояние игры
    def load_state(self, password:str):
        # подключение к базе берем из окружения (реализуется объектом Environment)
        db = Environment().db
        # вычитываем данные из таблицы hero по введенному иргоком паролю 
        query = f"select data from hero where password='{password}'"
        cursor = db.query(query)

        for row in cursor:
            enc_data = row['data']
            # если в базе нашли данные - дешифруем их паролем
            data = password_decrypt(enc_data, password)
            # возвращаем дешифрованные данные состояния игры
            return data.decode()
    
    # проверяем состояние - наличие раунда и уровня
    def check_state(self, state):
        # подключение к базе берем из окружения (реализуется объектом Environment)
        db = Environment().db
        # вычитываем данные из таблицы hero по введенному иргоком паролю 
        query = f"select 1 from levels where level='{state.level}' and round='{state.round}'"
        cursor = db.query(query)
        empty = True
        for row in cursor:
            empty = False
            break

        return not empty

                



        
        

