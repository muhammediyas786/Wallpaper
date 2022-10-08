from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Category)
admin.site.register(Wallpapers)
admin.site.register(Profile)
admin.site.register(Downloaded)
admin.site.register(Downloadcount)
admin.site.register(Uploadcount)