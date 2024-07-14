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

class TkinterPresenter(Presenter):
    def __init__(self, retriever):
        self.retriever = retriever
        self.image_filenames = self.retriever.get_image_filenames()
        self.birds = self.retriever.birds#[bird for bird in self.image_filenames]
        self.seen_birds = []
        self.audio_filenames = self.retriever.get_audio_filenames()
        print('self.birds: ', self.birds)
        print('image_filenames: ', self.image_filenames)
        print('audio_filenames: ', self.audio_filenames)
        self.text_stimulus = self.retriever.get_text_stimulus()
        self.root = tk.Tk()
        self.cur_bird_idx = 0
        self.cur_bird_image_idx = 0
        self.cur_bird = self.birds[self.cur_bird_idx]
        self.learned_birds = read_json_file(FILENAME_LEARNED_BIRDS)
        if self.cur_bird in self.learned_birds:
            self.cur_bird_text_idx = -1
        else:
            self.cur_bird_text_idx = 0
        self.cur_bird_text = self.text_stimulus[self.cur_bird][0]
        self.label_bird_name = tk.Label(
            self.root, 
            text=self.text_stimulus[self.cur_bird][self.cur_bird_text_idx],
            font=('Courier', 30)
            )
        self.label_consequence = tk.Label(
            self.root, 
            text='',
            font=('Courier', 30)
            )
        insect_image = Image.open('insect.jpg')
        self.insect_image = insect_image.resize(size=(64, 64))
        self.insect_image = ImageTk.PhotoImage(self.insect_image)
        self.button_food = tk.Button(self.root, image=self.insect_image)
        self.button_food.pack()
        self.get_image(self.image_filenames[self.cur_bird][self.cur_bird_image_idx], True)
        print('self.cur_bird: ', self.cur_bird)
        print('self.cur_bird_image_idx: ', self.cur_bird_image_idx)
        self.get_audio(self.audio_filenames[self.cur_bird][self.cur_bird_image_idx])
        self.entry = tk.Entry(
            self.root,
            font=('Courier', 40)
            )
        self.button = tk.Button(self.root, text='Send', command=self.get_entry)
        self.label_bird_name.pack()
        self.label_consequence.pack()
        # self.image.pack()
        self.label_image.pack()
        self.entry.pack()
        self.entry.focus()
        self.button.pack()
        # self.root.withdraw()
        self.root.mainloop()

    def get_audio(self, audio_filename):
        pg.mixer.init()
        pg.mixer.music.load(audio_filename)
        pg.mixer.music.play()
    #ToDo: Maybe separate the conditional from the first part
    def get_image(self, image_filename, first_time=False):
        image = Image.open(image_filename)
        image_array = np.array(image)
        #ToDo: adapt the noise when transfering from image to audio
        image_noise = image_array + 0*np.random.normal(size=image_array.shape)
        image_noise = np.clip(image_noise, 0, 255).astype(np.uint8)
        image = Image.fromarray(image_noise)
        # image = image + image_noise
        width = int(1.5*image.width) if image.width < 500 else 600
        height = int(1.5*image.height) if image.height < 500 else 600
        image = image.resize((width, height))
        self.image = ImageTk.PhotoImage(image)

        if first_time:
            self.label_image = tk.Label(self.root, image=self.image)
            self.label_image.image = self.image
        else:
            self.label_image.config(image=self.image)
            self.label_image.image = self.image

    def show_consequence_message(self, message='Good!'):
        self.label_consequence.config(text=message)
        self.entry.delete(0, 'end')
        self.entry.focus()

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

            
            
            self.label_bird_name.config(text=self.text_stimulus[self.cur_bird][self.cur_bird_text_idx])
            self.get_image(self.image_filenames[self.cur_bird][self.cur_bird_image_idx])
            self.get_audio(self.audio_filenames[self.cur_bird][self.cur_bird_image_idx])

    def get_entry(self):
            usu_response = self.entry.get()
            print('usu_response: ', usu_response, len(usu_response))
            print('self.cur_bird_text: ', self.cur_bird_text, len(self.cur_bird_text))
            if usu_response.lower().strip() == self.cur_bird_text.lower().strip():
                self.show_consequence_message('Good!!!!')
                self.change_stimuli(True)
                
            else:
                self.show_consequence_message('Bad!')
                self.change_stimuli(False)
        
    def generate_tk(self, stimuli, correct_response):
        self.label.config(text=stimuli)      

    def present(self, stimuli, correct_response):
        self.generate_tk(stimuli, correct_response)





if __name__ == '__main__':
    chosen_birds = get_birds_by_string_length(2)
    tp = TkinterPresenter(Retriever(chosen_birds, 'image-audio'))
    tp.present()
    