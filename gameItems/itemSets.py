    
# -*- coding: UTF-8 -*-


from gameItem import Item, Equip, Etc, Helmet, Chest, Boots, Weapon, Bottom
from gameStages.stageElements import DropedBag
import gameconfig.configLoader
from gameconfig.configLoader import getSprite, load_sprite_mainsheet
from random import randint
import pygame






#########################################################
BLACK = (0,0,0)
def text_objects(text, font):
    textSurface = font.render(u'%s' %text, True, BLACK)
    return textSurface, textSurface.get_rect()
#########################################################




class EquipSet():
    def __init__(self, helmet, chest, boots, weapon, second_weapon = None, special_item = None):
        self.helmet = helmet
        self.chest = chest
        self.bottom = None
        self.boots = boots
        self.weapon = weapon
        self.second_weapon = second_weapon
        self.special_item = special_item
        self.set = [self.helmet, self.chest, self.bottom, self.boots, self.weapon, self.second_weapon, self.special_item]
    
    def add(self, equip):
        if isinstance(equip, Helmet):
            if self.helmet == None:
                self.helmet = equip
            else:
                to_bag = self.helmet
                self.helmet = equip
                return to_bag
        if isinstance(equip, Chest):
            if self.chest == None:
                self.chest = equip
            else:
                to_bag = self.chest
                self.chest = equip
                return to_bag
        if isinstance(equip, Bottom):
            if self.bottom == None:
                self.bottom = equip
            else:
                to_bag = self.chest
                self.chest = equip
                return to_bag
        if isinstance(equip, Boots):
            if self.boots == None:
                self.boots = equip
            else:
                to_bag = self.boots
                self.boots = equip
                return to_bag
        if isinstance(equip, Weapon):
            if self.weapon == None:
                self.weapon = equip
            elif self.second_weapon == None:
                self.second_weapon = equip
            elif self.special_item == None:
                self.special_item = equip
            else:
                to_bag = self.weapon
                self.weapon = equip
                return to_bag
        
        self.set = [self.helmet, self.chest, self.bottom, self.boots, self.weapon, self.second_weapon, self.special_item]
        
        return None
    
    def remove(self, equip):
        if equip == "helmet":
            to_bag = self.helmet
            self.helmet = None
            return to_bag
        if equip == "chest":
            to_bag = self.chest
            self.chest = None
            return to_bag
        if equip == "boots":
            to_bag = self.boots
            self.boots = None
            return to_bag
    
    
    def get(self, equip):
        if equip == "helmet":
            return self.helmet
        elif equip == "chest":
            return self.chest
        elif equip == "boots":
            return self.boots
        elif equip == "bottom":
            return self.bottom
        elif equip == "weapon":
            return self.weapon
        elif equip == "second_weapon":
            return self.second_weapon
        elif equip == "special_item":
            return self.special_item
        else: return None
        
        
    def update(self):
        
        
        hp = 0
        mana = 0
        ad = 0
        ap = 0
        armor = 0
        mdef = 0
        movspeed = 0
        aspd = 0
        
        for equip in self.set:
            if equip:
                hp += equip.hp
                mana += equip.mana
                ad += equip.ad
                ap += equip.ap
                armor += equip.armor
                mdef += equip.mdef
                movspeed += equip.movspeed
                aspd += equip.aspd
        
        return hp, mana, ad, ap, armor, mdef, movspeed, aspd 
    
    def show(self):
        pass


    
    
class Inventory(object):
    def __init__(self, entity):
        self.entity = entity
        self.bag = {}
        self.item_id = 0
        self.max_size = 12
        self.sprite = load_sprite_mainsheet("icon01")
        self.updated_inventory = None
        self.update()
        self.selected = None
        self.largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
        self.smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 15)
        self.smallText.set_bold(True)
        
    def add_gameItem(self, item):
        if len(self.bag) < self.max_size:
            self.bag[self.item_id] = item
            item.id = self.item_id
            self.item_id += 1
#             print self.bag
#             for x in self.bag.itervalues():
#                 print x.id
            self.update()
            return True
        else:
            return False
    
    def remove_gameItem(self, item):
        del self.bag[item.id]
    
    def get_item(self, item):
        return self.bag[item.id]
    
    def select_item(self, item):
        self.selected = self.bag[item.id]
    
    def quick_use(self,  item_name):
        '''Usa o primeiro item com o nome igual ao passado como parametro'''
        for i in self.bag.itervalues():
            if i.name == item_name:
                i.use(self.entity)
                self.remove_gameItem(i)
                del i
                self.update()
                break
        
    
    
    def sort(self):
        pass
    
    def update(self):
        empty_slot = load_sprite_mainsheet("other01")
        inventory = []
        
        
        for i in self.bag.itervalues():
            slot_surface = empty_slot[0][0].copy()
            #slot_rect = slot.get_rect()
            icon_rect = i.icon.get_rect()
            icon_rect.center = (slot_surface.get_width()/2, slot_surface.get_height()/2)
            slot_surface.blit(i.icon, icon_rect)
            inventory.append((slot_surface, i.id, slot_surface.get_rect()))
            
        for s in range(self.max_size):
            if len(inventory) < self.max_size:
                slot_surface = empty_slot[0][0].copy()
                inventory.append((slot_surface, None,  slot_surface.get_rect()))
        
        self.updated_inventory = inventory
        
#         for j in self.updated_inventory:
#             print j
    
    def render(self, surface, mouse_pos):
        posx = 1
        posy = 1
        s_width = surface.get_width()
        s_height = surface.get_height()
        #max_cols = 4
        max_cols = int(s_width/(self.updated_inventory[0][2].width * 1.2))
        for i in self.updated_inventory:
            #slot_rect = i[0].get_rect()
            if posx > max_cols:
                posx = 1
                posy += 1
            
#             slot_rect.left = s_width/4 * posx - slot_rect.width
#             slot_rect.top = s_height/3 * posy - slot_rect.height
#             i[2].left = s_width/4 * posx - i[2].width
#             i[2].top = s_height/3 * posy - i[2].height
            i[2].centerx = s_width/5 * posx
            i[2].centery = s_height/4 * posy
            surface.blit(i[0], i[2])
            posx += 1
        
        caption, caption_rect = text_objects(u"Inventário", self.largeText)
        caption_rect.centerx = surface.get_width()/2
        caption_rect.top = 10
        
        
        surface.blit(caption, caption_rect)
        
        for i in self.updated_inventory:
            if i[2].collidepoint(mouse_pos) and self.bag.get(i[1]) != None:
                #descrip, descrip_rect = text_objects(self.bag.get(i[1]).name + ": " + self.bag.get(i[1]).description , self.smallText)
                #descrip_rect.center = (mouse_pos[0] + 50, mouse_pos[1] - 50)
                #surface.blit(descrip, descrip_rect)
                
                #descrip_rect.center = (mouse_pos[0], mouse_pos[1])
                #return (descrip, descrip_rect)
                
                descrip = self.smallText.render(u'%s' %(self.bag.get(i[1]).name + ": " + self.bag.get(i[1]).description ), True, (0, 60, 100), (240, 240, 240 ))
                return descrip
    
    def render_to_dock(self,  surface,  mouse_pos):
        posx = 1
        posy = 1
        s_width = surface.get_width()
        s_height = surface.get_height()
        empty_slot = load_sprite_mainsheet("otherslot02")
        slot1 = 0
        icon_potion = load_sprite_mainsheet("icon02")
        slot2 = 0
        icon_batery = load_sprite_mainsheet("icon03")
        slot3 = 0
        for i in self.bag.itervalues():
            if i.name == u"Poção de Cura":
                slot1 += 1
            elif i.name == "Bateria":
                slot2 += 1
        
        #if slot1 > 0:
        #   slot_surface = empty_slot[0][0].copy()
         
        #surface.blit(icon_potion[0][0], (s_width/16,  (s_height/6) ) )
        surface.blit(self.smallText.render(str(slot1),  True, (220, 220, 220)),((s_width/24)* 23,  (s_height/8)*2)  )
        surface.blit(self.smallText.render(str(slot2),  True, (220, 220, 220)),((s_width/24)* 23,  (s_height/8)*6)  )
        
        return surface
    
    def drop(self):
        droped_items = []
#         if len(self.bag) > 0:
#             print "tem coisa na bag"
        for i in self.bag.itervalues():
            print u"Item dropado: %s" %i.name
            droped = DropedBag(self.entity.stage, self.sprite, (self.entity.rect.centerx + randint(-32, 32), self.entity.rect.centery + randint(-32, 32)), i)
            droped_items.append(droped)
        if len(droped_items) > 0:
            for di in droped_items:
                self.entity.stage.add_element(di)
                #return droped_items
    
    def process(self, mouse_pos):
        #print mouse_pos
        #print self.updated_inventory[0]
        #mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        for i in self.updated_inventory:
            if i[2].collidepoint(mouse_pos) and self.bag.get(i[1]) != None:
                if mouse_click[0] == 0:
                    #print "clicaram no item %s" %self.bag[i[1]].name
                    if self.bag[i[1]].usable:
                        self.bag[i[1]].use(self.entity)
                        self.remove_gameItem(self.bag[i[1]])
                        del i
                        self.update()
                    return
     
