
# coding: utf-8

# In[4]:

import pygame
from pygame.locals import *
import numpy as np
class Renderer(object):
    
    def __init__(self, window_size=(1024, 768), render_fn=None, inplace=False, init=None):
        self.window_size = window_size
        self.inplace = inplace
        self.render_fn = render_fn
        if init is not None:
            assert init.dtype == np.uint8 and init.shape == (window_size[0], window_size[1], 3), 'wrong type or shape for init'
            self.pixarray = init
        else:
            self.pixarray = np.zeros((window_size[0], window_size[1], 3), dtype=np.uint8)
        self.screen = pygame.display.set_mode(window_size)

        
    def render_loop(self):
        ctr = 0
        try:
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                       raise StopIteration()

                if self.render_fn is not None:
                    if self.inplace:
                        self.render_fn(buf=self.pixarray, frame_id=ctr)
                        new_pix = self.pixarray
                    else:
                        new_pix = self.render_fn(buf=self.pixarray, frame_id=ctr).astype(np.uint8)
                    pygame.surfarray.blit_array(self.screen, new_pix)
                    pygame.display.flip()
                    self.pixarray = new_pix
                    ctr += 1
        except StopIteration:
            pass
        finally:
            pygame.display.quit()

                
    def __call__(self, fn):
        "decorator sugar"
        self.render_fn = fn
        self.render_loop()
        return fn

'''
# In[23]:

@Renderer(window_size=(1280, 1024))
def noise(buf, frame_id):
    return (np.random.rand(*buf.shape) * 255)


# In[20]:

@Renderer(init=(np.random.rand(1024, 768, 3) * 255).astype(np.uint8))
def pulse(buf, frame_id):
    res = (np.sin(np.roll(buf, 12)) * 128).astype(np.uint8)
    return res
'''



