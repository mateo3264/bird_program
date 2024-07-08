import json
import os
from formatters import format_name_for_save
from configurations import (
    DIRNAME_BIRD_IMAGES, 
    DIRNAME_BIRD_AUDIOS,
    FILENAME_BIRD_IMAGES
)
from PIL import Image
import pygame
import pygame as pg
from registers import read_json_file
from downloaders import BirdAudioDownloader, BirdImageDownloader

def get_from_downloaded(bird_name, data_type):
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
            datapoint = full_path
        if bird_name in datapoint:
            data.append(datapoint)
    
    return data

# ToDo: If bird_name exists (as img or audio) get it, else download and get it
def get_data(bird_name, data_type):
    original_bird_name = bird_name
    
    bird_name = format_name_for_save(bird_name)
    
    #print('DIRNAME_BIRD_IMAGES', DIRNAME_BIRD_IMAGES)
    json_file = read_json_file(FILENAME_BIRD_IMAGES)

    if bird_name not in json_file:
        print('bird not in local memory')
        bid = BirdImageDownloader(DIRNAME_BIRD_IMAGES)
        bid.get_data(original_bird_name)
        print('THE BIRD DATA BABY: ', bid.bird_data.keys())
        bid.save_data('jpg')
    
    data = get_from_downloaded(bird_name, data_type)
    
    return data
