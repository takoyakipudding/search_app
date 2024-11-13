from django.urls import path
from . import views

urlpatterns = [
    path('export/', views.export_search_results, name='export_search_results'),
    path('', views.search_view),
    path('search/', views.search_view, name='search_view'),
    path('signup/', views.signup_view, name='signup'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_list, name='cart_list'),  
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
