from difuminators import difuminate
import loaders
from PIL import Image
import matplotlib.pyplot as plt
import random
from schedulers import get_birds_by_string_length


class Retriever:
    def __init__(self, birds, how):
        """Present an image, audio or image and audio
        The how parameter receives 'image', 'audio' or 'image-audio'"""

        self.birds = birds
        self.images = {bird:[] for bird in birds}
        self.current_image_idx = 0
        self.current_audio_idx = 0
        self.audios = []
        self.how = how #'image-audio'
        print('self.how', self.how)
        self.image_filenames = {bird:[] for bird in birds}
        self.audio_filenames = {bird:[] for bird in birds}
        
        self.text_stimulus = {bird:difuminate(bird, 2) for bird in birds}
        

        self.consequetively_correct_responses = 0
        
        
        for bird_name in birds:
                print(bird_name)
                if self.how == 'image' or self.how == 'image-audio':
                    self.get_data_filenames(bird_name, 'image')
                if self.how == 'audio' or self.how == 'image-audio':
                    self.get_data_filenames(bird_name, 'audio')
        #self.url2obj()
        
        print(self.image_filenames)

    def get_data_filenames(self, bird_name, data_type):
        """Get the data by calling loaders.get_data()"""
        if self.how == 'image' or self.how == 'image-audio':
            self.image_filenames[bird_name] = loaders.get_data(bird_name, 'image')
            print('image filenames key and value')
            print(bird_name, self.image_filenames[bird_name])
        if self.how == 'audio' or self.how == 'image-audio':
            print('RETRIEVER AUDIO')
            self.audio_filenames[bird_name] = loaders.get_data(bird_name, 'audio')
            #self.audio_filenames.extend(loaders.get_data(bird_name, 'audio'))
        
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
               
