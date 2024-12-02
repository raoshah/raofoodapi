from django.urls import path
from .views import createProduct, getProducts, createProductReview

urlpatterns = [
    path('create-product/', createProduct, name='create-product'),
    path('get-products/', getProducts, name='get-products'),
    path('product/<str:pk>/reviews/', createProductReview, name="create-review"),
]