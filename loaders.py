import json
import os
from formatters import format_name_for_save
from configurations import (
    DIRNAME_BIRD_IMAGES, 
    DIRNAME_BIRD_AUDIOS,
    FILENAME_BIRD_IMAGES,
    FILENAME_BIRD_AUDIOS,
    IMAGE,
    AUDIO,
    TEXT
)
from PIL import Image
import pygame
import pygame as pg
from registers import read_json_file
from downloaders import BirdDownloader, BirdAudioDownloader, BirdImageDownloader, BirdTextDownloader

def get_from_downloaded(bird_name, data_type):
    data = []

    if data_type == AUDIO:
        dire = DIRNAME_BIRD_AUDIOS
        pygame.mixer.init()
    elif data_type == IMAGE:
        dire = DIRNAME_BIRD_IMAGES

    for f in os.listdir(dire):
        full_path = os.path.join(dire, f)
    
        if data_type == AUDIO:
            
            datapoint = full_path
        elif data_type == IMAGE:
            datapoint = full_path
        if bird_name in datapoint:
            data.append(datapoint)
    
    return data

def save_data(bird: str, downloader: BirdDownloader, format: str):
        print(f'DOWNLOADING {format} of {bird}')
        
        downloader.get_data(bird.strip())
        print(downloader, downloader.bird_data.keys())
        downloader.save_data(format)

# ToDo: Is not necessary to instantiate a Downloader each time this 
# function is called. change it so that only one time is done.
def download_and_save_data(bird):#, data_type):
    #print(f'bird: {original_bird_name} filename with format {data_type} not in local memory')
    
    #if data_type == IMAGE:
    save_data(bird, BirdImageDownloader(DIRNAME_BIRD_IMAGES), 'jpg')
    # format = 'jpg'
    # bird_downloader = BirdImageDownloader(DIRNAME_BIRD_IMAGES)
    # bird_downloader.get_data(original_bird_name)
    # bird_downloader.save_data(format)
    #elif data_type == AUDIO:
    save_data(bird, BirdAudioDownloader(DIRNAME_BIRD_AUDIOS), 'mp3')
    # format = 'mp3'
    # bird_downloader = BirdAudioDownloader(DIRNAME_BIRD_AUDIOS)
    # bird_downloader.get_data(original_bird_name)
    # bird_downloader.save_data(format)
    #elif data_type == TEXT:
    save_data(bird, BirdTextDownloader(), 'text')
    # format = 'text'
    # bird_downloader = BirdTextDownloader()
    # bird_downloader.get_data(original_bird_name)
    # bird_downloader.save_data(format)
    return True

# ToDo: If bird_name exists (as img or audio) get it, else download and get it
def get_data(bird_name, data_type):
    print(f'file: loaders.py, data_type: {data_type}')
    original_bird_name = bird_name
    
    bird_name = format_name_for_save(bird_name)
    
    #print('DIRNAME_BIRD_IMAGES', DIRNAME_BIRD_IMAGES)
    if data_type == IMAGE:
        json_file = read_json_file(FILENAME_BIRD_IMAGES)
        
    elif data_type == AUDIO:
        json_file = read_json_file(FILENAME_BIRD_AUDIOS)
        
    print(f'file: loaders.py, json_file: {json_file}')

    if bird_name not in json_file:
        download_and_save_data(original_bird_name)#, data_type)
    
    data = get_from_downloaded(bird_name, data_type)
    
    return data
