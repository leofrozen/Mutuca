    
# -*- coding: UTF-8 -*-


import pygame
import sys
#from gameStages.stageElements import Attack_Effect, InteractiveBox, RepelBox
#from utils.quickGenerator import generateAttackEffect, generateInteractiveBox, generateRepelBox
# import utils.quickGenerator
from gameStages.stageElements import ElementBuilder
from gameconfig.configLoader import load_sprite_mainsheet


class InputAction(object):
    
    def __init__(self):
        
        self.actions = {}
        self.action_id = 1
        self.active_state = None
    
    def add_action(self, action, pos = 0):
        if pos == 0:
            self.actions[self.action_id] = action
            self.action_id += 1
        elif pos >= 0 and pos <= 5:
            self.actions[pos] = action
        else:
            print "This action position is over the limit. How many buttons has your Joystick?"
    
    
    def act(self, action_id, time_passed):
#         if self.actions[action_id]:
#             self.actions[action_id].process(time_passed)
        try:
            if self.actions[action_id]:
                self.actions[action_id].process(time_passed)
#         except KeyError:
#             print "action not found"
        except: 
            
            for i in sys.exc_info():
                print "Error detail: %s" %i
            
#             e, en, em = sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
#             print "erro inesperado"
#             print "Unexpected error: %s  __  %s  ___ %s" %(e, en, em)
#             print "action_id:  %f" %action_id
             
            return

    def update(self, time_passed):
        for action in self.actions.itervalues():
            action.update(time_passed)



class Action(object):
    def __init__(self, delay):
        self.delay = delay
        self.last_use = delay
    
    def update(self, time_passed):
        if self.last_use >= self.delay:
            return
        else:
            self.last_use += time_passed
    
    def process(self):
        pass

class BasicAttack(Action):
    def __init__(self, entity, delay):
        Action.__init__(self, delay)
        self.entity = entity

    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        self.entity.acting = "attack"
        #self.entity.last_attack = 0
        

        beg, end, cost, sound = self.entity.equip_set.weapon.use(self.entity.rect.center, self.entity.last_direction)
        if cost > self.entity.mana:
            self.entity.to_talk(10, [u"Não tenho energia suficiente!!"])
            return
        else:
            self.entity.mana -= cost
    #                                                             stage, ent_name, sprite1, position, destination, aspd, atq_damage = 0, magic_damage = 0, sound = None
            attack_effect = ElementBuilder(type = "AttackEffect", stage = self.entity.stage, ent_name = self.entity.name, sprite = self.entity.equip_set.weapon.sprite, position = beg, destination = end, movspeed = self.entity.equip_set.weapon.bullet_speed, atq_damage = self.entity.ad, magic_damage = 0, cost = cost, sound = sound, direction = self.entity.last_direction)
            #attack_effect = Attack_Effect(self.entity.stage, self.entity.name, self.entity.equip_set.weapon.sprite, beg, end, self.entity.equip_set.weapon.aspd, self.entity.ad, self.entity.ap, sound)
                    
            self.entity.stage.add_element(attack_effect)


class SecondaryAttack(Action):
    def __init__(self, entity, delay):
        Action.__init__(self, delay)
        self.entity = entity

    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        self.entity.acting = "attack"
        #self.entity.last_attack = 0
        

        beg, end, cost, sound = self.entity.equip_set.second_weapon.use(self.entity.rect.center, self.entity.last_direction)
        if cost > self.entity.mana:
            self.entity.to_talk(10, [u"Não tenho energia suficiente!!"])
            return
        else:
            self.entity.mana -= cost
    #                                                             stage, ent_name, sprite1, position, destination, aspd, atq_damage = 0, magic_damage = 0, sound = None
            attack_effect = ElementBuilder(type = "AttackEffect", stage = self.entity.stage, ent_name = self.entity.name, sprite = self.entity.equip_set.second_weapon.sprite, position = beg, destination = end, movspeed = self.entity.equip_set.second_weapon.bullet_speed, atq_damage = 0, magic_damage = self.entity.ap, cost = cost, sound = sound, direction = self.entity.last_direction * 0)
            #attack_effect = Attack_Effect(self.entity.stage, self.entity.name, self.entity.equip_set.weapon.sprite, beg, end, self.entity.equip_set.weapon.aspd, self.entity.ad, self.entity.ap, sound)
                    
            self.entity.stage.add_element(attack_effect)


class ActiveItem(Action):
    def __init__(self, entity, delay):
        Action.__init__(self, delay)
        self.entity = entity

    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        self.entity.acting = "attack"
        #self.entity.last_attack = 0
        
        if self.entity.equip_set.special_item:
            beg, end, cost, sound = self.entity.equip_set.special_item.use(self.entity.rect.center, self.entity.last_direction)
            if cost > self.entity.mana:
                self.entity.to_talk(10, [u"Não tenho energia suficiente!!"])
                return
            else:
                self.entity.mana -= cost
        #                                                             stage, ent_name, sprite1, position, destination, aspd, atq_damage = 0, magic_damage = 0, sound = None
                attack_effect = ElementBuilder(type = "ItemAction", stage = self.entity.stage, ent_name = self.entity.name, sprite = self.entity.equip_set.special_item.sprite, position = beg, destination = end, movspeed = self.entity.equip_set.special_item.bullet_speed, atq_damage = 0, magic_damage = self.entity.ap, cost = cost, sound = sound, direction = self.entity.last_direction * 0)
                #attack_effect = Attack_Effect(self.entity.stage, self.entity.name, self.entity.equip_set.weapon.sprite, beg, end, self.entity.equip_set.weapon.aspd, self.entity.ad, self.entity.ap, sound)
                        
                self.entity.stage.add_element(attack_effect)
        else:
            self.entity.to_talk(10, [u"Não possuo itens especiais!!"])
            return



class DashForward(Action):
    def __init__(self, entity, delay):
        Action.__init__(self, delay)
        self.entity = entity
    
    
    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        self.entity.rect.center += self.entity.last_direction * time_passed * self.entity.speed*10
        


class DashBackward(Action):
    def __init__(self, entity, delay):
        Action.__init__(self, delay)
        self.entity = entity
    
    
    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        self.entity.rect.center -= self.entity.last_direction * time_passed * self.entity.speed*10


class Interact(Action):
    def __init__(self, entity, delay = 1.):
        Action.__init__(self, delay)
        self.entity = entity
        self.sprite = load_sprite_mainsheet("effinteract01")

    
    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        self.entity.acting = "interact"
        interact_rect = pygame.Rect((0,0), (20,20))
        interact_rect.center = (self.entity.rect.center) + (self.entity.last_direction * 28)
        interactive_box = ElementBuilder(type = "InteractiveBox", entity = self.entity, sprite = self.sprite, rect = interact_rect)
        self.entity.stage.add_element(interactive_box)

class Docking_01(Action):
    def __init__(self, entity, delay = 1.):
        Action.__init__(self, delay)
        self.entity = entity

    
    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        #self.entity.acting = "docking_01"
        self.entity.inventory.quick_use(u"Poção de Cura")

class Docking_02(Action):
    def __init__(self, entity, delay = 1.):
        Action.__init__(self, delay)
        self.entity = entity

    
    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        #self.entity.acting = "docking_02"
        self.entity.inventory.quick_use(u"Bateria")


class Repel(Action):
    def __init__(self, entity):
        Action.__init__(self, 1.)
        self.entity = entity

    
    def process(self, time_passed):
        if self.last_use < self.delay:
            return
        self.last_use = 0
        repel_rect = pygame.Rect((0,0), (25,25))
        repel_rect.center = (self.entity.rect.center) + (self.entity.last_direction * 15)
        repel_box = ElementBuilder(type = "RepelBox", stage = self.entity.stage, rect = repel_rect, speed = self.entity.speed, direction = self.entity.last_direction)
        self.entity.stage.add_element(repel_box)


