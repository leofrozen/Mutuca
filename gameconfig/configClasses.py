
#This class loads all config files and tests some issue before the game begins.


import json
import pygame
from utils.io_supporter import decrypt_file

#from configString import config_string as configuration
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
ORANGE = (250, 230, 0)


#



#configfile = "utils/config.json"

class ConfigLoader(object):
    def __init__(self, filename):
        self.filename = filename
        try:
            config =  decrypt_file(filename)
            self.json_data = json.loads(config)
            
            #with open(filename) as config:
                #self.json_data = json.loads(config.read())
            
            self.mapdir = self.json_data["mapdir"]
            self.soundtrackdir = self.json_data["soundtrackdir"]
            self.spritedir = self.json_data["spritedir"]
            self.soundeffectdir = self.json_data["soundeffectdir"]
            
            self.stages = self.json_data["stages"]
            self.stage_list = self.__stageToList()
            
            self.entities = self.json_data["entities"]
            self.enemy_list = self.__enemyToList() 
            self.npc_list = self.__npcToList()
            self.player_list = self.__playerToList()
            
            self.elements = self.json_data["elements"]
            self.portal_list = self.__portalToList()
            
            self.items = self.json_data["item"]
            self.item_list = self.__itemToList()
            
            self.equips = self.json_data["equip"]
            self.helmet_list = self.__equipToList("helmet")
            self.weapons_list = self.__weaponToList("weapon")
            
#                 self.weapons = self.json_data["weapons"]
#                 self.sword_list = self.__weaponToList("sword")
#                 self.noweapon_list = self.__weaponToList("noweapon")
            
            self.sprites = self.json_data["sprites"]
            self.ent_sprite_list = self.__spriteToList("entities")
            self.eff_sprite_list = self.__spriteToList("effects")
            self.icon_sprite_list = self.__spriteToList("icons")
            self.other_sprite_list = self.__spriteToList("others")
            
            self.sound_list = self.json_data["sounds"]
            #self.sound_list = self.__soundToList()
        
        except IOError:
            print("Cannot open config file {}".format(filename))
    
    
    
    ##########################
    def stageByID(self, id):
        for stg in self.stage_list:
            if stg.id == id:
                return stg
        print "no config info found for this stage id: %s" %id
        return None
    
    
    def __stageToList(self):
        list_of_stages = []
        for s in self.stages:
            list_of_stages.append(stageConfigClass(s, self.mapdir, self.soundtrackdir))
        
        if list_of_stages:
            return list_of_stages
        
        return None
    
    ################################# To List ################################
    
    def __portalToList(self):
        list_of_portals = []
        for p in self.elements['portal']:
            list_of_portals.append(portalConfigClass(p, self.spritedir))
        if list_of_portals:
            return list_of_portals
        return None
    
    
    def __entityToList(self):
        list_of_entities = []
        for e in self.entities:
            list_of_entities.append(entityConfigClass(e, self.spritedir))
        
        if list_of_entities:
            return list_of_entities
        
        return None
    
    def __enemyToList(self):
        list_of_enemies = []
        for e in self.entities['enemy']:
            list_of_enemies.append(entityConfigClass(e, self.spritedir))
    
        if list_of_enemies:
            return list_of_enemies
       
        return None
    
    def __npcToList(self):
        list_of_npc = []
        for e in self.entities['npc']:
            list_of_npc.append(entityConfigClass(e, self.spritedir))
    
        if list_of_npc:
            return list_of_npc
       
        return None
    
    def __playerToList(self):
        list_of_players = []
        for e in self.entities['player']:
            list_of_players.append(entityConfigClass(e, self.spritedir))
    
        if list_of_players:
            return list_of_players
       
        return None
    
    def __itemToList(self):
        list_of_item = []
        for w in self.items:
            list_of_item.append(itemConfigClass(w, self.spritedir, self.soundeffectdir))
    
        if list_of_item:
            return list_of_item
       
        return None
    
    
    def __equipToList(self, equip):
        list_of_equip = []
        for w in self.equips[equip]:
            list_of_equip.append(equipConfigClass(w, self.spritedir, self.soundeffectdir))
    
        if list_of_equip:
            return list_of_equip
       
        return None
    
    
#     def __helmetToList(self, equip):
#         list_of_equip = []
#         for w in self.equips[equip]:
#             list_of_equip.append(equipConfigClass(w, self.spritedir, self.soundeffectdir))
#     
#         if list_of_equip:
#             return list_of_equip
#        
#         return None
    
    
    def __weaponToList(self, weapon):
        list_of_weapons = []
        #for w in self.weapons[weapon]:
        for w in self.equips[weapon]:
            list_of_weapons.append(weaponConfigClass(w, self.spritedir, self.soundeffectdir))
    
        if list_of_weapons:
            return list_of_weapons
       
        return None
    
    def __spriteToList(self, sprite):
        list_of_sprites = []
        for w in self.sprites[sprite]:
            list_of_sprites.append(spriteConfigClass(w, self.spritedir))
    
        if list_of_sprites:
            return list_of_sprites
       
        return None
    
    ################################# END To List ################################
    
    ################################# By ID ################################
    def itemByID(self, id):
        for i in self.item_list:
            if i.id == id:
                return i
        return None
    
    def equipByID(self, id):
        if id.count("helmet"):
            for w in self.helmet_list:
                if w.id == id:
                    return w
        elif id.count("chest"):
            for w in self.chest_list:
                if w.id == id:
                    return w
        elif id.count("bottom"):
            for w in self.bottom_list:
                if w.id == id:
                    return w
        elif id.count("boots"):
            for w in self.boots_list:
                if w.id == id:
                    return w
        elif id.count("weapon"):
            for w in self.weapons_list:
                if w.id == id:
                    return w
        return None
    
    
    def weaponByID(self, id):
        if id.count('nw'):
            for w in self.noweapon_list:
                if w.id == id:
                    return w
        elif id.count('swd'):
            for w in self.sword_list:
                if w.id == id:
                    return w
        elif id.count('bow'):
            for w in self.bow_list:
                if w.id == id:
                    return w
        elif id.count('rod'):
            for w in self.rod_list:
                if w.id == id:
                    return w
        return None
    
    def entityByID(self, id):
        for e in self.entity_list:
            if e.id == id:
                return e
        return None
    
    def enemyByID(self, id):
        for e in self.enemy_list:
            if e.id == id:
                return e
        return None
    
    def NPCByID(self, id):
        for e in self.npc_list:
            if e.id == id:
                return e
        return None
    
    def playerByID(self, id):
        for p in self.player_list:
            if p.id == id:
                return p
        return None
    
    def portalByID(self, id):
        for p in self.portal_list:
            if p.id == id:
                return p
        return None
    
    def spriteByID(self, id):
        if id.count('ent'):
            for s in self.ent_sprite_list:
                if s.id == id:
                    return s
        elif id.count('eff'):
            for s in self.eff_sprite_list:
                if s.id == id:
                    return s
        elif id.count('icon'):
            for s in self.icon_sprite_list:
                if s.id == id:
                    return s
        elif id.count('other'):
            for s in self.other_sprite_list:
                if s.id == id:
                    return s

        return None
    
    def soundByID(self, id):
        if self.sound_list.get(id):
            sound = self.soundeffectdir + self.sound_list.get(id)
            return pygame.mixer.Sound(sound)
        return None
            
            
        
            
    ################################# END By ID ################################

    

class stageConfigClass(object):
    def __init__(self, dictStage, map_dir, soundtrack_dir):
        self.name = dictStage['name'] 
        self.id = dictStage['id']
        self.mapfile = map_dir + dictStage['mapfile']
        self.type = dictStage['type']
        self.npcs = dictStage['npcs']
        #self.npc_spot = dictStage['npc_spot']
        self.enemies = dictStage['enemies']
        self.properties = dictStage['properties']
        self.soundtrack = soundtrack_dir + dictStage['soundtrack']
        self.portals = dictStage['portals']
        self.startpoint = dictStage['startpoint']
        self.scriptID = dictStage['scriptID']



class entityConfigClass(object):
    def __init__(self, dictEntity, spritedir):
        self.name = dictEntity['name']
        #self.sprite = spritedir + dictEntity['sprite']
        self.sprite = dictEntity['sprite']
        self.id = dictEntity['id']
        self.type = dictEntity['type']
        self.dimensionx = dictEntity['dimensionx']
        self.dimensiony = dictEntity['dimensiony']
        self.weight = dictEntity['weight']
        self.stage = dictEntity['stage']
        #self.position = dictEntity['position']
        #self.spot = dictEntity['spot']
        self.dialogs = dictEntity['dialogs']
        self.properties = dictEntity['properties']
        self.status = dictEntity['status']
        


class portalConfigClass(object):
    def __init__(self, dictPortal, spritedir):
        self.id = dictPortal['id']
        self.sprite = dictPortal['sprite']
        #x, y =   dictPortal['position'][0], dictPortal['position'][1]
        #self.position = (x, y)
        self.position = dictPortal['position']
        self.destination = dictPortal['destination']
        self.dst_stage = dictPortal['dst_stage']


class itemConfigClass(object):
    def __init__(self, dictItem, spritedir, soundeffectdir):
        self.name = dictItem['name']
        self.description = dictItem['description']
        self.id = dictItem['id']
        self.sprite = dictItem['sprite']
        self.function = dictItem['function']
        self.parameter = dictItem['parameter']
    
    def use(self, action = None):
        if action != None:
            action(self.parameter)


class equipConfigClass(object):
    def __init__(self, dictEquip, spritedir, soundeffectdir):
        self.name = dictEquip['name']
        self.description = dictEquip['description']
        self.id = dictEquip['id']
        self.sprite = dictEquip['sprite']
        self.ad = dictEquip['ad']
        self.ap = dictEquip['ap']
        self.armor = dictEquip['armor']
        self.mdef = dictEquip['mdef']
        self.movspeed = dictEquip['movspeed']
        self.aspd = dictEquip['aspd']
        self.sound = soundeffectdir + dictEquip['sound']

class weaponConfigClass(object):
    def __init__(self, dictWeapon, spritedir, soundeffectdir):
        self.name = dictWeapon['name']
        self.description = dictWeapon['description']
        self.id = dictWeapon['id']
        self.sprite = dictWeapon['sprite']
        self.ad = dictWeapon['ad']
        self.ap = dictWeapon['ap']
        self.armor = dictWeapon['armor']
        self.mdef = dictWeapon['mdef']
        self.movspeed = dictWeapon['movspeed']
        self.aspd = dictWeapon['aspd']
        self.bullet_speed = dictWeapon['bullet_speed']
        self.energycost = dictWeapon['energycost']
        self.sound = soundeffectdir + dictWeapon['sound']
        self.s_range = int(dictWeapon['s_range'])
        self.e_range = int(dictWeapon['e_range'])

class spriteConfigClass(object):
    def __init__(self, dictSprite, spritedir):
        self.name = dictSprite['name']
        self.id = dictSprite['id']
        self.file = spritedir + dictSprite['file']
        self.lin  = dictSprite['lin']
        self.col  = dictSprite['col']
        self.atk_cols = dictSprite['atk_cols']
        self.sound = dictSprite['sound']
        
