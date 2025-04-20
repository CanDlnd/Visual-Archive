from django.contrib import admin
from .models import Image, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'upload_date', 'created_at')
    list_filter = ('category', 'upload_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'upload_date'
