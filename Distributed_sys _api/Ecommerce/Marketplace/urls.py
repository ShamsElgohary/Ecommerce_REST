from django.urls import path
from Marketplace import views

urlpatterns = [
    path('product_list/', views.product_list),
    path('product_detail/<int:pk>/', views.product_detail),
    path('review_list/', views.review_list),
    path('review_detail/<int:pk>/', views.review_detail),
    path('checkout_list/', views.checkout_list),
    path('checkout_detail/<int:pk>/', views.checkout_detail),
    path('order_list/', views.order_list),
    path('order_detail/<int:pk>/', views.order_detail),
    path('purchase_list/', views.purchase_list),
    path('purchase_detail/<int:pk>/', views.purchase_detail),
]