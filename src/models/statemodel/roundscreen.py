import pygame as pg
from models.statemodel.gamestate import GameState

from models.roundobject import RoundObject
from utils.characterstate import CharacterState
from utils.types import BrickAction, ExitAction, MonsterAction, TreasureAction

class RoundScreen(GameState):
    def __init__(self, game, model):
        self.data = None
        super().__init__(game, model, 'RoundScreen')

    def create_objects(self):
        self.roundobject = RoundObject(self.game, self)
        self.objects.append(self.roundobject)

    def create_handlers(self):
        self.keydown_handlers[pg.K_ESCAPE].append(self.roundobject.handle_keydown)
        self.keydown_handlers[pg.K_p].append(self.roundobject.handle_keydown)
        self.keydown_handlers[pg.K_SPACE].append(self.roundobject.handle_keydown)
        self.keydown_handlers[pg.K_RETURN].append(self.roundobject.handle_keydown)
        self.exit_handlers[ExitAction.SHOW].append(self.roundobject.handle_exit_show)
        self.exit_handlers[ExitAction.ACTIVE].append(self.roundobject.handle_exit_active)
        self.exit_handlers[ExitAction.OPEN].append(self.roundobject.handle_exit_open)
        self.exit_handlers[ExitAction.REPLAY].append(self.roundobject.handle_exit_replay)
        self.monster_handlers[MonsterAction.CREATE_EXTRA].append(self.roundobject.handle_create_extra_monsters)
        self.treasure_handlers[TreasureAction.SHOW].append(self.roundobject.handle_show_treasure)
        self.treasure_handlers[TreasureAction.OPEN].append(self.roundobject.handle_open_treasure)
        self.treasure_handlers[TreasureAction.HIDE].append(self.roundobject.handle_hide_treasure)
        self.treasure_handlers[TreasureAction.INACTIVE].append(self.roundobject.handle_inactive_treasure)
        self.brick_handlers[BrickAction.REMOVE].append(self.roundobject.handle_remove_brick)


