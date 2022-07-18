from django.db import models
from PIL import Image
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User



class Course(models.Model):
    # slug, title, desc, image
    slug = models.SlugField('Slug', help_text='Укажите уникальный идентификатор курса', unique=True)
    title = models.CharField('Название курса', max_length=120)
    desc = models.TextField('Описание курса')
    image = models.ImageField('Изображение', default='default.png', upload_to='course_images')
    is_free = models.BooleanField('Бесплатно?', default=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.width > 425 or img.height > 280:
            resize = (425, 280)
            img.thumbnail(resize)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    # slug, title, desc, course, number, video_url
    slug = models.SlugField('Уникальное название урока')
    title = models.CharField('Название урока', max_length=120)
    desc = models.TextField('Описание урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Какой курс?')
    number = models.IntegerField('Номер урока')
    video = models.CharField('Видео URL', max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson-detail', kwargs={'slug': self.course.slug, 'lesson_slug': self.slug})

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class Comment(models.Model):
    def now_time():
        return timezone.now()

    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    post = models.ForeignKey(Lesson, verbose_name='Урок', on_delete=models.CASCADE)
    text = models.TextField('Сообщение', max_length=500)

    def __str__(self):
        return f'{self.user}. Lesson: {self.post}.'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'