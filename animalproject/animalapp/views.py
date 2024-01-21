from django.shortcuts import render
from django.http import JsonResponse
from .models import Animal
import jaconv

def search_animal(request):
    # Ajaxリクエストを確認するためにヘッダーを使用
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        # ひらがなをカタカナに変換
        query_kana = jaconv.hira2kata(query)
        # カタカナでフィルタリング
        animals = Animal.objects.filter(animal_name__icontains=query_kana)
        # QuerySetをリストに変換してソート
        animals = sorted(list(animals), key=lambda animal: animal.animal_name.find(query_kana))
        results = [animal.animal_name for animal in animals]
        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'Not Ajax request'})

def home(request):
    return render(request, 'search.html')