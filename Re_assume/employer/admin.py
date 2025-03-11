from django.contrib import admin
from .models import *
# Register your models here.

class emp_table(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_no', 'created_at', 'updated_at')
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['created_at', 'updated_at']

admin.site.register(employer_table,emp_table)