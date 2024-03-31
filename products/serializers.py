from rest_framework import serializers

from .models import Product, Category, NewProduct, PreviewProduct


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            '_id',
            'user',
            'name',
            'slug',
            'image',
            'brand',
            'category',
            'category_name',
            'description',
            'rating',
            'numReviews',
            'price',
            'countinStock',
            'created'
        ]
        read_only_fields = ['category']

    def get_category_name(self, obj):
        return f'{obj.category}'
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class NewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewProduct
        fields = '__all__'
        
class PreviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviewProduct
        fields = '__all__'