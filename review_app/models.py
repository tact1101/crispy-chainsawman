from django.db import models

class Title(models.Model):
    image = models.ImageField(upload_to='images/', null=False, blank=False) # not allowed to have a title without a preview picture
    title = models.CharField(max_length=60)
    description = models.TextField(default="Here will be a description soon!")
    published_date = models.DateField()
    
    def __str__(self):
        return self.title
    
    def publish(self):
        self.save()