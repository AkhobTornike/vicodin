from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoute),
    # Products URL
    path('products/', views.getProducts, name='get-products'),
    path('products/<str:pk>', views.getProduct, name='get-solo-product'),

    # Users URL
    path('users', views.getUsers, name='get-users'),
    path('users/<str:pk>', views.getUser, name='get-solo-user'),

    # Category URL
    path('categoryes', views.getCategoryes, name='get-categoryes'),
    path('categoryes/<str:pk>', views.getCategory, name='get-solo-category'),

    # Images URL
    path('images', views.getImages, name='get-images'),
    path('images/<str:pk>', views.getImage, name='get-solo-image'),

    # Reviews URL
    path('reviews', views.getReviews, name='get-reviews'),
    path('reviews/<str:pk>', views.getReview, name='get-solo-review'),

    path('carts', views.getCarts, name='get-carts'),
    path('carts/<str:pk>', views.getCart, name='get-solo-cart'),
]