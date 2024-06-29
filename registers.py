import os
import json
from formatters import format_name_for_save
from configurations import (
    FILENAME_BIRD_AUDIOS, 
    FILENAME_BIRD_IMAGES,
    DIRNAME_BIRD_AUDIOS,
    DIRNAME_BIRD_IMAGES
)


def write_data_downloaded(bird_name, n_data_examples, data_type):
    bird_name = format_name_for_save(bird_name)
    
    if data_type == 'image':
        filename = FILENAME_BIRD_IMAGES
    elif data_type == 'audio':
        filename = FILENAME_BIRD_AUDIOS

    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            json.dump({}, file)
    with open(filename, 'r') as file:
            json_file = json.load(file)


    if bird_name in json_file:
        json_file[bird_name] += n_data_examples
    else:
        json_file[bird_name] = n_data_examples
    
    print(json_file)
    
    with open(filename, 'w') as file:
        json.dump(json_file, file)

def delete_files(bird_name, data_type):
    bird_name = format_name_for_save(bird_name)
    
    if data_type == 'audio': 
        for f in os.listdir(DIRNAME_BIRD_AUDIOS):
            if bird_name in f:                
                os.remove(os.path.join(DIRNAME_BIRD_AUDIOS, f))
        
        os.remove(FILENAME_BIRD_AUDIOS)

    elif data_type == 'image': 
        for f in os.listdir(DIRNAME_BIRD_IMAGES):
            if bird_name in f: 
                os.remove(os.path.join(DIRNAME_BIRD_IMAGES, f))
        
        os.remove(FILENAME_BIRD_IMAGES)



    



