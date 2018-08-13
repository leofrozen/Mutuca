    
# -*- coding: UTF-8 -*-

#This class loads all config files and tests some issue before the game begins.


import json
import pygame

#from gameEntities.gameEntity import *
from gameItems.gameItem import *
import gameItems.itemSets
from gameStages.stage import *
#from gameStages.stageElements import *
from gameStages.stageScript import *

from pygame.locals import *
from sys import exit
from gameconfig.configLoader import getStage, getItem, getPlayer, getEnemy, getNPC, getEntity, load_sprite_mainsheet, getPortal, getWeapon, getEquip
from utils.quickGenerator import Generator
from gameconfig import configLoader
#from cgitb import text



# CONSTANTS

## CONSTANTS
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

UP_LEFT = "UP_LEFT"
UP_RIGHT = "UP_RIGHT"
DOWN_LEFT = "DOWN_LEFT"
DOWN_RIGHT = "DOWN_RIGHT"

# Define as cores
BRIGHT_RED = (255, 0, 0)
RED = (200, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
GREEN = (0, 200, 0)
BRIGHT_BLUE = (0, 0, 255)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (247, 41, 234)
YELLOW = (230, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY  = (100,100,100)
ORANGE = (250, 230, 0)


#
clock = pygame.time.Clock()

def quit_game():
    pygame.quit()
    quit()

def unpause():
    global paused
    paused = False
    pygame.mixer.music.unpause()


def button(msg,x,y,w,h,ic,ac, surface, action = None):
    global intro
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
#     if x+w > mouse[0] > x and y+h > mouse[1] > y:
#         pygame.draw.rect(screen, ac,(x,y,w,h))
#     else:
#         pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    
    if textRect.collidepoint(mouse):
        pygame.draw.rect(surface, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(surface, ic,(x,y,w,h))
    surface.blit(textSurf, textRect)



#bg = pygame.transform.scale(bg, SCREEN_SIZE)
paused = False


def read_mission(surface, bg, mission):
    global paused
    paused = True
    pygame.mixer.music.pause()
    
    bg_rect = bg.get_rect()
    
    smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    height = 1
    for txt in mission:
        TextSurf, TextRect = text_objects(txt, smallText)
        TextRect.center = (bg_rect.centerx, bg_rect.y + 20 * height)
        bg.blit(TextSurf, TextRect)
        height += 1
    bg_rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        #screen.fill(GRAY)
        surface.fill((150,250,250))
        surface.blit(bg, bg_rect)
        button("Continue!!", 100, SCREEN_SIZE[1]-100, 100, 50, GREEN, BRIGHT_GREEN, surface, unpause)
        
        
        
        pygame.display.update()
    clock.tick(60)
        


######################################################################################

def text_objects(text, font):
    textSurface = font.render(u'%s' %text, True, BLACK)
    return textSurface, textSurface.get_rect()

######################################################################################
clean_zone = pygame.image.load("multimedia/windows/clean_zone.png")
clean_game = pygame.image.load("multimedia/windows/clean_game.png")
mutuca_icon = pygame.image.load("multimedia/windows/mutuca_icon.png")
############
class Game(object):
    def __init__(self):
        self.name = "First of All"
        self.stage = None
        self.player = None
        self.generator = Generator()
        self.status_bg = pygame.image.load("multimedia/windows/pq.png").convert_alpha()
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.smallText.set_bold(True)
        self.evarageText = pygame.font.Font("multimedia/fonts/comic.ttf", 14)
        self.evarageText.set_bold(True)
        self.largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
        self.message = None
        self.saved_state = None
        self.cleared_maps = []
        
        self.mutuca_score = 0
        self.focos_score = 0
        self.coins_score = 0
        self.actual_score = 0
        self.max_mutucas = int(configLoader.load_records()["maxmutucas"])
        self.max_focos = int(configLoader.load_records()["maxfocos"])
        self.max_coins = int(configLoader.load_records()["maxcoins"])
        self.max_score = int(configLoader.load_records()["maxscore"])
        
#     def print_StageName(self, text):
#         font = pygame.font.SysFont("Arial", 15)
#         text_surface = font.render(text, True, (0, 60, 100), (240, 240, 240 ))
#         
#         dialog_box = TextBox(self.stage, self.name, text_surface, self.rect.center)
#         self.stage.add_element(dialog_box)
#         
#         return text_surface
    
    def set_Stage(self, stage_id, **kwargs):
        
        # Get the stage config and start it
        cfgstage =  getStage(stage_id)
        self.stage = Stage(cfgstage)
        
        
        # Gets the entities configs and adds then to the stage
        try:
            
            for entity_stage in cfgstage.enemies:
                redpotion = self.generator.generateItem("item01")
                yellowpotion = self.generator.generateItem("item02")
                entity_id = entity_stage[0]
                entity_spot = (entity_stage[1],entity_stage[2])
                entity = self.generator.generateEnemy(self.stage, entity_spot, entity_id)
                entity.calc_status()
                entity.inventory.add_gameItem(redpotion)
                entity.inventory.add_gameItem(yellowpotion)
                entity.brain.set_state("exploring")
                self.stage.add_entity(entity)
                
            for entity_stage in cfgstage.npcs:
                entity_id = entity_stage[0]
                entity_spot = (entity_stage[1],entity_stage[2])
                entity = self.generator.generateNPC(self.stage, entity_spot, entity_id, "weapon01")
                #entity.inventory.add_gameItem(redpotion)
                entity.calc_status()
                entity.brain.set_state("roaming")
                self.stage.add_entity(entity)
                
                #
                #
                #   ADD HERE THE OTHERS TYPE OF ENTITIES
                #
                #
        except IOError:
            print("Unknown erro! Failed to load entities")
        
        # Gets the elements configs and adds then to the stage
#         try:
#             for element_id in cfgstage.portals:
#                 element = self.generator.generatePortal(self.stage, element_id)
#                 self.stage.add_element(element)
#                 #
#                 #
#                 #   ADD HERE THE OTHERS TYPE OF ELEMENTS
#                 #
#                 #
#         except IOError:
#             print("Unknown erro! Failed to load elements")


        stgscript = get_script(cfgstage.scriptID)
        script = stgscript(self.stage)
        self.stage.script = script
        if self.cleared_maps.count(stage_id):
            self.stage.script.clear = True
            #self.stage.script.clean_the_map()
        
        self.stage.script.start()
        
        
        if not self.stage.script.clear:
            self.message = [u'MISSÃO:'] + self.stage.script.message
        
        

    
        
            
    def read_message(self):
        msg = self.message
        self.message = None
        return msg
    
    def render_inventory(self, surface, mouse_pos):
        return self.player.inventory.render(surface, mouse_pos)
    
    def process_inventory(self, mouse):
        self.player.inventory.process(mouse)
    
    def show_hotkeys(self, surface):
        empty_slot = load_sprite_mainsheet("other01")
        icon_01 = load_sprite_mainsheet("icon04")[0][0]
        icon_02 = load_sprite_mainsheet("icon05")[0][0]
        icon_03 = load_sprite_mainsheet("icon06")[0][0]
        icon_04 = load_sprite_mainsheet("icon07")[0][0]
        
        icons = [icon_01, icon_02, icon_03, icon_04]
        
        
        discrip_01, discrip_01_rect = text_objects(u"'Q' - Ataque Básico!", self.smallText)
        discrip_02, discrip_02_rect = text_objects(u"'W' - Ataque Elétrico.", self.smallText)
        discrip_03, discrip_03_rect = text_objects(u"'E' - Interação", self.smallText)
        discrip_04, discrip_04_rect = text_objects(u"'R' - Upgrade Especial", self.smallText)
        discription = [(discrip_01, discrip_01_rect),(discrip_02, discrip_02_rect),(discrip_03, discrip_03_rect),(discrip_04, discrip_04_rect)]
        
        
        
        actions = []
#         atq_1 = empty_slot.copy()
#         atq_1_rect = atq_1.get_rect()
#         
#         atq_2 = empty_slot.copy()
#         atq_2_rect = atq_2.get_rect()
#         
#         inter = empty_slot.copy()
#         inter_rect = inter.get_rect()
#         
#         item  = empty_slot.copy() 
#         item_rect = item.get_rect()
#         
        
        pos = 1
        for i in range(4):
            
            surf = empty_slot[0][0].copy()
            surf_rect = surf.get_rect()
            surf_rect.center = (surface.get_width()/6, surface.get_height()/5 * pos)
            icon_rect = icons[i].get_rect()
            icon_rect.center = (surf.get_width()/2, surf.get_height()/2) 
            surf.blit(icons[i], icon_rect)
            actions.append((surf, surf_rect))
            
            discription[i][1].left = surf_rect.right + 10
            discription[i][1].centery = surf_rect.centery
            surface.blit(discription[i][0],discription[i][1])
            
            
            pos += 1
            surface.blit(surf, surf_rect)
        
        
        caption, caption_rect = text_objects("Comandos:", self.largeText)
        caption_rect.centerx = surface.get_width()/2
        caption_rect.top = 10
        surface.blit(caption, caption_rect)
#         actions[0][0].blit(icon_01)
#         actions[1][0].blit(icon_02)
#         actions[2][0].blit(icon_03)
            
    
    def add_Entity(self, *args):
        
        entity = self.generator.generateEnemy(*args)
        entity.calc_status()
        if self.stage.hascollision_ent(entity.rect):
#             print "houve colisao, tentando de novo"
            entity.rect.center = (entity.rect.centerx + randint(-32,32),entity.rect.centery + randint(-32,32))
            collide_list = self.stage.hascollision_ent(entity.rect)
            if collide_list :
                if entity.type == "boss":
                    for i in collide_list:
                        if i.type == "enemy":
#                             print "removendo %s entidades para adicionar o boss" %i
                            self.stage.remove_entity(i)
                else:
#                     print "cancelando adicao de: %s" %entity.type
#                     print "muitas entidades proximas, nao adicionar agora."
                    return
        
        self.stage.add_entity(entity)
#         if entity.type == "boss":
#             print"adicionado %s" %entity.type
     
    def load_Player(self, **kwargs):
        if kwargs:
            
            #self.player = None
            self.player = self.generator.generatePlayer(self.stage, "ent01", "weapon01", "weapon03")
            self.player.inventory = kwargs["inventory"]
            self.player.inventory.entity = self.player
            self.player.equip_set = kwargs["equip_set"]
            self.player.life = kwargs["life"]
            self.player.mana = kwargs["mana"]
            self.player.rect.center = kwargs["position"]
            self.player.calc_status()
            self.stage.add_entity(self.player)

        
        else:
            # Get the stage config and start it
            if self.player == None:
                self.player = self.generator.generatePlayer(self.stage, "ent01", "weapon01", "weapon03")
                self.player.calc_status()
                
                redpotion = self.generator.generateItem("item01")
                batery = self.generator.generateItem("item02")
                self.player.inventory.add_gameItem(redpotion)
                self.player.inventory.add_gameItem(batery)
                
                self.stage.add_entity(self.player)
            else:
                self.player.set_stage(self.stage)
                self.stage.add_entity(self.player)
            
        #if self.saved_state == None:
        self.save_point(self.stage.config.id, self.player.inventory, self.player.equip_set, self.player.life, self.player.mana, self.player.rect.center)
        
         
         
#         if entity:
#             return entity
#         return None
#     
#     
#     
#     def add_Elements(self, element_id):
#         cfgportal = getPortal(element_id)
#         sprite = load_sprite_mainsheet(cfgportal.sprite)
#         element = Portal(self.stage, sprite, cfgportal)
#         self.stage.add_element(element)
#         pass
#     
    
    def changeStage(self, stage_id, position):
        self.set_Stage(stage_id)
        self.load_Player()
        self.player.set_position(position)
        # mesmo sendo repetitivo, precios salvar a ultima posicao correta do Player
        self.save_point(stage_id, self.player.inventory, self.player.equip_set, self.player.life, self.player.mana, self.player.rect.center)
    
    def apply_affect_area(self, position, sprite):
        pass
        #self.stage.add_element(sprite)
        
    
    def render_dock_status_bar(self, surf):
        
        life_rect = pygame.Rect((0,0), (surf.get_width()/2, surf.get_height()/10))
        life_rect.center = (surf.get_width()/2 + 10, (surf.get_height()/8) *6 )
        
        green_bar = int((self.player.life * life_rect.width)/self.player.max_life) 
        green_rect = pygame.Rect((0,0),(green_bar,life_rect.height))
        green_rect.topleft = life_rect.topleft
        
        pygame.draw.rect(surf, RED, life_rect)
        pygame.draw.rect(surf, GREEN, green_rect)
        
        life_label = self.smallText.render("Vida:", True, WHITE)
        labelRect = life_label.get_rect()
        labelRect.center = (life_rect.x + 20, life_rect.centery,)
        
        life_status = self.smallText.render(str(int(self.player.life)) + "/" + str(int(self.player.max_life)), True, WHITE)
        statusRect = life_status.get_rect()
        statusRect.center =  (life_rect.centerx + 20,  life_rect.centery)
        
        surf.blit(life_label, labelRect)
        surf.blit(life_status, statusRect)
        
        ### MANA 
        
        mana_rect = pygame.Rect((0,0), (surf.get_width()/2, surf.get_height()/10))
        mana_rect.center = (surf.get_width()/2 + 10, (surf.get_height()/8 )* 7)
        
        blue_bar = int((self.player.mana * life_rect.width)/self.player.max_mana) 
        blue_rect = pygame.Rect((0,0),(blue_bar, mana_rect.height))
        blue_rect.topleft = mana_rect.topleft
        
        pygame.draw.rect(surf, DARK_GRAY, mana_rect)
        pygame.draw.rect(surf, BRIGHT_BLUE, blue_rect)
        
        mana_label = self.smallText.render("Energia:", True, WHITE)
        labelRect = life_label.get_rect()
        labelRect.center = (mana_rect.x + 20, mana_rect.centery)
        
        mana_status = self.smallText.render(str(int(self.player.mana)) + "/" + str(int(self.player.max_mana)), True, WHITE)
        statusRect = mana_status.get_rect()
        statusRect.center =  (mana_rect.centerx + 20,  mana_rect.centery)
        
        surf.blit(mana_label, labelRect)
        surf.blit(mana_status, statusRect)
    
    
    def render_status_bar(self, surf):
        
        caption = self.largeText.render("Status", True, BLACK)
        caption_rect = caption.get_rect()
        caption_rect.center = (surf.get_width()/2, surf.get_height()/10)
        surf.blit(caption, caption_rect)
        
        life_rect = pygame.Rect((0,0), (surf.get_width()/2, surf.get_height()/8))
        life_rect.center = (surf.get_width()/2, surf.get_height()/8*4)
        
        green_bar = int((self.player.life * life_rect.width)/self.player.max_life) 
        green_rect = pygame.Rect((0,0),(green_bar,life_rect.height))
        green_rect.topleft = life_rect.topleft
        
        pygame.draw.rect(surf, RED, life_rect)
        pygame.draw.rect(surf, GREEN, green_rect)
        
        life_label = self.evarageText.render("Vida:", True, BLACK)
        labelRect = life_label.get_rect()
        labelRect.center = (life_rect.centerx, life_rect.y - life_rect.height/2)
        
        life_status = self.evarageText.render(str(int(self.player.life)) + "/" + str(int(self.player.max_life)), True, BLACK)
        statusRect = life_status.get_rect()
        statusRect.center =  (life_rect.center)
        
        surf.blit(life_label, labelRect)
        surf.blit(life_status, statusRect)
        
        ### MANA 
        
        mana_rect = pygame.Rect((0,0), (surf.get_width()/2, surf.get_height()/7))
        mana_rect.center = (surf.get_width()/2, surf.get_height()/8*7)
        
        blue_bar = int((self.player.mana * life_rect.width)/self.player.max_mana) 
        blue_rect = pygame.Rect((0,0),(blue_bar, mana_rect.height))
        blue_rect.topleft = mana_rect.topleft
        
        pygame.draw.rect(surf, DARK_GRAY, mana_rect)
        pygame.draw.rect(surf, BRIGHT_BLUE, blue_rect)
        
        mana_label = self.evarageText.render("Energia:", True, BLACK)
        labelRect = life_label.get_rect()
        labelRect.center = (mana_rect.centerx, mana_rect.y - mana_rect.height/2)
        
        mana_status = self.evarageText.render(str(int(self.player.mana)) + "/" + str(int(self.player.max_mana)), True, BLACK)
        statusRect = mana_status.get_rect()
        statusRect.center =  (mana_rect.center)
        
        surf.blit(mana_label, labelRect)
        surf.blit(mana_status, statusRect)
        
    
    def render_status_tab(self):
        actual_status_bg = self.status_bg.copy()
        i = 1
        
        
        life_label = self.smallText.render("Vida:", True, BLACK)
        labelRect = life_label.get_rect()
        
        life_status = self.evarageText.render(str(int(self.player.life)) + "/" + str(int(self.player.max_life)), True, BLACK)
        actual_status_bg.blit(life_label, (self.status_bg.get_width()/4, labelRect.height*i))
        i += 1
        actual_status_bg.blit(life_status, (self.status_bg.get_width()/4 , labelRect.height*i))
        
        i += 2
        mana_label = self.smallText.render("Energia:", True, BLACK)
        mana_status = self.evarageText.render(str(int(self.player.mana)) + "/" + str(int(self.player.max_mana)), True, BLACK)
        actual_status_bg.blit(mana_label, (self.status_bg.get_width()/4, labelRect.height*i))
        i += 1
        actual_status_bg.blit(mana_status, (self.status_bg.get_width()/4 , labelRect.height*i))
        
        
#         i += 1
#         ad_label = self.smallText.render("AD:", True, BLACK)
#         ad_status = self.smallText.render(str(self.player.ad), True, BLACK)
#         actual_status_bg.blit(ad_label, (self.status_bg.get_width()/9, labelRect.height*i))
#         actual_status_bg.blit(ad_status, (self.status_bg.get_width()/2, labelRect.height*i))
#         i += 1
#         armor_label = self.smallText.render("Armor:", True, BLACK)
#         armor_status = self.smallText.render(str(self.player.armor), True, BLACK)
#         actual_status_bg.blit(armor_label, (self.status_bg.get_width()/9, labelRect.height*i))
#         actual_status_bg.blit(armor_status, (self.status_bg.get_width()/2 , labelRect.height*i))
#         i += 1
#         mdef_label = self.smallText.render("MDef:", True, BLACK)
#         mdef_status = self.smallText.render(str(self.player.mdef), True, BLACK)
#         actual_status_bg.blit(mdef_label, (self.status_bg.get_width()/9, labelRect.height*i))
#         actual_status_bg.blit(mdef_status, (self.status_bg.get_width()/2 , labelRect.height*i)) 
        
        
#         i += 1 
#         highscore_label = self.smallText.render("Pontos:", True, BLACK)
#         highscore_status = self.smallText.render(str(self.stage.mutuca_points + (self.player.life *100)/self.player.max_life), True, BLACK)
#         actual_status_bg.blit(highscore_label, (self.status_bg.get_width()/9, labelRect.height*i))
#         actual_status_bg.blit(highscore_status, (self.status_bg.get_width()/2, labelRect.height*i))
        
        return actual_status_bg
        
    def save_score(self):
        configLoader.save_records(maxmutucas = self.max_mutucas, maxfocos = self.max_focos, maxcoins = self.max_coins, maxscore = self.max_score)
    
    
    def load_score(self):
        mutuca_score = self.evarageText.render(str(self.stage.mutuca_dead + self.mutuca_score), True, BLACK, GRAY)
        focos_score = self.evarageText.render(str(self.stage.focos_taken + self.focos_score), True, BLACK, GRAY)
        coins_score = self.evarageText.render(str(self.coins_score), True, BLACK, GRAY)
        actual_score = self.evarageText.render(str(self.actual_score), True, BLACK, GRAY)
        
        max_mutucas = self.evarageText.render(str(self.max_mutucas), True, BLACK, GRAY)
        max_focos = self.evarageText.render(str(self.max_focos), True, BLACK, GRAY)
        max_coins = self.evarageText.render(str(self.max_coins), True, BLACK, GRAY)
        max_score = self.evarageText.render(str(self.max_score), True, BLACK, GRAY)
        
        return mutuca_score, focos_score, coins_score, max_mutucas, max_focos, max_coins
    
    def clear_score(self):
        self.mutuca_score = 0
        self.focos_score = 0
        self.coins_score = 0
        self.actual_score = 0
        
    
    def calculate_score(self):
        pass
    
    def process(self, time_passed, direction, action_button, screen):   
        self.player.set_direction(direction)
        self.action_Buttons(action_button, direction, time_passed)
        
        triggers = self.stage.process(time_passed)
        if triggers:
            for signal in triggers:
                #action, par1, par2 = signal
                action = signal[0]
                args = signal[1]
                self.read_triggers(action, *args)
        
        p_position = self.player.get_position()
        self.stage.render(screen, p_position)
        
        screen.blit(mutuca_icon, (screen.get_width()/20 * 16,20))
        screen.blit(self.load_score()[0],(screen.get_width()/20 * 17,25))
    
    def read_triggers(self, trigger, *args):
        
        if trigger == "teleporte":
            self.changeStage(*args)
        elif trigger == "respaw":
            self.add_Entity(*args)
        elif trigger == "cleared":
            self.clean_stage(*args)
    
    def clean_stage(self, name, id):
        #print 'limpando mapa %s' %name
        self.cleared_maps.append(id)
        if name.count("Final"):
            self.message = clean_game 
        else:
            self.message = clean_zone
        
        self.mutuca_score += self.stage.mutuca_dead
        self.focos_score += self.stage.focos_taken
        self.stage.mutuca_dead = 0
        self.stage.focos_taken = 0
        
        npcs = self.stage.get_npcs()
        if npcs:
            for e in npcs:
                if e.communicative == True:
                    self.coins_score += 1
        
        if self.mutuca_score > self.max_mutucas:
            self.max_mutucas = self.mutuca_score
        if self.focos_score > self.max_focos:
            self.max_focos = self.focos_score
        if self.coins_score > self.max_coins:
            self.max_coins = self.coins_score
        
        
        self.save_score()
    
    
    def action_Buttons(self, action_button, direction, time_passed):
        if action_button == "action1":
            self.player.act(1, time_passed)
        elif action_button == "action2":
            self.player.act(2, time_passed)
            #self.player.dash_forward(time_passed)
        elif action_button == "action3":
            self.player.act(3, time_passed)
        elif action_button == "action4":
            self.player.act(4, time_passed)
        elif action_button == "action5":
            self.player.act(5, time_passed)
        elif action_button == "action6":
            self.player.act(6, time_passed)
        elif action_button == "action7":
            pass
        
    
    
    def game_over(self, surface):
        if self.player.life < 1:
            self.stage.remove_entity(self.player)
            self.player = None
            return True
        elif self.stage.npc_dead:
            position = self.stage.npc_dead
            self.stage.render(surface, position)
            self.stage.remove_entity(self.player)
            self.player = None
            return True
        else: 
            return False

    
    def save_point(self, stage_id, inventory, equip_set, life, mana, position):
        self.atual_stage = stage_id
        inventory_items = []
        for item in inventory.bag.itervalues():
            inventory_items.append(item.cfg_id)
        new_inventory = gameItems.itemSets.Inventory(self.player)
        for item_id in inventory_items:
            new_inventory.add_gameItem(self.generator.generateItem(item_id))
        
        
        
        new_equip_set = gameItems.itemSets.EquipSet(None, None, None, None, None, None)
        
        
        
        if equip_set.get("helmet") != None:
            new_equip_set.add(self.generator.generateEquip(equip_set.get("helmet").cfg_id))
        if equip_set.get("chest") != None:
            new_equip_set.add(self.generator.generateEquip(equip_set.get("chest").cfg_id))
        if equip_set.get("bottom") != None:
            new_equip_set.add(self.generator.generateEquip(equip_set.get("bottom").cfg_id))
        if equip_set.get("boots") != None:
            new_equip_set.add(self.generator.generateEquip(equip_set.get("boots").cfg_id))
        if equip_set.get("weapon") != None:
            new_equip_set.add(self.generator.generateWeapon(equip_set.get("weapon").cfg_id))
        if equip_set.get("second_weapon") != None:
            new_equip_set.add(self.generator.generateWeapon(equip_set.get("second_weapon").cfg_id))
        if equip_set.get("special_item") != None:
            new_equip_set.add(self.generator.generateWeapon(equip_set.get("special_item").cfg_id))
        
        
        
        self.saved_state = {'inventory' : new_inventory, 'equip_set' : new_equip_set, 'life' : life, 'mana' : mana, 'position' : position }
        
    def load_last_SavePoint(self):
        self.set_Stage(self.atual_stage)
        self.load_Player(**self.saved_state)
    
        
    
# 
# class SavePoint(object):
#     def __init__(self):
#         self.stage
#         self.stage_script
#         self.inventory
#         self.equip_set
#         self.life
#         self.mana
#         self.position
#     
#     def save_state(self):
#         pass
#     
#     def load_stage(self):
#         pass
#     
#     
    
    
    
    

