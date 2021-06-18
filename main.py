import pygame as pg
from pygame.draw import line
from pygame.locals import *
from pygame.sprite import Sprite
from settings import *
from sprites import *
from inventory import *
from tilemap import *
import sys,os, random

class Game():
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.DISPLAY = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.load_data()
        self.running = True
        self.paused = False
        self.on_inventory= False

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.players = pg.sprite.Group()
#        for row, tiles in enumerate(self.map.data):
#            for col, tile in enumerate(tiles):
#                if tile == '1':
#                    Wall(self, col, row)
#                if tile == 'P':
#                    self.P1 = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'P1':
                self.P1 = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self,tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name =='NPCw':
                cooldown_npc = random.randint(35,100)
                Wandering_NPC(self, tile_object.x, tile_object.y, cooldown_npc)
            if tile_object.name =='NPCdireita':
                Standing_NPC(self, tile_object.x, tile_object.y, 'direita')
            if tile_object.name =='NPCesquerda':
                Standing_NPC(self, tile_object.x, tile_object.y, 'esquerda')
            if tile_object.name =='NPCfrente':
                Standing_NPC(self, tile_object.x, tile_object.y, 'frente')
            if tile_object.name =='NPCtras':
                Standing_NPC(self, tile_object.x, tile_object.y, 'tras')
        self.camera = Camera(self.map.width, self.map.height)
        self.run()
        
    def load_data(self):
        map_folder = os.path.join(game_folder, 'maps')
        self.map = TiledMap(os.path.join(map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.paused == False:
                self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.P1)

    def events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_TAB:
                    self.paused = not self.paused
                    self.on_inventory = not self.on_inventory

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.DISPLAY, BLACK, (x,0), (x,HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.DISPLAY, BLACK, (0,y), (WIDTH, y))

    def draw(self):
        self.DISPLAY.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.DISPLAY.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

jogo = Game()

while jogo.running:
    jogo.new()
    jogo.show_go_screen()

pg.quit()
sys.exit()