import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from presenters import Presenter, TkinterPresenter
import pygame as pg

class TkinterGUI(Presenter):
    def __init__(self, retriever):
        self.tp = TkinterPresenter(retriever)
        
        self.root = tk.Tk()
        
        self.label_bird_name = tk.Label(
            self.root, 
            text=self.tp.text_stimulus[self.tp.cur_bird][self.tp.cur_bird_text_idx],
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
        self.get_image(self.tp.image_filenames[self.tp.cur_bird][self.tp.cur_bird_image_idx], True)
        print('self.cur_bird: ', self.tp.cur_bird)
        print('self.cur_bird_image_idx: ', self.tp.cur_bird_image_idx)
        self.get_audio(self.tp.audio_filenames[self.tp.cur_bird][self.tp.cur_bird_image_idx])
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
            
    def update_media(self):        
        self.label_bird_name.config(text=self.tp.text_stimulus[self.tp.cur_bird][self.tp.cur_bird_text_idx])
        self.get_image(self.tp.image_filenames[self.tp.cur_bird][self.tp.cur_bird_image_idx])
        self.get_audio(self.tp.audio_filenames[self.tp.cur_bird][self.tp.cur_bird_image_idx])


    def get_entry(self):
            user_response = self.entry.get()
            print('user_response: ', user_response, len(user_response))
            print('self.cur_bird_text: ', self.tp.cur_bird_text, len(self.tp.cur_bird_text))
            user_response = self.tp.format_for_response(user_response)
            correct_response = self.tp.format_for_response(self.tp.cur_bird_text)
            if user_response == correct_response:
                self.show_consequence_message('Good!!!!')
                self.tp.change_stimuli(True)
                
            else:
                self.show_consequence_message('Bad!')
                self.tp.change_stimuli(False)
            
            self.update_media()
        
    def generate_tk(self, stimuli, correct_response):
        self.label.config(text=stimuli)      

    def present(self, stimuli, correct_response):
        self.generate_tk(stimuli, correct_response)
