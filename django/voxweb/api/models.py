from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ProductImage(models.Model):
    """
    Модель Изображение продукта
    """

    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = 'фотография товара'
        verbose_name_plural = 'фотографии товаров'

    file = models.ImageField(upload_to='products_pictures/', verbose_name='изображение товара')
    alt = models.TextField(verbose_name='описание изображения')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Возвращает строку c названием фото
        """
        return '{} {}'.format('Фото', self.alt)


class Product(models.Model):
    """
    Модель Продукт
    """

    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    href = models.CharField(verbose_name='ссылка', null=True, max_length=500)
    image = models.OneToOneField(ProductImage, verbose_name='изображение товара', blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, verbose_name='название')
    new_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена со скидкой')
    old_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена без скидки')
    sale = models.IntegerField(verbose_name='скидка', validators=[MinValueValidator(0), MaxValueValidator(100)])
    count_in_stock = models.CharField(verbose_name='количество в наличии', null=True, max_length=100)
    rating = models.DecimalField(decimal_places=1, max_digits=2, verbose_name='рейтинг', blank=True, null=True,
                                 default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        """
        Возвращает название продукта
        """
        return self.title


class ProductCountDownloaded(models.Model):
    """
    Модель Количество загруженных продуктов
    """

    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = 'загруженный товар'
        verbose_name_plural = 'загруженные товары'

    count = models.IntegerField(verbose_name='Количество добавленных товаров в БД')
    downloaded_at = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления в БД')
