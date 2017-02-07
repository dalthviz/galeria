from __future__ import unicode_literals

from django.contrib.auth.forms import forms
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.


class Imagen(models.Model):
    url = models.CharField(max_length=1000)
    title = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=5, blank=True)
    imageFile = models.ImageField(upload_to='images', null=True)
    user = models.ForeignKey(User, null=True)

class ImageForm(ModelForm):

    class Meta:
        model = Imagen
        fields = ['url', 'title', 'description', 'type', 'imageFile']


class UserForm(ModelForm):

    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email de usuario ya registrado')
        return email


    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Claves no coinciden')
        return password2

