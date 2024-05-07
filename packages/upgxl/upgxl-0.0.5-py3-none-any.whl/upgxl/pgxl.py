import pygame as pg
from pygame.color import Color
from abc import ABC, abstractmethod

from gptk import Singleton

class UPGXL(Singleton):
    '''
    '''
    
    def init(self, *args, **kwargs):
        '''
        '''
        self.running = False
        self.events  = dict()
        self.size = kwargs.get('size', (640, 480));
        
    def loop(self):
        '''
        '''
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.ACTIVEEVENT    #  gain, state
                    self.on_active_event(event);
                elif event.type == pg.KEYDOWN        #  key, mod, unicode, scancode
                    self.on_key_down(event);
                elif event.type == pg.KEYUP          #  key, mod, unicode, scancode
                    self.on_key_up(event);
                elif event.type == pg.MOUSEMOTION    #  pos, rel, buttons, touch
                    self.on_mousemotion(event);
                elif event.type == pg.MOUSEBUTTONUP  #  pos, button, touch
                    self.on_mousebutton_up(event);
                elif event.type == pg.MOUSEBUTTONDOWN#  pos, button, touch
                    self.on_mousebutton_down(event);
                elif event.type == pg.JOYAXISMOTION  #  joy (deprecated), instance_id, axis, value
                    self.on_joy_axis_motion(event);
                elif event.type == pg.JOYBALLMOTION  #  joy (deprecated), instance_id, ball, rel
                    self.on_joy_ball_motion(event);
                elif event.type == pg.JOYHATMOTION   #  joy (deprecated), instance_id, hat, value
                    self.on_joy_hat_motion(event);
                elif event.type == pg.JOYBUTTONUP    #  joy (deprecated), instance_id, button
                    self.on_joy_button_up(event); 
                elif event.type == pg.JOYBUTTONDOWN  #  joy (deprecated), instance_id, button
                    self.on_joy_button_down(event);
                elif event.type == pg.VIDEORESIZE    #  size, w, h
                    self.on_video_resize(event);
                elif event.type == pg.VIDEOEXPOSE    #  none	
                    self.on_video_expose(event);
                elif event.type == pg.USEREVENT      #  code
                    self.on_user_event(event);
            pg.display.update()

    def exit(self):
        '''
        '''
        pg.quit()


    def run(self):
        pg.init()
        self.screen = pg.display.set_mode(self.size)
        self.screen.fill(Color('Yellow'))
        pg.display.update()
        self.loop()
        self.exit()

    
    @abstractmethod
    def on_keydown(self, event):
        '''Is called whenever a pygame.KEYDOWN event is captured.
        '''
        

class ExamplePGXApp(PGXL):

    
    def on_keydown(self, event):
        if event.key == pg.K_r:
            self.screen.fill(Color('red'))
        if event.key == pg.K_g:
            self.screen.fill(Color('green'))
        if event.key == pg.K_b:
            self.screen.fill(Color('blue'))
        if event.key == pg.K_q:
            self.running = False

        
