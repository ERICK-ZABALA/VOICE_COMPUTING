import pygame
import pygame.mixer

def sync_playback(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    try:
        pygame.mixer.music.play(loops=1)
    except pygame.error as e:
        print("Pygame error:", e)

sync_playback('audio/one.wav')
