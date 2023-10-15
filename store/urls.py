from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>', views.products_detail),
    path('collection/<int:pk>', views.collection_detail,name='collection_detail'),
]