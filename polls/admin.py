from django.contrib import admin

# Register your models here.

from .models import index, category

admin.site.register(index)
admin.site.register(category)
