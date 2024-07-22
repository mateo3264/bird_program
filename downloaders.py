import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os
from abc import ABC, abstractmethod
from registers import write_data_downloaded, write_to_json, read_json_file
from configurations import DIRNAME_BIRD_AUDIOS, DIRNAME_BIRD_IMAGES, FILENAME_BIRD_TEXTS
import wikipedia
from formatters import format_name_for_save
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

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


# def get_bird_description(bird, verbose=False):
#     if verbose:
#         print('trying to get the description from wikipedia')
#     response = requests.get('https://es.wikipedia.org/wiki/' + bird)

#     text = response.text

    
#     soup = BeautifulSoup(text, 'html.parser')

#     ps = soup.find_all('p')
#     titles = soup.find_all('h2')
#     description = None
#     for t, p in zip(titles, ps):
#         if 'Descripción' in t.text:
#             description = p.text

#     return description

def get_bird_description(bird, language='es', verbose=False):
    print(bird)
    if verbose:
        print(f'Trying to get the description for {bird} from Wikipedia in {language}')
    
    url = f'https://{language}.wikipedia.org/wiki/{bird}'
    description_names = {
        'es': ['Descripción', 'Características'],
        'en': ['Description', 'Characteristics']
    }
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for desc_name in description_names.get(language, []):
            description_tag = soup.find('span', {'id': desc_name})
            if description_tag:
                paragraphs = description_tag.find_all_next('p', limit=3)
                if paragraphs:
                    return ' '.join(p.text for p in paragraphs)
        
        raise ValueError("Couldn't find a description")
    
    except requests.RequestException as e:
        print(f"Network error occurred: {e}")
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    
    return None
    


class BirdDownloader(ABC):
    def __init__(self, path=''):
        self.path = path

        if not os.path.isdir(self.path) and path != '':
            print('MAKING A FOLDER')
            os.mkdir(self.path)
        self.bird_data = {}
    
    @abstractmethod
    def get_data(self, bird):
        pass

    def save_data(self, format):
        #print(f'file downloaders.py, line 127, self.bird_data {self.bird_data}')
        if format == ('mp3', 'jpg'):
            for bird_name in self.bird_data:
                print(f'file downloaders.py, line 129, bird_name {bird_name}')
                for i, data_content in enumerate(self.bird_data[bird_name]):
                    filename = self.path + '\\' + bird_name + str(i) + '.' + format
                    with open(filename, 'wb') as f:
                        print(filename)
                        
                        f.write(data_content)
        
        if format == 'jpg':
            write_data_downloaded(bird_name, len(self.bird_data[bird_name]), 'image')
        elif format == 'mp3':
            print('bird_name: ', bird_name)
            print('self.bird_data: ', self.bird_data.keys())
            write_data_downloaded(bird_name, len(self.bird_data[bird_name]), 'audio')
        elif format == 'text':
            write_to_json(self.bird_data, FILENAME_BIRD_TEXTS)



class BirdAudioDownloader(BirdDownloader):
    def get_data(self, bird, limit=5):
        bird_name = format_name_for_save(bird, '%20') #bird.lower().strip().replace(' ', '%20')
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
            bird = format_name_for_save(bird)#bird.lower().replace(' ', '-')
            
            if bird not in self.bird_data:
                self.bird_data[bird] = []

            self.bird_data[bird].append(audio_content)
            
            audio_counter += 1
            if limit is not None:
                if audio_counter >= limit:
                    break
        
        if bird not in self.bird_data:
            print(f'Warning: xeno-canto doesnt have {bird} audios')
            self.bird_data[bird] = None

    
            # with open('./{}{}.mp3'.format(bird_name.replace('%20', '_'), i), 'wb') as f:
            #     f.write(audio_content)

class BirdImageDownloader(BirdDownloader):
        
    def get_data(self, bird, show=False, limit=None):
        original_bird = bird
        #ToDo: Replace with format function 
        bird = format_name_for_save(bird) #bird.lower().strip().replace(' ', '-')
        
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

#ToDo: text downloader
class BirdTextDownloader(BirdDownloader):
    def __init__(self, path):
        super().__init__(path)
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        self.url = 'https://ebird.org/species/{species_code}'
        
        self.df_ebird = pd.read_csv('ebird_taxonomy.csv')
    
    # ToDo: Check if already in birds_text.json
    def get_data(self, bird, limit=None):
        print(bird)
        json_bird_text_file = read_json_file(FILENAME_BIRD_TEXTS)
        # print('json_bird_text_file')
        # print(json_bird_text_file)

        if bird in json_bird_text_file:
            print(f'bird: {bird} already downloaded')
            return
        try:
            species_code = self.df_ebird[self.df_ebird['SCIENTIFIC_NAME'] == bird]['SPECIES_CODE'].values[0]
        except IndexError:
            print(f'{bird} not found in ebird taxonomy')
            species_code = None
        if species_code:

            self.driver.get(self.url.format(species_code=species_code))     
            self.driver.implicitly_wait(5)

            description_paragraph = self.driver.find_element(By.CLASS_NAME, 'u-stack-sm')

            if description_paragraph:
                html = description_paragraph.get_attribute('innerHTML')
                
                if bird not in self.bird_data:
                    self.bird_data[bird] = html
        wikipedia_text = get_bird_description(bird, verbose=True)
        if wikipedia_text is not None:
            self.bird_data[bird] += wikipedia_text
        print('DESCRIPTION COLLECTED:')
        for bird in self.bird_data:
            if self.bird_data[bird] != '':
                print('some data was gotten')
                #print(bird, ': ', self.bird_data[bird])
        self.save_data(format='text')
        
        

        


if __name__ == '__main__':
    btd = BirdTextDownloader()
    for bird in ['Myioborus ornatus', 'Ramphocelus dimidiatus', 'Pygochelidon cyanoleuca']:
        btd.get_data(bird)
    
    bad = BirdAudioDownloader(DIRNAME_BIRD_AUDIOS)
    print('bird data from bad: ', bad.bird_data)
    bid = BirdImageDownloader(DIRNAME_BIRD_IMAGES)
    print('bird data from bid: ', bid.bird_data)
    get_wikipedia_images('turdus fuscater', bid.bird_data)

    bad.get_data('turdus fuscater')
    bad.save_data('mp3')
    bid.get_data('turdus fuscater')
    bid.save_data('jpg')


