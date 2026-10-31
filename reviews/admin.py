from django.contrib import admin
from .models import Product
from .models import Review
from .models import MonthlyReport


admin.site.register(Product)
admin.site.register(Review)
admin.site.register(MonthlyReport)