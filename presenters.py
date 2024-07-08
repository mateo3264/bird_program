import matplotlib.pyplot as plt
import loaders
from PIL import Image, ImageTk
from difuminators import difuminate
from registers import read_bird_names
import random
from abc import ABC, abstractmethod
import tkinter as tk
from formatters import format_name_for_save
import os
import pandas as pd



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
        image = image.resize((image.width, image.height))
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
        

        
            
        
        #     return True
        # return False
    

class Retriever:
    def __init__(self, birds, how):
        """Present an image, audio or image and audio
        The how parameter receives 'image', 'audio' or 'image-audio'"""
        self.birds = birds
        self.images = {bird:[] for bird in birds}
        self.current_image_idx = 0
        self.current_audio_idx = 0
        self.audios = []
        self.how = how
        self.image_filenames = {bird:[] for bird in birds}
        self.audio_filenames = []
        
        self.text_stimulus = {bird:difuminate(bird, 2) for bird in birds}
        

        self.consequetively_correct_responses = 0
        
        
        for bird_name in birds:
                print(bird_name)
                self.get_data_filenames(bird_name, 'image')
        self.url2obj()
        
        print(self.image_filenames)

    def get_data_filenames(self, bird_name, data_type):
        
        if self.how == ('image' or 'image-audio'):
            self.image_filenames[bird_name] = loaders.get_data(bird_name, 'image')
            print('image filenames key and value')
            print(bird_name, self.image_filenames[bird_name])
        elif self.how == ('audio' or 'image-audio'):
            self.audio_filenames.extend(loaders.get_data(bird_name, 'audio'))
        
        return True

    def get_image_filenames(self):
        return self.image_filenames
    
    def get_audio_filenames(self):
        return self.audio_filenames

    def get_text_stimulus(self):
        return self.text_stimulus
    
    def url2obj(self):
        
        for bird_name, img_filenames in self.image_filenames.items():
            for img_fn in img_filenames:
                #print('bird_name: ', bird_name)
                #print('img_fn: ', img_fn)
                img = Image.open(img_fn)
                self.images[bird_name].append(img)  
    
    
    def present(self):
        for bird_name in self.birds:
            last_was_correct = None
            self.consequetively_correct_responses = 0
            #print('self.images ', self.images)
            #print('bird_name: ', bird_name)
            for imgs in self.images[bird_name]:

                difumination_of_bird_name = self.text_stimulus[bird_name]
                self.current_image_idx = self.current_image_idx % len(difumination_of_bird_name)
                image = random.choice(self.images[bird_name])
                plt.figure(figsize=(10, 10))
                
                plt.axis('off')
                plt.imshow(image)
                plt.show()
                
                stimuli = difumination_of_bird_name[self.current_image_idx]
                correct_response = bird_name.lower()
                # is_correct = self.consequence.present(stimuli,  correct_response)
                # last_was_correct = is_correct
                # if is_correct:
                #     if last_was_correct:
                #         self.consequetively_correct_responses += 1
                #     if self.consequetively_correct_responses == 5:
                #         self.current_image_idx = 0
                #         break    
                #     self.current_image_idx += 1

                    
                


birds = read_bird_names()

#chosen_birds = [random.choice(birds) for i, bird in enumerate(birds) if i <= 1]


df = pd.DataFrame({'Especie':birds})
new_idx = df.Especie.str.len().sort_values().index
new_df = df.reindex(new_idx)
chosen_birds = []
for row in new_df.head().iterrows():
    chosen_birds.append(row[1]['Especie'])

print(chosen_birds)


if __name__ == '__main__':
    #sp = SimplePresenter(chosen_birds, 'image', TkinterConsequence())
    tp = TkinterPresenter(Retriever(chosen_birds, 'image'))
    tp.present()
    