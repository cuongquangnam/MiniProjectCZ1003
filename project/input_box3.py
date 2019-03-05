"""
Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.

Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.
"""

import os.path

import pygame
import pygame.locals as pl

pygame.font.init()


class TextInput():
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(
            self,
            initial_string = " ",
            font_family = "Calibri",
            font_size = 30,
            antialias = True,
            text_color = (0, 0, 0),
            cursor_color = (0, 0, 1),
            repeat_keys_initial_ms = 400,
            repeat_keys_interval_ms = 35):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when helpd
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.input_string = initial_string  # Inputted text
        self.active = True
        self.rect = ""
        self.font_object = pygame.font.SysFont(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = not self.active
                else:
                    self.active = False
        if self.active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.cursor_visible = True  # So the user sees where he writes

                    # If none exist, create counter for that key:
                    if event.key not in self.keyrepeat_counters:
                        self.keyrepeat_counters[event.key] = [0, event.unicode]

                    if event.key == pygame.K_BACKSPACE:
                        self.input_string = (
                            self.input_string[:max(self.cursor_position - 1, 1)]
                            + self.input_string[self.cursor_position:]
                        )

                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 1)
                    elif event.key == pygame.K_DELETE:
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + self.input_string[self.cursor_position + 1:]
                        )

                    elif event.key == pygame.K_RETURN:
                        return True

                    elif event.key == pygame.K_RIGHT:
                        # Add one to cursor_pos, but do not exceed len(input_string)
                        self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                    elif event.key == pygame.K_LEFT:
                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 1)

                    elif event.key == pygame.K_END:
                        self.cursor_position = len(self.input_string)

                    elif event.key == pygame.K_HOME:
                        self.cursor_position = 0

                    else:
                        # If no special key is pressed, add unicode of key to input_string
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + event.unicode
                            + self.input_string[self.cursor_position:]
                        )
                        self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

                elif event.type == pygame.KEYUP:
                    # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                    if event.key in self.keyrepeat_counters:
                        del self.keyrepeat_counters[event.key]

            # Update key counters:
            for key in self.keyrepeat_counters:
                self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

                # Generate new key events if enough time has passed:
                if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                    self.keyrepeat_counters[key][0] = (
                        self.keyrepeat_intial_interval_ms
                        - self.keyrepeat_interval_ms
                    )

                    event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))

            # Re-render text surface:
            self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

            # Update self.cursor_visible
            self.cursor_ms_counter += self.clock.get_time()
            if self.cursor_ms_counter >= self.cursor_switch_ms:
                self.cursor_ms_counter %= self.cursor_switch_ms
                if self.active:
                    self.cursor_visible = not self.cursor_visible
                else: self.cursor_visible = False

            if self.cursor_visible:
                cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
                # Without this, the cursor is invisible when self.cfursor_position > 0:
                if self.cursor_position > 0:
                    cursor_y_pos -= self.cursor_surface.get_width()
                self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

            self.clock.tick(60)
            return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = " "
        self.cursor_position = 1

class TextInput1():
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(
            self,
            initial_string = "",
            font_family = "Consolas",
            font_size = 30,
            antialias = True,
            text_color = (0, 0, 0),
            cursor_color = (0, 0, 1),
            repeat_keys_initial_ms = 400,
            repeat_keys_interval_ms = 35):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when helpd
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.input_string = initial_string  # Inputted text
        self.active = True
        self.rect = ""
        self.font_object = pygame.font.SysFont(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = not self.active
                else:
                    self.active = False
        if self.active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.cursor_visible = True  # So the user sees where he writes

                    # If none exist, create counter for that key:
                    if event.key not in self.keyrepeat_counters:
                        self.keyrepeat_counters[event.key] = [0, event.unicode]

                    if event.key == pygame.K_BACKSPACE:
                        self.input_string = (
                            self.input_string[:max(self.cursor_position - 1, 0)]
                            + self.input_string[self.cursor_position:]
                        )

                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 0)
                    elif event.key == pygame.K_DELETE:
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + self.input_string[self.cursor_position + 1:]
                        )

                    elif event.key == pygame.K_RETURN:
                        return True

                    elif event.key == pygame.K_RIGHT:
                        # Add one to cursor_pos, but do not exceed len(input_string)
                        self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                    elif event.key == pygame.K_LEFT:
                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 0)

                    elif event.key == pygame.K_END:
                        self.cursor_position = len(self.input_string)

                    elif event.key == pygame.K_HOME:
                        self.cursor_position = 0

                    else:
                        # If no special key is pressed, add unicode of key to input_string
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + event.unicode
                            + self.input_string[self.cursor_position:]
                        )
                        self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

                elif event.type == pygame.KEYUP:
                    # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                    if event.key in self.keyrepeat_counters:
                        del self.keyrepeat_counters[event.key]

            # Update key counters:
            for key in self.keyrepeat_counters:
                self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

                # Generate new key events if enough time has passed:
                if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                    self.keyrepeat_counters[key][0] = (
                        self.keyrepeat_intial_interval_ms
                        - self.keyrepeat_interval_ms
                    )

                    event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))

            # Re-render text surface:
            self.surface = self.font_object.render("*" * len(self.input_string), self.antialias, self.text_color)

            # Update self.cursor_visible
            self.cursor_ms_counter += self.clock.get_time()
            if self.cursor_ms_counter >= self.cursor_switch_ms:
                self.cursor_ms_counter %= self.cursor_switch_ms
                if self.active:
                    self.cursor_visible = not self.cursor_visible
                else: self.cursor_visible = False

            if self.cursor_visible:
                cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
                # Without this, the cursor is invisible when self.cfursor_position > 0:
                if self.cursor_position > 0:
                    cursor_y_pos -= self.cursor_surface.get_width()
                self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

            self.clock.tick(60)
            return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = " "
        self.cursor_position = 1

# Create TextInput-object
# textinput = TextInput()
# box = pygame.Rect(10, 10, 300, 40)
# textinput.rect = box
# screen = pygame.display.set_mode((1000, 200))
#
# clock = pygame.time.Clock()

# while True:
#     screen.fill((225, 225, 225))
#
#     pygame.draw.rect(screen, (255,255,255), box, 3)
#     events = pygame.event.get()
#     for event in events:
#         mouse = pygame.mouse.get_pos()
#         if event.type == pygame.QUIT:
#             exit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             pass
#
#     # Feed it with events every frame
#     textinput.update(events)
#     # Blit its surface onto the screen
#     screen.blit(textinput.get_surface(), box)
#
#     pygame.display.update()
#     clock.tick(30)
