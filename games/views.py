from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Game


def game_list(request):
    games = Game.objects.all()
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    
    if query:
        games = games.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_filter:
        games = games.filter(category=category_filter)
    
    categories = Game.CATEGORY_CHOICES
    
    context = {
        'games': games,
        'categories': categories,
        'selected_category': category_filter,
        'query': query,
    }
    return render(request, 'games/game_list.html', context)


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    related_games = Game.objects.filter(
        category=game.category
    ).exclude(pk=pk)[:4]
    
    context = {
        'game': game,
        'related_games': related_games,
    }
    return render(request, 'games/game_detail.html', context)
