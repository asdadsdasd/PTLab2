from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:product_id>/', views.PurchaseCreate.as_view(), name='buy'),
    path('purchase/create/<int:product_id>/', views.PurchaseCreate.as_view(), name='purchase_create'),
]

