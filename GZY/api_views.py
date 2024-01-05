from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models


class BannerSerializer(serializers.Serializer):
    url = serializers.URLField(read_only=True)
    alt_text = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class SegmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Segment
        exclude = (
            'visible',
            'power',
        )
        depth = 1


class SiteInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SiteInfo
        exclude = (
            'visible',
        )
        depth = 1


class CustomPageSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    raw_content = serializers.CharField(read_only=True)
    header_image = serializers.ImageField(read_only=True)
    footer_image = serializers.ImageField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class MenuModelSerializer(serializers.ModelSerializer):
    page_type = serializers.CharField(read_only=True, source='get_page_type_display')

    class Meta:
        model = models.Menu
        exclude = ('visible', 'created_at')
        depth = 2


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = ('visible', 'show_in_index')
        depth = 2

    def to_representation(self, instance: models.Product):
        ret = super().to_representation(instance)
        request: Request = self.context.get('request')
        if request.query_params.get('with_images'):
            ret['images'] = instance.get_all_detail_image_urls()
        return ret


class ArticleModelSerializer(MenuModelSerializer):
    class Meta:
        model = models.Article
        exclude = (
            'recommend',
            'visible',
        )
        depth = 1


class ArticleViewSets(ReadOnlyModelViewSet):
    serializer_class = ArticleModelSerializer
    queryset = models.Article.objects.filter(visible=True, recommend=True)


class ProductViewSets(ReadOnlyModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = models.Product.objects.filter(visible=True)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


class MenuViewSets(ReadOnlyModelViewSet):
    serializer_class = MenuModelSerializer
    queryset = models.Menu.objects.filter(visible=True)[:5]


class BannerViewSets(ReadOnlyModelViewSet):
    serializer_class = BannerSerializer
    queryset = models.Banner.objects.filter(visible=True)[:5]


class CustomPageViewSets(ReadOnlyModelViewSet):
    serializer_class = CustomPageSerializer
    queryset = models.CustomPage.objects.filter(show_in_mini_app=True, is_about_us=False)[:3]


class SegmentViewSets(ReadOnlyModelViewSet):
    serializer_class = SegmentModelSerializer
    queryset = models.Segment.objects.filter(visible=True)[:3]


@api_view(['GET'])
def about_us_page(request: Request) -> Response:
    return Response(
        CustomPageSerializer(models.CustomPage.objects.filter(is_about_us=True, show_in_mini_app=True).first()).data,
    )


@api_view(['GET'])
def site_info(request: Request) -> Response:
    return Response(
        SiteInfoModelSerializer(models.SiteInfo.get_enabled_one()).data,
    )
