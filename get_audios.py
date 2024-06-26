import requests 
from bs4 import BeautifulSoup


def get_bird_audio(bird_name):
    bird_name = bird_name.lower().replace(' ', '%20')
    url = 'https://xeno-canto.org/explore?query=' + bird_name
    print(url)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    audios = soup.find_all('audio', class_='xc-mini-player')

    audio_srcs = []
    for audio in audios:
        audio_src = audio.get('src')
        print(audio_src)
        audio_srcs.append(audio_src)

    for i, audio_src in enumerate(audio_srcs):
        audio_content = requests.get('https:' + audio_src).content
        
        with open('./{}{}.mp3'.format(bird_name.replace('%20', '_'), i), 'wb') as f:
            f.write(audio_content)

if __name__ == '__main__':
    get_bird_audio('turdus fuscater')