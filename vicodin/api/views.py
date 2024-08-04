from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from vicodin.api.serializers import CartSerializer, CategorySerializer, ImagesSerializer, ProductSerializer, ReviewSerializer, UserSerializer
from vicodin.models import Category, Images, Review, User, Product, Cart

@api_view(['GET'])
def getRoute(request):
    routes = (
        'GET /api',

        'GET /api/products',
        'GET /api/products/:id',

        'GET /api/users',
        'GET /api/users/:id',

        'GET /api/categoryes',
        'GET /api/categoryes/:id',

        'GET /api/images',
        'GET /api/images/:id',

        'GET /api/reviews',
        'GET /api/reviews/:id',

        'GET /api/carts',
        'GET /api/carts/:id',
    )

    return Response(routes)

# Users GET POST
@api_view(['GET', 'POST'])
def getUsers(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)

# Product GET POST
@api_view(['GET', 'POST'])
def getProducts(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

# Category GET POST
@api_view(['GET', 'POST'])
def getCategoryes(request):
    if request.method == 'GET':
        categoryes = Category.objects.all()
        serializer = CategorySerializer(categoryes, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getCategory(request, pk):
    category = Category.objects.get(id=pk)
    serializer = CategorySerializer(category, many=False)

    return Response(serializer.data)

# Images GET POST
@api_view(['GET', 'POST'])
def getImages(request):
    if request.method == 'GET':
        images = Images.objects.all()
        serializer = ImagesSerializer(images, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getImage(request, pk):
    image = Images.objects.get(id=pk)
    serializer = ImagesSerializer(image, many=False)

    return Response(serializer.data)

# Review GET POST
@api_view(['GET', 'POST'])
def getReviews(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def getReview(request, pk):
    review = Review.objects.get(id=pk)
    serializer = ReviewSerializer(review, many=False)

    return Response(serializer.data)

@api_view(['GET'])
def getCarts(request):
    carts = Cart.objects.all() 
    serializer = CartSerializer(carts, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getCart(request, pk):
    cart = Cart.objects.get(id=pk)
    serializer = CartSerializer(cart)
    
    return Response(serializer.data)

