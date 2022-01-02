from sqlite_utils import Database
from utils.singleton import MetaSingleton

class Environment(metaclass=MetaSingleton):
    def __init__(self, db_filename:str):
        self.filename = db_filename
        self.database = Database(db_filename, memory=False)

    @property
    def db(self):
        return self.database


    

    