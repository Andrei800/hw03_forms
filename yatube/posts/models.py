from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название группы',
                             help_text='')
    slug = models.SlugField(unique=True,
                            default='title',
                            verbose_name='Адрес группы',
                            help_text='')
    description = models.TextField(verbose_name='Описание',
                                   help_text='Описание группы')
    
    def __str__(self):
        return self.title
    

class Post(models.Model):
    text = models.TextField(verbose_name='Текст',
                            help_text='Текст нового поста')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    help_text='Дата')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор поста'
    )

    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )

    class Meta:
        ordering = ('-pub_date',)
        

    def __str__(self):
        return self.text[:15]
    