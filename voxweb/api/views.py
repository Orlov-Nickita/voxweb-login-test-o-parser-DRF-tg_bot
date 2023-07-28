import json
import os
from typing import List, Dict
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from api.serializers import ProductSerializer
from api.utils import get_items_from_page, download_image
from voxweb.settings import MEDIA_ROOT


class ProductsAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    
    def post(self, request, *args, **kwargs):
        """TODO"""
        products_count = request.data.get('products_count')
        if products_count is None:
            products_count = 10
        
        elif products_count < 1 or products_count > 50:
            if products_count < 1:
                data = {'error': 'Minimum of products count - 1'}
            else:
                data = {'error': 'Maximum of products count - 50'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # get_items_from_page(url=URL, html_file='source-page', product_count=products_count,
            #                     json_file_name='products')
            
            j_file = os.path.join(MEDIA_ROOT, 'products.json')
            
            with open(j_file, 'r', encoding='utf-8') as temp:
                products: List[Dict] = json.load(temp)
            
            for i_pr in products:
                image_url = i_pr.pop('image')
                i_pr.update(
                    {
                        'image': {
                            'file': download_image(image_url),
                            'alt': i_pr.get('title')
                        }
                    }
                )
                ps = ProductSerializer(data=i_pr)
                if ps.is_valid(raise_exception=True):
                    ps.save()
                else:
                    return Response(ps.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as Ex:
            err = json.dumps({'error': Ex})
            return Response(err, status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response('successful', status.HTTP_200_OK)

# curl -X POST http://127.0.0.1:5000/api/v1/products/ -H "Content-Type:application/json" -d "{\"products_count\": 15}"
