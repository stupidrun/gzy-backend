from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from django.http.request import HttpRequest
from django.conf import settings
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
        'site_info': models.SiteInfo.objects.filter(visible=True).first(),
        'qiniu_style_path': settings.QINIU_IMAGE_STYLE,
    }


def index(request: HttpRequest):
    return render(request, 'index.html', {
        'page_list': models.CustomPage.objects.filter(show_in_index=True).all(),
        'product_list': models.Product.objects.filter(show_in_index=True, visible=True).all(),
        'article_list': models.Article.objects.filter(visible=True, recommend=True).all()[:7],
    })


def menu(request: HttpRequest, id: int):
    m = get_object_or_404(models.Menu, pk=id)
    target_id = m.get_target_id()
    if not target_id:
        raise Http404()
    v = view_dict.get(m.page_type)
    return redirect(reverse(v, kwargs={'id': target_id}))


def article(request: HttpRequest, id: int, show_categories=True):
    if show_categories:
        categories = models.ArticleCategory.objects.all()
    else:
        categories = []
    a = models.Article.objects.filter(pk=id).first()
    return render(request, 'article.html', {
        'article_categories': categories,
        'article': a,
        'recently': models.Article.objects.exclude(pk=id).filter(visible=True)[:2],
    })


def product_list(request: HttpRequest, id: int = 0):
    product_queryset = models.Product.objects.filter(visible=True)
    return render(request, 'product_list.html', {
        'categories': models.ProductCategory.objects.distinct().all(),
        'products': product_queryset.filter(category_id=id).all() if id != 0 else product_queryset.all(),
        'current_category_id': id,
        'current_category': None if id == 0 else models.ProductCategory.objects.filter(pk=id).first(),
    })


def custom_page(request: HttpRequest, id: int):
    page = get_object_or_404(models.CustomPage, pk=id)
    return render(request, 'custom_page.html', {
        'page': page,
        'hidden_banner': page.banner_hidden,
    })
