import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import os
from abc import ABC, abstractmethod

class BirdDownloader(ABC):
    def __init__(self, path):
        self.path = path

        if not os.path.isdir(self.path):
            print('MAKING A FOLDER')
            os.mkdir(self.path)
        self.bird_data = {}
    
    @abstractmethod
    def get_data(self, bird):
        pass

    def save_data(self, format):
        for bird_name in self.bird_data:
            for i, data_content in enumerate(self.bird_data[bird_name]):
                filename = self.path + '\\' + bird_name + str(i) + '.' + format
                with open(filename, 'wb') as f:
                    print(filename)
                    f.write(data_content)


class BirdAudioDownloader(BirdDownloader):
    def get_data(self, bird):
        bird_name = bird.lower().replace(' ', '%20')
        url = 'https://xeno-canto.org/explore?query=' + bird_name
        
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        audios = soup.find_all('audio', class_='xc-mini-player')

        audio_srcs = []
        for audio in audios:
            audio_src = audio.get('src')
            
            audio_srcs.append(audio_src)

        for i, audio_src in enumerate(audio_srcs):
            audio_content = requests.get('https:' + audio_src).content
            bird = bird.lower().replace(' ', '-')
            self.bird_data[bird] = audio_content

    
            # with open('./{}{}.mp3'.format(bird_name.replace('%20', '_'), i), 'wb') as f:
            #     f.write(audio_content)

class BirdImageDownloader(BirdDownloader):
        
    def get_data(self, bird, show=False):
        
        bird = bird.lower().replace(' ', '-')
        print(bird)
        url = 'https://unsplash.com/es/s/fotos/' + bird

        res = requests.get(url)

        soup = BeautifulSoup(res.text, 'html.parser')

        divs = soup.find_all('div', class_='HcSeS')
        image_counter = 0
        
        for div in divs:
            
        
            img_tag = div.find_all('img')
        
            try:
                
                img_src = img_tag[0].get('src')
    
                if 'https' in img_src:
                    img_content = requests.get(img_src).content
                    if bird not in self.bird_data:
                        self.bird_data[bird] = []
                    self.bird_data[bird].append(img_content)
                    image_counter += 1
                    print(f'# of images {image_counter}')
                    if show:
                        
                        img = Image.open(BytesIO(img_content))
                        plt.imshow(img)
                        plt.show()
            except Exception as e:
                pass
            
        

                
            



if __name__ == '__main__':
    df = pd.read_excel('./aves-de-cota-observadas.xlsx', header=1)
    df = df.head(10)
    
    bid = BirdImageDownloader('./bird_images')
    bad = BirdAudioDownloader('./bird_audios')
    for r in df.iterrows():
        bird = r[1]['Especie']
        print('bird: ', bird)
        bid.get_data(bird)
        bad.get_data(bird)
        
        print(bid.bird_data.keys())
        print(bad.bird_data.keys())
        
    print('END OF GETTING IMAGES')
    bid.save_data(format='jpg')
    bad.save_data(format='mp3')
    
    


