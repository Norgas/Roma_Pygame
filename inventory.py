import pygame as pg
from settings import *
vec = pg.math.Vector2

class Inventario(pg.sprite.Sprite):
    def __init__(self, jogo):
        self.groups = jogo.all_sprites, jogo.inventario
        super().__init__(self.groups)
        self.jogo = jogo
        self.image = pg.image.load(os.path.join(img_folder, "wooden_wall.png"))
        self.surf = pg.Surface((WIDTH, HEIGHT))
        self.rect = self.surf.get_rect

    def update(self):
        if self.jogo.inventario_on == True:
            self.rect.x = 0
            self.rect.y = 0