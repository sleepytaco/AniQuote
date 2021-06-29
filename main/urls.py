from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('get-random-quote', get_random_quote),
    path('get-specific-quote', get_specific_quote),
    path('like-quote-<int:id>', like_quote),
    path('unlike-quote-<int:id>', unlike_quote)
]
