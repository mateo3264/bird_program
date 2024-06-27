from downloaders import BirdAudioDownloader, BirdImageDownloader
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import random
import os

#ToDo: get dataset with birds around the world separated by locations
df = pd.read_excel('./aves-de-cota-observadas.xlsx', header=1)


species = df['Especie'].tolist()


for i in range(5):
    original_specie = random.choice(species)
    specie = original_specie.lower().strip().replace(' ', '-')

    print(original_specie)


    bird_images = './bird_images'
    bird_audios = './bird_audios'


    #ToDo: Check first if bird already exists
    bid = BirdImageDownloader(bird_images)
    bad = BirdAudioDownloader(bird_audios)

    bid.get_data(original_specie, limit=5)
    bad.get_data(original_specie, limit=5)

    bid.save_data(format='jpg')
    bad.save_data(format='mp3')



    img = Image.open(os.path.join(bird_images, specie + str(0) + '.jpg'))

    plt.imshow(img)
    plt.show()

    usu = input('Name: ')

    if usu.lower() == original_specie.lower():
        print('GOOD')