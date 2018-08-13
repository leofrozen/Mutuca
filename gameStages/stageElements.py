from gameobjects_local.vector2 import Vector2
#from utils.mixer import CentralMixer
import gameconfig.configLoader
import utils.mixer
import pygame
from random import randint
from gameconfig.configLoader import getSound, getEnemy, load_sprite_mainsheet
import constants
#from utils.quickGenerator import Generator
#from gameEntities.gameEntity import EntityBuilder
#from game import Game
#cm = CentralMixer(44100, -16, 2, 1024*4)



def ElementBuilder(type, **kargs):
    
#     for key in kargs:
#         if key == "name":
#             name = kargs[key]
#         elif key == "stage":
#             stage = kargs[key]
#         elif key == "sprite":
#             sprite = kargs[key]
#         elif key == "position":
#             position = kargs[key]
#         elif key == "config":
#             config = kargs[key]
    
    if type == "Portal":
        return Portal(kargs["stage"], kargs["sprite"], kargs["config"])
    
    elif type == "AttackEffect":
        #stage, ent_name, sprite1, position, destination, aspd, atq_damage = 0, magic_damage = 0, sound = None
        return Attack_Effect(kargs["stage"], kargs["ent_name"], kargs["sprite"], kargs["position"], kargs["destination"], kargs["movspeed"], kargs["atq_damage"], kargs["magic_damage"], kargs["cost"], kargs["sound"], kargs["direction"])
    
    elif type == "ItemAction":
        #stage, ent_name, sprite1, position, destination, aspd, atq_damage = 0, magic_damage = 0, sound = None
        return ItemAction(kargs["stage"], kargs["ent_name"], kargs["sprite"], kargs["position"], kargs["destination"], kargs["movspeed"], kargs["atq_damage"], kargs["magic_damage"], kargs["cost"], kargs["sound"], kargs["direction"])
    
    elif type == "TextBox":
        # stage, entity, sprite, position, texts = ["..."]
        return TextBox(kargs["stage"], kargs["entity"], kargs["sprite"], kargs["position"])
    
    elif type == "InteractiveBox":
        # stage, rect
        return InteractiveBox(kargs["entity"], kargs["sprite"], kargs["rect"])
    
    elif type == "RepelBox":
        # stage, rect, speed, direction
        return RepelBox(kargs["stage"], kargs["rect"], kargs["speed"], kargs["direction"])
    
    elif type == "Foco":
        # self, stage, sprite, position
        return Foco(kargs["stage"], kargs["sprite"], kargs["position"])
    
    elif type == "SuperFoco":
        # self, stage, sprite, position
        return SuperFoco(kargs["stage"], kargs["sprite"], kargs["position"])
    
    elif type == "SpecialItem":
        # self, stage, sprite, position
        return SpecialItem(kargs["stage"], kargs["sprite"], kargs["position"])
    
    elif type == "Explosion":
        # self, stage, sprite, position
        return Explosion(kargs["stage"], kargs["sprite"], kargs["position"])
    
    elif type == "Lapide":
        # self, stage, sprite, position
        return Lapide(kargs["stage"], kargs["sprite"], kargs["position"])
    
    elif type == "DropedBag":
        return DropedBag(kargs["stage"], kargs["sprite"], kargs["position"], kargs["item"])
    
    elif type == "WarningSignal":
        return WarningSignal(kargs["stage"], kargs["sprite"], kargs["position"])




class GameElement(object):
    def __init__(self, stage, sprite, name, position):
        self.name = name
        self.stage = stage
        self.sprite = sprite     # resolver uma forma de nao precisar mais de uma imagem para conseguir as dimensoes
        self.rect = sprite[0][0].get_rect()
        #self.position = Vector2(0, 0)
        self.position = position
        self.destination = Vector2(0, 0)
        self.id = 0
        self.cell_dir = 0
        self.cell_pos = 0
        self.cell_count = 0
        self.sprite_delay = 3
        
        
    def render(self, surface):
#         x, y = self.position
#         
#         w, h = self.image.get_size()
#         surface.blit(self.image,(x - w/2, y - h/2))
        cell = self.sprite[self.cell_dir][self.cell_pos]
        surface.blit(cell, (self.rect.centerx - cell.get_width()/2, self.rect.centery - cell.get_height() + self.rect.height/2 ))

    
    def process(self):
        pass
    
    def update_sprite(self):
        self.cell_count += 1


        if self.cell_count >= self.sprite_delay: # just a timer to delay the refresh
            if self.cell_pos < len(self.sprite[self.cell_dir]) -1:
                self.cell_pos += 1
                self.cell_count = 1
            else:
                self.cell_pos = 0

    



class Portal(GameElement):
    def __init__(self, stage, sprite, cfgportal):
        GameElement.__init__(self, stage, sprite, "portal",  cfgportal.position)
        self.sprite = sprite
        
        self.position = Vector2(cfgportal.position)
        self.destination = Vector2(cfgportal.destination)
        self.dst_stage = cfgportal.dst_stage
        
        self.rect.center = self.position
        self.sprite_delay = 5
    
    def render(self, surface):
        GameElement.render(self, surface)

        
    def process(self, time_passed):
        
        target = self.stage.get_close_entity(self.rect.center, "player")
        if target:
            if self.position.get_distance_to(target.rect.center) < 32.:
                args = (self.dst_stage, self.destination)
                return "teleporte", args
       
        self.update_sprite()
        
    
        
    def change_stage(self):
        pass
    


class LockPass(GameElement):
    def __init__(self, stage, sprite, cfgportal):
        GameElement.__init__(self, stage, sprite, "lock",  cfgportal.position)
        self.sprite = sprite
        
        self.position = Vector2(cfgportal.position)
        self.destination = Vector2(cfgportal.destination)
        self.dst_stage = cfgportal.dst_stage
        
        self.rect.center = self.position
        self.sprite_delay = 5
    
    def render(self, surface):
        GameElement.render(self, surface)

        
    def process(self, time_passed):
        
        target = self.stage.get_close_entity(self.position, "player")
        if target:
            if self.position.get_distance_to(target.rect.center) < 32.:
                return "teleporte", self.dst_stage, self.destination
       
        self.update_sprite()
        
    
        
    def change_stage(self):
        pass



class Attack_Effect(GameElement):
    def __init__(self, stage, ent_name, sprite, position, destination, movspeed, atq_damage = 0, magic_damage = 0, cost = 0, sound = None, direction = (0,0)):
        GameElement.__init__(self, stage, sprite, "effect",  position)
        self.position = Vector2(position)
        self.destination = Vector2(destination)
        self.rect.center = self.position
        self.movspeed = movspeed
        self.sprite = sprite
        #self.sprite2 = sprite2
        self.alive = True
        self.atq_damage = atq_damage
        self.magic_damage = (magic_damage * cost / 10) 
        self.ttl = 5
        self.ent_name = ent_name
        self.sound = sound
        self.direction = direction
        
    
    def render(self, surface):
        GameElement.render(self, surface)

    
        
    def process(self, time_passed):
        if self.alive == False or self.ttl == 0:
            self.stage.remove_element(self)
            return
        
        self.update_position(time_passed)
        hitten = self.stage.hascollision_ent( self.rect) 
        elem_hitten = self.stage.hascollision_elem(self.rect)
        if elem_hitten:
            for e in elem_hitten:                
                #if e.name != self.ent_name and e.type != "npc":
                if isinstance(e, RepelBox):
                    self.explode()
                    print "ataque bloqueado"
                    return
        if hitten:
            for e in hitten:                
                #if e.name != self.ent_name and e.type != "npc":
                if e.name != self.ent_name:
                    e.hitten((self.atq_damage, self.magic_damage))
                    ''' --- KNOCKBACK --- 
                    comente a linha a baixo para remover o knockback dos ataques'''
                    #e.rect.center += self.direction * time_passed * 200
                    if self.ent_name == "player" and e.type == "enemy":
                        e.speed_base -= 20 
                        e.speed -= 30
                    self.explode()
        
        if self.stage.get_close_entity(self.position, "player", 320):
            #CentralMixer.play_effect(self, self.sound)
            utils.mixer.play_effect(self.sound)
            #self.sound.play()
        
        self.ttl -= 1
        
        
    def explode(self):
        #self.sprite = self.sprite2
        self.alive = False
    
    
    def update_position(self, time_passed):
        
        if self.destination != self.position and self.movspeed != 0:
            # Update player position
            vec_to_destination = self.destination - Vector2(self.rect.center)
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.movspeed)
            self.rect.center += travel_distance * heading
            
        self.update_sprite()
    

class ItemAction(GameElement):
    def __init__(self, stage, ent_name, sprite, position, destination, movspeed, atq_damage = 0, magic_damage = 0, cost = 0, sound = None, direction = (0,0)):
        GameElement.__init__(self, stage, sprite, "effect",  position)
        self.position = Vector2(position)
        self.destination = Vector2(destination)
        self.rect.center = self.position
        self.movspeed = movspeed
        self.sprite = sprite
        self.sprite_delay = 6
        #self.sprite2 = sprite2
        self.alive = True
        self.atq_damage = atq_damage
        self.magic_damage = ((magic_damage * cost) / 200) 
        self.ttl = 50
        self.ent_name = ent_name
        self.sound = sound
        self.direction = direction
        
    
    def render(self, surface):
        GameElement.render(self, surface)

    
        
    def process(self, time_passed):
        if self.alive == False or self.ttl == 0:
            self.stage.remove_element(self)
            return
        
        self.update_position(time_passed)
        hitten = self.stage.hascollision_ent( self.rect) 

        if hitten:
            for e in hitten:                
                #if e.name != self.ent_name and e.type != "npc":
                if e.name != self.ent_name:
                    e.hitten((self.atq_damage, self.magic_damage))
                    
                    
        
        if self.stage.get_close_entity(self.position, "player", 320):
            #CentralMixer.play_effect(self, self.sound)
            utils.mixer.play_effect(self.sound)
            #self.sound.play()
        
        self.ttl -= 1
        
        
    def explode(self):
        #self.sprite = self.sprite2
        self.alive = False
    
    
    def update_position(self, time_passed):
        
        if self.destination != self.position and self.movspeed != 0:
            # Update player position
            vec_to_destination = self.destination - Vector2(self.rect.center)
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.movspeed)
            self.rect.center += travel_distance * heading
            
        self.update_sprite()
    





class TextBox(GameElement):
    def __init__(self, stage, entity, sprite, position, texts = ["..."]):
        GameElement.__init__(self, stage, sprite, "text_box",  position)
        self.entity = entity
        self.position = Vector2(position)
        self.rect.center = self.position
        self.rect.centery -= 64
        self.sprite = sprite
        self.alive = True
        
      
        self.ttl = (self.sprite[self.cell_dir][self.cell_pos]).get_width()
        self.ent_name = self.entity.name
        
        
    
    def render(self, surface):
        GameElement.render(self, surface)

    
        
    def process(self, time_passed):
        self.update_position(time_passed)
        if self.alive == False or self.ttl == 0:
            self.stage.remove_element(self)
            return
        
        #self.update_position(time_passed)
        
        self.ttl -= 1
        if self.ttl == 1 and self.cell_pos < len(self.sprite[self.cell_dir])-1:
            self.cell_pos += 1
            self.ttl = (self.sprite[self.cell_dir][self.cell_pos]).get_width()
        
    
    
    def update_text(self, text): 
        pass
        # nao sei deixo o text_box com um vetor de sprites ou um unico sprite por vez
        
    
    def update_position(self, time_passed):
        
        self.rect.center = self.entity.rect.center
        self.rect.centery -= 64
        
        #self.update_sprite()
    

class BroadcastMessage(GameElement):
    def __init__(self, stage, sprite, position, background):
        GameElement.__init__(self, stage, sprite, "text box",  position)
        self.bg = background
        self.rect.center = background.center
        self.alive = True
        self.ttl = (self.sprite[self.cell_dir][self.cell_pos]).get_width()
        
    def render(self, surface):
        bg_copy = self.bg.copy()
        GameElement.render(self, bg_copy)
        

    
        
    def process(self, time_passed):
        self.update_position(time_passed)
        if self.alive == False or self.ttl == 0:
            self.stage.remove_element(self)
            return
        
        self.ttl -= 1
        if self.ttl == 1 and self.cell_pos < len(self.sprite[self.cell_dir])-1:
            self.cell_pos += 1
            self.ttl = (self.sprite[self.cell_dir][self.cell_pos]).get_width()
        
    
    
    
class InteractiveBox(GameElement):
    def __init__(self, entity, sprite, rect):
        GameElement.__init__(self, entity.stage, sprite, "Interactive", rect.center)
        #self.entity = entity
        self.entity = entity
        self.name = "InteractiveBox"
        self.rect = rect
        self.alive = True
        self.ttl = 10
        self.sprite_delay = 2
        
        #self.rect = self.entity.rect + (self.entity.direction * 32)
    
    def render(self, surface):
        GameElement.render(self, surface)
        #pygame.draw.rect(surface, (25,25,25), self.rect)
        
    
    def process(self, time_passed):
        if self.alive == False or self.ttl == 0:
            self.entity.acting = None
            self.stage.remove_element(self)
            return
#         self.ttl -= 1
        if self.cell_pos < len(self.sprite[self.cell_dir]) -1:
            self.update_sprite()
        else:
            self.entity.acting = None
            self.stage.remove_element(self)
            return
        hitten = self.stage.hascollision_ent( self.rect) 
        if hitten:
            for e in hitten:
                
                if e.type == "npc":
                    e.to_talk()
                    self.alive = False
                
#                 elif e.name != self.entity.name:
                elif e.name != "Player":
                    #print "ops, nao programado"
                    self.alive = False
#                     e.hitten(self.atq_damage)
#                     print "%s was hitten" %e.name
            self.alive = False
        element_hitten = self.stage.hascollision_elem( self.rect)
        if element_hitten:
            for e in element_hitten:
                if isinstance(e, Foco) or isinstance(e, SpecialItem):
                    e.touch()
    
    def destroy(self):
        self.alive = False



class RepelBox(GameElement):
    def __init__(self, stage, rect, speed, direction):
        #GameElement.__init__(self, stage, None, "RepelBox", rect.center)
        self.stage = stage
        self.sprite = None
        self.name = "RepelBox"
        self.rect = rect
        self.direction = direction
        self.speed = speed
        self.rect = rect
        self.alive = True
        self.ttl = 5
        #self.rect = self.entity.rect + (self.entity.direction * 32)
    
    def render(self, surface):
        #pygame.draw.rect(surface, (25,25,25), self.rect)
        pass
        
    
    def process(self, time_passed):
        if self.alive == False or self.ttl == 0:
            self.stage.remove_element(self)
            return
        self.ttl -= 1
        entity_hitten = self.stage.hascollision_ent( self.rect)         
        if entity_hitten:
            for e in entity_hitten:
                if e.type == "enemy":
                    "empurra o inimigos"
                    self.alive = False
                    e.rect.center += self.direction * time_passed * self.speed*10
        
        
        
    
    def destroy(self):
        self.alive = False





class DropedBag(GameElement):
    def __init__(self, stage, sprite, position, item):
        GameElement.__init__(self, stage, sprite, item.name, position)
        self.position = Vector2(position)
        self.rect.center = self.position
        #self.sprite = pygame.image.load("multimedia/sprites/dropedbag.png").convert_alpha()
        self.item = item
        self.activetime = 20
        self.alive = True
        self.sound = getSound("misc01")
    
    
    def render(self, surface): 
        #surface.blit(self.sprite, (self.position[0], self.position[1]))
        GameElement.render(self, surface)
    
    
    def process(self, time_passed):
        if self.alive == False:
            self.stage.remove_element(self)
            return
        
        self.activetime -= 1
        target = self.stage.get_close_entity(self.rect.center, "player")
        if target and self.activetime < 0:
            self.ttl = 0
            if self.position.get_distance_to(target.rect.center) < 32.:
                if target.inventory.add_gameItem(self.item):
                    utils.mixer.play_effect(self.sound)
                    self.alive = False
                    #self.stage.remove_element(self)
                    #self.destination = target.rect.center
                    #self.update_position(time_passed)
    
    
    def update_position(self, time_passed):
        
        if self.destination != self.position and self.aspd != 0:
            # Update player position
            vec_to_destination = self.destination - Vector2(self.rect.center)
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.aspd)
            self.rect.center += travel_distance * heading
            #self.direction = heading
            
        self.update_sprite()


class Foco(GameElement):
    def __init__(self, stage, sprite, position):
        GameElement.__init__(self, stage, sprite, "foco_do_mosquito", position)
        self.position = Vector2(position)
        self.rect.center = self.position
        #self.cfgentity_id = entity_id
        self.activetime = 20
        self.alive = True
        self.sound = getSound("misc01")
        if constants.GAMELEVEL == "HARD":
            self.respaw_delay = 5
        else:
            self.respaw_delay = 7
        self.last_respaw = 7
        self.touched = False
        self.drop = None
        
    def render(self, surface): 
        #surface.blit(self.sprite, (self.position[0], self.position[1]))
        GameElement.render(self, surface)
    
    
    def process(self, time_passed):
        if self.alive == False:
            self.stage.remove_element(self)
            return
        
        if self.last_respaw >= self.respaw_delay - 1:
            self.update_sprite()
        
        if self.last_respaw >= self.respaw_delay:
            self.last_respaw = 0
            
            return self.respaw()
        else:
            self.last_respaw += time_passed
    
    def respaw(self):
        if self.stage.how_many_entis() < 20 and self.stage.get_close_entity(self.rect.center, "player", 400):
            args = (self.stage, (self.rect.centerx + randint(-32, 32), self.rect.centery + randint(-32, 32)), "enemymutuca01", "weapon02")
            return "respaw", args
        self.last_respaw = 7
        #print "Mapa lotado de entidades: %s " %self.stage.how_many_entis()
    
    def touch(self):
        self.touched = True
        drop_sprite = load_sprite_mainsheet("icon01")
        if self.drop != None:
            for item in self.drop:
                self.stage.add_element( DropedBag(self.stage, drop_sprite, (self.rect.centerx + randint(-32, 32), self.rect.centery + randint(-32, 32)), item))
        self.alive = False
        self.stage.focos_taken += 1


class SuperFoco(Foco):
    def __init__(self, stage, sprite, position):
        Foco.__init__(self, stage, sprite, position)
        self.position = Vector2(position)
        self.rect.center = self.position
        #self.cfgentity_id = entity_id
        self.activetime = 20
        self.alive = True
        self.sound = getSound("misc01")
        self.respaw_delay = 6
        self.last_respaw = 6
        self.boss_alive = False
    
    
    def render(self, surface): 
        #surface.blit(self.sprite, (self.position[0], self.position[1]))
        GameElement.render(self, surface)
    
    
    def process(self, time_passed):
        return Foco.process(self, time_passed)
    
    def respaw(self):
        ''' Esse metodo deve ser chamado sempre dentro do ciclo do process(), caso contrario nao surtira o efeito de criacao de entidade'''
        args = None
        if self.stage.get_close_entity(self.position, "player", 280) and self.boss_alive == False:
            args = (self.stage, (self.rect.centerx + randint(-32, 32), self.rect.centery + randint(-32, 32)), "enemyaedes02", "weapon05")
            self.boss_alive = True
#             print "Ta saindo da jaula o monstro"
            return "respaw", args
        elif self.stage.how_many_entis() < 20 and self.stage.get_close_entity(self.rect.center, "player", 700):
            args = (self.stage, (self.rect.centerx + randint(-32, 32), self.rect.centery + randint(-32, 32)), "enemymutuca01", "weapon02")
            return "respaw", args
        self.last_respaw = 6
         
    
    def touch(self):
        self.touched = True
        drop_sprite = load_sprite_mainsheet("icon01")
        if self.drop != None:
            for item in self.drop:
                self.stage.add_element( DropedBag(self.stage, drop_sprite, (self.rect.centerx + randint(-32, 32), self.rect.centery + randint(-32, 32)), item))
        if self.boss_alive == False:
            self.last_respaw = 6
            self.touched = True
        elif self.boss_alive == True and self.touched == True:
            self.alive = False
        self.stage.focos_taken += 1



class Explosion(GameElement):
    def __init__(self, stage, sprite, position):
        GameElement.__init__(self, stage, sprite, "explosion01", position)
        self.position = Vector2(position)
        self.rect.center = self.position
    
    def render(self, surface): 
        GameElement.render(self, surface)
        
    def process(self, time_passed):
        
        if self.cell_pos < len(self.sprite[self.cell_dir]) -1:
            self.update_sprite()
        else:
            self.stage.remove_element(self)


class Lapide(GameElement):
    def __init__(self, stage, sprite, position):
        GameElement.__init__(self, stage, sprite, "lapide", position)
        self.position = Vector2(position)
        self.rect.center = self.position
    
    def render(self, surface): 
        #GameElement.render(self, surface)
        surface.blit(self.sprite[0][0], self.rect)
        
    def process(self, time_passed):
        pass
        


class SpecialItem(GameElement):
    def __init__(self, stage, sprite, position):
        GameElement.__init__(self, stage, sprite, "Over Power Item Plus ultra", position)
        self.position = Vector2(position)
        self.rect.center = self.position
        #self.cfgentity_id = entity_id
        self.activetime = 20
        self.alive = True
        self.sound = getSound("misc02")
        self.respaw_delay = 10
        self.last_respaw = 10
        self.touched = False
        self.drop = None
        
    def render(self, surface): 
        #surface.blit(self.sprite, (self.position[0], self.position[1]))
        GameElement.render(self, surface)
    
    
    def process(self, time_passed):
        if self.alive == False:
            self.stage.remove_element(self)
            return
        
        if self.last_respaw >= 3:
            self.update_sprite()
        
        if self.last_respaw >= self.respaw_delay:
            self.last_respaw = 0
            
#             return self.respaw()
        else:
            self.last_respaw += time_passed 
    
    def touch(self):
        self.touched = True
        if self.drop != None:
            utils.mixer.play_effect(self.sound)
            player = self.stage.get_close_entity(self.rect.center, "player", 64)
            if player:
                player.equip_set.special_item = self.drop
                player.to_talk(15, [u'Encontrei um Upgrade Especial!!', u'Pressione R para usar!'])
        self.alive = False
        
        sprite = load_sprite_mainsheet("effexplosion02")
        explosion = ElementBuilder(type = "Explosion", stage = self.stage, sprite = sprite, position = self.rect.center)
        self.stage.add_element(explosion)


class ItemNotification(GameElement):
    def __init__(self, stage, sprite, position):
        GameElement.__init__(self, stage, sprite, "Item Notification", position)
        self.position = Vector2(position)
        self.rect.center = self.position
        #self.cfgentity_id = entity_id
        self.activetime = 20
        self.alive = True
        self.sound = getSound("misc01")
        self.touched = False
        self.drop = None
        
    def render(self, surface): 
        GameElement.render(self, surface)
    
    
    def process(self, time_passed):
        if self.alive == False:
            self.stage.remove_element(self)
            return
        
        if self.last_respaw >= 3:
            self.update_sprite()
        
        if self.last_respaw >= self.respaw_delay:
            self.last_respaw = 0
            
#             return self.respaw()
        else:
            self.last_respaw += time_passed 
    
    def touch(self):
        self.touched = True
        if self.drop != None:
            player = self.stage.get_close_entity(self.rect.center, "player", 64)
            if player:
                player.equip_set.special_item = self.drop
                player.to_talk(15, [u'Encontrei um Upgrade Especial!!', u'Pressione R para usar!'])
        self.alive = False
        
        sprite = load_sprite_mainsheet("effexplosion02")
        explosion = ElementBuilder(type = "Explosion", stage = self.stage, sprite = sprite, position = self.rect.center)
        self.stage.add_element(explosion)


class WarningSignal():
    def __init__(self, stage, sprite, position):
        #GameElement.__init__(self, stage, sprite, "warning01", position)
        self.name = "warning01"
        self.stage = stage
        self.sprite = sprite
        self.rect = sprite.get_rect()
        self.position = Vector2(position)
        self.rect.center = self.position
        self.ttl = 3
    
    def render(self, surface): 
        #GameElement.render(self, surface)
        #surface.blit(self.sprite[0][0], self.rect)
        surface.blit(self.sprite, self.rect)
        
    def process(self, time_passed):
        self.ttl -= 1
        
        if self.ttl <= 0:
            self.stage.remove_element(self)
            
    
class JukeBox(GameElement):
    def __init__(self, stage, sprite, position):
        GameElement.__init__(self, stage, sprite, "JukeBox", position)
        self.position = Vector2(position)
        self.rect.center = self.position
        #self.cfgentity_id = entity_id
        self.activetime = 20
        self.alive = True
        self.sound = getSound("misc02") # arrumar um som de disco de DJ
        self.respaw_delay = 10
        self.last_respaw = 10
        self.touched = False
        self.drop = None
        
    def render(self, surface): 
        #surface.blit(self.sprite, (self.position[0], self.position[1]))
        GameElement.render(self, surface)
    
    
    def process(self, time_passed):
        if self.alive == False:
            self.stage.remove_element(self)
            return
        
        if self.last_respaw >= 3:
            self.update_sprite()
        
        if self.last_respaw >= self.respaw_delay:
            self.last_respaw = 0
            
#             return self.respaw()
        else:
            self.last_respaw += time_passed 
    
    def touch(self):
        self.touched = True
        # os processos de jukebox

    
    
