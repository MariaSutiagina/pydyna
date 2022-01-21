import io
import pygame as pg
from pygame.event import Event

from models.bombs import Bombs
from models.monsters import Monsters
from utils.constants import BRICK_HARDNESS_MAX, BRICK_SOLID_TYPE, E_BRICK, E_EXIT, E_TREASURE, EXIT_TILE_TYPE, FIELD_TILES_H, FIELD_TILES_W, TILE_SIZE, TREASURE_TILE_TYPE, TREASURE_TYPES_COUNT
from utils.environment import Environment
import random
from utils.resourcemanager import ResourceManager

from utils.types import BrickAction, ExitAction, TreasureAction

class Level:
    def __init__(self, game, level:int, round:int):
        self.level = level
        self.round = round
        self.game = game

        self.create_bombs()
        self.extract_resources()
        self.extract_data()

    def create_bombs(self):
        self.bombs = Bombs(self.game)

    def extract_resources(self):
        level = self.level
        # level = 1
        self.resources = dict()
        self.resources['floor'] = ResourceManager()[f'tile-road-{level:02}'].image
        self.resources['bricks'] = ResourceManager()[f'tile-brick-{level:02}'].image
        self.resources['solid'] = ResourceManager()[f'tile-solid-{level:02}'].image
        self.resources['wall-horz'] = ResourceManager()[f'wall-horz-{level:02}'].image
        self.resources['wall-vert'] = ResourceManager()[f'wall-vert-{level:02}'].image
        self.resources['corner-lt'] = ResourceManager()[f'wall-lt-{level:02}'].image
        self.resources['corner-rt'] = ResourceManager()[f'wall-rt-{level:02}'].image
        self.resources['corner-lb'] = ResourceManager()[f'wall-lb-{level:02}'].image
        self.resources['corner-rb'] = ResourceManager()[f'wall-rb-{level:02}'].image
        self.resources['portal'] = ResourceManager()[f'exit-{level:02}'].image
    
    def create_random_tile_surface(self, tiletype):
        surface = pg.image.load(io.BytesIO(random.choice(list(self.resources[tiletype].items()))[1].resource)).convert_alpha()
        return surface
    
    def load_tile_surface(self, data):
        return pg.image.load(io.BytesIO(data)).convert_alpha()

    def create_tile_surface(self, tiletype, resource_code):
        return self.load_tile_surface(self.resources[tiletype][resource_code].resource)

    def extract_layout(self, data):
        self.layout = []
        for line in data.split('\n'):
            if line !='':
                ld = map(int, line.split(','))
                self.layout.append(list(ld))
        
        rowpos = {}
        for ri, row in enumerate(self.layout):
            for ci, cell in enumerate(row):
                rowpos[(ci, ri)] = cell

        self.bricks = dict(map(lambda y: (y[0], (y[1], self.create_random_tile_surface('bricks'))), 
                              filter(lambda x: x[1] > 0 and x[1] <= BRICK_HARDNESS_MAX, rowpos.items())))
        self.solid = dict(map(lambda y: (y[0], (y[1], self.create_random_tile_surface('solid'))), 
                              filter(lambda x: x[1] == BRICK_SOLID_TYPE, rowpos.items())))
        self.floor = dict(map(lambda y: (y[0], (y[1], self.create_random_tile_surface('floor'))), 
                              filter(lambda x: x[1] == 0, rowpos.items())))

        self.wall_horz = []
        for _ in self.layout[0]:
            self.wall_horz.append(self.create_random_tile_surface('wall-horz'))

        self.wall_vert = []
        for _ in self.layout:
            self.wall_vert.append(self.create_random_tile_surface('wall-vert'))

        self.corner_lt = self.create_random_tile_surface('corner-lt')  
        self.corner_lb = self.create_random_tile_surface('corner-lb')  
        self.corner_rt = self.create_random_tile_surface('corner-rt')  
        self.corner_rb = self.create_random_tile_surface('corner-rb')  

        treasure_type = random.randint(TREASURE_TILE_TYPE, TREASURE_TILE_TYPE + TREASURE_TYPES_COUNT - 1)
        self.treasure_resources = []
        self.resources['treasure'] = ResourceManager()[f'treasure-{treasure_type - TREASURE_TILE_TYPE + 1:02}'].image

        for r in self.resources['treasure'].items():
            self.treasure_resources.append(self.load_tile_surface(r[1].resource))

        if self.bricks and len(self.bricks.items()) > 0:
            treasure_brick = random.choice(list(self.bricks.items()))
            self.treasure = (treasure_brick[0], (treasure_type, self.treasure_resources[0]))
            del self.bricks[treasure_brick[0]]

            self.exit = random.choice(list(self.bricks.items()))
        else:
            treasure_brick = None
            self.treasure = None
            self.exit = random.choice(list(self.floor.items()))
            self.floor[self.exit[0]] = (EXIT_TILE_TYPE, None)

        self.exit_resource = self.create_tile_surface('portal', 'N001')

        if self.treasure:
            self.bricks[self.treasure[0]] = (treasure_type, self.create_random_tile_surface('bricks'))
        


    def extract_monsters(self, data:str):
        rowpos = {}
        for ri, row in enumerate(self.layout):
            for ci, cell in enumerate(row):
                rowpos[(ci, ri)] = cell

        self.monster_bricks = []
        pairs = data.split(',')
        monsterdata = []
        for p in pairs:
            mt = p.split(':')
            monster_type = int(mt[0])
            monster_count = int(mt[1])
            for m in range(monster_count):
                brick = random.choice(list(self.floor.items()))
                monsterdata.append({'type': monster_type, 'pos': brick[0]})
                del self.floor[brick[0]]
                self.monster_bricks.append(brick)

        for b in self.monster_bricks:
            self.floor[b[0]] = b[1]

        self.monsters = Monsters(self.game, monsterdata)

    def extract_data(self):
        db = Environment().db
        query = f"select data, monsters from levels where level='{self.level:02}' and round='{self.round:02}'"
        cursor = db.query(query)
        for row in cursor:
            data = str(row['data'])
            monsters = str(row['monsters'])

            self.extract_layout(data)
            self.extract_monsters(monsters)

    def get_neighbour_obstacle_tiles(self, cellx:int, celly:int):
        tilex = cellx // TILE_SIZE
        tiley = celly // TILE_SIZE
        neighbours = []
        if tilex > 0:
            lt = self.layout[tiley][tilex - 1]
            if lt > 0 and lt <= BRICK_HARDNESS_MAX or lt == BRICK_SOLID_TYPE:
                neighbours.append((tilex - 1, tiley))
        if tilex < FIELD_TILES_W - 1:
            lt = self.layout[tiley][tilex + 1]
            if lt > 0  and lt <= BRICK_HARDNESS_MAX or lt == BRICK_SOLID_TYPE:
                neighbours.append((tilex + 1, tiley))
        if tiley > 0:
            lt = self.layout[tiley - 1][tilex]
            if lt > 0 and lt <= BRICK_HARDNESS_MAX or lt == BRICK_SOLID_TYPE:
                neighbours.append((tilex, tiley - 1))
        if tiley < FIELD_TILES_H - 1:
            lt = self.layout[tiley + 1][tilex]
            if lt > 0 and lt <= BRICK_HARDNESS_MAX or lt == BRICK_SOLID_TYPE:
                neighbours.append((tilex, tiley + 1))
        return neighbours

    def is_tile_free(self, cellx:int, celly:int):
        tilex = cellx // TILE_SIZE
        tiley = celly // TILE_SIZE
        tile_type = self.layout[tiley][tilex]
        return tile_type == 0 or tile_type == EXIT_TILE_TYPE or tile_type >= TREASURE_TILE_TYPE and tile_type <= TREASURE_TILE_TYPE + TREASURE_TYPES_COUNT

    def get_neighbour_free_tiles(self, cellx:int, celly:int, explosion_size:int=1):
        tilex = cellx // TILE_SIZE
        tiley = celly // TILE_SIZE
        neighbours = []
        for p in range(1,explosion_size + 1):
            if tilex - p >= 0:
                tile_type = self.layout[tiley][tilex - p]
                if tile_type < BRICK_SOLID_TYPE:
                    neighbours.append((tilex - p, tiley))
                    if tile_type > 0 and tile_type <= BRICK_HARDNESS_MAX:
                        break
                else:
                    break
            else:
                break
        for p in range(1,explosion_size + 1):
            if tilex + p < FIELD_TILES_W:
                tile_type = self.layout[tiley][tilex + p]
                if tile_type < BRICK_SOLID_TYPE:
                    neighbours.append((tilex + p, tiley))
                    if tile_type > 0 and tile_type <= BRICK_HARDNESS_MAX:
                        break
                else:
                    break
            else:
                break
        for p in range(1, explosion_size + 1):
            if tiley - p >= 0:
                tile_type = self.layout[tiley - p][tilex]
                if tile_type < BRICK_SOLID_TYPE:
                    neighbours.append((tilex, tiley - p))
                    if tile_type > 0 and tile_type <= BRICK_HARDNESS_MAX:
                        break
                else:
                    break
            else:
                break
        for p in range(1, explosion_size + 1):
            if tiley + p < FIELD_TILES_H:
                tile_type = self.layout[tiley + p][tilex]
                if tile_type < BRICK_SOLID_TYPE:
                    neighbours.append((tilex, tiley + p))
                    if tile_type > 0 and tile_type <= BRICK_HARDNESS_MAX:
                        break
                else:
                    break
            else:
                break
        return neighbours
         
    def remove_obstacles(self, cells):
        for c in cells:
            v = self.layout[c[1]][c[0]]
            if v > 0 and v <= BRICK_HARDNESS_MAX:
                v -= 1
                self.layout[c[1]][c[0]] = v
                if v == 0:
                    del self.bricks[c]
                    if c == self.exit[0]:
                        self.floor[c] = (EXIT_TILE_TYPE, None)
                        pg.event.post(Event(E_BRICK, action=BrickAction.REMOVE))
                        pg.event.post(Event(E_EXIT, action=ExitAction.SHOW))
                    elif c == self.treasure[0]:
                        self.floor[c] = self.treasure[1]
                        pg.event.post(Event(E_BRICK, action=BrickAction.REMOVE))
                        pg.event.post(Event(E_TREASURE, action=TreasureAction.SHOW, treasure=self.treasure, treasure_stage=1))
                    else:
                        self.floor[c] = (0, self.create_random_tile_surface('floor'))
                        pg.event.post(Event(E_BRICK, action=BrickAction.REMOVE))

    def remove_treasure(self):
        c = self.treasure[0]
        self.floor[c] = (0, self.create_random_tile_surface('floor'))
        self.treasure = (c, (-1, None))
            

            





            

            

