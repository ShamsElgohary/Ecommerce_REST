from types import SimpleNamespace
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout as auth_logout 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  UserCreationForm
import requests
from .models import *

def index(request):
    if "orders" not in request.session:
        request.session["orders"] = []
        request.session["currency"] = {"currencyName": "USD", "value":1 }
    if request.method == "POST":
        PARAMS={'search_key':'name','name':request.POST["search"].lower()}
        URL='http://127.0.0.1:8000/product_list/'
        products = requests.get(url = URL,params=PARAMS).json()
        for pro in products:
            pro["image"]=Image.objects.get(product=pro['id']).image
        return render(request, 'Marketplace/index.html', {
            "products": products,
            "message": "Search results"
        })
    else:
        products =  requests.get('http://127.0.0.1:8000/product_list/').json()
        for pro in products:
            pro["image"]=Image.objects.get(product=pro['id']).image
        return render(request, 'Marketplace/index.html', {
            "products":products,
            "message": "Shop all products"
        })



def login (request):
    if(not request.user.is_authenticated ):
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request,user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, 'Marketplace/login.html',{
                    "message":"wrong username or password"
                })
        return render(request, 'Marketplace/login.html')
    else :
        return HttpResponseRedirect(reverse("index"))


def register(request):
    if(not request.user.is_authenticated):
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user_data = User.objects.get(username=form.cleaned_data["username"])
                auth_login(request,user_data)
                if(request.POST["usertype"]=="option2"):
                    seller =Seller(user=user_data ,email=request.POST["email"])
                    seller.save()
                else:
                    customer =Customer(user=user_data ,email=request.POST["email"])
                    customer.save()
                return HttpResponseRedirect(reverse("index"))
        context = {'form': form}
        return render(request, 'Marketplace/register.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))



def product(request, id):
    PARAMS={'search_key':'id','id':id}
    URL='http://127.0.0.1:8000/product_list/'
    product = requests.get(url = URL,params=PARAMS).json()
    product["image"]=Image.objects.get(product=product['id']).image
    category = product['category']
    reviews = requests.get('http://127.0.0.1:8000/review_detail/'+str(id)).json()
    if type(reviews)==dict:
        if reviews["product"]==None:
            reviews=[]
    PARAMS={'search_key':'category','category':category}
    similar_products = requests.get(url = URL,params=PARAMS).json()
   
    if type(similar_products)==dict:
        if similar_products["name"]==None:
            similar_products=[]
    for pro in similar_products:
        pro["image"]=Image.objects.get(product=pro['id']).image
    
    for i in range(len(similar_products)):
        print(similar_products[i])
        if similar_products[i] == product:
            similar_products.pop(i)
            break

    return render(request, 'Marketplace/product.html', {
        'product': product,
        'reviews': reviews,
        "similar_products": similar_products
    })



def category(request, cat):
    PARAMS={'search_key':'category','category':cat}
    URL='http://127.0.0.1:8000/product_list/'
    products = requests.get(url = URL,params=PARAMS).json()
    for pro in products:
            pro["image"]=Image.objects.get(product=pro['id']).image
    return render(request, 'Marketplace/index.html', {
            "products": products, "message": f"{cat} category "
        })



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index"))



def dashboard(request):
    try:
        seller_id = request.user.seller.id
    except:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        product = {
            "seller":request.user.seller.id,
            "name":request.POST["name"],
            "price":request.POST["price"], 
            "category":request.POST["category"], 
            "stock":request.POST["stock"]
            }
        r=requests.post("http://127.0.0.1:8000/product_list/", json = product)
        Image( product=r.json()['id'],image=request.FILES["image"]).save()
        
    PARAMS={'search_key':'seller','seller':seller_id}
    URL='http://127.0.0.1:8000/product_list/'
    products = requests.get(url = URL,params=PARAMS).json()
    for pro in products:
        print(type(pro))
        pro["image"]=Image.objects.get(product=pro['id']).image
    return render(request, 'Marketplace/dashboard.html', {
        'products': products
})



def addtocart(request, id):
    if request.session["orders"]:
        flag =0
        for i in range(len(request.session["orders"])):
            if request.session["orders"][i]["product_id"] == id :
                flag =1
                quantity =request.session["orders"][i]["quantity"] +int(request.POST["quantity"])
                request.session["orders"].pop(i)
                request.session["orders"] += [{"product_id": id, "quantity": quantity}]
        if flag ==0 :
            request.session["orders"] += [{"product_id": id, "quantity": int(request.POST["quantity"])}]
    else: 
        request.session["orders"] += [{"product_id": id, "quantity": int(request.POST["quantity"])}]
    return HttpResponseRedirect(reverse("index"))



def cart(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        check_out = {
            "seller":request.user.seller.id,
            "payment_method":request.POST["paymentMethod"]
            }
        r=requests.post("http://127.0.0.1:8000/checkout_list/", json = check_out).json()
        for orders in request.session["orders"]:
            product_id = orders["product_id"]
            PARAMS={'search_key':'id','id':product_id}
            URL='http://127.0.0.1:8000/product_list/'
            product = requests.get(url = URL,params=PARAMS).json()
            quantity = orders["quantity"]
            buyer=Seller.objects.get(id=request.user.seller.id)
            seller=Seller.objects.get(id=product['seller'])
            buyer.money=buyer.money-int(product['price'])*quantity
            seller.money=seller.money+int(product['price'])*quantity
            buyer.save()
            seller.save()
            order = {
            "product":product['id'],
            'quantity':quantity,
            "checkout":r['id']
            }
            requests.post("http://127.0.0.1:8000/order_list/", json = order)
            #Order(product=Product.objects.get(id=product_id), quantity=quantity, checkout=cart).save()
            purchase = {
            "product":product['id'],
            "seller": product['seller'],
            'buyer':request.user.seller.id
            }
            requests.post("http://127.0.0.1:8000/purchase_list/", json = purchase)
            #Purchase(product=Product.objects.get(id=product_id),seller=Product.objects.get(id=product_id).seller,buyer=request.user).save()  ### save purchase
            return HttpResponseRedirect(reverse("index"))
    else:
        user_cart = []
        total = 0
        for order in request.session["orders"]:
            product_id = order['product_id']
            quantity = order['quantity']
            PARAMS={'search_key':'id','id':product_id}
            URL='http://127.0.0.1:8000/product_list/'
            products = requests.get(url = URL,params=PARAMS).json()
            if products != []:
                total+=products['price']*quantity
                products["image"]=Image.objects.get(product=products['id']).image
            user_cart.append([products, quantity])
        total= total*request.session["currency"]["value"]
        return render(request, 'Marketplace/cart.html', {
            'cart': user_cart ,
            "total" : total})



def addreview(request, id):
    if request.user.is_authenticated:
        review = request.POST["review"]
        requests.post("http://127.0.0.1:8000/review_list/", json = {"seller":str(request.user.seller.id),"review":review,"product":id})
        return HttpResponseRedirect(reverse("index"))
    else :
        return HttpResponseRedirect(reverse("login"))

def changequantity(request,id):
    for order in request.session["orders"]: 
        if order["product_id"] ==id:
            if not int(request.POST["quantity"]) ==0:
                request.session["orders"].remove(order) 
                request.session["orders"] += [{"product_id": id, "quantity": int(request.POST["quantity"])}]
            else:
                request.session["orders"].remove(order) 
                request.session["orders"] =request.session["orders"]+[]
 

    return HttpResponseRedirect(reverse("cart"))

    
            
def changecurrency(request ,id):
    # if not (id ==request.session["currency"]["value"]):
    #     if id ==15 :
    #         request.session["currency"] = {"currencyName": "EGP","value":15}
    #         for product in Product.objects.all():
    #             product.price = round(product.price*15)
    #             product.save()
    #     else:
    #         request.session["currency"] = {"currencyName": "USD","value":1}
    #         for product in Product.objects.all():
    #             product.price = round(product.price/15)
    #             product.save()
    return HttpResponseRedirect(reverse("index"))

def my_sales(request):
    PARAMS={'search_key':'id','id':request.user.seller.id}
    URL='http://127.0.0.1:8000/purchase_list/'
    purchases = requests.get(url = URL,params=PARAMS).json()
    print(purchases)
    for p in purchases:
        p['buyer']=Seller(id=p["product"])
        PARAMS={'search_key':'id','id':p['product']}
        URL='http://127.0.0.1:8000/product_list/'
        products = requests.get(url = URL,params=PARAMS).json()
        p['product']=products
    # seller_id = request.user.seller.id
    # purchases=Purchase.objects.all().filter(seller=seller_id)
    return render(request, 'Marketplace/my_sales.html', {"purchases": purchases})


def my_purchases(request):
    PARAMS={'search_key':'id','id':request.user.seller.id}
    URL='http://127.0.0.1:8000/purchase_list/'
    purchases = requests.get(url = URL,params=PARAMS).json()
    print(purchases)
    for p in purchases:
        p['seller']=Seller(id=p["seller"])
        PARAMS={'search_key':'id','id':p['product']}
        URL='http://127.0.0.1:8000/product_list/'
        products = requests.get(url = URL,params=PARAMS).json()
        p['product']=products
    #purchases = Purchase.objects.filter(buyer=request.user)
    return render(request, 'Marketplace/my_purchases.html', {"purchases": purchases})

def my_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == 'POST':
        seller= Seller.objects.get(user=request.user)
        seller.money= int(request.POST["money"])+seller.money
        seller.save()
        return render(request, 'Marketplace/my_profile.html', {"seller": seller}) 
    seller= Seller.objects.get(user=request.user)
    return render(request, 'Marketplace/my_profile.html', {"seller": seller})



def make_purchase(request):
    if request.method == 'POST' and request.user.is_anonymous():
        try:
            product = Product.objects.get(id=request.POST['product_id'])
        except Product.DoesNotExist:
            return redirect('login')

    return redirect('login')
