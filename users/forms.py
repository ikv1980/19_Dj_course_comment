from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, GENDER_CHOICES


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        required=True,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'})
    )
    password1 = forms.CharField(
        label='Пароль',
        required=True,
        help_text='Пароль не должен быть маленьким и простым',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторно введите пароль'})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        required=True,
        help_text='Обязательное поле. Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label='Загрузить фото',
        required=False,
        widget=forms.FileInput
    )
    gender = forms.CharField(
        label='Выберите пол', 
        required=False,
        widget=forms.Select(choices=GENDER_CHOICES)
        )

    agreement = forms.BooleanField(
        label = 'Согласие на отправку уведомлений на почту',
        required=False,
        )

    class Meta:
        model = Profile
        fields = ['img', 'gender', 'agreement']

