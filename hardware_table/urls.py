from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('need_buy', views.hw_need_buy, name='need-buy'),
]
