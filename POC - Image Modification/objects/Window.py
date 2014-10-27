import pygame,resourceManager,Paint
from pygame.locals import *

class WindowRectangle(pygame.sprite.Sprite):
    def __init__(self,programSize,pos,w=200,h=600,borderColor=(0,0,0),fillColor=(240,240,240)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.width = w
        self.height = h
        self.color_border = borderColor
        self.color_fill = fillColor

        self.rect_border = pygame.Rect(0,0,self.width,self.height)
        self.rect_border.topleft = (self.pos[0] - self.width/2,self.pos[1]-1)
        
        self.rect = pygame.Rect(0,0,self.width-2,self.height-2)
        self.rect.topleft = (self.pos[0]+1 - self.width/2,self.pos[1])
         
    def update(self,events,mousePos):
        pass
    
    def draw(self,screen):
        pygame.draw.rect(screen,self.color_border,self.rect_border)
        pygame.draw.rect(screen,self.color_fill,self.rect)

class WindowPaint(WindowRectangle):
    def __init__(self,programSize,pos,w=100,h=600,borderColor=(0,0,0),fillColor=(240,240,240)):
        WindowRectangle.__init__(self,programSize,pos,w,h,borderColor,fillColor)

        self.brushes = []
        self.currentBrush = None
        self.currentColor = Paint.ColorIcon(programSize,(270,210-35),35,35,(0,0,0),(255,255,255),True)
        self.image = Paint.PaintImage((10,250),300,300)
        self.wheel = Paint.ColorWheel((10,10),200)

        brush1 = Paint.PaintBrush((285,10+(10)),10)
        brush2 = Paint.PaintBrush((285,10+(20*1.5)),20)
        brush3 = Paint.PaintBrush((285,10+(30*2)),30)
        brush4 = Paint.PaintBrush((285,10+(40*2.5)),40)
        
        self.brushes.append(brush1)
        self.brushes.append(brush2)
        self.brushes.append(brush3)
        self.brushes.append(brush4)

    def resize(self,size,resize=True):
        if not resize:
            return
        self.height = size[1] + 1
        self.rect_border = pygame.Rect(0,0,self.width,self.height+1)
        self.rect_border.topleft = (0,self.pos[1]-1)
        
        self.rect = pygame.Rect(0,0,self.width-2,self.height-1)
        self.rect.topleft = (1,self.pos[1])

    def update(self,events,mousePos):
        WindowRectangle.update(self,events,mousePos)
        
        b = True
        for i in self.brushes:
            if i.is_click(events) == True:
                if self.image.is_mouse_over(mousePos) == False and self.wheel.is_mouse_over(mousePos) == False:
                    if i.is_mouse_over(mousePos) == True:
                        i.selected = True
                        b = False
                        self.currentBrush = i
                    else:
                        i.selected = False
            i.update(events,mousePos)

            
        self.currentColor.update(events,mousePos)
        self.image.update(events,mousePos,self.currentColor,self.currentBrush)
        self.wheel.update(events,mousePos,self.currentColor)
    def draw(self,screen):
        WindowRectangle.draw(self,screen)
        for i in self.brushes:
            i.draw(screen)
        self.currentColor.draw(screen)

        self.image.draw(screen)
        self.wheel.draw(screen)
