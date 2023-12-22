from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from . import models


view_dict = {
    models.PageTypeChoices.ARTICLE_TYPE: 'article',
    models.PageTypeChoices.CUSTOM_TYPE: 'custom_page',
    models.PageTypeChoices.PRODUCT_TYPE: 'product',
    models.PageTypeChoices.PRODUCT_LIST_TYPE: 'product_list',
}


def menu_request_context(request: HttpRequest):
    return {
        'menu_list': models.Menu.objects.filter(visible=True).all()[:4],
    }


def index(request: HttpRequest):
    return render(request, 'index.html', {
    })


def menu(request: HttpRequest, id: int):
    m = get_object_or_404(models.Menu, pk=id)
    target_id = m.get_target_id()
    if not target_id:
        raise Http404()
    v = view_dict.get(m.page_type)
    return redirect(reverse(v, kwargs={'id': target_id}))


def article(request: HttpRequest, id: int):
    return HttpResponse('article')


def product_list(request: HttpRequest, id: int):
    category = get_object_or_404(models.ProductCategory, pk=id)
    return render(request, 'product_list.html', {
        'categories': models.ProductCategory.objects.distinct().all(),
        'category': category,
    })


def custom_page(request: HttpRequest, id: int):
    page = get_object_or_404(models.CustomPage, pk=id)
    return render(request, 'custom_page.html', {
        'page': page,
        'hidden_banner': page.banner_hidden,
    })
