import pygame


def stop_sfx_sounds():
    """Stop pygame mixer sounds from playing"""
    pygame.mixer.stop()


def set_music_volume(volume: str):
    """Set pygame mixer music volume.

    Args:
        volume (float): _description_
    """
    pygame.mixer.music.set_volume(float(volume))
