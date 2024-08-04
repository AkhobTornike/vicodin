from .models import Cart, CartItem, Category
from django.db.models import Count

def site_context(request):
    popular_categoryes = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')[:5]

    return {
        'popular_categoryes': popular_categoryes
    }

def cart_context(request):
    if request.method == 'POST':
        if 'delete-cartItem' in request.POST:
            cartItem_id = request.POST.get('delete-cartItem')
            try:
                cartItem = CartItem.objects.get(id=cartItem_id)
                cartItem.delete()
            except CartItem.DoesNotExist:
                pass
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartItems = CartItem.objects.filter(cart=cart)
            total_price = cart.total_price
        except Cart.DoesNotExist:
            total_price = 0
            cart = None
            cartItems = []
    else:
        total_price = 0
        cart = None
        cartItems = []      
            
    return {
        'cart': cart,
        'cartItems': cartItems,
        'total_price': total_price,
        'total_items': len(cartItems)
    }

def url_context(request):
    path_segments = extract_between_slashes(request.path)
    
    return {
        'path_segments': path_segments
    }

def extract_between_slashes(path):
    segments = [segment for segment in path.split('/') if segment]
    cumulative_urls = []
    for i in range(len(segments)):
        cumulative_urls.append('/' + '/'.join(segments[:i+1]))
    return list(zip(segments, cumulative_urls))

