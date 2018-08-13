    
# -*- coding: UTF-8 -*-


import pygame
from gameconfig.configLoader import getEnemy, load_sprite_mainsheet, getPortal, getWeapon, getEquip
from gameEntities.gameEntity import Enemy
from gameItems.gameItem import *
from gameStages.stageElements import ElementBuilder
from utils.quickGenerator import generateItem, generateWeapon
from random import randint
import utils.mixer 



class StageScript(object):
    def __init__(self, stage, clear = False):
        self.clear = clear
        self.stage = stage
    
    
    def start(self):
        pass
    
    def process(self, time_passed):
        if self.clear:
            return
        
#         if self.last_respaw >= self.respaw_delay:
#             #self.respaw()
#             self.last_respaw = 0
#         else:
#             self.last_respaw += time_passed
        
        if self.is_clear():
            #print "LIMPO!!!"
            self.clear = True
            self.clean_the_map()
            self.reward()
            self.play_cleared_stage_sound()
            return "cleared", (self.stage.name, self.stage.config.id)
    
    def clean_the_map(self):
        #print "MAPA LIMPO - PORTAL ADICIONADO"
        for element_id in self.stage.config.portals:
            cfgportal = getPortal(element_id)
            sprite = load_sprite_mainsheet(cfgportal.sprite)
            element = ElementBuilder(type = "Portal", stage = self.stage, sprite = sprite, config = cfgportal)
            self.stage.add_element(element)
            self.clear = True
    
    def respaw(self):
        for entity in self.enemies:
            cfgentity = getEnemy(entity[0])
            sprite = load_sprite_mainsheet(cfgentity.sprite)
            rect = pygame.Rect(0, 0, int( cfgentity.dimensionx), int(cfgentity.dimensiony) )
            entity = Enemy(self.stage, sprite, rect, cfgentity, (entity[1],entity[2]))
            entity.equip_set.add(self.weapon)
            entity.brain.set_state("exploring")
            self.stage.add_entity(entity)
    
    def is_clear(self):
        if self.stage.is_ent_alive("Enemy"):
            return False
        elif self.stage.is_elem_alive("Foco"):
            return False
        else:
            return True
    
    def reward(self):
        pass
    
    def play_cleared_stage_sound(self):
        sound_clear = pygame.mixer.Sound("multimedia/soundEffects/lvlup.ogg")
        utils.mixer.play_effect(sound_clear)

# def reset_all():
#     stg01_clear = False
#     stg02_clear = False
#     stg03_clear = False
#     stg04_clear = False
#     stg05_clear = False
#     stg06_clear = False
#     stg07_clear = False
#     stg08_clear = False
#     stg09_clear = False
#     stg10_clear = False
# 
# reset_all()

def get_script(id):
    if id == 1:
        return StgScript01
    if id == 2:
        return StgScript02
    if id == 3:
        return StgScript03
    if id == 4:
        return StgScript04
    if id == 5:
        return StgScript05
    if id == 6:
        return StgScript06
    if id == 7:
        return StgScript07
    if id == 8:
        return StgScript08
    if id == 9:
        return StgScript09
    if id == 10:
        return StgScript10
    

class StgScript01(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = [["enemymutuca01", 150, 450],["enemymutuca01", 450, 450],["enemymutuca01", 1050, 450]]
        self.message = [u"Ajude a sua vizinhança!", 
                        u"Não deixe baldes ou garrafas",
                         u"expostas à chuva", 
                         u"e evite a reprodução do mosquito!"]
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite = load_sprite_mainsheet("otherbalde01")
            element_sprite3 = load_sprite_mainsheet("otherprato01")
            element_sprite4 = load_sprite_mainsheet("otherpets01")
            
            focos = []
            
            focos.append(ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1500,350)))
            focos.append(ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (1530 + randint(-100, 100),650 + randint(-100, 100))))
            focos.append(ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite3, position = (1230,770)))
            focos.append(ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (1030 + randint(-100, 100),470 + randint(-100, 100))))
            
            focos[0].drop  = [generateItem("item01"),generateItem("item02")]
            for f in focos:
                self.stage.add_element(f)
            
            self.stage.focos_total = len(focos)
#             element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1500,350))
#             element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (1530 + randint(-100, 100),650 + randint(-100, 100)))
#             element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite3, position = (1230,770))
#             element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (1030 + randint(-100, 100),470 + randint(-100, 100)))
#              
#             
#             element.drop = [generateItem("item01"),generateItem("item02")]
#             
#             
#             self.stage.add_element(element)
#             self.stage.add_element(element2)
#             self.stage.add_element(element3)
#             self.stage.add_element(element4)
    

            


class StgScript02(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = []
        self.message = ["Latas e garrafas de suco", "ou refrigerante podem ajudar", "o mosquito a se reproduzir.",
                        "Acabe com os focos do mosquito!"
                        ]
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite2 = load_sprite_mainsheet("otherbalde02")
            element_sprite4 = load_sprite_mainsheet("otherpets01")
            element_sprite3 = load_sprite_mainsheet("othervaso02")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (1600,755))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (1200 + randint(-100, 100),200 + randint(-100, 100)))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (1350 + randint(-100, 100),225 + randint(-100, 100)))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (1400 + randint(-100, 100),200 + randint(-100, 100)))
            element5 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite3, position = (848,752))
            
            element2.drop = [generateItem("item02")]
            element3.drop = [generateItem("item01")]
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
            self.stage.add_element(element5)
    

class StgScript03(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = []
        self.message = [u"Mantenha as latas de lixo", u"sempre tampadas!",
                        u"Qualquer outro foco do mosquito", u"também deve ser retirado."]
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite = load_sprite_mainsheet("otherpets01")
            element_sprite2 = load_sprite_mainsheet("otherlixeira01")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (1168,816))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (1424,816))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1200 + randint(-100, 100),700 + randint(-100, 100)))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1400 + randint(-100, 100),700 + randint(-100, 100)))
            element5 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1488,120))
            
            element.drop = [generateItem("item01")]
            element2.drop = [generateItem("item02")]
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
            self.stage.add_element(element5)
    
    


class StgScript04(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = []
        self.message = [u"Cuide bem da sua praça!",
                        u"E mantenha a cidade livre", u" do mosquito da dengue e zika!"]
        cfgweapon = getEquip("weapon01")
        sprite = load_sprite_mainsheet(cfgweapon.sprite)
        self.weapon = NoWeapon(cfgweapon, sprite)
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite = load_sprite_mainsheet("otherlixeira01")
            element_sprite2 = load_sprite_mainsheet("otherpets01")
            element_sprite3 = load_sprite_mainsheet("otherbarril01")
            element_sprite4 = load_sprite_mainsheet("othervaso01")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (432,80))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite3, position = (912,80))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (976,80))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1040,80))
            element5 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1392,496))
            element6 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (1392,560))
            
            element7 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (872 + randint(-200, 200),512 + randint(-200, 200)))
            element8 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (1028 + randint(-200, 200),522 + randint(-200, 200)))
            
            element8.drop = [generateItem("item01"),generateItem("item02")]
            element7.drop = [generateItem("item02")]
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
            self.stage.add_element(element5)
            self.stage.add_element(element6)
            self.stage.add_element(element7)
            self.stage.add_element(element8)
    
    



class StgScript05(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = []
        self.message = [u"As vezes, encontramos focos", u"do mosquito dentro da", u"nossa própria casa.",
                        u"Cubra potes e outros", u"reservatórios de água."]
        
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite = load_sprite_mainsheet("othervaso01")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (528,272))
            self.stage.add_element(element)
    
    
    def reward(self):
        reward = [generateItem("item01"),generateItem("item01"),generateItem("item02"),generateItem("item02")]
        #drops = []
        drop_sprite = load_sprite_mainsheet("icon01")
        for item_rw in reward:
            self.stage.add_element(ElementBuilder(type = "DropedBag", stage = self.stage, sprite = drop_sprite, position = (600 + randint(-64, 64), 344 ), item = item_rw))


class StgScript06(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = []
        self.message = ["Acabe com os focos do mosquito", "no quintal de casa!"]
        
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite = load_sprite_mainsheet("otherbalde01")
            element_sprite2 = load_sprite_mainsheet("otherbalde02")
            element_sprite4 = load_sprite_mainsheet("otherpets01")
            element_sprite3 = load_sprite_mainsheet("othervaso01")
            
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (680,190))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (630,170))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite3, position = (496,144))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (400,200))
            element5 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (680,300))
            element6 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite3, position = (720,144))
            
            element.drop = [generateItem("item02")]
            element2.drop = [generateItem("item01")]
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
            self.stage.add_element(element5)
            self.stage.add_element(element6)



class StgScript07(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = []
        self.message = [u"Não deixe pratos ou vasos", u"acumulando água no seu jardim!"]
        
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite = load_sprite_mainsheet("otherbalde01")
            element_sprite4 = load_sprite_mainsheet("otherprato01")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (700,380))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (368,570))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (368,600))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (660,624))
            
            element.drop = [generateItem("item02")]
            element2.drop = [generateItem("item01")]
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
    

class StgScript08(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.stage_song = "multimedia/soundtrack/DST-BossRide.ogg"
        self.enemies = []
        self.message = [u"As vezes, o foco do mosquito está", u"na casa de um vizinho.",
                        u"Mantenha caixas d'água e outros", u"recipientes sempre tampados",
                        u"e ajude a combater essa ameaça!",
                        
                        ]
        
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            self.stage.playback(self.stage_song)
            element_sprite4 = load_sprite_mainsheet("otherpets01")
            element_sprite5 = load_sprite_mainsheet("othercaixadagua01")
            element_sprite6 = load_sprite_mainsheet("otherbarril01")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite6, position = (496,720))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite6, position = (528,720))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite6, position = (560,720))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (512,576))
            element5 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite4, position = (584,576))
            element6 = ElementBuilder(type = "SuperFoco", stage = self.stage, sprite = element_sprite5, position = (670,700))
            
            
            element.drop = [generateItem("item01"),generateItem("item02")]
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
            self.stage.add_element(element5)
            self.stage.add_element(element6)
    
    def reward(self):
        reward = [generateItem("item01"),generateItem("item01"),generateItem("item02"),generateItem("item02")]
        #drops = []
        drop_sprite = load_sprite_mainsheet("icon01")
        for item_rw in reward:
            self.stage.add_element(ElementBuilder(type = "DropedBag", stage = self.stage, sprite = drop_sprite, position = (640 + randint(-64, 64), 450 + randint(-64, 64)), item = item_rw))
        self.stage.playback()
        


class StgScript09(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.respaw_delay = delay
        self.last_respaw = delay
        self.enemies = []
        self.message = [u"Mesmo próximo a hortas e plantações", u"o mosquito pode encontrar", 
                        u"um lugar pra se multiplicar.",
                        u"Use sua força e acabe com", u"a festa dos mosquitos!"
                        ]
    
    def start(self):
        if self.clear:
            self.clean_the_map()
        else:
            element_sprite = load_sprite_mainsheet("otherpets01")
            element_sprite2 = load_sprite_mainsheet("othervaso01")
            element_sprite3 = load_sprite_mainsheet("otherbarril01")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (368,112))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (464,112))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (496,112))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (528,112))
            element5 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (560,112))
            element6 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite3, position = (784,112))
            element7 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (160,192))
            element8 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (170,210))
            element9 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (150,230))
            element10 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (162,250))
            element11 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (168,260))
            element10 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (200,275))
            element11 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (220,290))
            
            
            element.drop = [generateItem("item02")]

            
            element_sprite5 = load_sprite_mainsheet("otherspecial01")
            element20 = ElementBuilder(type = "SpecialItem", stage = self.stage, sprite = element_sprite5, position = (780,580))
            element20.drop = generateWeapon("weapon04")
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
            self.stage.add_element(element5)
            self.stage.add_element(element6)
            self.stage.add_element(element7)
            self.stage.add_element(element8)
            self.stage.add_element(element9)
            self.stage.add_element(element10)
            self.stage.add_element(element11)
            self.stage.add_element(element20)
    
    def reward(self):
        reward = [generateItem("item01"),generateItem("item02"),generateItem("item02")]
        #drops = []
        drop_sprite = load_sprite_mainsheet("icon01")
        for item_rw in reward:
            self.stage.add_element(ElementBuilder(type = "DropedBag", stage = self.stage, sprite = drop_sprite, position = (510 + randint(-64, 64), 450 + randint(-64, 64)), item = item_rw))



class StgScript10(StageScript):
    def __init__(self, stage, delay= 30):
        StageScript.__init__(self, stage)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 12)
        self.text_bg = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
        self.stage_song = "multimedia/soundtrack/DST-BossRide.ogg"
        self.enemies = []
        self.message = [u"Dê o exemplo! Não deixe", u"pneus velhos abandonados.",
                        u"Se for guardá-los,", u"cubra-os com uma lona."]
        
    
    def start(self):
        if self.clear:
            self.clean_the_map()
            
        else:
            self.stage.playback(self.stage_song)
            self.pre_reward()
            self.stage.vision = 320
            
            element_sprite = load_sprite_mainsheet("otherpets01")
            element_sprite2 = load_sprite_mainsheet("otherpneu01")
            element_sprite3 = load_sprite_mainsheet("otherpneu02")
            element = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (650,325))
            element2 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (620,390))
            element3 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (1100,420))
            element4 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (1000,380))
            element9 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite2, position = (1180,460))
            element5 = ElementBuilder(type = "Foco", stage = self.stage, sprite = element_sprite, position = (480,230))
            
            element6 = ElementBuilder(type = "SuperFoco", stage = self.stage, sprite = element_sprite3, position = (1248,160))
            element7 = ElementBuilder(type = "SuperFoco", stage = self.stage, sprite = element_sprite3, position = (1376,160))
            element8 = ElementBuilder(type = "SuperFoco", stage = self.stage, sprite = element_sprite3, position = (1376,288))
            
            
#             element.drop = [generateItem("item01"),generateItem("item02")]
            element5.drop = [generateItem("item01"),generateItem("item02")]
#            element7.drop = [generateItem("item01"),generateItem("item02")]
            element9.drop = [generateItem("item01"),generateItem("item02")]
            
            self.stage.add_element(element)
            self.stage.add_element(element2)
            self.stage.add_element(element3)
            self.stage.add_element(element4)
            self.stage.add_element(element5)
            self.stage.add_element(element6)
            self.stage.add_element(element7)
            self.stage.add_element(element8)
            self.stage.add_element(element9)
    
    def clean_the_map(self):
        StageScript.clean_the_map(self)
        self.stage.vision = 540
    
    
    
    def reward(self):
        self.stage.playback()
        self.play_cleared_stage_sound()
    
    
    def play_cleared_stage_sound(self):
        StageScript.play_cleared_stage_sound(self)
        sound_clear = pygame.mixer.Sound("multimedia/soundEffects/aplausos.ogg")
        utils.mixer.play_effect(sound_clear)
    
    def pre_reward(self):
        reward = [generateItem("item01"),generateItem("item01"),generateItem("item01"),generateItem("item02"),generateItem("item02"),generateItem("item02"),
                  generateItem("item01"),generateItem("item01"),generateItem("item02")
                  ]
        
        drop_sprite = load_sprite_mainsheet("icon01")
        for item_rw in reward:
            self.stage.add_element(ElementBuilder(type = "DropedBag", stage = self.stage, sprite = drop_sprite, position = (1432 + randint(-32, 32), 1100 + randint(-32, 32)), item = item_rw))
    
    





