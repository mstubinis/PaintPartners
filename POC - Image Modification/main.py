import sys, pygame, resourceManager
from pygame.locals import *
pygame.init()
from objects import Window

class Program(object):
    def __init__(self):
        self.size = (330,700)
        self.color = 200, 200, 200

        self.screen = pygame.display.set_mode(self.size,RESIZABLE)
        pygame.display.set_caption("Image Modification")
        self.clock = pygame.time.Clock()
        
        self.state = "STATE_MAIN_WINDOW"
        self.last_state = self.state
        
        #create windows
        self.window_paint = Window.WindowPaint(self.size,(self.size[0]-100,0),325)

    def update(self):
        listOfEvents = pygame.event.get()
        mousePos = pygame.mouse.get_pos()
        
        self.screen.fill(self.color)

        self.window_paint.update(listOfEvents,mousePos)

        for event in listOfEvents:
            if event.type == pygame.QUIT:
                self.client.disconnect_from_server()
                pygame.quit()
                sys.exit(1)
            elif event.type == VIDEORESIZE:
                self.resize(event.w,event.h)
                
    def resize(self,width,height):
        self.size = (width,height)
        self.screen = pygame.display.set_mode(self.size,RESIZABLE)
        self.screen.fill(self.color)
        self.window_paint.resize(self.size)
        
    def draw(self):
        self.window_paint.draw(self.screen)
        pygame.display.flip()
      
if __name__ == "__main__":
    program = Program()
    while True:
        program.clock.tick(60)
        program.update()
        program.draw()
    pygame.quit()
