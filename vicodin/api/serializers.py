from rest_framework.serializers import ModelSerializer, ReadOnlyField

from vicodin.models import Cart, CartItem, Category, Images, Review, User, Product

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'first_name', 'last_name', 'age', 'avatar']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ImagesSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CartItemSerializer(ModelSerializer):
    item_price = ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'item_price']

class CartSerializer(ModelSerializer):
    total_price = ReadOnlyField()
    cart_items = CartItemSerializer(many=True, read_only=True, source='cartItem')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'cart_items']