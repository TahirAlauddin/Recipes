from django.shortcuts import render
from .models import Category
from django.core.paginator import Paginator

# View for category page
def view_category(request):
    categories = Category.objects.all()
    if request.method == 'GET' and request.GET.get('q'):
        q = request.GET.get('q')
        categories = categories.filter(title__icontains=q)
    paginator = Paginator(categories, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()
    context = {'is_paginated': is_paginated,
                'page_obj': page_obj}
    return render(request, 'recipes/category.html', context=context)


# View for category detail page
def view_category_detail(request, slug):
    category = Category.objects.get(slug=slug)

    recipes = category.recipes.filter(approved=True)
    if request.method == 'GET' and request.GET.get('q'):
        q = request.GET.get('q')
        recipes = recipes.filter(title__icontains=q)

    context = {'recipes': recipes}
    return render(request, 'recipes/category_detail.html', context=context)

