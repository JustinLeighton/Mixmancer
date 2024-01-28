# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:12:55 2023

@author: Justin Leighton
"""

from pygame import mixer
import os


class music_manager():
    def __init__(self):
        mixer.init()
    
    
    def check_for_file(self, file: str) -> str:
        self.files = [x for x in os.listdir('mp3') if x.split('.')[-1].lower() in ['mp3', 'wav']]
        for f in self.files:
            if f.split('.')[0].lower() == file:
                return f
        return ''
   
    
    def print_help(self):
        print('Music currently available:', *set([x.split('.')[0] for x in self.files]), sep='\n\t')
        

    def play(self, music_input: str):
        music_path = self.check_for_file(music_input)
        mixer.music.stop()
        mixer.music.unload()
        if music_path:
            mixer.music.load(f'mp3\{music_path}')
            mixer.music.play(-1)
        else:
            self.print_help()