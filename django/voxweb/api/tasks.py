from celery import shared_task
import json
from typing import List, Dict
import os

from rest_framework import status
from rest_framework.response import Response

from api.models import ProductCountDownloaded
from api.serializers import ProductSerializer
from api.utils import get_items_from_page, download_image, send_message_in_bot
from voxweb.loader import URL
from voxweb.settings import MEDIA_ROOT


@shared_task
def parse_html(count: int):
    """
    Парсит сайт и добавляет данные в БД
    """
    try:
        get_items_from_page(url=URL, html_file='source-page', product_count=count,
                            json_file_name='products')

        j_file = os.path.join(MEDIA_ROOT, 'products.json')

        with open(j_file, 'r', encoding='utf-8') as temp:
            products: List[Dict] = json.load(temp)

        for i_pr in range(count):
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
        ProductCountDownloaded.objects.create(count=count)
        send_message_in_bot(products_count=count)
