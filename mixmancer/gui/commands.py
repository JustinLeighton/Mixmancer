import pygame

def stop_sfx_sounds():
    pygame.mixer.stop()

def set_music_volume(volume):
    pygame.mixer.music.set_volume(float(volume)) 