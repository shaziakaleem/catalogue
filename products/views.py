from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from helpers import JsonValidationHelper
from rest_framework.response import Response
from .serializers import CategorySerializer,ProductCategorySerializer
from .models import *
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
)

from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_category(request):
    expected_json_keys = {"category_name": None}
    try:
        data = JsonValidationHelper.validate(request.data, expected_json_keys)
    except JsonValidationHelper.MalformedDataException as exception:
        return Response(str(exception), status=HTTP_400_BAD_REQUEST)
    try:
        category = Category.objects.get(category_name=data["category_name"])
        return Response("Category already present",status=HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        category_data = {
            "category_name": data["category_name"],
            "created_by": request.user.uuid,
        }
    serializer = CategorySerializer(data=category_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product_category(request):
    expected_json_keys = {"category_name": None,"product":None}
    try:
        data = JsonValidationHelper.validate(request.data, expected_json_keys)
    except JsonValidationHelper.MalformedDataException as exception:
        return response(str(exception), status=HTTP_400_BAD_REQUEST)
    try:
        category = Category.objects.get(category_name=data["category_name"])
        product = Product.objects.get(product_name=data["product_name"])
    except Category.DoesNotExist:
        return Response("Category not found",status=HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response("Product not found",status=HTTP_400_BAD_REQUEST)
    data = {
        "category": category.uuid,
        "product":product.uuid,
        "created_by": request.user.id,
    }
    serializer = ProductCategorySerializer(data=category_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def search_product(request):
    query = request.GET.get("query", None)
    if not query:
        return Response("Please provide a search parameter.", status.HTTP_400_BAD_REQUEST)
    
    products_names = Product.objects.filter(product_name__icontains=query)
    products_tags = Product.objects.filter(tags__icontains=query)
    products = product_names|products_tags #merge querysets
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def filter_product(request):
    price_filter = request.GET.get("price_filter", None)
    search_results = request.GET.get("search_results",None) #hold searched queryset in form of list of product ids
    if not query:
        return Response("Please provide a filter.", status.HTTP_400_BAD_REQUEST)
    products = Product.objects.filter(uuid__in=search_results)
    products_filetered = products.filter(price__gt=price_filter)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status.HTTP_200_OK)



class ProductViewSet(DocumentViewSet):
    document = Product
    serializer_class = ProductSerializer
    ordering = ('id',)
    lookup_field = 'id'

    filter_backends = [
        DefaultOrderingFilterBackend,
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'product',
        'price',
    )

    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'product': 'product',
    }

    suggester_fields = {
        'product_suggest': {
            'field': 'product.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }
