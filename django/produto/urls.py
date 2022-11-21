from django.urls import path
from .views import produto

urlpatterns = [
    path('produtos/', produto, name="produto")
]