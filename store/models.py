from uuid import uuid4

from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Manager
from django.conf import settings
from django.contrib import admin


# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # products


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, primary_key=True)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, related_name='products', null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    # def number_of_customers(self):
    #     self.aggregate(number_of_customers=models.)


class ProductManager(models.Manager):
    def average_inventory(self):
        # {'average_inventory' : 50 }
        return self.aggregate(average_inventory=models.Max('inventory'))['average_inventory']


# aggregate(count,avg,sum,min ,max)


class Product(models.Model):
    objects = ProductManager()
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, null=True, blank=True, related_name='product')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = (
        (MEMBERSHIP_BRONZE, 'Boronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    )
    phone = models.CharField(max_length=15)
    birth_date = models.DateTimeField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class OrderManager(models.Manager):
    def count(self):
        return self.aggregate(count=models.Count('id'))['count']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'p'
    PAYMENT_STATUS_COMPLETE = 'c'
    PAYMENT_STATUS_FAILED = 'f'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'pending'),
        (PAYMENT_STATUS_COMPLETE, 'complete'),
        (PAYMENT_STATUS_FAILED, 'failed')
    ]
    objects = OrderManager()
    place_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        permissions = [
            ('cancel_order', ('Can cancel order'))
        ]


class OrderItem(models.Model):
    objects = OrderManager()
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    create_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]
