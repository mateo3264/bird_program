import pygame
import pygame as pg
# Initialize the mixer module
pygame.mixer.init()

# Load the MP3 file
for i in range(10):
    pygame.mixer.music.load(f'bird_audio{i}.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the script running until the music finishes playing
    while pygame.mixer.music.get_busy():
        
        pygame.time.Clock().tick(10)


    print(i)

