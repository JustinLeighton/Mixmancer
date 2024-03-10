import pygame
from typing import Callable
from mixmancer.exceptions import InvalidVolumeError, InvalidChannelError
import os


class Mixer:
    """Pygame music mixer"""

    def __init__(self):
        self.sfx_volume = 0.5
        self.active_sound_effects: list[pygame.mixer.Sound] = []  # Keep track of active sound effects
        self.current_track: str = ""

    def play_music(self, music_path: str):
        """Plays an .mp3 file through pygame music mixer"""
        self.current_track = music_path
        pygame.mixer.music.load(self.current_track)
        pygame.mixer.music.play()

    def get_current_track(self, max_length: int = 15) -> str:
        """Returns current music track playing"""
        file_name = os.path.basename(self.current_track)
        if len(file_name) > max_length:
            return file_name[:max_length] + "..."
        return file_name

    def play_sfx(self, sfx_path: str):
        """Plays an .wav file through pygame mixer"""
        sound_effect = pygame.mixer.Sound(sfx_path)
        sound_effect.set_volume(self.sfx_volume)
        sound_effect.play()
        self.active_sound_effects.append(sound_effect)  # Keep track of active sound effect

    def stop_sfx_sounds(self):
        """Stops all active sound effects"""
        for sound_effect in self.active_sound_effects:
            sound_effect.stop()
        self.active_sound_effects.clear()  # Clear the list of active sound effects

    def set_volume(self, volume_string: str, channel: str):
        """Convert input to float then pass to set_music_volume

        Args:
            volume_string (str): string representation of a float from 0.0 to 1.0
            channel (str): Accepts either "music" or "sfx"

        Raises:
            InvalidVolumeError: If the volume is not between 0 and 1.
            InvalidChannelError: If the channel is neither "music" nor "sfx".
        """
        try:
            volume = float(volume_string)
            if not 0 <= volume <= 1:
                raise InvalidVolumeError("Volume must be between 0 and 1")
        except ValueError:
            raise InvalidVolumeError("Invalid volume value: " + volume_string)

        if channel not in ["music", "sfx"]:
            raise InvalidChannelError("Invalid channel: " + channel)

        volume_setter_method: dict[str, Callable[[float], None]] = {
            "music": self.set_music_volume,
            "sfx": self.set_sfx_volume,
        }
        volume_setter_method[channel](volume)

    def set_music_volume(self, volume: float):
        """Set pygame mixer music volume.

        Args:
            volume (float): Volume of music from 0 to 1

        Raises:
            ValueError: If the volume is outside the valid range [0, 1].
        """
        if 0 <= volume <= 1:
            pygame.mixer.music.set_volume(volume)
        else:
            raise ValueError("Volume must be between 0 and 1")

    def set_sfx_volume(self, volume: float):
        """Set pygame mixer volume

        Args:
            volume (float): Volume of music from 0 to 1

        Raises:
            ValueError: If the volume is outside the valid range [0, 1].
        """
        if 0 <= volume <= 1:
            self.sfx_volume = volume
        else:
            raise ValueError("Volume must be between 0 and 1")
