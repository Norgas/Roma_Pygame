import pygame as pg
from pygame.locals import *
from settings import *
import os, random, sys
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, jogo, x, y):
        self.groups = jogo.all_sprites, jogo.players
        super().__init__(self.groups)
        self.jogo = jogo
        self.image = pg.image.load(os.path.join(img_folder, 'player_frente.png')).convert()
        self.surf = pg.Surface((TILESIZE, TILESIZE))
        self.image.set_colorkey(WHITE)
        self.rect = pg.Rect(0,0, 28,28)
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        self.lastpress = ''

    def get_keys(self):
        self.vel = vec(0,0)
        pressed_keys = pg.key.get_pressed()

        if pressed_keys[K_d]:
            self.vel.x = PLAYERSPEED
            self.lastpress = 'd'
        if pressed_keys[K_a]:
            self.vel.x = -PLAYERSPEED
            self.lastpress = 'a'
        if pressed_keys[K_w]:
            self.vel.y = -PLAYERSPEED
            self.lastpress = 'w'
        if pressed_keys[K_s]:
            self.vel.y = PLAYERSPEED
            self.lastpress = 's'
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def swap_img_position(self):
        if self.lastpress == 'd' or self.lastpress == 'a':
            self.image = pg.image.load(os.path.join(img_folder, 'player_lado.png')).convert()
        if self.lastpress == 'w' or self.lastpress == 's':
            self.image = pg.image.load(os.path.join(img_folder, 'player_frente.png')).convert()

    def wall_collide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.jogo.walls, False)
            if hits:
                if self.vel.x > 0 :
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.jogo.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def npc_collide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.jogo.npcs, False)
            if hits:
                if self.vel.x > 0 :
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.jogo.npcs, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        self.swap_img_position()
        self.image.set_colorkey(WHITE)
        self.pos += self.vel * self.jogo.dt 
        self.rect.x = self.pos.x
        self.wall_collide('x')
        self.npc_collide('x')
        self.rect.y = self.pos.y
        self.wall_collide('y')
        self.npc_collide('y')
        #self.image.fill(RED)

class Wandering_NPC(pg.sprite.Sprite):
    def __init__(self, jogo, x, y, cooldown):
        self.groups = jogo.all_sprites, jogo.npcs
        super().__init__(self.groups)
        self.jogo = jogo
        self.image = pg.image.load(os.path.join(img_folder, 'legionario_frente.png')).convert()
        self.surf = pg.Surface((TILESIZE, TILESIZE))
        self.image.set_colorkey(WHITE)
        self.rect = pg.Rect(0,0, 28,28)
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        self.NPC_clock = cooldown - 1
        self.cooldown = cooldown
        self.starting_cooldown = cooldown

    def wall_collide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.jogo.walls, False)
            if hits:
                if self.vel.x > 0 :
                    self.pos.x = hits[0].rect.left - self.rect.width
                    self.image = pg.image.load(os.path.join(img_folder, 'legionario_esquerda.png')).convert()
                    self.image.set_colorkey(WHITE)
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                    self.image = pg.image.load(os.path.join(img_folder, 'legionario_direita.png')).convert()
                    self.image.set_colorkey(WHITE)
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.jogo.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.image = pg.image.load(os.path.join(img_folder, 'legionario_tras.png')).convert()
                    self.image.set_colorkey(WHITE)
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                    self.image = pg.image.load(os.path.join(img_folder, 'legionario_frente.png')).convert()
                    self.image.set_colorkey(WHITE)
                self.vel.y = 0
                self.rect.y = self.pos.y

    def npc_collide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.jogo.npcs, False)
            if len(hits) >= 2:
                if self.vel.x > 0 :
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.jogo.npcs, False)
            if len(hits) >= 2:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def playercollide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.jogo.players, False)
            if hits:
                if self.vel.x > 0 :
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.jogo.players, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def wander(self):
        self.vel = vec(0,0)
        movement_choices = ['W', 'E', 'N', 'S']
        choice = random.choice(movement_choices)
        if choice == 'W':
            self.vel.x = -NPCSPEED
            self.image = pg.image.load(os.path.join(img_folder, 'legionario_esquerda.png')).convert()
        if choice == 'E':
            self.vel.x = NPCSPEED
            self.image = pg.image.load(os.path.join(img_folder, 'legionario_direita.png')).convert()
        if choice == 'N':
            self.vel.y = -NPCSPEED
            self.image = pg.image.load(os.path.join(img_folder, 'legionario_tras.png')).convert()
        if choice == 'S':
            self.vel.y = NPCSPEED
            self.image = pg.image.load(os.path.join(img_folder, 'legionario_frente.png')).convert()
#        if choice == 'NW':
#            self.vel = vec(-NPCSPEED, -NPCSPEED)
#            self.image = pg.image.load(os.path.join(img_folder, 'NPC_ladoesquerda.png')).convert()
#        if choice == 'NE':
#            self.vel = vec(NPCSPEED, -NPCSPEED)
#            self.image = pg.image.load(os.path.join(img_folder, 'NPC_ladodireita.png')).convert()
#        if choice == 'SW':
#            self.vel = vec(-NPCSPEED, NPCSPEED)
#            self.image = pg.image.load(os.path.join(img_folder, 'NPC_ladoesquerda.png')).convert()
#        if choice == 'SE':
#            self.vel = vec(NPCSPEED, NPCSPEED)
#            self.image = pg.image.load(os.path.join(img_folder, 'NPC_ladodireita.png')).convert()

    def update(self):
        self.NPC_clock += 1
        if self.NPC_clock == self.cooldown:
            self.cooldown += self.starting_cooldown
            self.wander()
        if self.NPC_clock == self.cooldown - 20:
            self.vel = vec(0,0)
        self.image.set_colorkey(WHITE)
        self.pos += self.vel * self.jogo.dt
        self.rect.x = self.pos.x
        self.wall_collide('x')
        self.npc_collide('x')
        self.playercollide('x')
        self.rect.y = self.pos.y
        self.wall_collide('y')
        self.npc_collide('y')
        self.playercollide('y')
        #self.image.fill(RED)

class Standing_NPC(pg.sprite.Sprite):
    def __init__(self, jogo, x, y, facing):
        self.groups = jogo.all_sprites, jogo.npcs
        super().__init__(self.groups)
        self.jogo = jogo
        if facing == 'direita':
            self.image = pg.image.load(os.path.join(img_folder, 'legionario(crista)_direita.png')).convert()
        if facing == 'esquerda':
            self.image = pg.image.load(os.path.join(img_folder, 'legionario(crista)_esquerda.png')).convert()
        if facing == 'frente':
            self.image = pg.image.load(os.path.join(img_folder, 'legionario(crista)_frente.png')).convert()
        if facing == 'tras':
            self.image = pg.image.load(os.path.join(img_folder, 'legionario(crista)_tras.png')).convert()
        self.surf = pg.Surface((TILESIZE, TILESIZE))
        self.image.set_colorkey(WHITE)
        self.rect = pg.Rect(0,0, 28,28)
        self.pos = vec(x,y)

    def update(self):
        self.image.set_colorkey(WHITE)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        #self.image.fill(RED)

class Wall(pg.sprite.Sprite):
    def __init__(self, jogo, x, y):
        self.groups = jogo.all_sprites, jogo.walls
        super().__init__(self.groups)
        self.jogo = jogo
        self.image = pg.image.load(os.path.join(img_folder, 'wooden_wall.png'))
        self.surf = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, jogo, x, y, w, h):
        self.groups = jogo.walls
        super().__init__(self.groups)
        self.jogo = jogo
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y