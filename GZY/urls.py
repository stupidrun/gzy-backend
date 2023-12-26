from django.urls import path
from django.views.generic import DetailView
from . import views, models


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
]