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


def get_icp_info():
    return 'ABCDEFGHIJKL'


def get_company_name():
    return 'Haoxuan'


def menu_request_context(request: HttpRequest):
    return {
        'menu_list': models.Menu.objects.filter(visible=True).all()[:4],
        'ICP': get_icp_info(),
        'company_name': get_company_name(),
        'banner_list': models.Banner.objects.filter(visible=True)[:5],
        'categories': models.ProductCategory.objects.distinct().all(),
    }


def index(request: HttpRequest):
    return render(request, 'index.html', {
        'page_list': models.CustomPage.objects.filter(show_in_index=True).all(),
        'product_list': models.Product.objects.filter(show_in_index=True).all(),
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
        'current_category_id': id,
    })


def custom_page(request: HttpRequest, id: int):
    page = get_object_or_404(models.CustomPage, pk=id)
    return render(request, 'custom_page.html', {
        'page': page,
        'hidden_banner': page.banner_hidden,
    })
