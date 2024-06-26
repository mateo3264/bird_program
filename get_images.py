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

    def save_images(self, format):
        for bird_name in self.bird_data:
            for i, data_content in enumerate(self.bird_data[bird_name]):
                filename = self.path + '\\' + bird_name + str(i) + '.' + format
                with open(filename, 'wb') as f:
                    print(filename)
                    f.write(data_content)



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
            
        ##    print(div)
            img_tag = div.find_all('img')
        ##    print(img_tag)
            try:
                
                img_src = img_tag[0].get('src')
    ##            print(img_src)
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
    for r in df.iterrows():
        bird = r[1]['Especie']
        print('bird: ', bird)
        bid.get_data(bird)
        
        print(bid.bird_data.keys())
        
    print('END OF GETTING IMAGES')
    bid.save_images(format='jpg')
    
    


