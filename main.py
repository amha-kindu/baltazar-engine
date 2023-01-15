import pygame as pg
import moderngl as mgl
import sys

from model import *
from camera import Camera



class Baltazar:

    def __init__(self, win_size=(1000, 600)):
        # initialize pygame
        pg.init()

        # Set opengl attributes
        self.WIN_SIZE = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # Create an OpenGL context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Detect and use existing opengl context
        self.context = mgl.create_context()

        # Create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0

        # Initialize scene
        self.camera  = Camera(self)

        # self.scene = Triangle(self)
        self.scene = Cube(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.dispose()

                pg.quit()
                sys.exit()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def render(self):
        # Clear framebuffer
        self.context.clear(color=(0.08, 0.16, 0.18))

        # Render scene
        self.scene.render()

        # Swap buffers
        pg.display.flip()

    def run(self):
        while True:
            self.get_time()

            self.check_events()
            self.render()

            self.clock.tick(60)




if __name__ == '__main__':
    game_engine = Baltazar()
    game_engine.run()