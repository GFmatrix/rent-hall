
import os
import random
import string
import uuid
from django.utils.timezone import now
from django.db import models
from django.urls import reverse_lazy

def upload_path_hall(instance, filename):
    return os.path.join(instance.name, filename)

def upload_path_hall_image(instance, filename):
    return os.path.join(instance.hall.name, filename)

def generate_short_application_id(length=6):
    while True:
        application_id = ''.join(random.choices(string.digits, k=length))
        if not Application.objects.filter(application_id=application_id).exists():
            return application_id

STATUS_CHOICES = (
    ('review', 'Kurib chiqilmoqda'),
    ('accept', 'Tasdiqlandi'),
    ('reject', 'Bekor qilindi'),
)

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Hall(models.Model):
    name = models.CharField(max_length=200, verbose_name='Zal nomi')
    image = models.ImageField(upload_to=upload_path_hall, verbose_name='Rasm')
    director = models.CharField(max_length=200, verbose_name='Ma\'sul odam')
    description = models.TextField(verbose_name='Tavsif')
    price = models.BigIntegerField(verbose_name='Narxi/so\'m')
    capacity = models.IntegerField(verbose_name='Sig\'imi')
    inn = models.BigIntegerField(verbose_name='INN')
    phone_number = models.CharField(max_length=200, verbose_name='Telefon raqam')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name='Viloyat')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name='Tuman')
    address = models.CharField(max_length=200, verbose_name='Manzil')
    size = models.CharField(max_length=200, verbose_name='Hajmi/m2')
    google_map = models.URLField(max_length=400,blank=True, null=True, verbose_name='Google map havolasi')
    availability = models.BooleanField(default=True, verbose_name='Mavjudligi')
    view_count = models.PositiveIntegerField(default=0, editable=False, verbose_name='Ko\'rishlar soni')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='O\'zgartirilgan vaqti')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.id})
    
    def location(self):
        return f"{self.region}, {self.district}, {self.address}"
    
    def uploaded(self):
        delta = now() - self.created_at
        if delta.days >= 365:
            years = delta.days // 365
            return f"{years} yil oldin"
        elif delta.days >= 30:
            months = delta.days // 30
            return f"{months} oy oldin"
        elif delta.days >= 1:
            return f"{delta.days} kun oldin"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} soat oldin"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} daqiqa oldin"
        else:
            return "Hozir"

    def delete(self, *args, **kwargs):
        if self.image and self.image.storage:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Zal'
        verbose_name_plural = 'Zallar'

class HallImage(models.Model):
    hall = models.ForeignKey(Hall, related_name='images', on_delete=models.CASCADE, verbose_name='Zal')
    image = models.ImageField(upload_to=upload_path_hall_image, verbose_name='Rasm')

    def __str__(self):
        return f"Image for {self.hall.name}"
    
    class Meta:
        verbose_name = 'Rasm'
        verbose_name_plural = 'Rasmlar'

class Application(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, verbose_name='Zal', related_name='applications')
    application_id = models.CharField(max_length=6, blank=True, unique=True, verbose_name='Ariza ID')
    name = models.CharField(max_length=200, verbose_name='Tashkilot nomi')
    director = models.CharField(max_length=200, verbose_name='Rahbar')
    phone_number = models.CharField(max_length=200, verbose_name='Telefon raqam')
    email = models.EmailField(verbose_name='Elektron pochta')
    inn = models.CharField(max_length=200, verbose_name='INN')
    account_number = models.CharField(max_length=200, verbose_name='Hisob raqam')
    address = models.CharField(max_length=200, verbose_name='Manzil')
    date_from = models.DateField(verbose_name='Boshlanish sanasi')
    date_to = models.DateField(verbose_name='Tugash sanasi')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='review', verbose_name='Holat')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')

    def __str__(self):
        return f"{self.application_id} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.application_id:
            self.application_id = generate_short_application_id()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Ariza'
        verbose_name_plural = 'Arizalar'