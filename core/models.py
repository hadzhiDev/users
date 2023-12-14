from django.db import models
from utils.models import TimeStampAbstractModel


class Post(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('-created_at',)

    title = models.CharField('название', max_length=200)
    content = models.TextField('контент')
    author = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='Владелец', null=True)