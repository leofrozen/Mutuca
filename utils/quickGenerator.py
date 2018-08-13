import pygame

import gameEntities.gameEntity
import gameStages.stageElements




#from gameEntities.gameEntity import *
#from gameStages.stageElements import GameElement, Portal, Attack_Effect, InteractiveBox, RepelBox
from gameconfig.configLoader import getPlayer, getEnemy, getNPC, getPortal, load_sprite_mainsheet, getEquip, getItem
from gameItems.gameItem import SimpleWeapon, Item, Helmet, Chest, Bottom, Boots
from gameStages import stageElements
import constants





generator = None
def init():
    global generator
    generator = Generator()

def generateAttackEffect(stage, entity_name, weapon_sprite, beg, end, weapon_aspd, entity_ad, entity_ap, sound):
    global generator
    return generator.generateAttackEffect(stage, entity_name, weapon_sprite, beg, end, weapon_aspd, entity_ad, entity_ap, sound)

def generateRepelBox( entity, repel_rect):
    global generator
    return generator.generateRepelBox(entity, repel_rect)

def generateItem(item_id):
    global generator
    return generator.generateItem( item_id )

def generateWeapon(equip_id):
    global generator
    return generator.generateWeapon(equip_id)

def generateInteractiveBox(entity, rect):
    global generator
    return generator.generateInteractiveBox(entity, rect)

def generatePlayer(stage, entity_id = "ent01", weapon_id = "weapon01"):
    global generator
    return generator.generatePlayer(stage, entity_id, weapon_id)

def generateEnemy(stage, entity_spot, entity_id = "enemymutuca01", weapon_id = "weapon02"):
    global generator
    return generator.generateEnemy(stage, entity_spot, entity_id, weapon_id)

def generateNPC(self, stage, entity_spot, entity_id = "npc01", weapon_id = "weapon01"):
    global generator
    return generator.generateNPC(stage, entity_spot, entity_id, weapon_id)


class Generator():
    def __init__(self):
        pass
    
    def generatePlayer(self, stage, entity_id = "ent01", weapon_id = "weapon01", second_weapon_id = "weapon03"):
        cfgentity = getPlayer(entity_id)
        sprite = load_sprite_mainsheet(cfgentity.sprite)
        rect = pygame.Rect(0, 0, int( cfgentity.dimensionx), int(cfgentity.dimensiony) )
        entity = gameEntities.gameEntity.Player(stage, sprite, rect, cfgentity)
        weapon = self.generateWeapon(weapon_id)
        entity.equip_set.add(weapon)
        second_weapon = self.generateWeapon(second_weapon_id)
        entity.equip_set.add(second_weapon)        
        return entity
    
    def generateEnemy(self, stage, entity_spot, entity_id = "enemymutuca01", weapon_id = "weapon02", second_weapon_id = "weapon06"):
        cfgentity = getEnemy(entity_id)
        sprite = load_sprite_mainsheet(cfgentity.sprite)
        rect = pygame.Rect(0, 0, int( cfgentity.dimensionx), int(cfgentity.dimensiony) )
        entity = gameEntities.gameEntity.Enemy(stage, sprite, rect, cfgentity, entity_spot)
        weapon = self.generateWeapon(weapon_id)
        entity.equip_set.add(weapon)
        
        if constants.GAMELEVEL == "HARD":
            entity.max_life = float(entity.max_life*1.2)
            entity.life_base = float(entity.life_base*1.2)
            entity.life = float(entity.life*1.2)
            
            entity.max_mana = float(entity.max_mana*2)
            entity.mana_base = float(entity.mana_base*2)
            entity.mana = float(entity.mana*2)
        
        if cfgentity.type == "boss":
#             print "preparing boss"
            special_item = self.generateWeapon(second_weapon_id)
            entity.equip_set.special_item = special_item
            entity.brain.set_state("boss_exploring")
#             print "adding a boss"
            
        else:
            entity.brain.set_state("exploring")
        return entity
    
    def generateNPC(self, stage, entity_spot, entity_id = "npc01", weapon_id = "weapon01"):
        cfgentity = getNPC(entity_id)
        sprite = load_sprite_mainsheet(cfgentity.sprite)
        rect = pygame.Rect(0, 0, int( cfgentity.dimensionx), int(cfgentity.dimensiony) )
        entity = gameEntities.gameEntity.NPC(stage, sprite, rect, cfgentity, entity_spot)
        weapon = self.generateWeapon(weapon_id)
        entity.equip_set.add(weapon)
        entity.brain.set_state("roaming")
        return entity

    
    def generateWeapon(self, equip_id = "weapon01"):
        cfgweapon = getEquip(equip_id)
        sprite = load_sprite_mainsheet(cfgweapon.sprite)
        weapon = SimpleWeapon(cfgweapon, sprite)
        return weapon
    
    def generateEquip(self, equip_id = "helmet01"):
        cfgequip = getEquip(equip_id)
        sprite = load_sprite_mainsheet(cfgequip.sprite)
        
        equip = None
        if equip_id.count("helmet"):
            equip = Helmet(cfgequip, sprite)
        if equip_id.count("chest"):
            equip = Chest(cfgequip, sprite)
        if equip_id.count("boots"):
            equip = Boots(cfgequip, sprite)
        if equip_id.count("bottom"):
            equip = Bottom(cfgequip, sprite)

        #equip = Helmet(cfgequip, sprite)
        return equip
    
    def generateItem(self, item_id = "item01"):
        cfgitem = getItem(item_id)
        sprite = load_sprite_mainsheet(cfgitem.sprite)
        item = Item(cfgitem, sprite)
        return item
    
    def generatePortal(self, stage, element_id):
        cfgportal = getPortal(element_id)
        sprite = load_sprite_mainsheet(cfgportal.sprite)
        element = gameStages.stageElements.Portal(stage, sprite, cfgportal)
        return element
        #stage.add_element(element)
    
    def generateAttackEffect(self, stage, entity_name, weapon_sprite, beg, end, weapon_aspd, entity_ad, entity_ap, sound):
        attack_effect = gameStages.stageElements.Attack_Effect(stage, entity_name, weapon_sprite, beg, end, weapon_aspd, entity_ad, entity_ap, sound)
        return attack_effect
    
    
    def generateInteractiveBox(self, entity, rect):
        interactive_box = gameStages.stageElements.InteractiveBox(entity, rect)
        return interactive_box
    
    def generateRepelBox(self, entity, repel_rect):
        rbox = gameStages.stageElements.RepelBox(entity, repel_rect)
        return rbox
    
    def generateTextBox(self, stage, entity, dialog_sprite, pos):
        tx = gameStages.stageElements.TextBox(stage, entity, dialog_sprite, pos)
        return tx
    
    
