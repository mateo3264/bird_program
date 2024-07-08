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
        self.birds = [bird for bird in self.image_filenames]
        print('tp: ', self.birds)
        print('tp: ', self.image_filenames)
        self.audio_filenames = self.retriever.get_audio_filenames()
        self.text_stimulus = self.retriever.get_text_stimulus()
        self.root = tk.Tk()
        self.cur_bird_idx = 0
        self.cur_bird_image_idx = 0
        self.cur_bird = self.birds[self.cur_bird_idx]
        self.cur_bird_text_idx = 0
        self.cur_bird_text = self.text_stimulus[self.cur_bird][self.cur_bird_text_idx]
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
        self.get_image(self.image_filenames[self.cur_bird][self.cur_bird_image_idx], True)
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

    def get_image(self, image_filename, first_time=False):
        image = Image.open(image_filename)
        width = int(1.5*image.width) if image.width < 500 else 800
        height = int(1.5*image.height) if image.height < 500 else 800
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
                self.cur_bird_idx = (self.cur_bird_idx + 1) % len(self.birds)
                self.cur_bird_image_idx = 0
                self.cur_bird_text_idx = 0
                self.cur_bird = self.birds[self.cur_bird_idx]
                self.cur_bird_text = self.text_stimulus[self.cur_bird][self.cur_bird_text_idx]
            else:
                self.cur_bird_image_idx += 1
                self.cur_bird_text_idx += 1

            
            
            self.label_bird_name.config(text=self.text_stimulus[self.cur_bird][self.cur_bird_text_idx])
            self.get_image(self.image_filenames[self.cur_bird][self.cur_bird_image_idx])

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
    chosen_birds = get_birds_by_string_length()
    tp = TkinterPresenter(Retriever(chosen_birds, 'image'))
    tp.present()
    