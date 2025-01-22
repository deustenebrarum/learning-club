from django.db import models
from django.contrib.auth.models import User
import re


class Course(models.Model):
    title = models.CharField(
        max_length=100, blank=False, verbose_name='название'
    )
    description = models.TextField(verbose_name='описание')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления'
    )
    is_active = models.BooleanField(default=True, verbose_name='активен')
    preview_image = models.ImageField(upload_to='courses/', verbose_name='превью')
    
    class Meta:
        verbose_name_plural = 'курсы'
        verbose_name = 'курс'
    
    def __str__(self):
        return self.title

class UserCourse(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=False, verbose_name='пользователь'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        null=False, verbose_name='курс'
    )
    is_finished = models.BooleanField(default=False, verbose_name='завершен')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания'
    )
    
    class Meta:
        verbose_name_plural = 'пользователи курсов'
        verbose_name = 'пользователь курса'
    
    def __str__(self):
        return f'{self.user} - {self.course}'


class Lesson(models.Model):
    topic = models.CharField(
        max_length=100, blank=False, verbose_name='тема'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        null=False, verbose_name='курс'
    )
    description = models.TextField(verbose_name='описание')
    video = models.FileField(
        null=True, blank=True,
        upload_to='uploads/%Y/%m/%d/',
        verbose_name='видео'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания'
    )

    class Meta:
        verbose_name_plural = 'уроки'
        verbose_name = 'урок'
