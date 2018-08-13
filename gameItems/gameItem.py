import pygame
from pygame.locals import *
#from gameobjects_local.vector2 import Vector2
#from gameStages.stageElements import Attack_Effect
from itemActions import *


## CONSTANTS
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

UP_LEFT = "UP_LEFT"
UP_RIGHT = "UP_RIGHT"
DOWN_LEFT = "DOWN_LEFT"
DOWN_RIGHT = "DOWN_RIGHT"


class GameItem(object):
    def __init__(self, name, description, groupable, usable, sprite):
        self.name = name
        self.description = description
        self.groupable = groupable 
        self.usable = usable
        self.sprite = sprite
        self.id = 0
        self.icon = sprite[0][0]
        #self.rect = sprite.get_rect()
    
    def select(self):
        """ 'Seleciona' o item mostrando as possiveis 
        acoes que podem ser realizadas com ele """
        pass
    
    def use(self):
        pass
    
    def render(self, surface):
        surface.blit(self.sprite)


class Item(GameItem):
    def __init__(self, cfg, sprite):
        GameItem.__init__(self, cfg.name, cfg.description, True, True, sprite)
        self.parameter = int(cfg.parameter)
        self.function = cfg.function
        self.cfg_id = cfg.id
    
    def use(self, entity):
        if self.function == "heal":
            heal(entity, self.parameter)
        if self.function == "energyup":
            energyup(entity, self.parameter)
       


class Etc(GameItem):
    def __init__(self, name):
        GameItem.__init__(self, name, True, False)


# class BasicAtack(object):
#     def __init__(self, name, damage, type, sprite):
#         self.name = name
#         self.damage = damage
#         self.type = type
#         self.sprite = sprite



class Equip(GameItem):
    def __init__(self, cfg, sprite):
        GameItem.__init__(self, cfg.name, cfg.description, False, True, sprite)
        self.name = cfg.name
        self.cfg_id = cfg.id
        self.hp = 0
        self.mana = 0
        self.ad = int(cfg.ad)
        self.ap = int(cfg.ap) 
        self.armor = int(cfg.armor)
        self.mdef = float(cfg.mdef)
        self.movspeed = float(cfg.movspeed)
        self.aspd = float(cfg.aspd)
        #self.type = cfg.type
        self.sprite = sprite
    
    def get_status(self):
        return self.name, self.armor, self.mdef, self.movspeed, self.aspd, self.sprite



class Weapon(Equip):
    def __init__(self, cfg, sprite):
        Equip.__init__(self, cfg, sprite)
        self.name = cfg.name
        self.ad = int(cfg.ad)
        self.aspd = float(cfg.aspd)
        self.bullet_speed = float(cfg.bullet_speed)
        self.movspeed = float(cfg.movspeed)
        self.energycost = cfg.energycost
        self.sprite = sprite
        self.sound = pygame.mixer.Sound(cfg.sound)
        self.sound.set_volume(0.1)
        self.s_range = cfg.s_range
        self.e_range = cfg.e_range
        self.total_range = cfg.s_range + cfg.e_range
    
    def use(self):
        pass
    
    def range_effect(self):
        pass
    
    def render(self):
        pass
    
    def stero_pan(self, x_coord, screen_width):
    
        right_volume = float(x_coord) / screen_width
        left_volume = 1.0 - right_volume
        
        return (left_volume, right_volume)
    
    def play_soundeffect(self):
        channel = self.sound.play()
        width, height = self.surface.get_size()
        if channel is not None:
            # Get the left and right volumes
            left, right = self.stero_pan(self.position.x, width)
            channel.set_volume(left, right)
    
class NoWeapon(Weapon):
    def __init__(self, cfg, sprite):
        
        Weapon.__init__(self, cfg, sprite)
        self.type = "noweapon"
    
    def use(self, position, direction):
        #self.sound.play()
        return (position + direction * self.range), (position + direction * self.range), self.energycost, self.sound



class SimpleWeapon(Weapon):
    def __init__(self, cfg, sprite):
        
        Weapon.__init__(self, cfg, sprite)
        self.type = "racket"
    
    def use(self, position, direction):
        #self.sound.play()
        return (position + direction * self.s_range), (position  + direction * self.s_range * self.e_range ), self.energycost, self.sound
    

class RacketOn(Weapon):
    def __init__(self, cfg, sprite):
        
        Weapon.__init__(self, cfg, sprite)
        self.type = "racket"
    
    def use(self, position, direction):
        #self.sound.play()
        return (position + direction * self.range), 2*(position + direction * self.range), self.sound
    

class Chest(Equip):
    def __init__(self, cfg, sprite):
        Equip.__init__(self, cfg, sprite)
    
    def render(self, surface):
        pass
        

class Helmet(Equip):
    def __init__(self, cfg, sprite):
        Equip.__init__(self, cfg, sprite)

class Boots(Equip):
    def __init__(self, cfg, sprite):
        Equip.__init__(self, cfg, sprite)

class Bottom(Equip):
    def __init__(self, cfg, sprite):
        Equip.__init__(self, cfg, sprite)

