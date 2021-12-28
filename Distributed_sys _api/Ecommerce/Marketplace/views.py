from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        key =request.GET.get('search_key')
        if key== None:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            try:
                if key =="seller":
                    snippet = Product.objects.filter(seller=request.GET.get(key))
                    serializer = ProductSerializer(snippet, many=True)
                    return JsonResponse(serializer.data, safe=False)
                elif key=='id':
                    snippet = Product.objects.get(id=request.GET.get(key))
                elif key=='name':
                    snippet = Product.objects.get(name=request.GET.get(key))
                else:
                    snippet = Product.objects.filter(category=request.GET.get(key))
                    serializer = ProductSerializer(snippet, many=True)
                    return JsonResponse(serializer.data, safe=False)
            except Product.DoesNotExist:
                return HttpResponse(status=404)
        if request.method == 'GET':
            serializer = ProductSerializer(snippet)
            return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt

def product_detail(request, pk):
    try:
        snippet = Product.objects.get(seller=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ProductSerializer(snippet)
        return JsonResponse(serializer.data)
@csrf_exempt

def review_list(request):
    if request.method == 'GET':
        Product = Review.objects.all()
        serializer = ReviewSerializer(Product, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt

def review_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        print(pk)
        snippet = Review.objects.filter(product=pk)
        print(snippet)
    except Checkout.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ReviewSerializer(snippet, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReviewSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
@csrf_exempt

def checkout_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Checkout.objects.all()
        serializer = CheckoutSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CheckoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt

def checkout_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Checkout.objects.get(seller=pk)
    except Checkout.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CheckoutSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CheckoutSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
@csrf_exempt

def order_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Order.objects.all()
        serializer = OrderSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt

def order_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Order.objects.get(seller=pk)
    except Order.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = OrderSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OrderSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
@csrf_exempt

def purchase_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Purchase.objects.all()
        serializer = PurchaseSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PurchaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def purchase_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Purchase.objects.get(seller=pk)
    except Purchase.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PurchaseSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PurchaseSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)