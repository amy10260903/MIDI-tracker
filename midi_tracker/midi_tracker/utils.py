import os
from django.conf import settings

from processor import main as midi_processor

def check_output_directory():
    if not os.path.exists(settings.DOWNLOAD_DIR):
        os.mkdir(settings.DOWNLOAD_DIR)

def midi_tracks_generator(file):
    check_output_directory()
    output_filename = midi_processor.main(file, settings.BASE_DIR)
    return output_filename