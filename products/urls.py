from django.urls import path

from .views import (
    ProductsList,
    PreviewProductDetails,
    ProductDetails,
    NewProductView
)

app_name = 'api'


urlpatterns = [
    path('', ProductsList.as_view(), name='products'),
    path('new/', NewProductView.as_view(), name='newklproduct'),
    path('<str:slug>/<int:template_id>/', ProductDetails.as_view(), name='product-details'),
    path('preview/<str:slug>/', PreviewProductDetails.as_view(), name='preview-product-details'),
]
