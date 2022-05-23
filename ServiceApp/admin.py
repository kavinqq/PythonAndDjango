from django.contrib import admin
from .models import Staff

class StaffAdmin(admin.ModelAdmin):
    list_display =  ('username', 'email')

# Register your models here.
admin.site.register(Staff,StaffAdmin)
