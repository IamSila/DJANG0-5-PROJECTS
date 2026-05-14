from django.contrib import admin
from .models import Csv
# Register your models here.



@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_at', 'activated']
    search_fields = ['file_name', 'uploaded_at', 'activated']
