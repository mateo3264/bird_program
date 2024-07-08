import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os
from abc import ABC, abstractmethod
from registers import write_data_downloaded
from configurations import DIRNAME_BIRD_AUDIOS, DIRNAME_BIRD_IMAGES
import wikipedia
from formatters import format_name_for_save

def get_wikipedia_images(bird_name, bird_data_container):
    # Base URL for the Wikipedia API
    birdname_for_save = format_name_for_save(bird_name)
    api_url = "https://en.wikipedia.org/w/api.php"
    print('birdname_for_save: ', birdname_for_save)
    try:
        common_bird_name = wikipedia.search(bird_name)[0]
        print(common_bird_name)
    except Exception as e:
        raise e

    page_title = common_bird_name

    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "images",
        "imlimit": "max"  # Get maximum number of images per request
    }

    image_titles = []

    while True:
        # Make the API request
        response = requests.get(api_url, params=params)
        data = response.json()

        # Extract page data
        page = next(iter(data["query"]["pages"].values()))

        # Add image titles to our list
        if "images" in page:
            image_titles.extend(image["title"] for image in page["images"])

        # Check if there are more images to fetch
        if "continue" in data:
            params["imcontinue"] = data["continue"]["imcontinue"]
        else:
            break

    # Now fetch the actual URLs for these images
    image_urls = []
    for i in range(0, len(image_titles), 50):  # Process in batches of 50
        chunk = image_titles[i:i+50]
        params = {
            "action": "query",
            "format": "json",
            "titles": "|".join(chunk),
            "prop": "imageinfo",
            "iiprop": "url"
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        for page in data["query"]["pages"].values():
            if "imageinfo" in page:
                image_urls.append(page["imageinfo"][0]["url"])

    
    #image_urls = get_wikipedia_images(page_title)
    print(f"Found {len(image_urls)} images:")

    # Define headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i, url in enumerate(image_urls):
        print(f"Processing image {i+1}: {url}")
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to download image {i+1}. Status code: {response.status_code}")
            continue

        # Get the file extension from the URL
        file_extension = os.path.splitext(url)[1].lower()
        
        # Only process JPEG and PNG images
        if file_extension in ['.jpg', '.jpeg', '.png']:
            filename = f"{page_title}{i}{file_extension}"
            
            # Save the image
            with open(filename, 'wb') as file:
                if birdname_for_save not in bird_data_container:
                    bird_data_container[birdname_for_save] = []
                bird_data_container[birdname_for_save].append(response.content)
                file.write(response.content)
            
            # Check if the file was saved successfully
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"Failed to save image {i+1} to file: {filename}")
                continue
    
    return bird_data_container


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
        
        if format == 'jpg':
            write_data_downloaded(bird_name, len(self.bird_data[bird_name]), 'image')
        elif format == 'mp3':
            write_data_downloaded(bird_name, len(self.bird_data[bird_name]), 'audio')



class BirdAudioDownloader(BirdDownloader):
    def get_data(self, bird, limit=5):
        bird_name = bird.lower().strip().replace(' ', '%20')
        url = 'https://xeno-canto.org/explore?query=' + bird_name
        
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        audios = soup.find_all('audio', class_='xc-mini-player')

        audio_srcs = []
        for audio in audios:
            audio_src = audio.get('src')
            
            audio_srcs.append(audio_src)

        audio_counter = 0
        for i, audio_src in enumerate(audio_srcs):
            audio_content = requests.get('https:' + audio_src).content
            print(audio_src)
            bird = bird.lower().replace(' ', '-')
            
            if bird not in self.bird_data:
                self.bird_data[bird] = []

            self.bird_data[bird].append(audio_content)
            
            audio_counter += 1
            if limit is not None:
                if audio_counter >= limit:
                    break
        
        if bird not in self.bird_data:
            print(f'Warning: Unsplash doesnt have {bird} images')

    
            # with open('./{}{}.mp3'.format(bird_name.replace('%20', '_'), i), 'wb') as f:
            #     f.write(audio_content)

class BirdImageDownloader(BirdDownloader):
        
    def get_data(self, bird, show=False, limit=None):
        original_bird = bird
        #ToDo: Replace with format function 
        bird = bird.lower().strip().replace(' ', '-')
        
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
                    print(img_src)
                    img_content = requests.get(img_src).content
                    if bird not in self.bird_data:
                        self.bird_data[bird] = []
                    self.bird_data[bird].append(img_content)
                    image_counter += 1
                    if limit is not None:
                        if image_counter >= limit:
                            break
                    print(f'# of images {image_counter}')
                    if show:
                        
                        img = Image.open(BytesIO(img_content))
                        plt.imshow(img)
                        plt.show()
            except Exception as e:
                pass
        
        if bird not in self.bird_data:
            print(f'Warning: Unsplash doesnt have {bird} images')
            print('Trying in wikipedia')
            self.bird_data = get_wikipedia_images(original_bird, self.bird_data)

        

if __name__ == '__main__':
    bad = BirdAudioDownloader(DIRNAME_BIRD_AUDIOS)
    bid = BirdImageDownloader(DIRNAME_BIRD_IMAGES)
    get_wikipedia_images('turdus fuscater', bid.bird_data)

    bad.get_data('turdus fuscater')
    bad.save_data('mp3')
    bid.get_data('turdus fuscater')
    bid.save_data('jpg')


