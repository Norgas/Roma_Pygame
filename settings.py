import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
map_folder = os.path.join(game_folder, 'maps')

WIDTH = 640
HEIGHT = 640

FPS = 30

WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

TITLE = 'Roma'

PLAYERSPEED = 150
NPCSPEED = 40