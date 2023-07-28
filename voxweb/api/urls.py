from django.urls import path

from api.views import ProductsAPIView

app_name = 'api'

urlpatterns = [
    path('v1/products/', ProductsAPIView.as_view(), name='products'),
    # path('v1/products/<int:product_id>', 'MyLoginView', name='product_details'),
]