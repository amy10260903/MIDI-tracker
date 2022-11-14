from django.http import HttpResponse
from rest_framework import viewsets

class FileUploadAPIView(viewsets.ViewSet):

    def create(self, request):
        print('>>> create')
        for filename, file in request.FILES.items():
            print(f'* {filename} {file.name}')
        return HttpResponse(status=201)