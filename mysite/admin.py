from django.contrib import admin
from .models import *

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name','category')

admin.site.register(User)
admin.site.register(Item,ItemAdmin)
admin.site.register(Restaurant)
admin.site.register(OrderItems)
admin.site.register(Order)
admin.site.register(Menu)
