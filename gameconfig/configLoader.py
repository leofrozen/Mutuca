'''
Created on 20/04/2016

@author: frozen
'''

import pygame
from configClasses import *
import json
from utils.io_supporter import decrypt_file,  encrypt_file

#This class loads all config files and tests some issue before the game begins.

configloader = None
def init(configfile):
    global configloader
    configloader = ConfigLoader(configfile)


def getEquip( id ):
    global configloader
    return configloader.equipByID(id)

def getStage( id ):
    global configloader
    return configloader.stageByID(id)

def getWeapon( id ):
    global configloader
    return configloader.weaponByID(id)

def getEntity(id):
    global configloader
    return configloader.entityByID(id)

def getEnemy(id):
    global configloader
    return configloader.enemyByID(id)

def getNPC(id):
    global configloader
    return configloader.NPCByID(id)

def getPlayer(id):
    global configloader
    return configloader.playerByID(id)

def getPortal(id):
    global configloader
    return configloader.portalByID(id)

def getSprite(id):
    global configloader
    return configloader.spriteByID(id)

def getSound(id):
    global configloader
    return configloader.soundByID(id)

def getItem(id):
    global configloader
    return configloader.itemByID(id)

def load_sprite_mainsheet(sprite_id):
    spritecfg = getSprite(sprite_id)
    
    mainsheet = None
    try:
        mainsheet = pygame.image.load(spritecfg.file).convert_alpha()
    except IOError:
        print("IOError! Failed to load file $s" %spritecfg.file)
    if mainsheet == None:
        print "adicionar um processamento desse erro e carregar uma imagem de erro padrao"
        pygame.quit()
    
    sheet_size = mainsheet.get_size()
    cols = int(spritecfg.col)
    lins = int(spritecfg.lin)
    cell_width = sheet_size[0] / cols
    cell_height = sheet_size[1] / lins
    
    cell_list_sprite=[]
    for y in range(0, sheet_size[1], cell_height):
        sprite_line = []
        for x in range(0, sheet_size[0], cell_width):
            surface = pygame.Surface((cell_width, cell_height), flags=pygame.SRCALPHA)
            surface.blit(mainsheet, (0,0), (x, y, cell_width, cell_height))
            #colorkey = surface.get_at((0, 0))
            #surface.set_colorkey(colorkey)
            sprite_line.append(surface)
        
        cell_list_sprite.append(sprite_line)
    
    if cell_list_sprite:
        return cell_list_sprite
    else:
        return None



def save_records(**kwargs):
    #filename = "gameconfig/savestate.json"
    filename = "gameconfig/SAVE.mut"
    
    json_data = {
            "maxmutucas" : kwargs["maxmutucas"],
            "maxfocos" : kwargs["maxfocos"],
            "maxcoins" : kwargs["maxcoins"],
            "maxscore" : kwargs["maxscore"]
            
            
    }
    
    try:
        #with open(filename, 'w') as records:
        encrypt_file(json.dumps(json_data),  out_filename= filename)
        #json_data = json.dumps(data)
        #    json.dump(json_data, records)
    
    except IOError:
        print("Cannot open records file {}".format(filename))
            


def load_records():
    #filename = "gameconfig/savestate.json"
    filename = "gameconfig/SAVE.mut"
    
    try:
        #with open(filename) as records:
        #    json_data = json.loads(records.read())
        
        # 02/12/2016 - o arquivo de configuracao foi alterado para DATA.mut e precisar descriptografado antes da leitura
        config =  decrypt_file(filename)
        json_data = json.loads(config)
        return json_data
#             maxmutucas = json_data["maxmutucas"]
#             maxscore = json_data["maxscore"]
#             
    
    except IOError:
        print("Cannot open records file {}. TRY TO OPEN THE GAME AGAIN.".format(filename))
#        json_data = {
#            "maxmutucas" : 0,
#            "maxfocos" : 0,
#            "maxcoins" : 0,
#            "maxscore" : 0            
#        }
        save_records(maxmutucas = 0, maxfocos = 0, maxcoins = 0, maxscore = 0)
    



            
