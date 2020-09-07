from .models import *
from rest_framework_mongoengine.serializers import (
    DocumentSerializer,
    EmbeddedDocumentSerializer,
)


class CategorySerializer(DocumentSerializer):
    class Meta:
        model = Category

class ProductSerializer(DocumentSerializer):
    class Meta:
        model = Product
        
class ProductCategorySerializer(DocumentSerializer):
    class Meta:
        model = ProductCategory

