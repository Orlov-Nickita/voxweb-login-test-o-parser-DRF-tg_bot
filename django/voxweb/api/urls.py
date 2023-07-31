from django.urls import path
from django.views.generic import TemplateView
from api.views import ProductsAPIView, EnvAddForBotAPIView, TgBotInfoAPIView

app_name = 'api'

urlpatterns = [
    path('v1/products/', ProductsAPIView.as_view(), name='products'),
    path('v1/products/<int:product_id>/', ProductsAPIView.as_view(), name='product_details'),
    path('v1/set_chat_id_for_bot/', EnvAddForBotAPIView.as_view(), name='set_key_in_env'),
    path('v1/get_downloaded_products/', TgBotInfoAPIView.as_view(), name='get_downloaded_products'),

    # docs
    path('docs/', TemplateView.as_view(template_name='api/swagger-ui.html',
                                       extra_context={'schema_url': 'openapi-schema'})),
]
