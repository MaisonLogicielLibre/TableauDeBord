from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from app.home.models import RoomType, Room, Rent
from _builder import FloorMap
from ast import literal_eval
import os

MEDIA_PATH = os.path.join(settings.MEDIA_ROOT, "floor_map")
INPUT_FILENAME = "floor_map_base.jpg"
OUTPUT_FILENAME = "floor_map.jpg"

# ToDo: Add color field in RoomType
# Colors
CLR_GREY = (200, 200, 200)
CLR_ORANGE = (250, 147, 29)
CLR_VIOLET = (175, 41, 76)
CLR_RED = (240, 61, 67)
# ToDo end


class Command(BaseCommand):
    def handle(self, *args, **options):
        input_image = os.path.join(MEDIA_PATH, INPUT_FILENAME)
        output_image = os.path.join(MEDIA_PATH, OUTPUT_FILENAME)

        map_settings = {}

        floor_map = FloorMap(input_image, map_settings)

        rooms = Room.objects.all()

        for room in rooms:
            company = room.get_owner_name()

            if room.is_rental():
                if company:
                    room_label = company
                else:
                    room_label = "Libre"
            else:
                room_label = room.static_label

            # ToDo: Fetch color from color field in RoomType options
            if room.type_id == 1:
                bg_color = CLR_GREY
            elif room.type_id == 2:
                bg_color = CLR_VIOLET
            elif room.type_id == 3:
                if company:
                    bg_color = CLR_ORANGE
                else:
                    bg_color = CLR_RED
            else:
                bg_color = CLR_GREY
            # ToDo end

            if room.text_coords:
                room.text_coords = literal_eval(room.text_coords)

            data = {
                'label': room_label,
                'code': room.code,
                'coords': literal_eval(room.coords),
                'text_coords': room.text_coords,
            }

            options = {
                'show_code': (len(room.code) > 0),
                'bg_color': bg_color,
            }
            
            floor_map.add_room(data, options)

        floor_map.render_image()
        floor_map.save_to(output_image)
