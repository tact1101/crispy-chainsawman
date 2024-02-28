from django.shortcuts import render
from .models import Title

def anime(request):
    titles = Title.objects.order_by('title')
    return render(request, 'review_app/anime.html', {'titles': titles})
