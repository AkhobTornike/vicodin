from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, modelformset_factory, PasswordInput, TextInput, Form, CharField

from .models import Blog, Card, Comment, Images, User, Product, Address, Order

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'username', 'age', 'phone', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'first_name', 'last_name', 'email', 'age', 'phone', 'bio']
        
class ChangePasswordForm(Form):
    old_password = CharField(widget=PasswordInput())
    new_password = CharField(widget=PasswordInput())
    confirm_password = CharField(widget=PasswordInput())

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount', 'description', 'main_image']

class ImagesForm(ModelForm):
    class Meta:
        model = Images
        fields = ['image']

ImageFormSet = modelformset_factory(Images, form=ImagesForm, extra=10)

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'body', 'topic_title1', 'image1', 'body1', 'topic_title2', 'image2', 'body2', 'topic_title3', 'image3', 'body3', 'author_description']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'card_holder', 'expiration_date', 'cvv']
        widgets = {
            'card_number': TextInput(attrs={'placeholder': '1234 5678 9012 3456'}),
            'card_holder': TextInput(attrs={'placeholder': 'Card Holder Name'}),
            'expiration_date': TextInput(attrs={'placeholder': 'YYYY-MM'}),
            'cvv': PasswordInput(attrs={'placeholder': 'CVV'}),
        }

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'apartment', 'zip_code']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['card', 'address']