    
# -*- coding: UTF-8 -*-



## IMPORTS 
import pygame
from pygame.locals import *
from sys import exit
import constants


import os, sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(__file__))
    #os.path.dirname(os.path.abspath(__file__))


#print( 'os.getcwd is', os.getcwd() )

#from gameEntities.gameEntity import *
#from gameStages.stage import *
#from gameStages.stageElements import *
from gameControls.maincontrol import *

import utils.quickGenerator
from utils.gameUtil import *
import gameconfig.configLoader
#from utils.mixer import CentralMixer
import utils.mixer
#Sfrom utils.mixer import music_load,  music_play
#from utils.windows import exitWindow, QuestBox, ExitMenu

from utils import quickGenerator
## 




## IS ANDROID PLATAFORM ?
try:
    import android
except ImportError:
    android = None

## 

FPS = 60
intro = True
paused = False

WINDOW = "windowed"
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
#pygame.mixer.pre_init(44100, -16, 2, 1024*4)
#cm = CentralMixer(44100, -16, 2, 1024*4)
utils.mixer.init(44100, -16, 2, 1024*4)
#gameconfig.configLoader.init("gameconfig/config.json")
gameconfig.configLoader.init("gameconfig/DATA.mut")
quickGenerator.init()
clock = pygame.time.Clock()
gameicon = pygame.image.load("icon.png")
pygame.display.set_icon(gameicon)


#if android:
#    android.init()
#    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

def text_objects(text, font):
    textSurface = font.render(u'%s' %text, True, BLACK)
    return textSurface, textSurface.get_rect()


obj01 = pygame.image.load("multimedia/sprites/obj01.png").convert_alpha()
obj02 = pygame.image.load("multimedia/sprites/obj02.png").convert_alpha()
speed = -8
anima_x = 400
anima_y = 230
cell_x = 1
cell_y = 1
def intro_animation(surface):
    global anima_x
    global anima_y
    global speed
    global cell_x
    global cell_y
    surface.blit(obj01, (anima_x, anima_y),(cell_x * 32, cell_y * 64,32,64))
    surface.blit(obj02, (anima_x - speed*5, anima_y+32),(cell_x * 32, cell_y * 32,32,32))
    anima_x += speed
    if anima_x < -64:
        speed = 8
        cell_y  = 0
        anima_y = 280
    if anima_x > (SCREEN_SIZE[0] + 64):
        speed = -8
        cell_y = 1
        anima_y = 230
    
    cell_x += 1
    if cell_x > 8:
        cell_x = 2
        
    

bg_intro = pygame.image.load("multimedia/windows/bg_intro.png").convert_alpha()
bg_intro = pygame.transform.scale(bg_intro, SCREEN_SIZE)
utils.mixer.music_load("multimedia/soundtrack/opening.ogg")
utils.mixer.music_play(-1, 0.0)
def game_intro():
    global intro
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        #screen.fill(WHITE)
        screen.blit(bg_intro, (0,0))
        
        intro_animation(screen)
        
        #largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 80)
        #TextSurf, TextRect = text_objects("My Monograph", largeText)
        #TextRect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
        #screen.blit(TextSurf, TextRect)
        mouse_pos = pygame.mouse.get_pos()
        button_02(u"Começar!!", SCREEN_SIZE[0]/3, SCREEN_SIZE[1]-180, bg_button_green_01, bg_button_green_02, screen, mouse_pos, main_loop)
        button_02(u"Opções!!", SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-180, bg_button_blue_01, bg_button_blue_02, screen, mouse_pos, options)
        button_02(u"Fechar!!", SCREEN_SIZE[0]/3 * 2, SCREEN_SIZE[1]-180, bg_button_red_01, bg_button_red_02, screen, mouse_pos, quit_game)
        button_02(u"Manual!!", SCREEN_SIZE[0]/10*9, SCREEN_SIZE[1]-240, bg_button_blue_01, bg_button_blue_02, screen, mouse_pos, manual)
        button_02(u"Créditos!!", SCREEN_SIZE[0]/10*9, SCREEN_SIZE[1]-180, bg_button_blue_01, bg_button_blue_02, screen, mouse_pos, credits)
        
        pygame.display.update()
        clock.tick(15)

bg_manual = pygame.image.load("multimedia/windows/bg_how_to.png").convert_alpha()
def manual():
    manual = True
    screen.blit(bg_manual,(0,0))
    while manual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        #screen.fill(WHITE)
        
        mouse_pos = pygame.mouse.get_pos()
        
        button_02("Voltar!!", SCREEN_SIZE[0]-300, SCREEN_SIZE[1]/8 * 7, bg_button_red_01, bg_button_red_02, screen, mouse_pos, game_intro)
        
        pygame.display.update()
        clock.tick(30)


bg_credits = pygame.image.load("multimedia/windows/bg_credits.png").convert_alpha()
def credits():
    manual = True
    screen.blit(bg_credits,(0,0))
    while manual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        #screen.fill(WHITE)
        
        mouse_pos = pygame.mouse.get_pos()
        
        button_02("Voltar!!", SCREEN_SIZE[0]/6 * 5, SCREEN_SIZE[1]/8 * 7, bg_button_red_01, bg_button_red_02, screen, mouse_pos, game_intro)
        
        pygame.display.update()
        clock.tick(30)


failed_zone = pygame.image.load("multimedia/windows/failed_zone.png").convert_alpha()
def play_again():
    global intro
    intro = True
    
    failed_rect = failed_zone.get_rect()
    failed_rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/4 )
    
    
    
    
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    proceed()
        
#         largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 80)
#         TextSurf, TextRect = text_objects("Você falhou!!", largeText)
#         TextRect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/5)
#         screen.blit(TextSurf, TextRect)
        screen.blit(failed_zone, failed_rect)
        
        
        mouse_pos = pygame.mouse.get_pos()
        button_02(u"Continue!!", SCREEN_SIZE[0]/3, SCREEN_SIZE[1]-100, bg_button_green_01, bg_button_green_02, screen, mouse_pos, proceed)
        #button_02(u"Recomeçar!!", SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-100, bg_button_green_01, bg_button_green_02, screen, mouse_pos, main_loop)
        button_02(u"Sair!!", SCREEN_SIZE[0]/3*2, SCREEN_SIZE[1]-100, bg_button_red_01, bg_button_red_02, screen, mouse_pos, game_intro)
        
        pygame.display.update()
        clock.tick(10)


def proceed():
#     mygame.load_last_SavePoint()
#     pygame.mixer.music.unpause()
    main_loop(True)


def button(msg,x,y,w,h,ic,ac, action = None):
    global intro
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
#     if x+w > mouse[0] > x and y+h > mouse[1] > y:
#         pygame.draw.rect(screen, ac,(x,y,w,h))
#     else:
#         pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    
    if textRect.collidepoint(mouse):
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    screen.blit(textSurf, textRect)



bg_button_red_01 = pygame.image.load("multimedia/windows/red_button_01.png")
bg_button_red_02 = pygame.image.load("multimedia/windows/red_button_02.png")
bg_button_green_01 = pygame.image.load("multimedia/windows/green_button_01.png")
bg_button_green_02 = pygame.image.load("multimedia/windows/green_button_02.png")
bg_button_blue_01 = pygame.image.load("multimedia/windows/blue_button_01.png")
bg_button_blue_02 = pygame.image.load("multimedia/windows/blue_button_02.png")


right_button_01 = pygame.image.load("multimedia/windows/right_button_01.png")
right_button_02 = pygame.image.load("multimedia/windows/right_button_02.png")

left_button_01 = pygame.image.load("multimedia/windows/left_button_01.png")
left_button_02 = pygame.image.load("multimedia/windows/left_button_02.png")

#rect_button = bg_button_red_01.get_rect()

def button_02(msg,x,y,bt1,bt2, surface, mouse_relative_pos, action = None):
    
    click = pygame.mouse.get_pressed()
    
    smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (x, y )
    rect_button = bt1.get_rect()
    rect_button.center = (x,y)
    
    if rect_button.collidepoint(mouse_relative_pos):
        surface.blit(bt2, rect_button)
        if click[0] == 1 and action != None:
            action()
    else:
        surface.blit(bt1, rect_button)

    surface.blit(textSurf, textRect)
    

def button_03_pressed(x,y,bt1,bt2, surface, mouse_relative_pos, action = None):
    
    rect_button = bt1.get_rect()
    rect_button.center = (x,y)
    
    if rect_button.collidepoint(mouse_relative_pos):
        if pygame.mouse.get_pressed()[0] == 0 and action != None:
            surface.blit(bt2, rect_button)
            action()
    else:
        surface.blit(bt1, rect_button)

def button_03(x,y,bt1, surface):
    
    rect_button = bt1.get_rect()
    rect_button.center = (x,y)
    
    surface.blit(bt1, rect_button)

def button_04(msg,x,y,bt1,bt2, surface, mouse_relative_pos, mouse_click,  action = None):
    
    click = pygame.mouse.get_pressed()
    
    smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (x, y )
    rect_button = bt1.get_rect()
    rect_button.center = (x,y)
    
    if rect_button.collidepoint(mouse_relative_pos):
        surface.blit(bt2, rect_button)
        if mouse_click == 1 and action != None:
            action()
    else:
       surface.blit(bt1, rect_button)

    surface.blit(textSurf, textRect)

#def has_joystick():
#    if pygame.joystick.get_count() > 0:
#        joystick = pygame.joystick.Joystick(0)
#        joystick.init()
#    
#    if joystick:
#        name = joystick.get_name()
#        if name.count('stick'):
#            return joystick
#    else:
#        pygame.joystick.quit()
#        return None



def choose_control():
    #if android:
    #    return AndroidControl()
    #
    #elif has_joystick():
    #    return JoyStickControl(has_joystick())
    #
    #else:
    return KeyBoardControl()

def up_volume():
    
    atual_vol = utils.mixer.get_music_volume() + 0.10
    if atual_vol > 1:
        atual_vol = 1
    
    utils.mixer.set_music_volume(atual_vol)
    
def down_volume():
    
    atual_vol = utils.mixer.get_music_volume() - 0.10
    if atual_vol < 0:
        atual_vol = 0
    
    utils.mixer.set_music_volume(atual_vol)

def up_sound_effect():
    
    atual_vol = utils.mixer.get_sound_volume() + 0.10
    if atual_vol > 1:
        atual_vol = 1
    
    utils.mixer.set_sound_volume(atual_vol)

def down_sound_effect():
    atual_vol = utils.mixer.get_sound_volume() - 0.10
    if atual_vol < 0:
        atual_vol = 0
    
    utils.mixer.set_sound_volume(atual_vol)


def quit_game():
    pygame.quit()
    sys.exit()


def unpause():
    global paused
    paused = False
    utils.mixer.music_unpause()

def change_game_level(level = None):
    if level == None:
        if constants.GAMELEVEL == "MEDIUM":
            constants.GAMELEVEL = "HARD"
        elif constants.GAMELEVEL == "HARD":
            constants.GAMELEVEL = "MEDIUM"
    else:
        constants.GAMELEVEL = level

def game_level_set_hard():
    constants.GAMELEVEL = "HARD"

def game_level_set_normal():
    constants.GAMELEVEL = "NORMAL"

bg_options = pygame.image.load("multimedia/windows/bg_options.png").convert_alpha()
def options():
    opt = True
    
    
    largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    
    while opt:
        mouse_click = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = 1
        #screen.fill(WHITE)
        
        options_bg = bg_options.copy()
        mouse_pos = pygame.mouse.get_pos()
        gamelevel = largeText.render(str(constants.GAMELEVEL),  True,  BLACK,  GRAY)
        
        button_04(u"Dificuldade!!", SCREEN_SIZE[0]/7, SCREEN_SIZE[1]/6, bg_button_blue_01, bg_button_blue_02, options_bg, mouse_pos, mouse_click,  change_game_level)
        options_bg.blit(gamelevel,  (SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/7))
        
        button_02("Voltar!!", SCREEN_SIZE[0]/6 * 5, SCREEN_SIZE[1]/8 * 7, bg_button_red_01, bg_button_red_02, options_bg, mouse_pos, game_intro)
        
        screen.blit(options_bg,(0,0))
        pygame.display.update()
        clock.tick(30)
    

bg_pause = pygame.image.load("multimedia/windows/bg_pause.png").convert_alpha()
inventory = pygame.image.load("multimedia/windows/inventory.png").convert_alpha()
bg_config = pygame.image.load("multimedia/windows/configuration.png").convert_alpha()
bg_records = pygame.image.load("multimedia/windows/records_small.png").convert_alpha()
mutuca_icon = pygame.image.load("multimedia/windows/mutuca_icon.png")
balde_icon = pygame.image.load("multimedia/windows/balde_icon.png")
mutuca_coin = pygame.image.load("multimedia/windows/mutuca_coin.png")
#bg_pause = pygame.transform.scale(bg_pause, SCREEN_SIZE)
def pause(render_inventory, process_inventory):
    global paused
    paused = True
    utils.mixer.music_pause()
    largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    
    invent_rect = inventory.get_rect()
    invent_rect.center = (bg_pause.get_width()/2, bg_pause.get_height() * 0.65)
    
    hotkeys_rect = invent_rect.copy()
    hotkeys_rect.center = (bg_pause.get_width()/6, bg_pause.get_height() * 0.65)
    
    
    records_rect = bg_records.get_rect()
    records_rect.center = (bg_pause.get_width()/6, bg_pause.get_height() * 0.2)
    
    status_rect = bg_records.get_rect()
    status_rect.center = (bg_pause.get_width()/2, bg_pause.get_height() * 0.2)
    
    bg_records_copy = bg_records.copy()
    draw_score(bg_records_copy, largeText)
    
    
    bg_config_rect = bg_config.get_rect()
    bg_config_rect.center = (bg_pause.get_width()/6 * 5, bg_pause.get_height()/2)
    
    
    while paused:
        mouse = pygame.mouse.get_pos()
        x = mouse[0] - invent_rect.x
        y = mouse[1] - invent_rect.y
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    unpause()
        #screen.fill(GRAY)
        
        
        invent_copy = inventory.copy()
        inventory_pop_up = render_inventory(invent_copy, (x,y))
        
        hotkeys_copy = inventory.copy()
        mygame.show_hotkeys(hotkeys_copy)
        
        bg_config_copy = bg_config.copy()
        config_rect_copy = bg_config_copy.get_rect()
        config_rect_copy.center =  bg_config_rect.center
        bg_status_copy = bg_records.copy()
        
        
        mygame.render_status_bar(bg_status_copy)
        draw_config(bg_config_copy, largeText, (mouse[0] - config_rect_copy.x, mouse[1] - config_rect_copy.y), click)
        
        
#         bg_records_copy.blit(mutuca_icon, (bg_records_copy.get_width()/3, 20))
#         bg_records_copy.blit(mygame.score()[0], (bg_records_copy.get_width()/2, 25))
        
        bg_pause_copy = bg_pause.copy()
        bg_pause_copy.blit(invent_copy, invent_rect)
        bg_pause_copy.blit(hotkeys_copy, hotkeys_rect)
        bg_pause_copy.blit(bg_config_copy, bg_config_rect)
        bg_pause_copy.blit(bg_status_copy, status_rect)
        bg_pause_copy.blit(bg_records_copy, records_rect)
        
        if inventory_pop_up:
            bg_pause_copy.blit(inventory_pop_up, (mouse[0] - 150, mouse[1] - 50))
            #bg_pause_copy.blit(inventory_pop_up[0], inventory_pop_up[1].x + x, inventory_pop_up[1].y + y)
        
        screen.blit(bg_pause_copy, (0,0))
        
#         largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 80)
#         TextSurf, TextRect = text_objects("Paused", largeText)
#         TextRect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
#         screen.blit(TextSurf, TextRect)
        
#         process_inventory((mouse[0] + invent_rect.centerx, mouse[1] + invent_rect.centery), click)
        if click[0] == 1:
            process_inventory((x,y))
                
        #screen.blit(mygame.render_status_tab(),(0,0))
        

        
#         button_02("Continue!!", SCREEN_SIZE[0]-140, SCREEN_SIZE[1]-170, 100, 50,bg_button_green_01, bg_button_green_02, screen, unpause)
#         button_02("Quit!!", SCREEN_SIZE[0]-140, SCREEN_SIZE[1]-100, 100, 50, bg_button_red_01, bg_button_red_02, screen, quit_game)
        
        
#         smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
#         TextSurf, TextRect = text_objects("Volume: %.2f" %pygame.mixer.music.get_volume() , smallText)
#         button_02("UP", SCREEN_SIZE[0] - 200, 100, 80, 60, right_button_01, right_button_02, screen, up_volume)
#         button_02("DOWN", SCREEN_SIZE[0] - 140, 100, 80, 60, right_button_01, right_button_02, screen, down_volume)
#         TextRect.center = (SCREEN_SIZE[0] - 100, 80)
#         screen.blit(TextSurf,TextRect)
        
        
        #TextSurf, TextRect = text_objects("Volume: %.2f" %pygame.mixer.music.get_volume() , smallText)
        #button("UP", SCREEN_SIZE[0] - 240, 100, 80, 60, GREEN, BRIGHT_GREEN, up_sound_effect)
        #button("DOWN", SCREEN_SIZE[0] - 240, 180, 80, 60, GREEN, BRIGHT_GREEN, down_sound_effect)
        
        
        pygame.display.update()
        clock.tick(30)

def draw_score(surf, largeText):
    cfg_caption, cfg_caption_rect = text_objects(u'Pontuação', largeText )
    cfg_caption_rect.centerx = surf.get_width()/2
    cfg_caption_rect.top = 10
    surf.blit(cfg_caption, cfg_caption_rect)
    
    surf.blit(mutuca_icon, (surf.get_width()/20*2, 40))
    surf.blit(mygame.load_score()[0], (surf.get_width()/20*5, 45))
    
    surf.blit(balde_icon, (surf.get_width()/20*8, 40))
    surf.blit(mygame.load_score()[1], (surf.get_width()/20*11, 45))
    
    surf.blit(mutuca_coin, (surf.get_width()/20*14, 40))
    surf.blit(mygame.load_score()[2], (surf.get_width()/20*17, 45))
    
    
    
    cfg_caption, cfg_caption_rect = text_objects(u'Records do Jogo', largeText )
    cfg_caption_rect.centerx = surf.get_width()/2
    cfg_caption_rect.top = surf.get_height()/2
    surf.blit(cfg_caption, cfg_caption_rect)
    
    surf.blit(mutuca_icon, (surf.get_width()/20*2, 120))
    surf.blit(mygame.load_score()[3], (surf.get_width()/20*5, 125))
    
    surf.blit(balde_icon, (surf.get_width()/20*8, 120))
    surf.blit(mygame.load_score()[4], (surf.get_width()/20*11, 125))
    
    surf.blit(mutuca_coin, (surf.get_width()/20*14, 120))
    surf.blit(mygame.load_score()[5], (surf.get_width()/20*17, 125))

def draw_config(bg_config_copy, largeText, mouse_pos, click):
    
#     cfg_caption, cfg_caption_rect = text_objects("Configurações", largeText )
#     cfg_caption_rect.centerx = bg_config_copy.get_width()/2
#     cfg_caption_rect.top = 10
#     bg_config_copy.blit(cfg_caption, cfg_caption_rect)
    cfg_caption, cfg_caption_rect = text_objects(u'Configurações', largeText )
    cfg_caption_rect.centerx = bg_config_copy.get_width()/2
    cfg_caption_rect.top = 10
    bg_config_copy.blit(cfg_caption, cfg_caption_rect)
    
    
    button_02("Continue!!", bg_config_copy.get_width()/3, bg_config_copy.get_height()/8 * 6, bg_button_green_01, bg_button_green_02, bg_config_copy, mouse_pos, unpause)
    button_02("Quit!!", bg_config_copy.get_width()/3, bg_config_copy.get_height()/8 * 7, bg_button_red_01, bg_button_red_02, bg_config_copy, mouse_pos, game_intro)
    
    
    smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    TextSurf, TextRect = text_objects("Volumes:" , smallText)
    TextRect.center =  (bg_config_copy.get_width()/2,  bg_config_copy.get_height()/10 * 1.5)
    bg_config_copy.blit(TextSurf,TextRect)
    
    
    music_vol = utils.mixer.get_music_volume()
    TextSurf, TextRect = text_objects(u'Música: %s' %music_vol , smallText)
    TextRect.center =  (bg_config_copy.get_width()/2,  bg_config_copy.get_height()/6 * 1.5)
    bg_config_copy.blit(TextSurf,TextRect)
    
    effect_vol = utils.mixer.get_sound_volume()
    TextSurf, TextRect = text_objects(u'Efeitos: %s' %effect_vol , smallText)
    TextRect.center =  (bg_config_copy.get_width()/2,  bg_config_copy.get_height()/6 * 2)
    bg_config_copy.blit(TextSurf,TextRect)
    
    smallText = pygame.font.Font("multimedia/fonts/comic.ttf", 20)
    TextSurf, TextRect = text_objects(u'Vídeo:', smallText)
    TextRect.center =  (bg_config_copy.get_width()/2,  bg_config_copy.get_height()/10 * 4.5)
    bg_config_copy.blit(TextSurf,TextRect)
    next_video_mode = "Tela Cheia"
    if  WINDOW == "fullscreen":
        next_video_mode = "Janela"
    
    
    
    
    
    if click[0] == 1:
        button_03_pressed( bg_config_copy.get_width()/8, bg_config_copy.get_height()/6 * 1.5 , left_button_01, left_button_02, bg_config_copy, mouse_pos, down_volume)
        button_03_pressed( bg_config_copy.get_width()/8 * 7, bg_config_copy.get_height()/6 * 1.5, right_button_01, right_button_02, bg_config_copy, mouse_pos, up_volume)
        button_03_pressed( bg_config_copy.get_width()/8, bg_config_copy.get_height()/6 * 2, left_button_01, left_button_02, bg_config_copy, mouse_pos, down_sound_effect)
        button_03_pressed( bg_config_copy.get_width()/8 * 7, bg_config_copy.get_height()/6 * 2, right_button_01, right_button_02, bg_config_copy, mouse_pos, up_sound_effect)
        
        button_02( next_video_mode,  bg_config_copy.get_width()/2, bg_config_copy.get_height()/10 * 5.5 , bg_button_blue_01, bg_button_blue_02,  bg_config_copy, mouse_pos,  toggle_fullscreen)
        
    else:
        button_03( bg_config_copy.get_width()/8, bg_config_copy.get_height()/6 * 1.5 , left_button_01, bg_config_copy,)
        button_03( bg_config_copy.get_width()/8 * 7, bg_config_copy.get_height()/6 * 1.5, right_button_01, bg_config_copy)
        button_03( bg_config_copy.get_width()/8, bg_config_copy.get_height()/6 * 2, left_button_01, bg_config_copy)
        button_03( bg_config_copy.get_width()/8 * 7, bg_config_copy.get_height()/6 * 2, right_button_01, bg_config_copy)
        
        button_02( next_video_mode,  bg_config_copy.get_width()/2, bg_config_copy.get_height()/10 * 5.5 , bg_button_blue_01, bg_button_blue_02,  bg_config_copy, mouse_pos,  toggle_fullscreen)
        #button_03( bg_config_copy.get_width()/2, bg_config_copy.get_height()/10 * 5.5 , bg_button_blue_02, bg_config_copy)
   


def toggle_fullscreen():
    global WINDOW
    global SCREEN_SIZE
    if WINDOW == "windowed":
        pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)
        WINDOW = "fullscreen"
    else:
        pygame.display.set_mode(SCREEN_SIZE)
        WINDOW = "windowed"



def play_message(message):
    global paused
    paused = True
    #pygame.mixer.music.pause()
    """ Adiciona mais um frame antes de mostrar a mensagem!"""
    mygame.process(0.1, maincontrol.get_direction(), maincontrol.get_action(), screen)
    
    
    bg_message = pygame.image.load("multimedia/windows/message_bg.png").convert_alpha()
    
    
    if isinstance(message, pygame.Surface):
        bg_message = message
        bg_rect = message.get_rect()
        
#         msg_rect = message.get_rect()
#         msg_rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
#         bg_message.blit(message, msg_rect)
    
    else:
        bg_rect = bg_message.get_rect()
        largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 80)
        normalText = pygame.font.Font("multimedia/fonts/comic.ttf", 25)
        
        paragraph = 1
        for text in message:
            #TextSurf, TextRect = text_objects(txt, normalText)
            TextSurf, TextRect= text_objects(text, normalText)
            TextRect.center = (bg_rect.centerx, bg_rect.y + 40 * paragraph)
            bg_message.blit(TextSurf, TextRect)
            paragraph += 1
    
    bg_rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    unpause()
            
        #screen.fill(GRAY)
        screen.blit(bg_message, bg_rect)
#         largeText = pygame.font.Font("multimedia/fonts/comic.ttf", 80)
#         TextSurf, TextRect = text_objects("Missão", largeText)
#         TextRect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/6)
#         screen.blit(TextSurf, TextRect)
        mouse_pos = pygame.mouse.get_pos()
        button_02("Continue!!", SCREEN_SIZE[0]-200, SCREEN_SIZE[1]-100, bg_button_green_02, bg_button_green_01, screen, mouse_pos, unpause)
        
        
        pygame.display.update()
        clock.tick(10)





pygame.time.set_timer(USEREVENT+1, 400)
font = pygame.font.Font("multimedia/fonts/comic.ttf", 15)
def show_fps():
    text = int(clock.get_fps())
    fps_surface = font.render("fps:"+str(text), True, (0, 60, 100))
    return fps_surface


    
##########  MAIN ############# 

## in test

mygame = Game()
#mygame.set_Stage("chptown01")


##


maincontrol = choose_control()

atual_fps = show_fps()
window_caption = u'Mutuca  - Beta Version 0.6'
pygame.display.set_caption(u'%s' %window_caption)
    
itemdock = pygame.image.load("multimedia/windows/dock_comandos.png").convert_alpha()


#slot_dock_01 = pygame.image.load("multimedia/windows/slot_dock_01.png")
humor_normal = pygame.image.load("multimedia/windows/humor_normal.png").convert_alpha()
humor_hitten = pygame.image.load("multimedia/windows/humor_hitten.png").convert_alpha()
def render_dock():
    dock = mygame.player.inventory.render_to_dock(itemdock.copy(),  None)
    if mygame.player.humor[1] == -1:
        dock.blit(humor_normal, (dock.get_width()/20, dock.get_height()/5))
    else:
        dock.blit(humor_hitten, (dock.get_width()/20, dock.get_height()/5))
        mygame.player.humor[1] -= 1
    
    mygame.render_dock_status_bar(dock)
    return dock

def main_loop(proceed = False):
    utils.mixer.music_stop()
    
    if proceed:
        mygame.load_last_SavePoint()
        utils.mixer.music_rewind()
    else:
        del mygame.cleared_maps[:]
        mygame.clear_score()
        mygame.set_Stage("map01")
        mygame.player = None
        mygame.load_Player()
        #mygame.cleared_maps = []
    utils.mixer.set_music_volume(utils.mixer.get_music_volume())
    #pygame.mixer.music.set_volume(0.5)
    global atual_fps
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause(mygame.render_inventory, mygame.process_inventory)
            if event.type == USEREVENT+1:
                atual_fps = show_fps()
        if mygame.game_over(screen):
            play_again()
        if mygame.message:
            play_message(mygame.read_message())
            
        
        maincontrol.process()
        
        # Take the time and convert it to seconds
        time_passed = clock.tick(FPS)
        time_passed_seconds = time_passed / 1000.0
        screen.fill(BLACK)
        """TESTE: QUANDO O FPS FICA MUITO BAIXO PODE ATRAPALHAR A MOVIMENTACAO E DETECCAO DE COLISOES
            PORTANTO TOU USANDO ESSE 'FREIO'!!
            PARA VOLTAR AO NORMAL: COMENTAR AS DUAS LINHAS ABAIXO E DESCOMENTAR A TERCEIRA."""
        secured_time_passed = min(time_passed_seconds,  0.05)
        mygame.process(secured_time_passed, maincontrol.get_direction(), maincontrol.get_action(), screen)
        #mygame.process(time_passed_seconds, maincontrol.get_direction(), maincontrol.get_action(), screen)
        screen.blit(atual_fps, (SCREEN_SIZE[0] - 60, 20))
        screen.blit(render_dock(), (0,  SCREEN_SIZE[1] - itemdock.get_height()))
        
        
        
        #if android:
        #    maincontrol.render(screen)
        
        
        pygame.display.update()


# def close_mygame():
#     mygame.player = None
#     mygame.stage = None
#     mygame = None
#     game_intro()

game_intro()
#main_loop()
