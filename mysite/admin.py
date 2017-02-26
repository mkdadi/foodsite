from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(Menu)
