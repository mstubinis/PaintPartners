import pygame,os,sys
from pygame.locals import *
pygame.init()

def parse_message(message,typeMessage=""):
    messageList = []
    count = 0
    part = ''
    for char in message:
        if count != 0:
            if count > len(typeMessage)-1:
                if char == "_" or char == "|":
                    messageList.append(part)
                    part = ''
                else:
                    part += char
                    if count == len(message) - 1:
                        messageList.append(part)
                        part = ''
        count += 1
    return messageList

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image: ' + str(name))
        raise SystemExit,message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound: ' + str(wav))
        raise SystemExit, message
    return sound
