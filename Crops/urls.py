from django.urls import path
from .views import home, periodic_update, add_stock, alerts
urlpatterns = [
    path('', home, name='home'),
    path('periodic_update/', periodic_update),
    path('add_stock/', add_stock),
    path('alert/', alerts),
]