from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('shoping/', views.shopingPage, name='shoping'),
    path('featured-products/', views.featuredProducts, name='featured-products'),
    path('latest-products/', views.latestProducts, name='latest-products'),
    path('trending-products/', views.trendingProducts, name='trending-products'),
    
    path('blog-page/', views.blogPage, name='blog-page'),
    re_path(r'^blog-page/create_update_new/(?P<type>create|update)/(?P<id>\d+)?$', views.CreateUpdateBlog, name='create-update-blog'),
    path('blog-page/delete_blog/<int:pk>', views.DeleteBlog, name='delete-blog'),
    path('blog-page/blog-detail/<str:pk>', views.detailBlogPage, name='blog-detail'),
    path('blog-page/blog-detail/<int:pk>/comment-reply/<str:type>/<int:id>/', views.commentBlog, name='blog-comment-reply'),
    path('blog-page/edit_comment_replt/<int:pk>', views.EditCommentReply, name='edit-comment-reply'),
    path('blog-page/delete/<int:pk>', views.DeleteComment, name='delete-comment'),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name='logout'),

    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('cart', views.cartPage, name='cart'),
    path('checkout', views.CheckoutPage, name='checkout'),
    path('add-new-card', views.CreateCard, name='add-card'),
    path('add-new-address', views.CreateAddress, name='add-address'),

    path('product/<str:pk>', views.productDetail, name='product-detail'),
    path('create-product/', views.createProduct, name='create-product'),
    path('update-product/<str:pk>', views.updateProduct, name='update-product'),
    re_path(r'update-product/(?P<pk>[^/]+)/image/(?P<type>add|edit-delete)(?:/(?P<id>\d+))?/$', views.ImagesPage, name='product-images'),
    path('delete-product/<str:pk>', views.deleteProduct, name='delete-product'),

    path('edit-review/<str:pk>', views.editReview, name='edit-review'),
    path('delete-review/<str:pk>', views.deleteReview, name='delete-review'),

]