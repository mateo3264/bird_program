import matplotlib.pyplot as plt
import loaders
from PIL import Image, ImageTk
from difuminators import difuminate
import random
from abc import ABC, abstractmethod
import tkinter as tk
from formatters import format_name_for_save
import os
import pandas as pd
from retrievers import Retriever
from schedulers import get_birds_by_string_length
import pygame
import pygame as pg
import numpy as np
from registers import read_json_file
from configurations import FILENAME_LEARNED_BIRDS
import json


class Presenter(ABC):
    @abstractmethod
    def present(self, stimuli, correct_response):
        pass

class ConsolePresenter(Presenter):
    def present(self, stimuli, correct_response):
        print(10*'\n')
        usu_response = input(stimuli + ': ')

        if usu_response.lower() == correct_response:
            print('GOOD')
            
        
            return True
        return False

class TkinterPresenter:
    def __init__(self, retriever):
        self.retriever = retriever
        self.image_filenames = self.retriever.get_image_filenames()
        self.birds = self.retriever.birds#[bird for bird in self.image_filenames]
        self.seen_birds = []
        self.audio_filenames = self.retriever.get_audio_filenames()
        self.text_filenames = self.retriever.get_text_filenames()
        print('self.birds: ', self.birds)
        print('image_filenames: ', self.image_filenames)
        print('audio_filenames: ', self.audio_filenames)
        print('text_filenames: ', self.text_filenames)
        self.text_stimulus = self.retriever.get_text_stimulus() 
        self.text_descriptions = self.text_filenames
        self.cur_bird_idx = 0
        self.cur_bird_image_idx = 0
        self.cur_bird = self.birds[self.cur_bird_idx]
        self.learned_birds = read_json_file(FILENAME_LEARNED_BIRDS)
        if self.cur_bird in self.learned_birds:
            self.cur_bird_text_idx = -1
        else:
            self.cur_bird_text_idx = 0
        self.cur_bird_text = self.text_stimulus[self.cur_bird][0]


    def change_stimuli(self, is_response_correct):
        if is_response_correct:
            if self.text_stimulus[self.cur_bird][self.cur_bird_text_idx] == self.text_stimulus[self.cur_bird][-1]: 
                print('self.cur_bird: ', self.cur_bird)
                print('EXPRESSION: ', self.cur_bird in self.seen_birds)
                self.learned_birds[self.cur_bird] = True
                with open(FILENAME_LEARNED_BIRDS, 'w') as file:

                    json.dump(self.learned_birds, file)
                
                self.seen_birds.append(self.cur_bird)
                print('self.seen_birds: ', self.seen_birds)
                self.cur_bird_idx = (self.cur_bird_idx + 1) % len(self.birds)
                self.cur_bird_image_idx = 0
                self.cur_bird_text_idx = 0
                self.cur_bird = self.birds[self.cur_bird_idx]
                self.cur_bird_text = self.text_stimulus[self.cur_bird][0]
                
                if self.cur_bird in self.seen_birds or self.cur_bird in self.learned_birds:
                    print('ENTERED self.cur_bird in self.seen_birds')
                    self.cur_bird_text_idx = -1
                    #self.cur_bird_idx = random.randint(0, len(self.birds))
                    #self.cur_bird = self.birds[self.cur_bird_idx]
                    #self.cur_bird_text = self.text_stimulus[self.cur_bird][0]


            else:
                self.cur_bird_image_idx += 1
                self.cur_bird_text_idx += 1  

    def format_for_response(self, text):
        return text.lower().strip()
    