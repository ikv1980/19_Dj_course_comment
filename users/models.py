from django.db import models
from django.contrib.auth.models import User
from PIL import Image

GENDER_CHOICES = [
    ('N', 'Не указан'),
    ('M', 'Мужской'),
    ('F','Женский'),
]

TYPE_ACCOUNT = (
    ('full', 'Полный пакет'),
    ('free', 'Бесплатный пакет')
)

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default='user.png', upload_to='user_images')
    gender = models.CharField('Пол пользователя', choices=GENDER_CHOICES, default='N', max_length=1)
    agreement = models.BooleanField('Согласие на отправку уведомлений на почту', default=True)
    account_type = models.CharField(choices=TYPE_ACCOUNT, default='free', max_length=30)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'
