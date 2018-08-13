import thread
import pygame
from pygame.locals import *
from gameobjects_local.vector2 import Vector2
from math import fabs
#import pytmx_local
#from pytmx_local import *
from maploader import *
from gameconfig.configLoader import load_sprite_mainsheet
#from mako.util import sorted_dict_repr

# maximum size
SCREEN_SIZE = (960,540)

# default size
#SCREEN_SIZE = (640,480)


class Stage(object):
    def __init__(self, cfgstage):
        self.config = cfgstage
        self.name = cfgstage.name
        self.elements = {}
        self.element_id = 0
        
        self.entities = {}
        self.entity_id = 0
        self.npc_dead = None
        self.mutuca_dead = 0
        self.focos_taken = 0
        
        self.effects = {}
        self.effect_id = 0
        
        self.map = None
        #self.map_surface = None
        self.main_surface = None
        self.top_surface = None
        self.stage_surface = None
        self.walls = None
        self.bg_x = self.bg_y = 0
        
        # Get the songtrack
        self.soundtrack = cfgstage.soundtrack
        
        
        # Load the map and some atribuites
        self.load_map(cfgstage.mapfile)
        self.startpoint = cfgstage.startpoint
        self.bg_width, self.bg_height = self.map.get_size()
        
        # Stage process
        self.script = None
        self.vision = 540
    
    def start_stage(self):
        pass
    
    def load_map(self, map_file):
        self.map = GameMap(map_file)
        #self.map_surface = self.map.get_map_surface()
        self.main_surface, self.top_surface = self.map.get_map_surface()
        self.stage_surface = pygame.Surface(self.map.get_size())
        self.walls = self.map.get_walls()
        self.stop_playback()
        self.playback()
        #sortedwalls = sorted(self.walls, key=lambda thing: thing.centery)
        #self.walls = sortedwalls
#         for wall in self.walls:
#             print wall.center
        #print "Total de blocos: %s " %len(self.walls)
    
    def add_element(self, element):
        self.elements[self.element_id] = element
        element.id = self.element_id
        self.element_id += 1
    
    def remove_element(self, element):
        del self.elements[element.id]
    
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
    
    def remove_entity(self, entity):
        del self.entities[entity.id]
    
    def get_close_entity(self, position, name, range=100.):
        
        position = Vector2(position)
        
        for entity in self.entities.itervalues():
            if entity.name.count(name):
                distance = position.get_distance_to(entity.rect.center)
                if distance < range:
                    return entity
        return None
    
    def get_all_close_unity(self, position, range=100.):
        unity_list = []
        chat = []
        position = Vector2(position)
        for entity in self.entities.itervalues():
            distance = position.get_distance_to(entity.rect.center)
            if distance < range:
                unity_list.append(entity)
        for element in self.elements.itervalues():
            distance = position.get_distance_to(element.rect.center)
            if distance < range:
                if element.name == "text_box":
                    chat.append(element)
                else:
                    unity_list.append(element)
        
        return unity_list, chat
    
    
    def get_entity(self,entity_id):
        
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
    
    def get_npcs(self):
        npcs = []
        for entity in self.entities.itervalues():
            if entity.type == "npc":
                npcs.append(entity)
        if len(npcs) > 0:
            return npcs
        return False
    
    def get_entity_by_name(self,entity_name):
        
        for entity in self.entities.itervalues():
                if entity.name == entity_name:
                    return entity
        else:
            return None
    
    def is_ent_alive(self, type):
        if type == "Enemy":
            for entity in self.entities.itervalues():
                if entity.name.count("enemy"):
                    return True
            return False
    
    def is_elem_alive(self, type):
        if type == "Foco":
            for element in self.elements.itervalues():
                if element.name.count("foco"):
                    return True
            return False
    
    def how_many_entis(self):
        return len(self.entities)
    
    def hascollision_ent(self, ori):
        hitten_list = []
        for entity in self.entities.itervalues():            
            if ori.colliderect(entity.rect):
                #print "testa colisao"
                hitten_list.append(entity)
        if len(hitten_list) > 0:
            return hitten_list
        return None
    
    def hascollision_elem(self, ori):
        hitten_list = []
        for element in self.elements.itervalues():            
            if ori.colliderect(element.rect):
                #print "testa colisao"
                hitten_list.append(element)
        if len(hitten_list) > 0:
            return hitten_list
        return None
        
    
    # soft collision
    def soft_collision(self, ent, block):
        
        ent.collision[0] = block.collidepoint(ent.rect.topleft)
        ent.collision[1] = block.collidepoint(ent.rect.topright)
        ent.collision[2] = block.collidepoint(ent.rect.bottomleft)
        ent.collision[3] = block.collidepoint(ent.rect.bottomright)

        ent.collision[4] = block.collidepoint(ent.rect.midleft)
        ent.collision[5] = block.collidepoint(ent.rect.midright)
        ent.collision[6] = block.collidepoint(ent.rect.midtop)
        ent.collision[7] = block.collidepoint(ent.rect.midbottom)

        ent.collision[8] = block.collidepoint(ent.rect.center)
        
        
        """Solve the Collisions"""
        if ent.collision[4]:
            ent.rect.left = block.right
        if ent.collision[5]:
            ent.rect.right = block.left
        if ent.collision[6]:
            ent.rect.top = block.bottom
        if ent.collision[7]:
            ent.rect.bottom = block.top
        
        dx = fabs(ent.rect.centerx - block.centerx)
        dy = fabs(ent.rect.centery - block.centery)
        
        x_overlap = (ent.rect.width + block.width)*0.5 - dx
        y_overlap = (ent.rect.height + block.height)*0.5 - dy
        
        if ent.collision[0]:
            if x_overlap >= y_overlap:
                ent.rect.top = block.bottom
            else:
                ent.rect.left = block.right
        
        if ent.collision[1]:
            if x_overlap >= y_overlap:
                ent.rect.top = block.bottom
            else:
                ent.rect.right = block.left
        
        if ent.collision[2]:
            if x_overlap >= y_overlap:
                ent.rect.bottom = block.top
            else:
                ent.rect.left = block.right
        
        if ent.collision[3]:
            if x_overlap >= y_overlap:
                ent.rect.bottom = block.top
            else:
                ent.rect.right = block.left
    

    def block_of_process(self, i, entity, entilist, time_passed):
        #thread.start_new_thread(entity.process, (time_passed, self.walls))
        entity.process(time_passed, self.walls)
        for j, entity2 in enumerate(entilist):
            if i != j:
                entity.collision = [False]*9
                self.check_collision_enti(entity, entity2, time_passed)
        
        """ Walls Collision Detection """
        entity.collision = [False]*9
        for block in self.walls:
            self.soft_collision(entity, block)
    
    
    def process(self, time_passed):
        signal_list = []
        signal = self.script.process(time_passed)
        if signal:
            signal_list.append(signal)
        
        entilist = self.entities.values()
        for i, entity in enumerate(entilist):
            #thread.start_new_thread(self.block_of_process, (i, entity, entilist, time_passed))
            entity.process(time_passed, self.walls)
            for j, entity2 in enumerate(entilist):
                if i != j:
                    entity.collision = [False]*9
                    self.check_collision_enti(entity, entity2, time_passed)
             
            """ Walls Collision Detection """
            entity.collision = [False]*9
            for block in self.walls:
                self.soft_collision(entity, block)

                
        

        
#         for entity in self.entities.values():
#             entity.process(time_passed, self.walls)
        
        for element in self.elements.values():
            signal = element.process(time_passed)
            if signal:
                signal_list.append(signal)
        if signal_list:
            return signal_list
    
    
#     def check_collision_enti(self, ent1, ent2):
#         ent2.check_collision(ent1.rect)
    
    def check_collision_enti(self, ent1, ent2, time_passed):
        
        
        if ent1.rect.colliderect(ent2.rect):
            """ Soft Collision """
            self.soft_collision(ent1, ent2.rect)

            
#             """ Hard Collision """   It's not Working

#             impact1 = ent2.direction * time_passed * ent2.speed/10
#             impact2 = ent1.direction * time_passed * ent1.speed/10
#             ent1.set_position(ent1.rect.center + impact1)
#             ent2.set_position(ent2.rect.center + impact2)  

        
    
    def render(self, surface, position):
        
        # Renders the background image and other objects of the map
        self.stage_surface.blit(self.main_surface, (0, 0))
        
        
#         render_list = []         
#         
#         # Renders all entity on the level surface
#         for entity in self.entities.itervalues():
#             #entity.render(self.stage_surface)
#             render_list.append(entity)
#         
#         for element in self.elements.itervalues():
#             #element.render(self.stage_surface)
#             render_list.append(element)
#         
#         for i in sorted(render_list, key=lambda thing: thing.rect.centery):
#             i.render(self.stage_surface)  
#         
        close_unity, chat = self.get_all_close_unity(position, self.vision)

        for i in sorted(close_unity, key=lambda thing: thing.rect.centery):
            i.render(self.stage_surface)  
        
        
        # render the top surface over other surfaces
        self.stage_surface.blit(self.top_surface, (0,0))
        
        # rend the chat over all
        for i in sorted(chat, key=lambda thing: thing.rect.centery):
            i.render(self.stage_surface)
        
        # Capture a slice of the surface to blit on screen
        if SCREEN_SIZE[0]/2  <= position[0] and position[0] <= (self.bg_width - SCREEN_SIZE[0]/2):
            self.bg_x = position[0] - SCREEN_SIZE[0]/2
        elif (self.bg_width - SCREEN_SIZE[0]/2) <= position[0]:
            self.bg_x = (self.bg_width - SCREEN_SIZE[0])
        elif SCREEN_SIZE[0]/2 >= position[0]:
            self.bg_x = 0
        
        if SCREEN_SIZE[1]/2  <= position[1] and position[1] <= (self.bg_height - SCREEN_SIZE[1]/2):
            self.bg_y = position[1] - SCREEN_SIZE[1]/2
        elif (self.bg_height - SCREEN_SIZE[1]/2) <= position[1]:
            self.bg_y = (self.bg_height - SCREEN_SIZE[1])
        elif SCREEN_SIZE[1]/2 >= position[1]:
            self.bg_y = 0
        
        
        
        # Final blit on screen
        surface.blit(self.stage_surface, (0, 0), (self.bg_x, self.bg_y, self.bg_x + SCREEN_SIZE[0], self.bg_y + SCREEN_SIZE[1]))
    
    def playback(self, soundtrack = None):
        if soundtrack:
            try:
                pygame.mixer.music.load(soundtrack)
                pygame.mixer.music.play(-1, 0.0)
            except:
                print("Unknown erro! Maybe unable to read song file!")
        elif self.soundtrack:
            try:
                pygame.mixer.music.load(self.soundtrack)
                pygame.mixer.music.play(-1, 0.0)
            except:
                print("Unknown erro! Maybe unable to read song file!")
    def stop_playback(self):
        pygame.mixer.music.stop()
    

    def get_size(self):
        return self.bg_width, self.bg_height
    


class GameMap(object):
    def __init__(self, map_file):
        
        self.map_file = map_file
        self.walls = []
        self.size = None
        
        # in tests
        self.surface_list = []
        self.main_surface, self.top_surface = self.render()
        # 
        #self.map_surface = self.render()
        
        self.rect_list = []
        
        
    def get_size(self):
        return self.size
    
    
    def get_walls(self):
        
        #return self.walls
        return self.optimizewall()
        
        
        #return self.rect_list
    
    def get_map_surface(self):
        #return self.map_surface
        return self.main_surface, self.top_surface
    
    def render(self):
        
        #tmx_data = load_pygame(self.map_file, pixelalpha=True)
        tmx_data = MapLoader(self.map_file)
        
        tw = tmx_data.tilewidth
        th = tmx_data.tileheight
        gt = tmx_data.getTileImageByGid
        
        self.size = tmx_data.width * tw, tmx_data.height * th
        
        #self.map_surface = pygame.Surface(self.size)
        self.main_surface = pygame.Surface(self.size)
        self.top_surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        
        # Fill the background color
#         if tmx_data.background_color:
#             self.map_surface.fill(tmx_data.background_color)
#         
        
        # draw map tiles
        for layer in tmx_data.visibleLayers:
            index = 0
            
            
            if isinstance(layer, TiledLayer):
                if layer.name == "solid_objects":
                    # temporary surface 
                    layerSurface = pygame.Surface(self.size)
                    
                    for y in  range(0, layer.height):
                        for x in range(0, layer.width):
                            
                            if layer.data[index] != 0:
                                tile = gt[layer.data[index]]
                                
                                layerSurface.blit(tile, (x * tw, y * th))
                                
#                                 self.map_surface.blit(tile, (x * tw, y * th))
                                self.main_surface.blit(tile, (x * tw, y * th))
                                self.walls.append(pygame.Rect(x * tw, y * th, tw, th))
                            index +=1
                        
                            
            
                elif layer.name.count("top"):
                    # temporary surface 
                    layerSurface = pygame.Surface(self.size)
                    
                    for y in  range(0, layer.height):
                        for x in range(0, layer.width):
                             
                            if layer.data[index] != 0:
                                tile = gt[layer.data[index]]
                                
                                #layerSurface.blit(tile, (x * tw, y * th))
                                #self.map_surface.blit(tile, (x * tw, y * th))
                                
                                self.top_surface.blit(tile, (x * tw, y * th))
                            index +=1
                
                else:
                    # temporary surface 
                    layerSurface = pygame.Surface(self.size)
                    
                    for y in  range(0, layer.height):
                        for x in range(0, layer.width):
                             
                            if layer.data[index] != 0:
                                tile = gt[layer.data[index]]
                                
                                self.main_surface.blit(tile, (x * tw, y * th))
                            index +=1
            
            # add the new surface to the list
            #self.surface_list.append(layerSurface)
            
        #return self.map_surface
        return self.main_surface, self.top_surface
        
    
    def update_layer(self):
            pass
    
    
    def optimizewall(self):
        clonewalls = self.walls
        sortedwalls = sorted(clonewalls, key=lambda thing: thing.centery)
        w, h = self.size
        w = w/32
        h = h/32
        collpoint = [16,16]
        new_wall = []
        montedwalls = []
        
        for x in range(1,w+1):
            
            #print "##### Starting block X ######"
            collpoint[0] = (x*32 -16)
            for y in range(1, h+1):
            #    print "##### Starting block Y ######"
                
                collpoint[1] = (y*32 - 16)
                collided = False
                for i, block in enumerate(sortedwalls):
                    if block.collidepoint(collpoint):
                        new_wall.append(block)
                        collided = True
                        break
                        
                
                if len(new_wall) == 1 and collided == False or len(new_wall) == 1 and y >= h:
#                    print "apenas um block encontrado proximo a [%i,%i] ==> [%i,%i]" %(collpoint[0], collpoint[1], x,y)
                    new_wall = []
                     
                elif len(new_wall) > 1 and collided == False or len(new_wall) > 1 and y >= h:
#                    print "adicionando new_walls: %i blocks" %len(new_wall)
                    
                    wall = new_wall[0].unionall(new_wall)
                     
                    montedwalls.append(wall)
#                    print "new wall dimension - top: %i, bottom: %i, left: %i, right: %i" %(wall.top, wall.bottom, wall.left, wall.right)
                    for o in new_wall:
#                        print "removendo: ( %i , %i )" %(o.centerx, o.centery)
                        sortedwalls.remove(o)
                    
                    new_wall = []
                    wall = None
        
        
        
        #print " ###############  CRIANDO LINHAS HORIZONTAIS!! ############"
        collpoint = [16,16]
        for y in range(1,h+1):
            
            #print "##### Starting block X ######"
            collpoint[1] = (y*32 -16)
            for x in range(1, w+1):
            #    print "##### Starting block Y ######"
                
                collpoint[0] = (x*32 - 16)
                collided = False
                for block in sortedwalls:
                    if block.collidepoint(collpoint):
                        new_wall.append(block)
                        collided = True
                        break
                        
                
                if len(new_wall) == 1 and collided == False or len(new_wall) == 1 and y > h:
#                    print "apenas um block encontrado proximo a [%i,%i] ==> [%i,%i]" %(collpoint[0], collpoint[1], x,y)
                    new_wall = []
                     
                elif len(new_wall) > 1 and collided == False or len(new_wall) > 1 and y > h:
#                    print "adicionando new_walls: %i blocks" %len(new_wall)
                    
                    wall = new_wall[0].unionall(new_wall)
                     
                    montedwalls.append(wall)
 #                   print "new wall dimension - top: %i, bottom: %i, left: %i, right: %i" %(wall.top, wall.bottom, wall.left, wall.right)
                    for o in new_wall:
#                        print "removendo: ( %i , %i )" %(o.centerx, o.centery)
                        sortedwalls.remove(o)
                    
                    new_wall = []
                    wall = None
        
        
        overmonted = []
        new_wall = []
        wall = None
        
        
        
        #print " ###############  CRIANDO SUPER BLOCOS HORIZONTAIS!! ############"
        
        for y in range(1,h+1):
            newblock = None
            #print "##### Starting block Y ######"
            collpoint[1] = (y*32 -16)
            x = 1
            while x <= w+1:
            #    print "##### Starting block X %i ######" %x
                
                collpoint[0] = (x*32 - 16)
                collided = False
                for block in montedwalls:
                    if block.collidepoint(collpoint):
                        if len(new_wall) > 0:
                            if new_wall[-1].top == block.top and new_wall[-1].bottom == block.bottom:
  #                              print "blocos proximos: <%i - %i> <%i - %i >" %(new_wall[-1].left, new_wall[-1].right, block.left, block.right)
                                x = block.right/32
                                new_wall.append(block)
                                collided = True
                                break
                            else:
 #                               print "colidiu, mas nao presta"
                                x = new_wall[-1].right/32
                                collided = False
                                
                                
                                break
                                
                        else:
                            x = block.right/32
#                            print "primeiro new_wall"
                            new_wall.append(block)
                            collided = True
                            break
                
                x += 1
                

                
                if len(new_wall) == 1 and collided == False or len(new_wall) == 1 and y >= h:
#                    print "apenas um block encontrado proximo a [%i,%i] ==> [%i,%i]" %(collpoint[0], collpoint[1], x,y)
                    new_wall = []
                     
                elif len(new_wall) > 1 and collided == False or len(new_wall) > 1 and y >= h:
#                    print "adicionando new_walls: %i blocks" %len(new_wall)
                    
                    wall = new_wall[0].unionall(new_wall)
                    overmonted.append(wall)
#                    print "new wall dimension - top: %i, bottom: %i, left: %i, right: %i" %(wall.top, wall.bottom, wall.left, wall.right)
                    for o in new_wall:
#                        print "removendo: (%i,%i)" %(o.centerx, o.centery)
                        montedwalls.remove(o)
                    
                    new_wall = []
                    wall = None
            
        
        # Remova os comentarios para verificar o resultado da construcao dos blocos
#         for r in overmonted:
#             s = pygame.Surface(r.size)
#             s.fill((255,0,0))
#             self.main_surface.blit(s, (r.x, r.y))
#         for r in montedwalls:
#             s = pygame.Surface(r.size)
#             s.fill((0,255,0))
#             self.main_surface.blit(s, (r.x, r.y))
#         for r in sortedwalls:
#             s = pygame.Surface(r.size)
#             s.fill((0,0,255))
#             self.main_surface.blit(s, (r.x, r.y))
#         
#         
#         print "overmonted: %i" %len(overmonted)
#         print "montedwalls: %i" %len(montedwalls)
#         print "sortedwalls: %i" %len(sortedwalls)
        
        return overmonted + montedwalls + sortedwalls
    
#         print "montedwalls: %i" %len(montedwalls)
#         print "sortedwalls: %i" %len(sortedwalls)
#         return montedwalls + sortedwalls
    
