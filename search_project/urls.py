from django.contrib import admin 
from django.urls import path, include 

urlpatterns = [ 
    path("admin/", admin.site.urls), 
    path('', include('search_app.urls')),  # 正しく search_app を含めます
]
