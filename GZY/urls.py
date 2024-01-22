from django.urls import path, include
from django.views.generic import DetailView
from . import views, models, api_views
from contact_message import api_views as message_api
from rest_framework.routers import DefaultRouter


api_router = DefaultRouter()
api_router.register('banner', api_views.BannerViewSets)
api_router.register('custom_page_home', api_views.CustomPageViewSets)
api_router.register('menu', api_views.MenuViewSets)
api_router.register('product', api_views.ProductViewSets)
api_router.register('article', api_views.ArticleViewSets)
api_router.register('segment', api_views.SegmentViewSets)


urlpatterns = [
    path('', views.index, name='index'),
    path('menu/<int:id>/', views.menu, name='menu'),
    path('article/<int:id>/', views.article, name='article'),
    path('custom_page/<int:id>/', views.custom_page, name='custom_page'),
    path('product/<int:id>/', DetailView.as_view(
        context_object_name='product',
        queryset=models.Product.objects.filter(visible=True),
        template_name='product.html',
        pk_url_kwarg='id',
    ), name='product'),
    path('product_list/<int:id>/', views.product_list, name='product_list'),
    path('product_list/', views.product_list, name='product_list'),

    # api views
    # path('api/v1/product/<int:product_id>/images/', api_views.product_detail_images),
    path('api/v1/about_us_page/', api_views.about_us_page),
    path('api/v1/site_info/', api_views.site_info),
    path('api/v1/', include(api_router.urls)),

    # Message API View
    path('api/v1/message/', message_api.CreateMessageView.as_view()),
]
