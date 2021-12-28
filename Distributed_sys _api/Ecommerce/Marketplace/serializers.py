from rest_framework import serializers

from .models import Customer,Seller,Checkout,Product,Order,Purchase,Review

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta :
#         model = Customer
#         fields='__all__'

# class SellerSerializer(serializers.ModelSerializer):
#     class Meta :
#         model = Seller
#         fields='__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta :
        model = Checkout
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
   # product=serializers.IntegerField(Product,on_delete=serializers.SET_NULL,blank=True,null=True)
    class Meta :
        model = Order
        fields='__all__'
        
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta :
        model = Purchase
        fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
    #seller = serializers.IntegerField(Seller)
    class Meta :
        model = Review
        fields='__all__'
        