from rest_framework import serializers
from decimal import Decimal

from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'inventory', 'description', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


# id = serializers.IntegerField()
# title = serializers.CharField(max_length=255)
# price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')

# collection = serializers.HyperlinkedRelatedField(
#     queryset=Collection.objects.all(),
#     view_name='collection_detail'
# )

# collection=CollectionSerializer()
# collection=serializers.StringRelatedField()
# collection=serializers.PrimaryKeyRelatedField(
#     queryset=Collection.objects.all()
# )


def calculate_tax(self, product: Product):
    return product.unit_price * Decimal(1.1)

# def validate(self,data):
#     if data['password'] != data['confirm_password']:
#         return serializers.ValidationError("password do not match")
#     return data
# def validate(self, data):
#     if data['unit_price'] >= 70:
#         raise serializers.ValidationError("price groneh")
#     return data
# def create(self, validated_data):
#     product = Product(**validated_data)  # def create for post method http
#     product.other = 1
#     product.save()
#     return product
#
# def update(self, instance, validated_data):
#     instance.unit_price = validated_data.get('unit_price')  # def update for  put/pacth method http
#     instance.save()
#     return instance
