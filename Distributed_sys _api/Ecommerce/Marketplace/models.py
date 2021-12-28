from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE ,null=True )
    email = models.CharField(max_length=200 ,null=True)
    address = models.CharField(max_length=200 ,null=True)
    credit_card_number =models.IntegerField(null=True)
    money = models.IntegerField( default=30 )
    def __str__ (self):
        return self.user.username
    def password_validate(self):
        pw = self.user.password
        return len(pw) >= 8


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE ,null=True )
    email = models.CharField(max_length=200 ,null=True)
    address = models.CharField(max_length=200 ,null=True )
    credit_card_number =models.IntegerField(null=True)
    money = models.IntegerField( default=30 )
    def __str__ (self):
        return self.user.username

    def password_validate(self):
        pw = self.user.password
        return len(pw) >= 8

class Checkout(models.Model):
    Payment_Method=(
        ('Cash', 'Cash'),
        ('Visa', 'Visa'),
    )

    seller = models.IntegerField(null=True)
    payment_method=models.CharField(max_length=64,null=True,choices=Payment_Method)
    def Checkout_Valid(self):
        if(self.payment_method != "Cash" and self.payment_method != "Visa" ):
            return False
        else:
            return True


class Product(models.Model):
    CATEGORY = (
       ('electronics','electronics'),
       ('cloth','cloth'),
       ('sport','sport'))
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True,choices=CATEGORY )
    price = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    #image = models.ImageField(null=True, blank=True ,default='empty.jpg')
    seller = models.IntegerField(null=True)
    def _str_(self):
        return self.name
    def Product_Valid(self):
        return self.price > 0 and self.name != None

class Order (models.Model):
    product=models.IntegerField(null=True)
    quantity=models.IntegerField(default=0,blank=True,null=True)
    checkout=models.IntegerField(null=True)
    def _str_(self):
        return self.checkout.id
    def Order_Valid(self):
        return self.quantity>0 and self.product != None


class Review(models.Model):
    seller = models.IntegerField(null=True)
    review = models.IntegerField(null=True)
    product = models.IntegerField(null=True)

    def str(self):
        return f"{self.seller.username} review is {self.review} on product {self.product.name}"

class Purchase(models.Model):
    product = models.IntegerField(null=True)
    seller = models.IntegerField(null=True)
    buyer = models.IntegerField(null=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.name