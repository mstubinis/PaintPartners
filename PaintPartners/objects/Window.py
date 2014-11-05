import pygame,Paint,TextField,ConfigParser
from pygame.locals import *

class Slider(pygame.sprite.Sprite):
    def __init__(self,pos,horizontal=True,length=190,height=8,boxLength=5,boxHeight=25,color=(65,65,65),boxColor=(225,225,225),boxBorder=(0,0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.width = length
        self.height = height
        self.horizontal = horizontal
        self.box_width = boxLength
        self.box_height = boxHeight
        self.color = color
        self.box_color = boxColor
        self.box_color_border = boxBorder
        self.highlighted = False
        self.moving = False

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.midleft = (self.pos[0],self.pos[1])

        self.rect_box = pygame.Rect(0,0,self.box_width,self.box_height)
        self.rect_box_border = pygame.Rect(0,0,self.box_width+2,self.box_height+2)
        if horizontal == True:
            self.set_box_pos((self.pos[0] + self.width,self.pos[1]))
        else:
            self.set_box_pos((self.pos[0],self.pos[1] + self.height))


    def is_mouse_over(self,mousePos):
        if mousePos[0] < self.rect_box_border.x or mousePos[0] > self.rect_box_border.x + self.rect_box_border.w or mousePos[1] < self.rect_box_border.y or mousePos[1] > self.rect_box_border.y + self.rect_box_border.h:
            return False
        return True

    def get_value(self):
        value = 0.00
        if self.horizontal == True:
            value = (self.rect_box_border.centerx - self.pos[0])/float(self.width)
        else:
            value = (self.rect_box_border.centery - self.pos[1])/float(self.height)
        return value

    def set_box_pos(self,pos):
        self.rect_box.center = (pos[0],pos[1])
        self.rect_box_border.center = (pos[0],pos[1])
    def get_box_pos(self):
        return (self.rect_box_border.x,self.rect_box_border.y)

    def is_click(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False

    def update(self,events,mousePos):
        if self.is_mouse_over(mousePos) == True:
            self.highlighted = True
            if self.is_click(events) == True:
                self.moving = True
        else:
            self.highlighted = False

        if self.moving == True:
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] != 1:
                        self.moving = False
                        return
                if event.type == pygame.MOUSEBUTTONUP:
                    self.moving = False
                    return
                if self.horizontal == True:
                    self.set_box_pos((mousePos[0],self.pos[1]))
                else:
                    self.set_box_pos((self.pos[0],mousePos[1]))

        if self.horizontal == True:
            if self.get_box_pos()[0] < self.pos[0]:
                self.set_box_pos((self.pos[0],self.pos[1]))
            elif self.get_box_pos()[0] > self.pos[0] + self.width:
                self.set_box_pos((self.pos[0] + self.width,self.pos[1]))
        else:
            if self.get_box_pos()[1] < self.pos[1]:
                self.set_box_pos((self.pos[0],self.pos[1]))
            elif self.get_box_pos()[1] > self.pos[1] + self.height:
                self.set_box_pos((self.pos[0],self.pos[1] + self.height))
            
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.box_color_border,self.rect_box_border)
        if self.highlighted == False:
            pygame.draw.rect(screen,self.box_color,self.rect_box)
        else:
            pygame.draw.rect(screen,(185,185,185),self.rect_box)

class Button(pygame.sprite.Sprite):
    def __init__(self,pos,message,font,borderColor=(0,0,0),fillColor=(225,225,225),highlightColor=(255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.width = font.size(message)[0]+10
        self.height = font.size(message)[1]+6
        self.color_border = borderColor
        self.color_fill = fillColor
        self.color_highlight = highlightColor
        self.highlighted = False
        self.message = message
        self.font = font
        self.text = self.font.render(message, 1,(0,0,0))

        self.rect_border = pygame.Rect(0,0,self.width,self.height)
        self.rect_border.center = (self.pos[0],self.pos[1])
        
        self.rect = pygame.Rect(0,0,self.width-2,self.height-2)
        self.rect.center = (self.pos[0],self.pos[1])
        
    def is_mouse_over(self,mousePos):
        if mousePos[0] < self.rect_border.x or mousePos[0] > self.rect_border.x + self.rect_border.w or mousePos[1] < self.rect_border.y or mousePos[1] > self.rect_border.y + self.rect_border.h:
            return False
        return True
    
    def is_click(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False
    
    def update(self,events,mousePos):
        self.highlighted = False
        if self.is_mouse_over(mousePos) == True:
            self.highlighted = True
            
    def draw(self,screen):
        pygame.draw.rect(screen,self.color_border,self.rect_border)
        if self.highlighted == True:
            pygame.draw.rect(screen,self.color_highlight,self.rect)
        else:
            pygame.draw.rect(screen,self.color_fill,self.rect)
        screen.blit(self.text, self.rect)
        
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

class WindowClients(WindowRectangle):
    def __init__(self,programSize,pos,w=100,h=600,borderColor=(0,0,0),fillColor=(255,255,255)):
        WindowRectangle.__init__(self,programSize,pos,w,h,borderColor,fillColor)
        self.clients = []
    def resize(self,size,resize=True):
        if not resize:
            return
        self.height = size[1]/2 - 8 + 1
        self.rect_border = pygame.Rect(0,0,self.width,self.height+1)
        self.rect_border.topleft = (self.pos[0],self.pos[1]-1)
        
        self.rect = pygame.Rect(0,0,self.width-2,self.height-1)
        self.rect.topleft = (self.pos[0]+1,self.pos[1])

    def add_client(self,client):
        if not client in self.clients:
            self.clients.append(client)

    def remove_client(self,client):
        self.clients.remove(client)
            
    def update(self,events,mousePos):
        WindowRectangle.update(self,events,mousePos)

    def draw(self,screen,font):
        WindowRectangle.draw(self,screen)
        count = 0
        for i in self.clients:
            label = font.render(i, 1, (0,0,0))
            screen.blit(label, (self.pos[0] + 8, self.pos[1] + 8 + (count * 15)))
            count += 1

class WindowPrompt(WindowRectangle):
    def __init__(self,programSize,pos,font,w=100,h=600,borderColor=(0,0,0),fillColor=(240,240,240)):
        WindowRectangle.__init__(self,programSize,pos,w,h,borderColor,fillColor)
        
        self.rect_border.center = (self.pos[0],self.pos[1])
        self.rect.center = (self.pos[0],self.pos[1])

        self.username_field = TextField.TextField((self.pos[0],self.pos[1] - self.height/2 + 50),20,14,"Username: ",font)
        self.server_field = TextField.TextField((self.pos[0],self.username_field.pos[1]+50),20,14,"Server IP: ",font)
        self.server_pass_field = TextField.TextField((self.pos[0],self.server_field.pos[1]+50),20,14,"Server Password: ",font,True)
        self.connect_button = Button((self.pos[0],self.pos[1] + h/2 - 25),"Connect",font)

        self.load_cfg()

    def load_cfg(self):
        config = ConfigParser.RawConfigParser()
        try:
            config.readfp(open('profile.cfg'))
            server_ip = config.get('ProfileInfo','server')
            username = config.get('ProfileInfo','username')

            self.username_field.set_message(username)
            self.server_field.set_message(server_ip)
            
        except Exception as e:
            config.add_section('ProfileInfo')
            config.set('ProfileInfo','username','')
            config.set('ProfileInfo','server','localhost')
            with open('profile.cfg', 'w') as configfile:
                config.write(configfile)
                
    def write_cfg(self):
        config = ConfigParser.RawConfigParser()
        config.readfp(open('profile.cfg'))
        config.set('ProfileInfo','username',self.username_field.message)
        config.set('ProfileInfo','server',self.server_field.message)
        with open('profile.cfg', 'w') as configfile:
            config.write(configfile)
    
    def resize(self,size,resize=True):
        if not resize:
            return
        self.rect_border = pygame.Rect(0,0,self.width,self.height+1)
        self.rect_border.center = (size[0]/2,size[1]/2)
        
        self.rect = pygame.Rect(0,0,self.width-2,self.height-1)
        self.rect.center = (size[0]/2,size[1]/2)

    def update(self,events,mousePos):
        WindowRectangle.update(self,events,mousePos)
        self.username_field.update(events,mousePos)
        self.server_field.update(events,mousePos)
        self.server_pass_field.update(events,mousePos)
        self.connect_button.update(events,mousePos)

    def draw(self,screen):
        WindowRectangle.draw(self,screen)
        self.username_field.draw(screen)
        self.server_field.draw(screen)
        self.server_pass_field.draw(screen)
        self.connect_button.draw(screen)

class WindowPaint(WindowRectangle):
    def __init__(self,programSize,pos,w=100,h=600,borderColor=(0,0,0),fillColor=(240,240,240)):
        WindowRectangle.__init__(self,programSize,pos,w,h,borderColor,fillColor)

        self.brushes = []
        self.currentBrush = None
        self.currentColor = Paint.ColorIcon(programSize,(258,210-35),35,35,(0,0,0),(255,255,255))
        self.wheel = Paint.ColorWheel((10,10),200)

        self.value_slider = Slider((15,235))

        #brush1 = Paint.PaintBrush((275,10+(10)),10)
        brush2 = Paint.PaintBrush((275,10+(20*1.5)),20)
        #brush3 = Paint.PaintBrush((275,10+(30*2)),30)
        #brush4 = Paint.PaintBrush((275,10+(40*2.5)),40)
        
        #self.brushes.append(brush1)
        self.brushes.append(brush2)
        #self.brushes.append(brush3)
        #self.brushes.append(brush4)

    def resize(self,size,resize=True):
        if not resize:
            return
        self.height = size[1]/2 - 8 + 1
        self.rect_border = pygame.Rect(0,0,self.width,self.height+1)
        self.rect_border.topleft = (self.pos[0],self.pos[1]-1)
        
        self.rect = pygame.Rect(0,0,self.width-2,self.height-1)
        self.rect.topleft = (self.pos[0]+1,self.pos[1])

    def update(self,events,mousePos):
        WindowRectangle.update(self,events,mousePos)

        for i in self.brushes:
            if i.is_click(events) == True:
                if i.is_mouse_over(mousePos) == True:
                    i.selected = True
                    self.currentBrush = i
                    for s in self.brushes:
                        if s is not i:
                            s.selected = False
            i.update(events,mousePos)
            
        self.currentColor.update(events,mousePos)
        self.wheel.update(events,mousePos,self.currentColor,self.value_slider)
        self.value_slider.update(events,mousePos)
        
    def draw(self,screen):
        WindowRectangle.draw(self,screen)
        for i in self.brushes:
            i.draw(screen)
        self.currentColor.draw(screen)
        self.wheel.draw(screen)
        self.value_slider.draw(screen)
