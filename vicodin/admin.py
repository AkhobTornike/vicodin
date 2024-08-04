from django.contrib import admin

from .models import Blog, Card, Cart, CartItem, Comment, Order, Category, User, Product, Review, Images, WishList, Address

# Register your models here.

class ImageInline(admin.TabularInline):
    model = Images
    extra = 1
    max_num = 10

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    max_num = 10

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    max_num = 5

class CardInline(admin.TabularInline):
    model = Card
    extra = 1
    max_num = 3

class UserAdmin(admin.ModelAdmin):
    inlines = [AddressInline, CardInline]

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(WishList)
admin.site.register(Order)
admin.site.register(Cart, CartAdmin)
admin.site.register(Blog)
admin.site.register(Comment)
