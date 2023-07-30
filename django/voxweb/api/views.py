import json
import os
from typing import List, Dict

from dotenv import set_key
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Product
from api.serializers import ProductSerializer
from api.utils import get_items_from_page, download_image, send_message_in_bot
from voxweb.loader import URL
from voxweb.settings import MEDIA_ROOT, BASE_DIR


class ProductsAPIViewPagination(PageNumberPagination):
    """
    Пагинация для списка продуктов
    """
    page_size_query_param = 'limit'
    page_size = 10


class ProductsAPIView(ListAPIView, CreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductsAPIViewPagination
    queryset = Product.objects.select_related('image').all()
    
    def get(self, request, *args, **kwargs):
        """
        Получение списка всех продуктов
        """
        p_id = kwargs.get('product_id')
        if p_id:
            self.queryset = Product.objects.select_related('image').filter(id=p_id).get()
            self.pagination_class = None
            return Response(self.serializer_class(self.queryset).data)
        
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """TODO"""
        products_count = request.data.get('products_count')
        if products_count is None:
            products_count = 10
        
        elif products_count < 1 or products_count > 50:
            if products_count < 1:
                data = {'error': 'Минимальное значение - 1'}
            else:
                data = {'error': 'Максимальное значение - 50'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            get_items_from_page(url=URL, html_file='source-page', product_count=products_count,
                                json_file_name='products')
            
            j_file = os.path.join(MEDIA_ROOT, 'products.json')
            
            with open(j_file, 'r', encoding='utf-8') as temp:
                products: List[Dict] = json.load(temp)
            
            for i_pr in range(products_count):
                image_url = products[i_pr].pop('image')
                products[i_pr].update(
                    {
                        'image': {
                            'file': download_image(image_url),
                            'alt': products[i_pr].get('title')
                        }
                    }
                )
                ps = ProductSerializer(data=products[i_pr])
                if ps.is_valid(raise_exception=True):
                    ps.save()
                else:
                    return Response(ps.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as Ex:
            err = json.dumps({'error': Ex})
            return Response(err, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            send_message_in_bot(products_count=products_count)
            return Response('Успешный парсинг. Уведомление отправлено в телеграмм бот', status.HTTP_200_OK)


# curl -X POST http://127.0.0.1:5000/api/v1/products/ -H "Content-Type:application/json" -d "{\"products_count\": 15}"

class EnvAddForBot(APIView):
    """TODO"""
    def post(self, request):
        try:
            chat_id = request.data.get('id')
            if not chat_id:
                return Response('Отсутствует id', status=status.HTTP_404_NOT_FOUND)
            
            env = os.path.join(BASE_DIR, 'voxweb', '.env')
            set_key(dotenv_path=env, key_to_set='CHAT_ID', value_to_set=str(chat_id))
            return Response('Ваш ID успешно добавлен в .env файл. Этот ID будет использован для рассылки оповещений',
                            status=status.HTTP_202_ACCEPTED)
        except Exception as Ex:
            return Response(f'{Ex}', status=status.HTTP_400_BAD_REQUEST)
