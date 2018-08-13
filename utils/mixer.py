
    # Se eu ainda for compilar para android ... vale a pena verificar isso///
try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer



GENERAL_VOLUME = 0.5
SOUND_VOLUME = 0.2
MUSIC_VOLUME = 0.5


def init(frequency=44100, size=-16, channels=4, buffer=4096):
    mixer.pre_init(frequency, size, channels, buffer)
    global GENERAL_VOLUME
    global SOUND_VOLUME
    global MUSIC_VOLUME

def get_general_volume():
    return GENERAL_VOLUME

def get_sound_volume():
    return SOUND_VOLUME

def get_music_volume():
    return MUSIC_VOLUME

def set_general_volume(value):
    global GENERAL_VOLUME
    if value > 1:
        value = 1
    if value < 0:
        value = 0
    GENERAL_VOLUME = value

def set_sound_volume(value):
    global SOUND_VOLUME
    if value > 1:
        value = 1
    if value < 0.1:
        value = 0
    SOUND_VOLUME = value

def set_music_volume(value):
    global MUSIC_VOLUME
    if value > 1:
        value = 1
    if value < 0.1:
        value = 0
    MUSIC_VOLUME = value
    mixer.music.set_volume(MUSIC_VOLUME)

def play_effect(sound):
    global SOUND_VOLUME
    sound.set_volume(SOUND_VOLUME)
    sound.play()

def change_music(song):
    global MUSIC_VOLUME
    global MUSIC_VOLUME
    mixer.music.set_volume(MUSIC_VOLUME)

def music_load(file):
    mixer.music.load(file)

def music_play(arg1,  arg2):
    mixer.music.play(arg1, arg2)

def music_stop():
    mixer.music.stop()

def music_unpause():
    mixer.music.unpause()

def music_pause():
    mixer.music.pause()

def music_rewind():
    mixer.music.rewind()

class CentralMixer():
    def __init__(self, frequency=44100, size=-16, channels=4, buffer=4096):
        mixer.pre_init(frequency, size, channels, buffer)
        global GENERAL_VOLUME
        global SOUND_VOLUME
        global MUSIC_VOLUME
    
    def get_general_volume(self):
        return GENERAL_VOLUME
    
    def get_sound_volume(self):
        return SOUND_VOLUME
    
    def get_music_volume(self):
        return MUSIC_VOLUME
    
    def set_general_volume(self, value):
        if value > 1:
            value = 1
        if value < 0:
            value = 0
        GENERAL_VOLUME = value
    
    def set_sound_volume(self, value):
        if value > 1:
            value = 1
        if value < 0:
            value = 0
        SOUND_VOLUME = value
    
    def set_music_volume(self, value):
        global MUSIC_VOLUME
        if value > 1.0:
            value = 1.0
        if value < 0.0:
            value = 0.0
        MUSIC_VOLUME = value
        mixer.music.set_volume(MUSIC_VOLUME)
    
    def play_effect(self, sound):
        global SOUND_VOLUME
        sound.set_volume(SOUND_VOLUME)
        sound.play()
    
