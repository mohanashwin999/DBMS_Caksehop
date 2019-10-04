from django.contrib import admin
from .models import *

admin.site.register(user)
admin.site.register(order)
admin.site.register(price_calculate)
admin.site.register(feedback)
admin.site.register(cake)

