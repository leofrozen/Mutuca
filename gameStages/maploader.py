import json
import pygame

from pygame.locals import *
from sys import exit
# def load_map():
#     pass


class MapLoader(object):
    def __init__(self, filename):
        try:
            with open(filename) as mapfile:
                self.json_data = json.loads(mapfile.read())
                
                self.tilewidth = self.json_data["tilewidth"]
                self.tileheight = self.json_data["tileheight"]
                self.width = self.json_data["width"]
                self.height = self.json_data["height"]
                self.size = ( self.tilewidth * self.width, self.tileheight * self.height)
                
                self.layers = self.json_data["layers"]
                self.visibleLayers = self.layer_load(self.layers)
                
                self.tileSet = self.json_data["tilesets"]
                self.getTileImageByGid = self.tileset_load()
        
        except IOError:
            print("Cannot open map file {}".format(filename))
    
    def layer_visible(self, layers):
        return layers['visible']
    
    def layers_get_visibles(self, layers):
        visibleLayers = filter(self.layer_visible, self.layers)
        return visibleLayers

    def layers_get_by_name(self):
        layernames = {}
        indice = 0
        for l in self.layers:
            layernames[l['name']]=self.layers[indice]
            indice +=1
        return layernames
    
    def layer_load(self, layers):
        list_layers = []
        visibles = self.layers_get_visibles(layers)
        for l in visibles:
            list_layers.append(TiledLayer(l))
        return list_layers
    
#     def tileset_load(self):
#         tileImages = {}
#         tile_id = 1
#         for ts in self.tileSet:
#             ini = ts['firstgid']
#             
#             imagefile = ts['image']
#             #image = pygame.image.load("gameStages/maps/"+imagefile)
#             image = pygame.image.load("maps/"+imagefile).convert_alpha()
#             image_w = ts['imagewidth']
#             image_h = ts['imageheight']
#             
#             tilewidth = int(ts['tilewidth'])
#             tileheight = int(ts['tileheight'])
#             
#             
#             width = image_w / tilewidth
#             height = image_h / tileheight
#             
#             # contado que nao ha margens ou espacos entre os tiles
#             #margin = ts['margin']
#             #spacing = ts['spacing']
#             
#             for x in range(0, width):
#                 for y in range(0, height):
#                     surface = pygame.Surface((tilewidth, tileheight))
#                     surface.blit(image, (0,0), (x*tilewidth, y*tileheight, tilewidth, tileheight))
#                     #tileImages[ini]=surface
#                     
#                     #surface.blit(image, (0,0), (y*tileheight, x*tilewidth, tileheight, tilewidth))
#                     tileImages[tile_id]=surface
#                     ini += 1
#                     tile_id +=1
#         return tileImages
#
    
    def tileset_load(self):
        #tilesets = self.mapdict["tilesets"]
        tile_id = 1
        self.all_tiles = {}

        for tileset in self.tileSet:
            tilesurface = pygame.image.load("gameStages/maps/" + tileset["image"]).convert_alpha()
            for y in range(0, tileset["imageheight"], 32):
                for x in range(0, tileset["imagewidth"], 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    tile = tilesurface.subsurface(rect)
                    self.all_tiles[tile_id] = tile
                    tile_id += 1
        return self.all_tiles
    
    
    
    def updateLayers(self):
        pass
    



class TiledLayer(object):
    def __init__(self, dictLayer):
        self.data = dictLayer['data']
        self.x = dictLayer['x']
        self.y = dictLayer['y']
        self.width = dictLayer['width']
        self.height = dictLayer['height']
        self.name = dictLayer['name']
        self.opacity = dictLayer['opacity']
        self.type = dictLayer['type']
        self.visible = dictLayer['visible']




class TileSet(object):
    def __init__(self, dictTile):
        self.firstgid = dictTile['firstgid']
        self.image = dictTile['image']
        self.imageheight = dictTile['imageheight']
        self.imagewidth = dictTile['imagewidth']
        self.margin = dictTile['margin']
        self.name = dictTile['name']
        self.properties = dictTile['properties']
        self.spacing = dictTile['spacing']
        self.tileheight = dictTile['tileheight']
        self.tilewidth = dictTile['tilewidth']

