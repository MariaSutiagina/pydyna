from sqlite_utils import Database
from utils.constants import DB_FILENAME
from utils.singleton import MetaSingleton

class Environment(metaclass=MetaSingleton):
    def __init__(self):
        self.database = Database(DB_FILENAME, memory=False)

    @property
    def db(self):
        return self.database


    

    