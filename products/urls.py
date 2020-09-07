from django.urls import path
from products import views
from products import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()


urlpatterns = [
    path('categories/all', views.list_categories),
    path('add/category', views.add_category),
    path('add/product/category', views.add_product_category),
    path('search/product', views.search_product),
    path('filter/product', views.filter_product),

]

urlpatterns += router.urls
