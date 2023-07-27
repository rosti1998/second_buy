from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='images/', blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_photo = models.ImageField(upload_to='item_photos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    message = models.TextField()
    username = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(max_length=255, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='inquiries')


class Discussion(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    context = models.TextField()
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    message = models.TextField()
    username = models.CharField(max_length=50, blank=True, null=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)