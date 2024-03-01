from django.db import models
from django.utils import timezone

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
    name = models.CharField(max_length=30)
    text = models.TextField()
    approved_comment = models.BooleanField(default=False)
    published_time = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name}'s comment: {self.text[:40]}"
    
    def approve(self):
        self.approved_comment = True
        self.save()       