from django.db import models
from django.utils.crypto import get_random_string


def product_image_path_and_filename(instance, filename):
    return f'static/upload/{instance.title or "general"}/{get_random_string(length=3)}_{filename}'


def product_detail_image_path_and_filename(instance, filename):
    return f'static/upload/{instance.product.title}/details/{get_random_string(length=3)}_{filename}'


class PageTypeChoices(models.IntegerChoices):
    PRODUCT_TYPE = 1, '产品页'
    CUSTOM_TYPE = 2, '自定义页'
    ARTICLE_TYPE = 3, '文章页'
    PRODUCT_LIST_TYPE = 4, '产品分类页'


class CustomPage(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)
    content = models.TextField(verbose_name='Content')
    banner_hidden = models.BooleanField(verbose_name='Banner Hidden', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at', '-updated_at')


class ProductCategory(models.Model):
    title = models.CharField(verbose_name='Title', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-created_at',
        )
        verbose_name_plural = 'Product Categories'

    def get_visible_products(self):
        return self.product_set.filter(visible=True).all()


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        verbose_name='Category',
    )
    title = models.CharField(verbose_name='Title', max_length=200)
    price = models.PositiveIntegerField(verbose_name='Price', default=9999)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    spec = models.CharField(verbose_name='Spec', null=True, blank=True, max_length=200)
    visible = models.BooleanField(verbose_name='Visible', default=True)
    main_img = models.ImageField(
        verbose_name='Main Image',
        upload_to=product_image_path_and_filename,
    )
    power = models.PositiveSmallIntegerField(verbose_name='Power of sort', default=100)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-power', '-created_at')

    def get_all_detail_images(self):
        return self.detail_images.filter(visible=True).all()


class ProductDetailImage(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Product',
        on_delete=models.PROTECT,
        related_name='detail_images',
    )
    index = models.PositiveSmallIntegerField(default=1, verbose_name='Index')
    visible = models.BooleanField(verbose_name='Visible', default=True)
    image = models.ImageField(
        verbose_name='Image',
        upload_to=product_detail_image_path_and_filename,
    )
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)

    def __str__(self):
        return f'{self.product.title} - {self.index}'

    class Meta:
        ordering = (
            'index',
            '-created_at',
        )


class Menu(models.Model):
    title = models.CharField(verbose_name='Title', max_length=100)
    index = models.PositiveSmallIntegerField(verbose_name='Index', default=1)
    page_type = models.IntegerField(
        verbose_name='Page Type',
        choices=PageTypeChoices.choices,
        default=PageTypeChoices.ARTICLE_TYPE,
    )
    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        verbose_name='Product Category',
        null=True, blank=True,
    )
    custom_page = models.ForeignKey(
        CustomPage,
        on_delete=models.PROTECT,
        verbose_name='Custom Page',
        null=True, blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Product',
        null=True, blank=True,
    )
    visible = models.BooleanField(verbose_name='Visible', default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        ordering = ('index', '-created_at')
        verbose_name_plural = verbose_name = 'Menu'

    def __str__(self):
        return self.title

    def get_target_id(self):
        if self.page_type == PageTypeChoices.CUSTOM_TYPE:
            return self.custom_page_id
        elif self.page_type == PageTypeChoices.PRODUCT_TYPE:
            return self.product_id
        elif self.page_type == PageTypeChoices.PRODUCT_LIST_TYPE:
            return self.product_category_id
