import pygame,resourceManager,copy,math,colorsys
from pygame.locals import *

class ColorWheel(object):
    def __init__(self,pos,r):
        self.pos = pos
        self.radius = r
        self.image = pygame.Surface((r,r))
        self.image.fill((255,255,255))
        self.pos = pos
        self.image_rect = pygame.Rect(0,0,r,r)
        self.image_rect.topleft = (pos[0]+1,pos[1])
        self.image_rect_border = pygame.Rect(0,0,r+2,r+2)
        self.image_rect_border.topleft = (pos[0],pos[1]-1)

        self.pixels = pygame.PixelArray(self.image)

        radius = r/2
        
        for x in range(r):
            for y in range(r):
                side1 = (x - radius)
                side2 = (y - radius)

                side3 = math.sqrt((side1**2) + (side2**2))

                hue = (math.atan2(side2,side1)+3.14159)/(3.14159*2)
                if side3 <= radius:
                    rgb = colorsys.hsv_to_rgb(hue,(side3/radius),1)
                    self.pixels[x,y] = (rgb[0]*255,rgb[1]*255,rgb[2]*255)
                
        self.image = self.pixels.make_surface()
        del self.pixels

    def is_click(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False
    
    def is_mouse_over(self,mousePos):
        if mousePos[0] < self.image_rect.x or mousePos[0] > self.image_rect.x + self.image_rect.w or mousePos[1] < self.image_rect.y or mousePos[1] > self.image_rect.y + self.image_rect.h:
            return False
        return True
    
    def update(self,events,mousePos,currentColor):
        if self.is_mouse_over(mousePos) == True:
            for x in range(self.radius):
                for y in range(self.radius):
                    if self.is_click(events) == True:
                        try:
                            self.pixels = pygame.PixelArray(self.image)
                            xPos = mousePos[0] - self.pos[0]
                            yPos = mousePos[1] - self.pos[1]
                            currentColor.color_fill = self.image.unmap_rgb(self.pixels[xPos,yPos])
                            del self.pixels
                        except:
                            pass
                        return
                        
    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.image_rect_border)
        screen.blit(self.image,self.image_rect)

    
class PaintBrush(object):
    def __init__(self,pos,r):
        self.radius = r/2
        self.pos = pos
        self.image = pygame.Surface((r,r))
        self.image.fill((255,255,255))
        self.image_rect = pygame.Rect(0,0,r,r)
        self.image_rect.midtop = (pos[0]+1,pos[1])
        self.image_rect_border = pygame.Rect(0,0,r+2,r+2)
        self.image_rect_border.midtop = (pos[0],pos[1]-1)
        self.selected = False
        self.pixels = pygame.PixelArray(self.image)
        for x in range(r):
            for y in range(r):
                side1 = (x - self.radius)
                side2 = (y - self.radius)
                side3 = math.sqrt((side1**2) + (side2**2))
                if side3 <= self.radius:
                    self.pixels[x,y] = (0,0,0)
        self.image = self.pixels.make_surface()
        del self.pixels

    def is_click(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False
    
    def is_mouse_over(self,mousePos):
        if mousePos[0] < self.image_rect.x or mousePos[0] > self.image_rect.x + self.image_rect.w or mousePos[1] < self.image_rect.y or mousePos[1] > self.image_rect.y + self.image_rect.h:
            return False
        return True
    
    def update(self,events,mousePos):
        pass
    def draw(self,screen):
        if self.selected == True:
            pygame.draw.rect(screen,(220,220,220),self.image_rect_border)
        screen.blit(self.image,self.image_rect)
    
class PaintImage(object):
    def __init__(self,pos,w,h):
        self.image = pygame.Surface((w,h))
        self.image.fill((255,255,255))
        self.pos = pos
        self.image_rect = pygame.Rect(0,0,w,h)
        self.image_rect.topleft = (pos[0]+1,pos[1])
        self.image_rect_border = pygame.Rect(0,0,w+2,h+2)
        self.image_rect_border.topleft = (pos[0],pos[1]-1)

        self.pixels = pygame.PixelArray(self.image.copy())
        
    def is_click(self,events):
        mouseState = pygame.mouse.get_pressed()
        if mouseState[0] == 1:
            return True
        return False
    
    def is_mouse_over(self,mousePos):
        if mousePos[0] < self.image_rect.x or mousePos[0] > self.image_rect.x + self.image_rect.w or mousePos[1] < self.image_rect.y or mousePos[1] > self.image_rect.y + self.image_rect.h:
            return False
        return True
        
    def update(self,events,mousePos,currentColor,currentBrush=None):
        x = mousePos[0] - self.pos[0]
        y = mousePos[1] - self.pos[1]
        if self.is_mouse_over(mousePos):
            if self.is_click(events):

                if currentBrush == None:
                    self.pixels[x,y] = currentColor.color_fill
                else:
                    startX = x - currentBrush.radius
                    startY = y - currentBrush.radius
                    for i in range(currentBrush.radius*2):
                        for j in range(currentBrush.radius*2):
                            side1 = (i - currentBrush.radius)
                            side2 = (j - currentBrush.radius)
                            side3 = math.sqrt((side1**2) + (side2**2))
                            if side3 <= currentBrush.radius:
                                try:
                                    self.pixels[startX+i,startY+j] = currentColor.color_fill
                                except:
                                    pass
                
                self.image = self.pixels.make_surface()
    
    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.image_rect_border)
        screen.blit(self.image,self.image_rect)
        
class ColorIcon(pygame.sprite.Sprite):
    def __init__(self,programSize,pos,w=5,h=5,borderColor=(0,0,0),fillColor=(225,225,225),drawBorder=False):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.width = w
        self.height = h
        self.color_border = borderColor
        self.color_fill = fillColor

        self.rect_border = None
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.topleft = self.pos

        if drawBorder:
            self.rect_border = pygame.Rect(0,0,self.width+2,self.height+2)
            self.rect_border.topleft = (self.pos[0]-1,self.pos[1]-1)

    def is_click(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False
    
    def is_mouse_over(self,mousePos):
        if mousePos[0] < self.rect.x or mousePos[0] > self.rect.x + self.rect.w or mousePos[1] < self.rect.y or mousePos[1] > self.rect.y + self.rect.h:
            return False
        return True
    
    def update(self,events,mousePos):
        pass
    
    def draw(self,screen):
        if self.rect_border != None:
            pygame.draw.rect(screen,self.color_border,self.rect_border)
        pygame.draw.rect(screen,self.color_fill,self.rect)
