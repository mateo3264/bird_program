import os
import json
from formatters import format_name_for_save
from configurations import (
    FILENAME_BIRD_AUDIOS, 
    FILENAME_BIRD_IMAGES,
    DIRNAME_BIRD_AUDIOS,
    DIRNAME_BIRD_IMAGES,
    ALL_BIRDS,
    IMAGE,
    AUDIO
)
import csv

def read_json_file(filename):
    with open(filename, 'r') as file:
        json_file = json.load(file)
        return json_file

def read_bird_names():
    birds = []

    with open(ALL_BIRDS, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            
            birds.append(row['Especie'])
    
    return birds


def write_data_downloaded(bird_name, n_data_examples, data_type):
    bird_name = format_name_for_save(bird_name)
    
    if data_type == IMAGE:
        filename = FILENAME_BIRD_IMAGES
    elif data_type == AUDIO:
        filename = FILENAME_BIRD_AUDIOS

    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            json.dump({}, file)
    
    json_file = read_json_file(filename)

    if bird_name in json_file:
        json_file[bird_name] += n_data_examples
    else:
        json_file[bird_name] = n_data_examples
    
    print(json_file)
    
    with open(filename, 'w') as file:
        json.dump(json_file, file)


def delete_files(bird_name, data_type):
    bird_name = format_name_for_save(bird_name)
    
    if data_type == AUDIO: 
        for f in os.listdir(DIRNAME_BIRD_AUDIOS):
            if bird_name in f:                
                os.remove(os.path.join(DIRNAME_BIRD_AUDIOS, f))
        
        os.remove(FILENAME_BIRD_AUDIOS)

    elif data_type == IMAGE: 
        for f in os.listdir(DIRNAME_BIRD_IMAGES):
            if bird_name in f: 
                os.remove(os.path.join(DIRNAME_BIRD_IMAGES, f))
        
        os.remove(FILENAME_BIRD_IMAGES)


if __name__ == '__main__':
    for i, bird in enumerate(read_bird_names()):
        print(i, bird)

        if i == 5:
            break


    



