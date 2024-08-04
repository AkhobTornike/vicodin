from django.db import models

from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    avatar = models.ImageField(null=True, upload_to='users_images/', default='avatar.svg')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    apartment = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street} {self.apartment}, {self.zip_code}'

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=200)
    expiration_date = models.CharField(
        max_length=7,
        validators=[RegexValidator(regex=r'^\d{4}-\d{2}$', message='Date must be in YYYY-MM format')]
    )    
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return  self.card_holder + ' | ' + '*' * (len(self.card_number) - 4) + self.card_number[-4:] + ' ' 

    def show_card_number(self):
        return '*' * (len(self.card_number) - 4) + self.card_number[-4:]

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Here will be Products
    """
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.ImageField(upload_to='product_images/', null=True, default='prod_def.png')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return str(self.name)
    
    @property
    def discounted_price(self):
        if self.discount:
            return self.price - ((self.price * self.discount) / 100)
        return self.price
    
class Images(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', default='prod_def.png')

    def __str__(self) -> str:
        return f"Image for {self.product.name}"
    
class Review(models.Model):
    STARS_CHOICES = [
        (0, '0 Stars'),
        (1, '1 Star'),
        (2, '2 Stars'), 
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=STARS_CHOICES)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.body[0:50]
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name   

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name}'  
    
    @property
    def total_price(self):
        return sum(item.item_price for item in self.cartItem.all())
    
    def cartItems(self):
        return self.cartItem.all()
    
    def clear_cart(self):
        self.cartItem.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartItem', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, default=1)

    def __str__(self):
        return f'{self.product.name} {self.quantity}'    
    
    @property
    def item_price(self):
        return self.product.discounted_price * self.quantity
    
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def update_quantity(self, new_quantity):
        if new_quantity > 0:
            self.quantity = new_quantity
            self.save()
        else:
            raise ValueError('Quantity must be greater than zero.')
        
class Order(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    ON_HOLD = 'On Hold'
    DELAYED = 'Delayed'

    ORDER_CATEGORY = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (ON_HOLD, 'On Hold'), 
        (DELAYED, 'Delayed')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_CATEGORY, default=PENDING)

    def __str__(self):
        return f'{self.user.username} | {self.date}' 

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    topic_title1 = models.CharField(max_length=200, null=True, blank=True)
    image1 = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    body1 = models.TextField(null=True, blank=True)
    
    topic_title2 = models.CharField(max_length=200, null=True, blank=True)
    image2 = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    body2 = models.TextField(null=True, blank=True)
    
    topic_title3 = models.CharField(max_length=200, null=True, blank=True)
    image3 = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    body3 = models.TextField(null=True, blank=True)
    
    author_description = models.CharField(max_length=200, null=True, blank=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
    
    def get_class_name(self):
        return self.__class__.__name__

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

    def get_class_name(self):
        return self.__class__.__name__
    
    @property
    def is_reply(self):
        return self.parent is not None
    