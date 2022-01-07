import pygame as pg
from models.statemodel.gamestate import GameState

from models.roundobject import RoundObject
from utils.characterstate import CharacterState
from utils.types import ExitAction, MonsterAction

class RoundScreen(GameState):
    def __init__(self, game, model):
        self.data = None
        super().__init__(game, model, 'RoundScreen')

    def handle_on_enter(self, eventdata):
        self.init_objects()
        self.init_handlers()

        self.create_objects()
        self.create_handlers()

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


