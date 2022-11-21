from django.contrib import admin
from django.urls import path, include
from django.contrib.admin import AdminSite


urlpatterns = [
    path('center/', admin.site.urls),
    path('',include('produto.urls'))
]

admin.AdminSite.site_header = "Ecomerce"
admin.AdminSite.site_title = "Ecomerce"
admin.AdminSite.index_title = "Painel adminstrativo"