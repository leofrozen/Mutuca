    
# -*- coding: UTF-8 -*-


from gameobjects_local.vector2 import Vector2
from random import randint
###############

class State(object):
    
    def __init__(self, name):
        self.name = name
    
    def do_actions(self):
        pass
    
    def check_conditions(self):
        pass
    
    def entry_actions(self):
        pass
    
    def exit_actions(self):
        pass


class StateMachine(object):
    
    def __init__(self):
        
        self.states = {}
        self.active_state = None
    
    def add_state(self, state):
        
        self.states[state.name] = state
    
    def think(self):
        
        if self.active_state is None:
            return
        
        self.active_state.do_actions()
        
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
    
    
    def set_state(self, new_state_name):
        
        if self.active_state is not None:
            self.active_state.exit_actions() 
        
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()
    


#########



class EntityStateExploring(State):
    def __init__(self, entity):
        
        State.__init__(self, "exploring")
        self.entity = entity
    
    
    def random_destination(self, surface):
        w, h = surface
        self.entity.destination = Vector2(randint(w-500, w+500), randint(h-500, h+500))
        #self.entity.destination = Vector2(randint(0, w), randint(0, h))
    
    def do_actions(self):
        
        if randint(1, 20) == 1:
            self.random_destination(self.entity.spot)
    
    def check_conditions(self):
        #entity_position = Vector2(self.entity.rect.center)
        
        target = self.entity.stage.get_close_entity(self.entity.rect.center, "player", self.entity.vision)
        if target:
            if Vector2(self.entity.rect.center).get_distance_to(target.rect.center) < self.entity.vision and target.life > 0:
                self.entity.target_id = target.id
                return "hunting"
        # Caso nao encontre um player, procure por npcs 
        target = self.entity.stage.get_close_entity(self.entity.rect.center, "npc", self.entity.vision)
        if target:
            if Vector2(self.entity.rect.center).get_distance_to(target.rect.center) < self.entity.vision and target.life > 0:
                self.entity.target_id = target.id
                return "hunting" 
        
        if self.entity.life <= 0:
            return "dead"
        return None
    
    def entry_actions(self):
        #print "starting exploring state"
        self.entity.speed = self.entity.speed_base + randint(-30, 30)
        self.random_destination(self.entity.spot)



class EntityStateHunting(State):
    
    def __init__(self, entity):
        State.__init__(self, "hunting")
        self.entity = entity
        self.got_kill = False
    
    def do_actions(self):
        entity_position = Vector2(self.entity.rect.center)
        
        target = self.entity.stage.get_entity(self.entity.target_id)
        
        if target is None:
            return 
        
        
        self.entity.destination = Vector2(target.rect.center)
        
        if entity_position.get_distance_to(target.rect.center) < self.entity.equip_set.weapon.total_range:
            
            self.entity.acting = "attack"
        

            
            if target.life <= 0:
                self.got_kill = True
     
    def check_conditions(self):
        
        if self.got_kill:
            print "morre ai troxa"
            return "exploring"
        
        target = self.entity.stage.get_entity(self.entity.target_id)
        
        # If the target has been killed the return to exploring state
        if target is None:
            self.entity.target_id = None
            return "exploring"
        
        # If the target gets far enough away, return to exploring state
        if Vector2(target.rect.center).get_distance_to(self.entity.rect.center) > self.entity.vision :
            return "exploring"
        
        if self.entity.life <= 0:
            return "dead"
        
        return None
    
        
    def entry_actions(self):
        #print "starting hunting state"
        self.entity.speed = self.entity.speed_base + randint(0, 30)
    
    def exit_actions(self):
        self.entity.acting = None
        self.got_kill = False



class EntityStateWaiting(State):
    
    def __init__(self, entity):
        State.__init__(self, "waiting")
        self.entity = entity
    
    def do_actions(self):
        #print self.name
        if self.entity.rect.center != self.entity.spot:
            return
        
        entity_position = Vector2(self.entity.rect.center)
        
        target = self.entity.stage.get_close_entity(self.entity.rect.center, "player", self.entity.vision)
        if target == None:
            return
        
        if entity_position.get_distance_to(target.rect.center) < self.entity.vision:
            self.lookathim(target.rect.center)
        else:
            self.cell_dir = 0
            self.cell_pos = 0
        
        #target = self.entity.stage.get(self.entity.target_id)
        
        
        
        
    
    def check_conditions(self):
        target = self.entity.stage.get_close_entity(self.entity.rect.center, "player", self.entity.vision)
        if target:
            if Vector2(self.entity.rect.center).get_distance_to(target.rect.center) < self.entity.vision and target.life > 0 and self.entity.talking:
                self.entity.target_id = target.id
                return "talking"
        return None
        
        if self.entity.talking:
            
            return "talking"
        
        
    def entry_actions(self):
        self.entity.destination = self.entity.spot
    
    def exit_actions(self):
        pass
    
    def lookathim(self, target_pos):
        pass


class EntityStateTalking(State):
    
    def __init__(self, entity):
        State.__init__(self, "talking")
        self.entity = entity
    
    def do_actions(self):
        self.entity.destination = self.entity.spot
        
        entity_position = Vector2(self.entity.rect.center)
        if entity_position != self.entity.spot:
            print entity_position
            print self.entity.spot
            
            return
        
        else:
            self.cell_dir = 0
            self.cell_pos = 0
        
        #self.entity.to_talk()
    
    def check_conditions(self):

        target = self.entity.stage.get_entity(self.entity.target_id)
        
        # If the target has been killed the return to waiting state
        if target is None:
            self.entity.target_id = None
            return "waiting"
        
        # If the target gets far enough away, return to waiting state
        if Vector2(target.rect.center).get_distance_to(self.entity.rect.center) > self.entity.vision :
            return "waiting"
        
        return None
             
        
        
    def entry_actions(self):
        self.entity.destination = self.entity.spot
    
    def exit_actions(self):
        self.entity.talking = False



class EntityStateRoaming(State):
    def __init__(self, entity):
        
        State.__init__(self, "roaming")
        self.entity = entity
    
    
    def random_destination(self, surface):
        w, h = surface
        self.entity.destination = Vector2(randint(w-500, w+500), randint(h-500, h+500))
    
    def do_actions(self):
        
        if randint(1, 30) == 1:
            self.random_destination(self.entity.spot)
    
    def check_conditions(self):
#         target = self.entity.stage.get_close_entity(self.entity.rect.center, "player", self.entity.vision)
#         if target:
#             if Vector2(self.entity.rect.center).get_distance_to(target.rect.center) < self.entity.vision and target.life > 0:
#                 self.entity.target_id = target.id
#                 return "hunting"
#         
        target = self.entity.stage.get_close_entity(self.entity.rect.center, "enemy", self.entity.vision)
        if target:
            if Vector2(self.entity.rect.center).get_distance_to(target.rect.center) < self.entity.vision and target.life > 0:
                self.entity.target_id = target.id
                return "running"
        if self.entity.life <= 0:
            return "dead"
        
        return None
    
    def entry_actions(self):
        #print "starting roaming state"
        self.entity.speed = self.entity.speed_base + randint(-30, 10)
        self.random_destination(self.entity.spot)



class EntityStateRunning(State):
    
    def __init__(self, entity):
        State.__init__(self, "running")
        self.entity = entity
        self.got_safe = False
    
    def do_actions(self):
        entity_position = Vector2(self.entity.rect.center)
        
        target = self.entity.stage.get_entity(self.entity.target_id)
        
        if target is None:
            return 
        
        
        self.entity.destination =  Vector2(target.rect.center)
        
        if entity_position.get_distance_to(target.rect.center) < 150.:
            #self.got_safe = False
            self.entity.running = True
            self.entity.to_talk(20, [u"Socooorro!!"])
            
            # If the enemy is dead
            if target.life <= 0:
                self.got_safe = True
        else:
            self.got_safe = True
        
     
    def check_conditions(self):
        
        if self.got_safe:
            self.entity.running = False
            return "roaming"
        
        target = self.entity.stage.get_entity(self.entity.target_id)
        
        # If the target has been killed the return to exploring state
        if target is None:
            self.entity.target_id = None
            return "roaming"
        
        # If the target gets far enough away, return to exploring state
        if Vector2(target.rect.center).get_distance_to(self.entity.rect.center) > 150 :
            return "roaming"
        
        if self.entity.life <= 0:
            return "dead"
        
        return None
    
        
    def entry_actions(self):
        #print "starting running state"
        self.entity.speed = self.entity.speed_base + randint(10, 30)
    
    def exit_actions(self):
        self.entity.acting = None
        self.got_safe = False


class EntityStateDead(State):
    
    def __init__(self, entity):
        
        State.__init__(self, "dead")
        self.entity = entity
        
        self.knockout_time = 0
    
    def do_actions(self):
        self.knockout_time += 0.2
    
    def check_conditions(self):
#         if self.entity.life > 0:
#             self.entity.revive()
#             return "roaming"
        if self.knockout_time > 5:
            if self.entity.type == "npc":
                self.entity.stage.npc_dead = self.entity.rect.center
            if self.entity.type == "enemy":
                self.entity.stage.mutuca_dead += 1
            self.entity.explode()
            self.entity.stage.remove_entity(self.entity)
        
    def entry_actions(self):
        self.entity.inventory.drop()
        self.knockout_time = 1
        ## sprite de morte
    
    def exit_actions(self):
        self.knockout_time = 0
    


class EntityStateExploring02(State):
    def __init__(self, entity):
        
        State.__init__(self, "boss_exploring")
        self.entity = entity
    
    
    def random_destination(self, surface):
        w, h = surface
        self.entity.destination = Vector2(randint(w-500, w+500), randint(h-500, h+500))
        #self.entity.destination = Vector2(randint(0, w), randint(0, h))
    
    def do_actions(self):
        
        if randint(1, 20) == 1:
            self.random_destination(self.entity.spot)
    
    def check_conditions(self):
        #entity_position = Vector2(self.entity.rect.center)
        
        target = self.entity.stage.get_close_entity(self.entity.rect.center, "player", self.entity.vision)
        if target:
            if Vector2(self.entity.rect.center).get_distance_to(target.rect.center) < self.entity.vision and target.life > 0:
                self.entity.target_id = target.id
                return "boss_hunting"
        # Caso nao encontre um player, procure por npcs 
        target = self.entity.stage.get_close_entity(self.entity.rect.center, "npc", self.entity.vision)
        if target:
            if Vector2(self.entity.rect.center).get_distance_to(target.rect.center) < self.entity.vision and target.life > 0:
                self.entity.target_id = target.id
                return "boss_hunting" 
        
        if self.entity.life <= 0:
            return "dead"
        return None
    
    def entry_actions(self):
        #print "starting exploring state"
        self.entity.speed = 80. + randint(-30, 30)
        self.random_destination(self.entity.spot)



class EntityStateHunting02(State):
    
    def __init__(self, entity):
        State.__init__(self, "boss_hunting")
        self.entity = entity
        self.got_kill = False
    
    def do_actions(self):
        entity_position = Vector2(self.entity.rect.center)
        
        target = self.entity.stage.get_entity(self.entity.target_id)
        
        if target is None:
            return 
        
        
        self.entity.destination = Vector2(target.rect.center)
        
        if entity_position.get_distance_to(target.rect.center) < self.entity.equip_set.weapon.total_range:
            self.entity.acting = "attack"
        elif entity_position.get_distance_to(target.rect.center) < self.entity.equip_set.special_item.total_range and self.entity.mana > 40:
            self.entity.acting = "attack02"

            # If the spider is dead, move it back to the nest
            if target.life <= 0:
                self.got_kill = True
     
    def check_conditions(self):
        
        if self.got_kill:
            print "morre ai troxa"
            return "boss_exploring"
        
        target = self.entity.stage.get_entity(self.entity.target_id)
        
        # If the target has been killed the return to exploring state
        if target is None:
            self.entity.target_id = None
            return "boss_exploring"
        
        # If the target gets far enough away, return to exploring state
        if Vector2(target.rect.center).get_distance_to(self.entity.rect.center) > 200 :
            return "boss_exploring"
        
        if self.entity.life <= 0:
            return "dead"
        
        return None
    
        
    def entry_actions(self):
        #print "starting hunting state"
        self.speed = 100. + randint(0, 50)
    
    def exit_actions(self):
        self.entity.acting = None
        self.got_kill = False










# estados de maquina para um fazendeiro: 
# buscar feno
# alimentar o gado
# buscar agua
# levar agua ao gado
# descansar




