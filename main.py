import pygame as pg

pg.init()

pg.mixer.music.load('resources/midi/01 Title Screen.mid')

pg.mixer.music.play(500)

while pg.mixer.music.get_busy():
    pg.time.wait(100)