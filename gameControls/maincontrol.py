import pygame
from gameobjects_local.vector2 import Vector2
from pygame.locals import *


# CONSTANTS
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

#

class GameControl(object):
    def __init__(self):
        self.key_direction = Vector2(0,0)
        self.action = None
        #self.key_direction = None
    
    def get_direction(self):
        return self.key_direction
    
    def get_action(self):
        return self.action
    
    def render(self):
        pass
    
    def process(self):
        pass
    


class AndroidControl(GameControl):
    def __init__(self):
        GameControl.__init__(self)
        
        #self.screen = pygame.Surface((480,320))
        # movement Buttons
        self.rect_right = pygame.Rect(70, 265, 25, 25)
        self.rect_left = pygame.Rect(20, 265, 25, 25)
        self.rect_up = pygame.Rect(45, 240, 25, 25)
        self.rect_down = pygame.Rect(45, 290, 25, 25)
        
        self.rect_top_right = pygame.Rect(50, 250, 25, 25)
        self.rect_top_left = pygame.Rect(10, 250, 25, 25)
        self.rect_down_right = pygame.Rect(50, 290, 25, 25)
        self.rect_down_left = pygame.Rect(10, 290, 25, 25)
        
        # Action Buttons
        self.rect_actionA = pygame.Rect(385, 265, 25, 25)
        self.rect_actionB = pygame.Rect(435, 265, 25, 25)
        self.rect_actionC = pygame.Rect(410, 240, 25, 25)
        self.rect_actionD = pygame.Rect(410, 290, 25, 25)
        
        self.action_button_image = pygame.image.load("gameControls/images/action_button.png").convert_alpha()
        self.action_button_pressed_image = pygame.image.load("gameControls/images/action_button_pressed.png").convert_alpha()
        
        self.left_button_image = pygame.image.load("gameControls/images/left_button.png").convert_alpha()
        self.right_button_image = pygame.image.load("gameControls/images/right_button.png").convert_alpha()
        self.up_button_image = pygame.image.load("gameControls/images/up_button.png").convert_alpha()
        self.down_button_image = pygame.image.load("gameControls/images/down_button.png").convert_alpha()


    def render(self, surface):
            # Move buttons
        surface.blit(self.left_button_image, self.rect_left)
        surface.blit(self.right_button_image, self.rect_right)
        surface.blit(self.up_button_image, self.rect_up)
        surface.blit(self.down_button_image, self.rect_down)
        
        
            # Actions Buttons Controls
        surface.blit(self.action_button_image, self.rect_actionA)
        surface.blit(self.action_button_image, self.rect_actionB)
        surface.blit(self.action_button_image, self.rect_actionC)
        surface.blit(self.action_button_image, self.rect_actionD)
        
    def process(self):
        
        mouse_pos = (x, y) = pygame.mouse.get_pos()
        
        self.key_direction = Vector2(0,0)
        self.action = None

        #self.direction = self.last_direction
        if self.rect_up.collidepoint(mouse_pos):
            self.key_direction.y = -1
            #self.last_direction = self.direction
        elif self.rect_down.collidepoint(mouse_pos):
            self.key_direction.y = +1
            #self.last_direction = self.direction
        
        elif self.rect_right.collidepoint(mouse_pos):
            self.key_direction.x = +1
            #self.last_direction = self.direction
        elif self.rect_left.collidepoint(mouse_pos):
            self.key_direction.x = -1
            #self.last_direction = self.direction
        
        # Diagonal movements
#         elif rect_top_right.collidepoint(mouse_pos):
#             self.direction = "up_right"
#             self.last_direction = self.direction
#             
#         elif rect_top_left.collidepoint(mouse_pos):
#             self.direction = "up_left"
#             self.last_direction = self.direction
#             
#         elif rect_down_right.collidepoint(mouse_pos):
#             self.direction = "down_right"
#             self.last_direction = self.direction
#             
#         elif rect_down_left.collidepoint(mouse_pos):
#             self.direction = "down_left"
#             self.last_direction = self.direction
        
        else:
            self.direction = None
        
#         if direction: 
#             return self.direction
        
        mouse_pos = (x, y) = pygame.mouse.get_pos()
        self.action = None
        #print "action button on (%i,%i)" %mouse_pos
        if self.rect_actionA.collidepoint(mouse_pos):
            self.action = "action1"

            #self.direction = self.last_direction
        elif self.rect_actionB.collidepoint(mouse_pos):
            self.action = "action2"

            #self.direction = self.last_direction
        elif self.rect_actionC.collidepoint(mouse_pos):
            self.action = "action3"

            #self.direction = self.last_direction
        elif self.rect_actionD.collidepoint(mouse_pos):
            self.action = "action4"

            #self.direction = self.last_direction



class KeyBoardControl(GameControl):
    def __init__(self):
        GameControl.__init__(self)
    
    
    def process(self):
        
        pressed_keys = pygame.key.get_pressed()
        self.key_direction = Vector2(0,0)
        self.action = None
        
        
        
        if pressed_keys[K_LEFT]:
            self.key_direction.x = -1
        elif pressed_keys[K_RIGHT]:
            self.key_direction.x = +1
        if pressed_keys[K_UP]:
            self.key_direction.y = -1
        elif pressed_keys[K_DOWN]:
            self.key_direction.y = +1
        
        
        self.key_direction.normalize()
        
        
        
        if pressed_keys[K_q]:
            self.action = "action1"
        elif pressed_keys[K_w]:
            self.action = "action2"
        elif pressed_keys[K_e]:
            self.action = "action3"
        elif pressed_keys[K_r]:
            self.action = "action4"
        elif pressed_keys[K_v]:
            self.action = "action5"
        elif pressed_keys[K_b]:
            self.action = "action6"
        
    
class JoyStickControl(GameControl):
    def __init__(self, joystick):
        GameControl.__init__(self)
        self.joystick = joystick
    
    def process(self):
        
        self.key_direction = Vector2(0,0)
        self.action = None
        
        # get direction
#         if self.joystick.get_numhats() > 0:
#             axis_x, axis_y = self.joystick.get_hat(0)
#             print "pegando as paradas"
#  
#             if axis_x < 0:
#                 self.key_direction.x = -1
#             elif axis_x > 0:
#                 self.key_direction.x = +1
#             
#             if axis_y > 0:
#                 self.key_direction.y = -1
#             elif axis_y < 0:
#                 self.key_direction.y = +1
#             
#             
#         print "Hats values: ________________ (%f, %f)" %(axis_x, axis_y)
        
        
        if self.joystick.get_numaxes() >= 2:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)
            
        # solving joystick deadzones
        if abs(axis_x) < 0.1:
            axis_x = 0.
        if abs(axis_y) < 0.1:
            axis_y = 0.
            
        if axis_x < 0:
            self.key_direction.x = -1
        elif axis_x > 0:
            self.key_direction.x = +1
        
        if axis_y > 0:
            self.key_direction.y = +1
        elif axis_y < 0:
            self.key_direction.y = -1
        
 
#         if axis_x < 0:
#                 self.direction = LEFT
#         elif axis_x > 0:
#             self.direction = RIGHT
#         
#         elif axis_y > 0:
#             self.direction = DOWN
#         elif axis_y < 0:
#             self.direction = UP
        self.key_direction.normalize()
        
        
        # get action_buttons
        for button_no in xrange(self.joystick.get_numbuttons()):
            if self.joystick.get_button(button_no):
                if button_no == 0:
                    self.action = "action1"
                if button_no == 1:
                    self.action = "action2"
                if button_no == 2:
                    self.action = "action3"
                if button_no == 3:
                    self.action = "action4"


