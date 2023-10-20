from django.db.models import Count
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
# from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from .pagination import DefaultPagination
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, \
    AddCartItemSerializer, UpdateCartItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'errors': 'product contact be delete because it is associate with an order item. '},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


# def delete(self, request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if product.orderitems.count() > 0:
#         return Response({'errors': 'product contact be delete because it is associate with an order item. '},
#                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     product.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(product=kwargs['pk']).count() > 0:
            return Response({'errors': 'collection contact be delete because it is associate with an order item. '},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


# class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
#     queryset = Cart.objects.prefetch_related('items__product').all()
#     serializer_class = CartSerializer
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart__id=self.kwargs['cart_pk']).select_related('product')

# def delete(self, request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
#     if collection.product.count() > 0:
#         return Response({'errors': 'collection contact be delete because it is associate with an order item. '},
#                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     collection.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer

# def get_serializer_context(self):
#     return {'request': self.request}


# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('product')).all()
#         serializer = CollectionSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product'))
#     serializer_class = CollectionSerializer


# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
# class ProductList(ListCreateAPIView):


#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer


# def get_queryset(self):
#     return  Product.objects.select_related('collection').all()
# def get_serializer(self):
#     return ProductSerializer

# def get(self, request):
#     queryset = Product.objects.select_related('collection').all()
#     serializer = ProductSerializer(queryset, many=True, context={'request': request})
#     return Response(serializer.data)
#
# def post(self, request):
#     serializer = ProductSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
