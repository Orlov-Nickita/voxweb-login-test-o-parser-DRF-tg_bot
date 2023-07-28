from django.contrib import admin

from api.models import ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели ProductImage (Изображения продукта)
    """
    list_display = ['id', 'file', 'alt']
    list_display_links = ['id', 'alt']
