from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView

# from django.http import HttpResponse
from store.models import Product, Customer, Order
from tags.models import TagItem
from django.db.models import Value, F, Func, Count, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count
from django.contrib.contenttypes.models import ContentType
import requests



# from django.db.models import Q, F
# from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        response = requests.get('http://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name': 'mosh'})

# Create your views here.

# queryset = Product.objects.filter(title__icontains='coffe')
# queryset=Product.objects.filter(Q(inventory__lt=1,0)& Q(unit_price__lt=20))
# queryset=Product.objects.filter(description__icontains=True)
# queryset=Product.objects.filter(description__icontains='free')
# queryset=Product.objects.filter(last_update__day=13)
# exists = Product.objects.filter(pk=0).exists()
# queryset=Product.objects.filter(inventory=F('unit_price'))
# queryset = Product.objects.filter(inventory=F('collection_id'))
# queryset=Product.objects.order_by('title')
# queryset = Product.objects.order_by('unit_price','title').reverse()
# queryset = Product.objects.filter(collection_id=1).order_by('unit_price')
# queryset = Product.objects.earliest('unit_price')
# product = Product.objects.earliest('unit_price')
# queryset = Product.objects.order_by('unit_price')
# queryset = Product.objects.filter(
#     id__in=OrderItem.objects.values('product_id').distinct())
# queryset=Product.objects.defer('description')
# queryset=Product.objects.prefetch_related('promotions').select_related('collection')
# queryset=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('place_at')
# queryset=Order.objects.select_related('customer').order_by('place_at')[:5]
# result = Product.objects.filter(collection__id=1).aggregate(count=Count('id'), min_price=Min('unit_price'))
# result = Product.objectsf.aggregate(Count('id'))
# queryset=Customer.objects.annotate(is_new=Value(True))
# result = Customer.objects.annotate(
#     full_name=Func(F('first_name'),Value(''),F('last_name'),function='CONCAT')
# )
#
#     #     full_name=Concat('first_name',Value(''),'last_name')
#     # )result = Customer.objects.annotate(
# discounted_price = ExpressionWrapper(F('unit_price') * 0.8,output_field=DecimalField())
# queryset=Product.objects.annotate(
#     discounted_price=discounted_price
# )
# inventory= Product.objects.average_inventory()
# return render(request, 'hello.html', {'name': 'matin','products':inventory})
