import os

from django.conf import settings

def check_output_directory():
    if not os.path.exists(settings.DOWNLOAD_DIR):
        os.mkdir(settings.DOWNLOAD_DIR)

def midi_tracks_generator(file):
    check_output_directory()
    return 'test.py'