import json
import os
from formatters import format_name_for_save
from configurations import DIRNAME_BIRD_IMAGES, DIRNAME_BIRD_AUDIOS
from PIL import Image
import pygame
import pygame as pg


def get_data(bird_name, data_type):
    bird_name = format_name_for_save(bird_name)
    data = []

    if data_type == 'audio':
        dire = DIRNAME_BIRD_AUDIOS
        pygame.mixer.init()
    elif data_type == 'image':
        dire = DIRNAME_BIRD_IMAGES

    for f in os.listdir(dire):
        full_path = os.path.join(dire, f)
    
        if data_type == 'audio':
            
            datapoint = full_path
        elif data_type == 'image':
            datapoint = Image.open(full_path)

        data.append(datapoint)
    
    return data
