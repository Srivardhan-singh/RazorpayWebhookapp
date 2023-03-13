from django.urls import path
from .views import razorpay_webhook

urlpatterns = [
    path('webhook', razorpay_webhook, name='razorpay_webhook'),
    path('webhook/', razorpay_webhook, name='razorpay_webhook'),
]