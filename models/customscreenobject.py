import pygame as pg
import io

from pygame import Surface
from models.customobject import CustomObject
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH

# общий предок для всех игровых экранов
# реализует загрузку и отрисовку фоновых изображений и музыки
class CustomScreenObject(CustomObject):
    def __init__(self, state):
        super().__init__(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.state = state
        # инициализация параметров изображений
        self.image_timeout = pg.time.get_ticks() - 1
        self.image_num = 0
        self.image_surface = None
        # bybwbfkbpfwbz gfgfvtnhjd vepsrb
        self.music_num = 0
        self.music_timeout = pg.time.get_ticks() - 1
        self.music = None

    # создание фонового изображения
    def create_surface(self) -> Surface:
        images = self.state.resources.image
        if images:
            # достаем текущую картинку из ресурсов
            # и загружаем ее как поверхность pygame
            img_order = f'N{self.image_num:03}'
            surface = pg.transform.scale(pg.image.load(io.BytesIO(images[img_order].resource)).convert(), (self.right, self.bottom))
        else:    
            color = (128, 0, 0)
            surface = pg.Surface((self.right, self.bottom), pg.SRCALPHA)        
            surface.fill(color)

        return surface
    
    # создание текущей музыкальной темы
    def create_music(self) -> Surface:
        sound = None
        music = self.state.resources.midi
        if music:
            # достаем текущую композицию из ресурсов
            # и загружаем ее
            m_order = f'N{self.music_num:03}'
            sound = pg.mixer.music.load(io.BytesIO(music[m_order].resource))

        return sound

    def get_image(self) -> Surface:
        return self.image_surface
    
    # метод отрисовки экрана, который вызывается на каждом тике часов
    def draw(self, surface:Surface):
        surface.blit(self.get_image(), (self.left, self.top))

    # метод обновления состояния экрана, который вызывается на каждом тике часов
    # здесь происходит смена изображения и муз. композиции по таймаутам, прописанным в ресурсах
    def update_state(self):
        images = self.state.resources.image
        if images:
            if pg.time.get_ticks() > self.image_timeout:
                img_order = f'N{self.image_num + 1:03}'
                ii = images[img_order]
                if ii:
                    self.image_num += 1
                else:
                    self.image_num = 1
                    img_order = f'N{self.image_num :03}'

                self.image_timeout = pg.time.get_ticks() + images[img_order].duration
                self.image_surface = self.create_surface()
            
        music = self.state.resources.midi
        if music:
            if pg.time.get_ticks() > self.music_timeout:
                m_order = f'N{self.music_num + 1:03}'
                mm = music[m_order]
                if mm:
                    self.music_num += 1
                else:
                    self.music_num = 1
                    m_order = f'N{self.music_num:03}'

                self.music_timeout = pg.time.get_ticks() + music[m_order].duration
                self.music = self.create_music()
                pg.mixer.music.play(music[m_order].duration)
            
