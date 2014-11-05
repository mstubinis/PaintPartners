import sys, pygame,client,ConfigParser
from pygame.locals import *
pygame.init()
from objects import Window,Paint

class Program(object):
    def __init__(self,connectAsAdmin=False):
        self.size = (1280,700)
        self.color = 200, 200, 200

        self.screen = pygame.display.set_mode(self.size,RESIZABLE)
        pygame.display.set_caption("Paint Partners")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 16,True)
        self.state = "STATE_PROMPT"
        
        #create windows
        self.window_prompt = Window.WindowPrompt(self.size,(self.size[0]/2,self.size[1]/2),self.font,450,275)
        self.window_paint = Window.WindowPaint(self.size,(4,4),300,self.size[1]/2-4)
        self.window_clients = Window.WindowClients(self.size,(4,self.window_paint.height+6),300,self.size[1]/2-4)
        self.image = Paint.PaintImage((self.window_paint.pos[0] + self.window_paint.width + 4,self.window_paint.pos[1]),self.size[0] - self.window_paint.width - 14,550)

        self.client = client.Client(self)
        if connectAsAdmin == True:
            self.state = "STATE_MAIN"
            config = ConfigParser.RawConfigParser()
            config.readfp(open('server.cfg'))
            username = config.get('ServerInfo', 'AdminName')
            self.client.connect_to_server(username,"localhost","",True)
            self.window_clients.add_client(username)

    def update(self):
        events = pygame.event.get()
        mousePos = pygame.mouse.get_pos()
        
        self.screen.fill(self.color)

        if "STATE_MAIN" in self.state:
            if self.state == "STATE_MAIN_NOEDIT":
                self.image.update(events,mousePos,self.window_paint.currentColor,self.client,False,self.window_paint.currentBrush)
            else:
                self.image.update(events,mousePos,self.window_paint.currentColor,self.client,True,self.window_paint.currentBrush)
            self.window_paint.update(events,mousePos)
            self.window_clients.update(events,mousePos)
        elif self.state == "STATE_PROMPT":
            self.window_prompt.update(events,mousePos)
            if self.window_prompt.connect_button.is_click(events) == True and self.window_prompt.connect_button.is_mouse_over(mousePos) == True:
                result = self.client.connect_to_server(self.window_prompt.username_field.message,
                                                       self.window_prompt.server_field.message,
                                                       self.window_prompt.server_pass_field.message)
                self.window_prompt.write_cfg()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            elif event.type == VIDEORESIZE:
                self.resize(event.w,event.h)
                
    def resize(self,width,height):
        self.size = (width,height)
        self.screen = pygame.display.set_mode(self.size,RESIZABLE)
        self.screen.fill(self.color)

        self.window_prompt.resize(self.size)
        self.window_paint.resize(self.size)
        self.window_clients.resize(self.size)
        self.image.resize(self.size,(self.window_paint.pos[0] + self.window_paint.width + 4,self.window_paint.pos[1]))
        
    def draw(self):
        if "STATE_MAIN" in self.state:
            self.image.draw(self.screen)
            self.window_paint.draw(self.screen)
            self.window_clients.draw(self.screen,self.font)
        elif self.state == "STATE_PROMPT":
            self.window_prompt.draw(self.screen)
        pygame.display.flip()

    def main(self):
        while True:
            self.clock.tick(60)
            self.update()
            self.draw()
      
if __name__ == "__main__":
    program = Program()
    program.main()
    pygame.quit()
