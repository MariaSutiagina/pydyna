from utils.environment import Environment
from utils.singleton import MetaSingleton
from addict import Dict
import random

class ResourceManager(metaclass=MetaSingleton):
    def __getitem__(self, key):
        return self.get(key)

    def get(self, key):
        db = Environment().db
        query = 'select "type", "order", resource, duration from resources where name=? order by "type", "order"' 
        cursor = db.query(query, [key])
        resource = Dict()
        for row in cursor:
            rt = row['type']
            ro = row['order']
            ritem = resource[rt][f'N{ro:03}']
            ritem.resource = row['resource']
            ritem.duration = row['duration']
        return resource

    def create_layout(self, key, type, size):
        resource = self.get(key)
        items = resource[type]
        if len(items) <= 1:
            indexes = [1]
        else:
            indexes = random.choices(items, size)
        return (items, list(map(lambda x: f'N{x:002}', indexes)))




