from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings


def product_image_path_and_filename(instance, filename):
    return f'{instance.title or "general"}/{get_random_string(length=3)}_{filename}'


def product_detail_image_path_and_filename(instance, filename):
    return f'{instance.product.title}/details/{get_random_string(length=3)}_{filename}'


class SiteInfo(models.Model):
    site_name = models.CharField(verbose_name='Site Name', max_length=100)
    logo_url = models.URLField(verbose_name='LOGO URL', null=True, blank=True)
    mobile = models.CharField(verbose_name='Mobile Number', max_length=20)
    tel = models.CharField(verbose_name='Telephone', null=True, blank=True, max_length=25)
    address = models.CharField(verbose_name='Address', null=True, blank=True, max_length=255)
    agent_name = models.CharField(verbose_name='Agent Name', null=True, blank=True, max_length=50)
    email = models.EmailField(verbose_name='Email', null=True, blank=True, max_length=100)
    contact_qrcode = models.URLField(verbose_name='Qrcode for contact', null=True, blank=True)
    wechat_mp_qrcode = models.URLField(verbose_name='Qrcode for MP', null=True, blank=True)
    mini_program_qrcode = models.URLField(verbose_name='Qrcode for MiniProgram', null=True, blank=True)
    visible = models.BooleanField(verbose_name='Visible', default=False)

    @classmethod
    def get_enabled_one(cls):
        return cls.objects.filter(visible=True).first()

    def __str__(self):
        return f'{self.site_name}-{self.mobile}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.visible is True:
            self.__class__.objects.filter(visible=True).update(visible=False)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name_plural = verbose_name = 'Site Information'


class ArticleCategory(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Article Categories'
        verbose_name = 'Article Category'


class Article(models.Model):
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.PROTECT,
        verbose_name='Category',
    )
    title = models.CharField(verbose_name='Title', max_length=200)
    content = models.TextField(verbose_name='Content')
    visible = models.BooleanField(verbose_name='Visible', default=True)
    recommend = models.BooleanField(verbose_name='Recommend', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-created_at',
            '-updated_at',
        )


class Banner(models.Model):
    alt_text = models.CharField(
        verbose_name='Alter Text',
        null=True,
        blank=True,
        max_length=100,
    )
    url = models.URLField(verbose_name='Image URL')
    visible = models.BooleanField(verbose_name='Visible', default=True)
    created_at = models.DateTimeField(
        verbose_name='Created At',
        auto_now_add=True,
    )

    def __str__(self):
        return self.url

    class Meta:
        ordering = (
            '-created_at',
        )


class PageTypeChoices(models.IntegerChoices):
    PRODUCT_TYPE = 1, '产品页'
    CUSTOM_TYPE = 2, '自定义页'
    ARTICLE_TYPE = 3, '文章页'
    PRODUCT_LIST_TYPE = 4, '产品分类页'


class CustomPage(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)
    header_image = models.ImageField(verbose_name='Header Image', null=True, blank=True)
    footer_image = models.ImageField(verbose_name='Footer Image', null=True, blank=True)
    content = models.TextField(verbose_name='Content')
    raw_content = models.TextField(verbose_name='Raw Content', null=True, blank=True)
    banner_hidden = models.BooleanField(verbose_name='Banner Hidden', default=False)
    show_in_index = models.BooleanField(verbose_name='Show in homepage', default=False)
    show_in_mini_app = models.BooleanField(verbose_name='Show in mini app', default=False)
    is_about_us = models.BooleanField(verbose_name='Is About Us', default=False)
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
    show_in_index = models.BooleanField(verbose_name='Show in homepage', default=False)
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

    def get_all_detail_image_urls(self):
        return [v.url for v in self.detail_images.filter(visible=True).all()]

    def get_styled_main_image(self):
        try:
            return f'{self.main_img.url}{settings.QINIU_IMAGE_STYLE}'
        except:
            return ''


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

    @property
    def url(self):
        try:
            return f'{self.image.url}{settings.QINIU_IMAGE_STYLE}'
        except:
            return ''

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


class Segment(models.Model):
    title = models.CharField(verbose_name='Title', max_length=10)
    image = models.ImageField(verbose_name='image', null=True, blank=True)
    content = models.TextField(verbose_name='Content')
    visible = models.BooleanField(verbose_name='Visible', default=True)
    power = models.PositiveSmallIntegerField(verbose_name='Power of sort', default=10)
    created_at = models.DateTimeField(verbose_name='', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-power',
            '-created_at',
        )
