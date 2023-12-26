import datetime

from django.db import models


class Message(models.Model):
    phone = models.CharField(verbose_name='Phone', max_length=20)
    name = models.CharField(verbose_name='Name', max_length=50)
    content = models.TextField(verbose_name='Content', null=True, blank=True)
    followed = models.BooleanField(verbose_name='Followed', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    followed_at = models.DateTimeField(verbose_name='Followed At', null=True, blank=True, editable=False)

    def make_followed(self):
        self.followed = True
        self.followed_at = datetime.datetime.now()
        self.save()

    def __str__(self):
        return f'{self.name}-{self.phone}'

    class Meta:
        ordering = (
            '-created_at',
        )
