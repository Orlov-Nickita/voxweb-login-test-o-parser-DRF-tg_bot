from django.contrib import admin
from django.utils.html import format_html

from api.models import ProductImage, Product


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели ProductImage (Изображения продукта)
    """
    list_display = ['id', 'file', 'alt']
    list_display_links = ['id', 'alt']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Product
    """
    list_display = ['id', 'href_short', 'title', 'new_price', 'old_price', 'sale', 'count_in_stock', 'rating', 'date']
    list_display_links = ['id', 'title']

    def href_short(self, obj):
        """
        Возвращает миниатюру изображения категории в общем списке, а также в карточке конкретной категории
        """
        if obj.href:
            return format_html(f'<a href="{obj.href}">URL</a>')

    href_short.short_description = 'Ссылка'
