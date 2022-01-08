from utils.environment import Environment
from utils.singleton import MetaSingleton
from addict import Dict

class ResourceManager(metaclass=MetaSingleton):
    def __getitem__(self, key):
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

