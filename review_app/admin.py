from django.contrib import admin
from .models import Title, Comment, CustomUser

admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(CustomUser)
