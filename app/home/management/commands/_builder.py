# -*-coding:Utf-8 -*

from __future__ import print_function
import re
import math
from itertools import combinations
from PIL import Image, ImageDraw, ImageFont
from _utils import *

DEBUG_MODE = False

map_settings = {
        'image_quality': 100,
        'allow_word_split': True,
        'allow_word_truncate': True,
        'smallest_word_split': 3,
        'truncate_string': '...',
        'invalid_string': '-',
        'font_type': 'arial.ttf',
        'font_line_spacing': 4,
        'font_color': (0, 0, 0, 0),
        'font_size_step': 1,
        'font_size': {
            'min': 10,
            'max': 24
        },
        'text_padding': (0.05, 0.05),
        'text_align': 'center',
        'default_bg_color': (0, 0, 0, 0),
        'max_bump_work': 1000,
    }


class FloorMap:
    canvas = None
    _image_base = None
    _rooms = None

    def __init__(self, base_image, settings):
        global map_settings

        map_settings.update(settings)

        self._image_base = Image.open(base_image)
        self.canvas = ImageDraw.Draw(self._image_base)

        self._rooms = Rooms()

    def render_image(self):
        self._rooms.render_all()

    # Saves image
    def save_to(self, output_file, quality=None):
        if quality is None:
            quality = map_settings['image_quality']

        self._image_base.save(output_file, quality=quality)

        if DEBUG_MODE:
            print("[SUCCESS] A new copy was saved at %s" % output_file)

    def add_room(self, data, options=None):
        self._rooms.add_room(self, data, options)

    # Returns dimensions of a text label
    def text_size(self, size, text):
        font = ImageFont.truetype(map_settings['font_type'], size=size)
        label_size = self.canvas.multiline_textsize(text, font=font, spacing=map_settings['font_line_spacing'])

        return label_size


# Stores the list of rooms to draw
class Rooms:
    _list_rooms = None
    _floor_map = None

    def __init__(self):
        self._list_rooms = []

    # Room factory depending on type
    def add_room(self, floor_map, data, options):
        self._floor_map = floor_map

        if options['show_code']:
            label = "\n".join((data['label'], data['code']))
        else:
            label = data['label']

        new_room = Room(floor_map, label, data['coords'], data['text_coords'], options)
        self._list_rooms.append(new_room)

        if DEBUG_MODE:
            print("Added new entity with label : \"%s\" at %s&%s" %
                  (label.replace("\n", "\\n"), data['coords'], data['text_coords']))

    def render_all(self):
        lst = self._list_rooms

        if DEBUG_MODE:
            print("****************************************")
            print("Rendering %d entities:" % len(lst))

        for room in lst:
            room.draw()
            room.print_label()

        if DEBUG_MODE:
            print("****************************************")
            print("[SUCCESS] Render has completed.")


# Parent class for rooms
class Room:
    label = ""  # Text to display on the room
    coords = []  # Coordinates of the rectangle or poly defining the room shape
    _text_area_coords = []  # Coordinates of the rectangle defining the zone where label can be printed
    _text_area_size = (0, 0)
    _text_padding = (0, 0)

    _floor_map = None
    _options = None

    _log__room_format = []
    _log__room_bump = []

    def __init__(self, floor_map, label, coords, text_area, options):
        self._floor_map = floor_map

        self.label = label
        self._options = options

        # Transform rect into poly if needed
        if len(coords) == 4:  # If room is rectangle
            self.coords = [coords[0], coords[1], coords[2], coords[1], coords[2], coords[3], coords[0], coords[3]]
        else:  # If room is not rectangle
            self.coords = coords

        # Sets default text area if none was specified
        if text_area:
            # Cleans received text area & makes sure the coords are in the correct order
            self._text_area_coords = boundary_box(text_area)
        else:
            # Generates a new boundary box from the coordinates received
            self._text_area_coords = boundary_box(coords)

    # Bumps text to a new line and re-balances text to the smallest width
    def bump_text(self, text, bumps_wanted=0):
        text = text.strip()

        space_count = text.count(" ")
        bump_count = text.count("\n")
        bump_count -= (1 if self._options['show_code'] else 0)
        word_count = bump_count + space_count + 1

        if bumps_wanted == 0:
            bumps_wanted = bump_count + 1

        if bumps_wanted < len(self._log__room_bump):
            if DEBUG_MODE:
                print("Try bump #%d! " % bumps_wanted, end="")
            return self._log__room_bump[bumps_wanted]

        if bumps_wanted == word_count:
            if DEBUG_MODE:
                print("Skipping; Nothing to bump! ", end="")
            return text

        if bumps_wanted > word_count:
            ex = "Asked for %s bumps but found %s words! \"%s\"" %\
                 (bumps_wanted, word_count, text.replace("\n", "\\n"))
            raise ValueError(ex)

        if space_count == 1:
            # Text only has 1 bump option
            if DEBUG_MODE:
                print("Bump!", end="")
            return text.replace(" ", "\n")
        elif space_count > 1:
            # Text has multiple bump options, find best option
            # Discards previous bumps to get new optimized bump balance

            task_weight = combinations_nb(word_count, bumps_wanted) * bumps_wanted

            if task_weight > map_settings['max_bump_work']:
                print("\n[WARNING] Too many combinations! (%s) Skipping. " % task_weight, end="")
                # Logs bump for future usage
                self._log__room_bump.append(text)
                return text
            elif DEBUG_MODE:
                print("\nProcessing %s bumps..." % task_weight, end="")

            # Everything is set; proceed with splitting

            words = re.split(r"[ \n]+", text)

            splits = combinations(range(1, word_count), bumps_wanted)

            shortest_length = 0
            shortest_text = text

            # Loops on bump options and finds smallest size
            for cmb in splits:
                new_text = " ".join(words[0:cmb[0]])

                for i in range(0, len(cmb) - 1):
                    ind_start = cmb[i]
                    ind_end = cmb[i + 1]
                    new_text = "\n".join((new_text, " ".join(words[ind_start:ind_end])))

                ind_last = cmb[len(cmb) - 1]
                new_text = "\n".join((new_text, " ".join(words[ind_last:word_count])))

                text_length = self._floor_map.text_size(map_settings['font_size']['max'], new_text)[0]

                if (text_length <= shortest_length) | (shortest_length == 0):
                    shortest_length = text_length
                    shortest_text = new_text

            if self._options['show_code']:
                shortest_text = "\n".join((shortest_text, words[word_count]))

            # Logs bump for future usage
            self._log__room_bump.append(shortest_text)

            if DEBUG_MODE:
                print("bump! ", end="")

            return shortest_text
        else:
            ex = "An error occurred while trying to bump the text with values : (%s, %s)" % (text, bumps_wanted)
            raise ValueError(ex)

    def truncate_text(self, text):
        text = text.strip()

        words = re.split(r"[ \n]+", text)

        # Finds the last word to be truncated out
        last_word_ind = (len(words) - 1 if self._options['show_code'] else len(words)) - 1
        last_word = words[last_word_ind]

        # Ignores old truncate string
        if last_word.endswith(map_settings['truncate_string']):
            last_word = last_word[:-len(map_settings['truncate_string'])]

        # Removes split dash so it is not the last character
        if words[last_word_ind - 1].endswith("-"):
            words[last_word_ind - 1] = words[last_word_ind - 1][:-1]

        # Applies minimum word splitting rules
        if len(last_word) <= map_settings['smallest_word_split']:
            words.pop(last_word_ind)
            words[last_word_ind - 1] += map_settings['truncate_string']
        else:
            words[last_word_ind] = "".join((
                last_word[:map_settings['smallest_word_split']],
                map_settings['truncate_string']
            ))

        # Truncates string and returns
        if self._options['show_code']:
            return "\n".join((" ".join(words[:len(words) - 1]), words[len(words) - 1]))
        else:
            return " ".join(words)

    def split_long_words(self, text, area_size):
        text = text.strip()

        padding = self.get_padding()

        words = re.split(r"[ \n]+", text)

        ind_large_words = []

        # Loops on words to find if any would still be too large when at minimum font size
        for i in range(0, len(words)):
            word = words[i]

            label_size = self._floor_map.text_size(map_settings['font_size']['min'], word)
            area_size = (area_size[0] - padding[0] * 2, area_size[1] - padding[1] * 2)

            if label_size[0] > area_size[0]:
                ind_large_words.append(i)

        if len(ind_large_words) == 0:
            if DEBUG_MODE:
                print("[NOTICE] All words fit horizontally in the text area at minimum size.")
            return text
        elif DEBUG_MODE:
            print("[WARNING] Found %d word(s) that are too long to fit even at minimum size. Splitting..." %
                  (len(ind_large_words)), end="")

            for ind in ind_large_words:
                word = words[ind]
                split = int(math.ceil(len(word) / 2))
                word = "-\n".join((word[:split], word[split:]))

                words[ind] = word

            if self._options['show_code']:
                return "\n".join((" ".join(words[:len(words) - 1]), words[len(words) - 1]))
            else:
                return " ".join(words)

    def get_text_area_coords(self):
        return self._text_area_coords

    def get_text_area_size(self):
        # Initializes element if it wasn't already
        if self._text_area_size == (0, 0):
            bbox = self.get_text_area_coords()

            # Sets maximum size allowed for text area
            max_w = bbox[2] - bbox[0]  # maxX - minX
            max_h = bbox[3] - bbox[1]  # maxY - minY

            self._text_area_size = (max_w, max_h)
        return self._text_area_size

    def get_padding(self):
        # Initializes element if it wasn't already
        if self._text_padding == (0, 0):
            area = self.get_text_area_size()

            padding_w = map_settings['text_padding'][0]
            padding_h = map_settings['text_padding'][1]

            padding_w *= (area[0] if padding_w < 1 else 1)
            padding_h *= (area[1] if padding_h < 1 else 1)

            padding_w = math.floor(padding_w)
            padding_h = math.floor(padding_h)

            self._text_padding = (padding_w, padding_h)
        return self._text_padding

    def get_best_format(self, size, text, depth=0):

        if not map_settings['font_size']['min'] <= size <= map_settings['font_size']['max']:
            ex = "[ERROR] Invalid font size! Expected value to be within [%d, %d] but got %d." %\
                 (map_settings['font_size']['min'], map_settings['font_size']['max'], size)
            raise ValueError(ex)

        log_string = "%s, %s" % (size, text)

        if log_string in self._log__room_format:
            if DEBUG_MODE:
                print("Skipping; Already explored. ", end="")

            return None
        else:
            self._log__room_format.append(log_string)

        text_area_size = self.get_text_area_size()
        text_area_padding = self.get_padding()

        area_size = (text_area_size[0] - text_area_padding[0] * 2, text_area_size[1] - text_area_padding[1] * 2)
        label_size = self._floor_map.text_size(size, text)

        # Label fits in text area, return as best format
        if (label_size[0] <= area_size[0]) & (label_size[1] <= area_size[1]):
            if DEBUG_MODE:
                print("Fits at size %d! [%d] " % (size, depth), end="")

            return size, text
        elif DEBUG_MODE:
            print("Fetching [%d]..." % depth, end="")

        # Shrink text
        shrink_size = size - map_settings['font_size_step']
        if shrink_size > map_settings['font_size']['min']:
            if DEBUG_MODE:
                print("Shrinking %d => %d..." % (size, shrink_size), end="")

            option1 = self.get_best_format(shrink_size, text, depth + 1)
        else:
            option1 = None

        bumped = self.bump_text(text)

        # Bump text or return failed format if can't bump
        if bumped != text:
            option2 = self.get_best_format(size, bumped, depth + 1)
        else:
            option2 = None

        if (option1 is None) & (option2 is None):
            return None

        # Result if one of the options has failed
        if option1 is None:
            return option2
        elif option2 is None:
            return option1

        # Returns best option
        if option1[0] + 1 > option2[0]:
            return option1
        else:
            return option2

    def print_label(self):
        if self.label == "":
            return

        label = self.label
        label_pos = [0, 0]

        best_format = None
        valid_format = False
        truncate_attempt_nb = 0

        while not valid_format:
            self._log__room_format = []
            self._log__room_bump = []
            self._log__room_bump.append(label)

            truncate_attempt_nb += 1

            if map_settings['allow_word_split']:
                label = self.split_long_words(label, self.get_text_area_size())

                if DEBUG_MODE:
                    print("Done.")

            # Fetches the right text format to fit in the text area
            if DEBUG_MODE:
                print("****************************************")
                print("Searching for best result for \"%s\" :" % label.replace("\n", "\\n"))

            best_format = self.get_best_format(map_settings['font_size']['max'], label)

            if DEBUG_MODE:
                print("Done.")

            if best_format is None:
                if map_settings['allow_word_truncate']:
                    if DEBUG_MODE:
                        print("[WARNING] Text couldn't fit. Truncating (attempt #%d)..." % truncate_attempt_nb, end="")

                    label = self.truncate_text(label)

                    if DEBUG_MODE:
                        print("Done.")
                        print("[WARNING] Text truncated to \"%s\"." % label.replace("\n", "\\n"))
                else:
                    if DEBUG_MODE:
                        print("[WARNING] Text couldn't fit and truncating isn't allowed! Returning invalid string.")

                    best_format = (map_settings['font_size']['max'], map_settings['invalid_string'])

            valid_format = best_format is not None

        if DEBUG_MODE:
            print("[SUCCESS] Result found: (%s, \"%s\")" %
                  (best_format[0], best_format[1].replace("\n", "\\n")))

        best_size = best_format[0]
        best_text = best_format[1]

        label_size = self._floor_map.text_size(best_size, best_text)
        area_coords = self.get_text_area_coords()
        area_size = self.get_text_area_size()

        label_pos[0] = area_coords[0] + (area_size[0] - label_size[0]) / 2
        label_pos[1] = area_coords[1] + (area_size[1] - label_size[1]) / 2

        font = ImageFont.truetype(map_settings['font_type'], size=best_size)

        self._floor_map.canvas.multiline_text(
            label_pos,
            best_text,
            font=font,
            fill=map_settings['font_color'],
            spacing=map_settings['font_line_spacing'],
            align=map_settings['text_align'])

    def draw(self):
        if self._options['bg_color'] is None:
            bg_color = map_settings['default_bg_color']
        else:
            bg_color = self._options['bg_color']

        self._floor_map.canvas.polygon(self.coords, fill=bg_color)
