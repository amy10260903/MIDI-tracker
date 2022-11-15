import os

from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse


def index(request):
    return render(request, 'index.html',
                  {'base_url': settings.BASE_URL})

def downloadFile(request):
    filename = request.GET.get('filename')
    file = open(os.path.join(settings.DOWNLOAD_DIR, filename), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename="{filename}"'
    return response
