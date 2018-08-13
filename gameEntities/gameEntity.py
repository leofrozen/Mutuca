from gameobjects_local.vector2 import Vector2
from random import randint
from ia import *
#from actions import *
import actions
#from gameStages.stageElements import Attack_Effect, TextBox, InteractiveBox
from gameStages.stageElements import ElementBuilder
import pygame
import pygame.time
from gameItems.itemSets import EquipSet, Inventory
from gameconfig.configLoader import getSprite, load_sprite_mainsheet



# CONSTANTS
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

UP_LEFT = "UP_LEFT"
UP_RIGHT = "UP_RIGHT"
DOWN_LEFT = "DOWN_LEFT"
DOWN_RIGHT = "DOWN_RIGHT"

#


def EntityBuilder(type, **kargs):
    
    if type == "Player":
        return Player(kargs["stage"], kargs["sprite"], kargs["rect"], kargs["cfgentity"])
    
    if type == "Enemy":
        return Enemy(kargs["stage"], kargs["sprite"], kargs["rect"], kargs["cfgentity"], kargs["spot"])
    
    if type == "NPC":
        return NPC(kargs["stage"], kargs["sprite"], kargs["rect"], kargs["cfgentity"], kargs["spot"])


class GameEntity(object):
    def __init__(self, stage, sprite, rect, cfgentity, spot = (32,32)):
        self.stage = stage
        self.name = cfgentity.name
        self.type = cfgentity.type
        self.weight = cfgentity.weight
        self.dialogs = cfgentity.dialogs
        self.dialog_step = 0
        self.dialog_delay = 10
        self.range = 30 # temp, salvar isso nos configs
        self.collision = [False]*9
        self.rect = rect
        self.destination = Vector2(0, 0)
        self.id = 0
        self.effects = []
        #self.spot = cfgentity.spot
        self.spot = spot
        self.direction = Vector2(0, 0)
        self.last_direction = Vector2(0, 0)
        
        self.clock = pygame.time.Clock()
        self.last_attack = 0.
        
        # load all possible entity states
        self.brain = StateMachine()
        self.talking = False
        self.acting = None
        self.actions = actions.InputAction()
        
        self.communicative = False
        
        # Equipments
        self.equip_set = EquipSet(None, None, None, None, None)
        self.gear = None
        self.body = None
        self.boot = None
        self.weapon = None
        
        # Bag
        self.inventory = Inventory(self) 
        
        # Attributes
        self.level = 1
        self.load_attributes(cfgentity.status)
        
        # Sprite and auxs
        self.sprite = sprite
        self.cell_atk_cols = getSprite(cfgentity.sprite).atk_cols
        self.cell_dir = 0
        self.cell_pos = 0
        
        
        
        # Sprite speed
        self.max_count = int(self.speed/30)
        self.cell_count = 1

        
        
#         self.hp_base = None
#         self.mana_base = None
#         self.speed_base = None
#         self.ad_base = None
#         self.ap_base = None
#         self.armor_base = None
#         self.mdef_base = None
#         self.aspd_base = None
        
#         self.max_life = None
#         self.max_mana =  None
#         self.life = None
#         self.mana = None
        
        
        
#         # Here you can found the  definitive attributes
#         self.max_life = None
#         self.max_mana =  None
#         self.life = None
#         self.mana = None
#         
#         self.speed = None
#         self.ad = None
#         self.ap = None
#         self.armor = None
#         self.mdef = None
#         self.aspd = None
#         
#         
#         # Temp
#         self.life = 50.
#         self.mana = 20.
        

    
    
    def load_attributes(self, status_base):
        # only test
        
        self.life_base = self.max_life = float(status_base['life'])
        self.mana_base = self.max_mana =  float(status_base['mana'])
        self.life = float(status_base['life'])
        #self.life = self.max_life
        self.mana = self.max_mana
        
        self.speed_base = self.speed = float(status_base['movspd'])
        self.ad_base = self.ad = int(status_base['ad'])
        self.ap_base = self.ap = int(status_base['ap'])
        self.armor_base = self.armor = int(status_base['armor'])
        self.mdef_base = self.mdef = int(status_base['mdef'])
        self.aspd_base = self.aspd = float(status_base['aspd'])
        self.vision = int(status_base['vision'])
        self.delay_attack_animation = 4 * self.aspd
    
    
    def load_equipments(self, equips):
        pass
    
    def load_buffs(self, buffs):
        pass
    
    
    def act(self, action_id, time_passed):
        self.actions.act(action_id, time_passed)
    
    def render_effects(self, surface):
        pass
    
    
    def render_chat(self, surface):
        if self.chating:
            dialog_sprite = []
            font = pygame.font.Font("multimedia/fonts/comic.ttf", 15);
            if len(self.dialogs) == 0:
                return font.render("%s: ..."%self.name, True, (0,20,50))
            
            else:
                begin_dialog = []
                for txt in self.dialogs['begin']:
                    text_surface = font.render(txt, True, (0, 0, 255))
                    begin_dialog.append(text_surface)
                
                dialog_sprite.append(begin_dialog)    
                
#                 if self.dialogs['quest']:
#                     quest_dialog = []
#                     for txt in self.dialogs['quest']:
#                         text_surface = font.render(txt, True, (0, 0, 255))
#                         quest_dialog.append(text_surface)
#                 
#                 dialog_sprite.append(quest_dialog)
                
                if self.dialogs['end']:
                    end_dialog = []
                    for txt in self.dialogs['end']:
                        text_surface = font.render(txt, True, (0, 0, 255))
                        end_dialog.append(text_surface)
                dialog_sprite.append(end_dialog)
    
    def render_status_bar(self, surface):
        
        # Draw a health bar
        (x, y) = (self.rect.centerx, self.rect.centery)
        #w, h = self.sprite.get_size()
        w, h = self.rect.size
        bar_x = x - 12
        #bar_y = y + h/2
        bar_y = y + h*0.7
        
        bar_width = 25
        bar_height = 4
        
        # LIFE 
        prct_life = float( 100 * (self.life/self.max_life))
        life_bar = int((bar_width * prct_life)/100)
        
        surface.fill( (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        surface.fill( (0, 255, 0), (bar_x, bar_y, life_bar, bar_height))
        
        # MANA
        prct_mana = int( 100 * (self.mana/self.max_mana))
        mana_bar = int((bar_width * prct_mana)/100)
        
        surface.fill( (50, 20, 50), (bar_x, (bar_y + bar_height), bar_width, bar_height))
        surface.fill( (30, 30, 250), (bar_x, (bar_y + bar_height), mana_bar, bar_height))
    
    
    def render(self, surface):
        
        # Render Shadow
        shadow_color = pygame.Color(0,0,0, 127)
        shadow = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        sw, sy = shadow.get_size()
        #pygame.draw.circle(shadow, shadow_color, (sw/2, sy/2 - 5) , int(self.rect.width/2.5))
        pygame.draw.ellipse(shadow, shadow_color, (sw/10,8, sw*0.9, sy/2))
        surface.blit(shadow,(self.rect.x, self.rect.centery))
        
        
        cell = self.sprite[self.cell_dir][self.cell_pos]
        surface.blit(cell, (self.rect.centerx - cell.get_width()/2, self.rect.centery - cell.get_height() + self.rect.height/2 ))

        self.render_status_bar(surface)
        #surface.blit(self.image, (x-w/2, y-h/2))
    
    def stero_pan(self, x_coord, screen_width):
    
        right_volume = float(x_coord) / screen_width
        left_volume = 1.0 - right_volume
        
        return (left_volume, right_volume)
    
    def play_soundeffect(self, sound):
        channel = sound.play()
        width, height = self.stage.get_size()
        if channel is not None:
            # Get the left and right volumes
            left, right = self.stero_pan(self.rect.centerx, width)
            channel.set_volume(left, right)
    
    def update_position(self, time):
        pass
    
    
    def set_position(self, position):
        """ Change entity position with out alter the face direction! """
        self.rect.center = position
    
    
    def hard_collision(self, rect):
        """ Collision with impact effect """
        pass
    

    
    def update_sprite(self, direction, time_passed):
        
        ''' avaliar um meio do self.cell_count ser diretamente proprocional ao time_passed '''
        
        self.cell_count += 1
        last_dir = self.cell_dir
        
        if self.acting == "attack":
            
            
#             print "sprite de atacando"
#             if direction[0] == 0 and direction[1] > 0:
#                 # DOWN
#                 self.cell_dir = 4
#             if direction[0] == 0 and direction[1] < 0:
#                 # UP
#                 self.cell_dir = 5
#             if direction[0] > 0 and direction[1] == 0:
#                 # RIGHT
#                 self.cell_dir = 6
#             if direction[0] < 0 and direction[1] == 0:
#                 # LEFT
#                 self.cell_dir = 7
#             
            
            #if direction == [0,0]:
            """ Se o personagem estiver parado, o ataque deve sair da ultima direcao em que estava """
            if last_dir == 0:
                self.cell_dir = 4
            elif last_dir == 1:
                self.cell_dir = 5
            elif last_dir == 2:
                self.cell_dir = 6
            elif last_dir == 3:
                self.cell_dir = 7
            
            if self.cell_dir == last_dir:
                #if self.cell_count >= self.aspd:
                #if self.last_attack >= self.aspd:
#                 print time_passed
#                 print len(self.sprite[self.cell_dir])
#                 print self.aspd                 
#                 print (self.aspd / len(self.sprite[self.cell_dir]))
                if self.cell_count > self.delay_attack_animation:
                #if self.last_attack >= (self.aspd / len(self.sprite[self.cell_dir])):
                
                    #if self.cell_pos < len(self.sprite[self.cell_dir]) -1:
                    """ ISSO ABAIXO EH UMA GAMBIARRA!!
                     NO LUGAR O < 5 DEVIA SER FEITO UMA VERIFICACAO DO 
                     NUMERO DE COLUNAS DE ATAQUE NO ARQUIVO DE SPRITE
                    """
                    #if self.cell_pos < 5:
                    if self.cell_pos < self.cell_atk_cols -1:
                        self.cell_pos += 1
                        self.cell_count = 1
                    else:
                        self.acting = None
                        self.cell_pos = 0
                
            else:
                self.cell_pos = 0
            
            
            
            
        
        elif direction != (0,0):
            last_dir = self.cell_dir
            if direction[0] == 0 and direction[1] > 0:
                # DOWN
                self.cell_dir = 0
            if direction[0] == 0 and direction[1] < 0:
                # UP
                self.cell_dir = 1
            if direction[0] > 0 and direction[1] == 0:
                # RIGHT
                self.cell_dir = 2
            if direction[0] < 0 and direction[1] == 0:
                # LEFT
                self.cell_dir = 3
            
            # diagonal
            if direction[0] > 0 and direction[1] > 0 and direction[0] > direction[1]:
                # DOWN-RIGHT
                self.cell_dir = 2
            if direction[0] > 0 and direction[1] > 0 and direction[0] < direction[1]:
                # DOWN-RIGHT
                self.cell_dir = 0
            
            if direction[0] < 0 and direction[1] > 0 and abs(direction[0]) > abs(direction[1]):
                # DOWN-LEFT
                self.cell_dir = 3
            if direction[0] < 0 and direction[1] > 0 and abs(direction[0]) < abs(direction[1]):
                # DOWN-LEFT
                self.cell_dir = 0
            ####
            if direction[0] > 0 and direction[1] < 0 and abs(direction[0]) > abs(direction[1]):
                # UP-RIGHT
                self.cell_dir = 2
            if direction[0] > 0 and direction[1] < 0 and abs(direction[0]) < abs(direction[1]):
                # UP-RIGHT
                self.cell_dir = 1
            
            
            if direction[0] < 0 and direction[1] < 0 and abs(direction[0]) > abs(direction[1]):
                # UP-LEFT
                self.cell_dir = 3
            if direction[0] < 0 and direction[1] < 0 and abs(direction[0]) < abs(direction[1]):
                # UP-LEFT
                self.cell_dir = 3
            
            
            if last_dir == 4:
                self.cell_dir = 0
            if last_dir == 5:
                self.cell_dir = 1
            if last_dir == 6:
                self.cell_dir = 2
            if last_dir == 7:
                self.cell_dir = 3
            
            if self.cell_dir == last_dir:
                if self.cell_count >= 4:
                    if self.cell_pos < len(self.sprite[self.cell_dir]) -1:
                        self.cell_pos += 1
                        self.cell_count = 1
                    else:
                        self.cell_pos = 0
                
            else:
                self.cell_pos = 0
    
    # if no direction buttom was select, just chance the sprite to the stop position
        else:
            self.cell_pos = 0

    
    def process(self, time_passed, walls):
        
        if self.last_attack >= self.aspd:
            self.last_attack = self.aspd
        else:
            self.last_attack += time_passed


    
    
    
    def change_weapon(self, weapon):
        self.weapon = weapon
        self.calc_status()
    
    def attack(self, time_passed):
        
        if self.last_attack < self.aspd:
            return None, None, None, None, None
        self.last_attack = 0
        
        #self.direction = attack_direction
        hitten = None
        
        
        beg = Vector2(0,0)
        end = Vector2(0,0)
        beg, end = self.weapon.use(self.rect.center, self.last_direction)
        #self.play_soundeffect(self.weapon.sound)
        return "ATTACK", beg, end, self.ad, self.weapon.sprite


#     
#     def interact(self):
#         interactive_box = InteractiveBox(self)
#         self.stage.add_element(interactive_box)
#     
#     def dash_forward(self, time_passed):
#         if self.last_attack < self.aspd:
#             return
#         self.last_attack = 0
#         self.rect.center += self.direction * time_passed * self.speed*5
#     
#     def dash_backward(self, time_passed):
#         if self.last_attack < self.aspd:
#             return
#         self.last_attack = 0
#         self.rect.center -= self.last_direction * time_passed * self.speed*5
    
    
    
    def calc_status(self):
        # update character status based on new equipment or level
        # atualiza os status do personagem com base no novo equipamento ou nivel
        
        #self.ad = self.ad_base + self.weapon.ad
        
        hp, mana, ad, ap, armor, mdef, movspeed, aspd = self.equip_set.update()
        self.max_life = self.life_base + hp 
        self.max_mana = self.mana_base + mana
        self.ad = self.ad_base + ad
        self.ap = self.ap_base + ap
        self.armor = self.armor_base + armor
        self.mdef = self.mdef_base + mdef
        self.speed = self.speed_base + movspeed
        self.aspd = self.aspd_base + aspd
        
        
        
        
        
        
    
    def calc_damage(self, atq):
        
        total_damage = max((atq[0] - self.armor), 0) + max((atq[1] - self.mdef, 0))
        #print "dano real recebido %s" %total_damage
        return total_damage
    
    def hitten(self, atq):
         
        damage = self.calc_damage(atq)
        if damage < 1:
            #print "miss"
            # dano minimo
            self.life -= 1
        else:
            self.life -= damage
            #print "vida restante %d" %self.life
    
    
    def to_talk(self, size = 15, text = None):
        self.communicative = True
        
        if text:
            font = pygame.font.Font("multimedia/fonts/comic.ttf", size)
            dialog_sprite = []
#             text_surface = font.render(u'%s' %text, True, (225,0,0), (240,240,240))
#             begin_surface = []
#             begin_surface.append(text_surface)
#             dialog_sprite.append(begin_surface)
#             dialog_box = ElementBuilder(type="TextBox", stage = self.stage, entity = self, sprite = dialog_sprite, position = self.rect.center)
#             self.stage.add_element(dialog_box)
            dialog = []
            for txt in text:
                text_surface = font.render(u'%s' %txt, True, (0, 60, 100), (240, 240, 240 ))
                dialog.append(text_surface)
            dialog_sprite.append(dialog)
            dialog_box = ElementBuilder(type="TextBox", stage = self.stage, entity = self, sprite = dialog_sprite, position = self.rect.center)
            self.stage.add_element(dialog_box)
            
            return
            
        
        
        
        
        #  A TEXT_BOX PODIA SER TEXTO OU FIGURAS ...
        
        if len(self.dialogs) != 0:
            dialog_sprite = []
            font = pygame.font.Font("multimedia/fonts/comic.ttf", 15)
            
            begin_dialog = []
            for txt in self.dialogs['begin']:
                #print txt
                text_surface = font.render(u'%s' %txt, True, (0, 60, 100), (240, 240, 240 ))
                
                begin_dialog.append(text_surface)
            
            dialog_sprite.append(begin_dialog)    
#             if self.dialogs['quest']:
#                 quest_dialog = []
#                 for txt in self.dialogs['quest']:
#                     text_surface = font.render(txt, True, (0, 0, 255))
#                     
            
            dialog_box = ElementBuilder(type="TextBox", stage = self.stage, entity = self, sprite = dialog_sprite, position = self.rect.center)
            self.stage.add_element(dialog_box)
        
    
    def explode(self):
        sprite = load_sprite_mainsheet("effexplosion01")
        explosion = ElementBuilder(type = "Explosion", stage = self.stage, sprite = sprite, position = self.rect.center)
        self.stage.add_element(explosion)
    
    def loadDialogs(self, dictDialog):
        if len(dictDialog) == 0:
            return None, 0
        else:
            dialog_sprite = []
            font = pygame.font.Font("multimedia/fonts/comic.ttf", 15);
            keylist = dictDialog.keys()
            for i, dialog in enumerate(keylist):
                
                if dialog == 'begin':
                    begin_dialog = []
                    for txt in dictDialog['begin']:
                        text_surface = font.render(txt, True, (0, 0, 255))
                        begin_dialog.append(text_surface)
                    dialog_sprite.append(begin_dialog)
                    
                if dialog == 'quest':
                    quest_dialog = []
                    for txt in dictDialog['quest']:
                        text_surface = font.render(txt, True, (0, 0, 255))
                        quest_dialog.append(text_surface)
                    dialog_sprite.append(quest_dialog)
                    
                if dialog == 'end':
                    end_dialog = []
                    for txt in dictDialog['end']:
                        text_surface = font.render(txt, True, (0, 0, 255))
                        end_dialog.append(text_surface)
                    dialog_sprite.append(end_dialog)
        
        return dialog_sprite, len(dialog_sprite)
    


class Player(GameEntity):
    def __init__(self, stage, sprite, rect, cfgentity):
        GameEntity.__init__(self, stage, sprite, rect, cfgentity)
        self.humor = ["normal",  -1]
        
        
        self.rect.center = self.stage.startpoint
        

        action_attack = actions.BasicAttack(self, self.aspd)
        action_second_attack = actions.SecondaryAttack(self, self.aspd)
        action_interact = actions.Interact(self, .5)
        action_active_item = actions.ActiveItem(self, 3.0)
        
        action_docking01 = actions.Docking_01(self, 1.)
        action_docking02 = actions.Docking_02(self, 1.)
        
        
        self.actions.add_action(action_attack)
        self.actions.add_action(action_second_attack)
        self.actions.add_action(action_interact)
        self.actions.add_action(action_active_item)  
        self.actions.add_action(action_docking01)  
        self.actions.add_action(action_docking02)  
        
        
        self.last_pos = self.rect.center
    
    def hitten(self,  atq):
        GameEntity.hitten(self,  atq)
        self.humor = ["hitten",  20]
        
        
    
    def set_stage(self, stage):
        self.stage = stage
    
    def render(self, surface):
        GameEntity.render(self, surface)
    
    def set_direction(self, direction):
        if direction != Vector2(0,0):
            self.last_direction = direction
        self.direction = direction

    
    def choose_option(self):
        pass
    
    def explode(self):
        GameEntity.explode(self)
        sprite = load_sprite_mainsheet("efflapide01")
        lapide = ElementBuilder(type = "Lapide", stage = self.stage, sprite = sprite, position = self.rect.center)
        self.stage.add_element(lapide)
    
    def process(self, time_passed, walls):
        
#         if self.rect.centerx < 0 or self.rect.centerx > self.stage.stage_surface.get_width() or self.rect.centery < 0 or self.rect.centery > self.stage.stage_surface.get_height():
#             self.rect.center = self.last_pos
        
        GameEntity.process(self, time_passed, walls)
        if self.rect.centerx < 0 or self.rect.centerx > self.stage.stage_surface.get_width() or self.rect.centery < 0 or self.rect.centery > self.stage.stage_surface.get_height():
            self.rect.center = self.last_pos
            #self.rect.center = self.stage.startpoint
        
        
        self.actions.update(time_passed)
#         if self.talking:
#             self.choose_option()
#             return
    
        
        self.update_position(time_passed)
#         if self.rect.centerx < 0 or self.rect.centerx > self.stage.stage_surface.get_width() or self.rect.centery < 0 or self.rect.centery > self.stage.stage_surface.get_height():
#             self.rect.center = self.last_pos
        
        self.last_pos = self.rect.center
    
    def update_position(self, time):
        """ Update player position """
#         if direction:
#             self.direction = direction
        
        ''' se o personagem se mover mais rapido pra esquerda do que pra direita
            arredondar o valor de update pra um inteiro ou  descomentar abaixo: time = 0.02'''
        #time = 0.02
        update = self.direction * time * self.speed
        if self.acting == None:
            #self.rect.center += update
            ''' testando dessa forma para tentar consertar a velocidade de movimentos 
            que esta mais rapido pra esquerda e norte do que pra direita e sul'''
            self.rect.centerx += int(round(update[0]))
            self.rect.centery += int(round(update[1]))
        
        
#         """ Collision Detection """
#         self.collision = [False]*9
#         for block in walls:
#             self.check_collision(block)
#         
        
        # Ajusta a celula do SPRITE
        self.update_sprite(self.direction, time)
        
    
    
    
    
    def get_position(self):
        return self.rect.center
    

class IA_Entity(GameEntity):
    def __init__(self, stage, sprite, rect, cfgentity, spot):
        GameEntity.__init__(self, stage, sprite, rect, cfgentity, spot)
        GameEntity.load_attributes(self, cfgentity.status)
        self.rect.center = self.spot
        self.last_pos = self.rect.center
        
        self.target_id = None
        self.active_direction = None
        self.position = None
        self.destination = None
        self.acting = None
        self.running = False
        
    
    def update_position(self, time):
        
        ''' se o personagem se mover mais rapido pra esquerda do que pra direita
            arredondar o valor de update pra um inteiro ou  descomentar abaixo: time = 0.02 '''
        #time = 0.02
        
        # Update player position
        vec_to_destination = self.destination - Vector2(self.rect.center)
        distance_to_destination = vec_to_destination.get_length()
        heading = vec_to_destination.get_normalized()
        
        # isso eh o que faz o npc fugir
        if self.running:
            heading = -heading
            
        # according to my wish, nobody can attack and walking freelly
        if self.acting == None:
            travel_distance = min(distance_to_destination, time * self.speed)
            #self.rect.center += travel_distance * heading 
            
            ''' testando dessa forma para tentar consertar a velocidade de movimentos 
            que esta mais rapido pra esquerda e norte do que pra direita e sul'''
            update = travel_distance * heading
            self.rect.centerx += int(round(update[0]))
            self.rect.centery += int(round(update[1]))
            
        
        
        self.direction = heading
        if heading != Vector2(0,0):
            self.last_direction = heading
        
        # salva posicao
        self.last_pos = self.rect.center
        
        # Ajusta a celula do SPRITE
        self.update_sprite(heading, time)
        
    
    def process(self, time_passed, walls):
        GameEntity.process(self, time_passed, walls)
        self.actions.update(time_passed)
        self.brain.think()
        
        if self.speed > 0. and self.rect.center != self.destination:
            self.update_position(time_passed)
        if self.acting == "attack":
            self.act(1, time_passed)
        elif self.acting == "attack02":
            self.act(2, time_passed)
        

        

class Enemy(IA_Entity):
    def __init__(self, stage, sprite, rect, cfgentity, spot):
        IA_Entity.__init__(self, stage, sprite, rect, cfgentity, spot)
 
        self.destination = self.rect.center
        self.rect.center = self.spot
        
        self.target_id = None
        
        action_attack = actions.BasicAttack(self, self.aspd)
        action_active_item = actions.ActiveItem(self, 2.5)
        
        self.actions.add_action(action_attack)
        self.actions.add_action(action_active_item)
        
        exploring_state = EntityStateExploring(self)
        hunting_state = EntityStateHunting(self)
        dead_state = EntityStateDead(self)
        
        exploring_state_boss = EntityStateExploring02(self)
        hunting_state_boss = EntityStateHunting02(self)
        
        self.brain.add_state(exploring_state)
        self.brain.add_state(hunting_state)
        self.brain.add_state(dead_state)
        
        self.brain.add_state(exploring_state_boss)
        self.brain.add_state(hunting_state_boss)
    
    
    
    def render(self, surface):
        GameEntity.render(self, surface)
    
    
    def process(self, time_passed, walls):
        IA_Entity.process(self, time_passed, walls)
        if self.rect.centerx < 0 or self.rect.centerx > self.stage.stage_surface.get_width() or self.rect.centery < 0 or self.rect.centery > self.stage.stage_surface.get_height():
            self.life = 0
            return


class NPC(IA_Entity):
    def __init__(self, stage, sprite, rect, cfgentity, spot):
        IA_Entity.__init__(self, stage, sprite, rect, cfgentity, spot)
        self.destination = self.rect.center
        self.rect.center = self.spot
        
        self.target_id = None
        roaming_state = EntityStateRoaming(self)
        running_state = EntityStateRunning(self)
        dead_state = EntityStateDead(self)
        
        self.brain.add_state(roaming_state)
        self.brain.add_state(running_state)
        self.brain.add_state(dead_state)
        self.target_id = None
    
    
    def explode(self):
        IA_Entity.explode(self)
        sprite = load_sprite_mainsheet("efflapide01")
        lapide = ElementBuilder(type = "Lapide", stage = self.stage, sprite = sprite, position = self.rect.center)
        self.stage.add_element(lapide)
    
    def render(self, surface):
        GameEntity.render(self, surface)
    
    def hitten(self, atq):
        IA_Entity.hitten(self, atq)
        player = self.stage.get_entity_by_name("player") 
        if player:
            #player_pos = Vector2(player.rect.center) 
            if Vector2(self.rect.center).get_distance_to(player.rect.center) > player.vision:
                vec_to_destination = Vector2(player.rect.center) - Vector2(self.rect.center)
                heading = vec_to_destination.get_normalized()
                warning = pygame.image.load("multimedia/windows/warning.png").convert_alpha()
                warning_signal = ElementBuilder("WarningSignal", stage = self.stage, sprite = warning, position = player.rect.center - heading*350)
                
                self.stage.add_element(warning_signal)
                #self.stage.blit(warning, heading*100)
    
#     def process(self, time_passed, walls):
#         GameEntity.process(self, time_passed, walls)
#         self.brain.think()
#         
#         if self.speed > 0. and self.rect.center != self.destination:
#             self.update_position(time_passed, walls)
#         if self.acting:
#             action, beg, end, ad, atqsprite = self.attack(time_passed)
#             if action:
#                 attack_effect = Attack_Effect(self.stage, self.name, atqsprite, beg, end, 0, ad, 0)
#                 self.stage.add_element(attack_effect)


