import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class GameLoop:
    def __init__(self, drawables):
        self.exit_flag = False
        if not isinstance(drawables, set):
            raise TypeError("drawables should be a Set. Sets provide \
                fast lookup and avoid duplicates")

        self.drawables = drawables
        self._event_handlers = {}
        self.state = {}  # a dictionary for storing in-game variables.
        self.exit_flag = False  # a flag to exit the game.

    def define_handler(self, pygame_event, handler):
        '''
        A semantic way to add event handler functions to the game loop.

        :param pygame_event: The event object from PyGame.
        :param handler: A function that handles the event with the format
          def <name>(loop, event)

        An example of MOUSEBUTTONDOWN handler:
        def handle_click(loop, event):
            # loop: the event loop will pass itself in.
            # event: the event object from pygame
            if button == 1:  # left click
                loop.state['MOUSEDOWN'] = true  # set the loop state
                loop.drawables.append(potato)   # show a potato

        Common pygame events and their params:
            ACTIVEEVENT      gain, state
            KEYDOWN          unicode, key, mod
            KEYUP            key, mod
            MOUSEMOTION      pos, rel, buttons
            MOUSEBUTTONUP    pos, button
            MOUSEBUTTONDOWN  pos, button
            JOYAXISMOTION    joy, axis, value
            JOYBALLMOTION    joy, ball, rel
            JOYHATMOTION     joy, hat, value
            JOYBUTTONUP      joy, button
            JOYBUTTONDOWN    joy, button
            VIDEORESIZE      size, w, h
            VIDEOEXPOSE      none
            USEREVENT        code

        Note: pygame.QUIT is not overridable in the default loop to avoid jerks.
        '''
        self._event_handlers[pygame_event] = handler

    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."

        # OpenGL setup.
        # Set perspective, aspect ratio, clipping bounds
        gluPerspective(45, (display.get_width() / display.get_height()), 0.2, 10.)
        # Zoom out a bit.
        glTranslatef(0., 0., -1.)  # zoom out a bit
        # Rotate the entire field a bit to simulate a camera angle.
        glRotatef(22, 0, 0, 0)

        self.exit_flag = False
        while not self.exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type in self._event_handlers:
                    self._event_handlers[event.type](self, event)

            # clear the screen
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            for d in self.drawables:
                if (hasattr(d, 'GLDraw')):
                    d.GLDraw()
                else:
                    raise AttributeError('GameLoop: drawable has no .GLDraw() \
                        and cannot be drawn.')

        pygame.display.flip()
        clock.tick(clock_rate)

    def __enter__(self):  # A place to load game assets. Override as needed.
        "Actions performed when the class is created using a 'with' statement."
        print("Game loop created.")
        return self

    def __exit__(self, type, value, traceback):  # Destroy game assets. Override as needed.
        "Actions performed when the class exits."
        print("Exiting game loop.")
        return False  # do not supress any errors.