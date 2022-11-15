from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets

from .utils import midi_tracks_generator

class FileUploadAPIView(viewsets.ViewSet):

    def create(self, request):
        print('>>> create')
        if request.FILES:
            for _, file in request.FILES.items():
                print(f'* file: {file.name}')

            filename = midi_tracks_generator(file)
            result = {
                'filename': filename,
                'url': f'{settings.BASE_URL}/download?filename={filename}'
            }
            return JsonResponse(result)