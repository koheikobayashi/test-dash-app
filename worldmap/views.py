from django.shortcuts import render

def index(request):
    return render(request, 'worldmap/index.html')

def health(request):
    # 新しいビュー
    return render(request, 'worldmap/health.html')