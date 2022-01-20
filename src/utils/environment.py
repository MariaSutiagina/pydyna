import sys
import os
from sqlite_utils import Database
from utils.constants import DB_FILENAME
from utils.singleton import MetaSingleton

class Environment(metaclass=MetaSingleton):
    def __init__(self):
        self.database = Database(self.get_path(DB_FILENAME), memory=False)

    def get_path(self, path):
        try:
            return os.path.join(sys._MEIPASS, path)
        except AttributeError:
            return path

    @property
    def db(self):
        return self.database


    

    