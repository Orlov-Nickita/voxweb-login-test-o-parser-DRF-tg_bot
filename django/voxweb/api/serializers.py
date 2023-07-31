from urllib.parse import unquote

from rest_framework import serializers

from api.models import ProductImage, Product, ProductCountDownloaded


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ProductImage
    """
    file = serializers.ImageField(use_url=True)

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = ProductImage
        fields = ['file', 'alt']


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product
    """
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True, format="%H:%M %d-%m-%Y")
    image = ProductImageSerializer()

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Product
        fields = ['id', 'new_price', 'old_price', 'count_in_stock', 'date', 'title', 'image', 'rating', 'href', 'sale']

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        image_serializer = ProductImageSerializer(data=image_data)
        if image_serializer.is_valid(raise_exception=True):
            image = image_serializer.save()

            return Product.objects.create(**validated_data, image_id=image.id)

        return image_serializer.errors


class ProductCountDownloadedSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product
    """

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = ProductCountDownloaded
        fields = ['count']


class ProductShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Product
        fields = ['title', 'href']
