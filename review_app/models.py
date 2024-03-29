from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.conf import settings

class CustomUser(AbstractUser):
    
    def default_profile_picture():
        return 'default/lesfrogggg.jpg'
    pfp = models.ImageField(upload_to='pfp/', null=False, blank=False, default=default_profile_picture)
    
    # overriding existing fields from the parent class
    first_name = models.CharField(max_length=30, blank=True)  # Setting blank=True to allow empty values
    last_name = models.CharField(max_length=150, blank=True)  # Setting blank=True to allow empty values
    
    # Provide unique related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_group'  # Provide a unique related_name
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions'  # Provide a unique related_name
    )
    
    class Meta:
        permissions = [
            ('sudo_perm', 'Has admin permissions'),
        ]
        

class Title(models.Model):
    image = models.ImageField(upload_to='images/', null=False, blank=False) # not allowed to have a title without a preview picture
    title = models.CharField(max_length=60)
    description = models.TextField(default="Here will be a description soon!")
    published_date = models.DateField()
    
    def __str__(self):
        return self.title
    
    def publish(self):
        self.save()


class Comment(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='comments', null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True) 
    text = models.TextField()
    approved_comment = models.BooleanField(default=False)
    published_time = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.author}'s comment: {self.text[:40]}"
    
    def approve(self):
        self.approved_comment = True
        self.save()      
