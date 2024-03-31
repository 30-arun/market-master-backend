from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import  NewProduct, PreviewProduct
from .serializers import  NewProductSerializer, PreviewProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class ProductsList(ListAPIView):
    serializer_class = PreviewProductSerializer
    queryset = PreviewProduct.objects.all()

class PreviewProductDetails(RetrieveAPIView):
    queryset = PreviewProduct.objects.all()
    serializer_class = PreviewProductSerializer
    lookup_field = 'slug'

class ProductDetails(APIView):
    
    def get(self, request, slug, template_id, format=None):
        # Retrieve the product based on the slug
        product = get_object_or_404(NewProduct, slug=slug, user_template_id=template_id)
        # Serialize the product data
        serializer = NewProductSerializer(product)
        # Return the serialized data with an HTTP 200 status
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewProductView(APIView):	
    def get(self, request, format=None):
        user_template_id = request.query_params.get('template_id')
        new_product = NewProduct.objects.filter(user_template_id=user_template_id)
        serializer = NewProductSerializer(new_product, many=True)
        return Response(serializer.data)
	
    def post(self, request, format=None):
        serializer = NewProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user_template_id = request.query_params.get('template_id')
        new_product_id = request.query_params.get('product_id')
        new_product = NewProduct.objects.filter(user_template_id=user_template_id, _id=new_product_id)
        new_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
