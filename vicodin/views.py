from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404

from datetime import timedelta

from .models import Address, Card, Cart, CartItem, Comment, Order, User, Product, Review, Images, Category, WishList, Blog

from vicodin.forms import CardForm, ImageFormSet, ImagesForm, MyUserCreationForm, UserForm, ProductForm, CommentForm, BlogForm, AddressForm, OrderForm


logger = logging.getLogger(__name__)

# Create your function here.

@login_required(login_url='login')
def add_product_to_cart(request, product_id, quantity=1):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product.host == request.user:
        messages.error(request, "You can't add your own product to cart.")
        return redirect('product-detail', pk=product.id)
    else:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        messages.success(request, f'{product.name} added to cart successfully.')

        if not created:
            cart_item.update_quantity(cart_item.quantity + quantity)


@login_required(login_url='login')
def add_product_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if product.host == user:
        messages.error(request, "You can't add your own product to wishlist.")
        return redirect('product-detail', pk=product.id)
    else:
        WishList.objects.create(user=user, product=product)
        messages.success(request, f'{product.name} added to wishlist successfully.')


# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    products = Product.objects.all()
    categories = Category.objects.all()
    reviews = Review.objects.all()
    blogs = Blog.objects.all()

    one_month_ago = timezone.now() - timedelta(days=30)

    products = products.annotate(avg_rating=Avg('review__stars'))

    latestProducts = products.filter(created__gte=one_month_ago)[:8]
    trendingProducts = products.filter(avg_rating__gt=2)[:8]

    most_rating_product = products.order_by('-avg_rating').first()
    most_rating_product_reviews = reviews.filter(product=most_rating_product)

    most_latest_product = latestProducts[0]
    most_latest_product_reviews = reviews.filter(product=most_latest_product)

    most_discounted_product = products.order_by('-discount').first()
    most_discounted_product_reviews = reviews.filter(product=most_discounted_product)

    lates_blog = blogs.first()

    products =  products.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(category__name__icontains=q) |
        Q(host__username__icontains=q)
    )[:8]

    if request.method == 'POST':
        if 'add-to-cart' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-cart')
            add_product_to_cart(request, product_id)
        if 'add-to-wishlist' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-wishlist')
            add_product_to_wishlist(request, product_id)

    for product in products:
        avg_rating = product.avg_rating or 0
        product.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]

    for product in trendingProducts:
        avg_rating = product.avg_rating or 0
        product.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]

    for product in latestProducts:
        avg_rating = product.avg_rating or 0
        product.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]

    context = {
        'q': q,

        'products' : products,
        'categories' : categories,
        'blogs' : blogs,

        'latestProducts' : latestProducts,
        'trendingProducts' : trendingProducts,

        'most_rating_product' : most_rating_product,
        'most_rating_product_reviews' : most_rating_product_reviews,

        'most_latest_product' : most_latest_product,
        'most_latest_product_reviews' : most_latest_product_reviews,

        'most_discounted_product' : most_discounted_product,
        'most_discounted_product_reviews' : most_discounted_product_reviews,

        'latest_blog': lates_blog,
    }
    return render(request, 'vicodin/home.html', context) 

def featuredProducts(request):
    one_month_ago = timezone.now() - timedelta(days=30)
    products = Product.objects.all()

    products = products.annotate(avg_rating=Avg('review__stars'))

    for product in products:
        avg_rating = product.avg_rating or 0
        product.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]

    latestProducts = products.filter(created__gte=one_month_ago)

    if request.method == 'POST':
        if 'add-to-cart' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-cart')
            add_product_to_cart(request, product_id)
        if 'add-to-wishlist' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-wishlist')
            add_product_to_wishlist(request, product_id)

    context = {
        'products' : products,
        'latestProducts' : latestProducts,
    }
    return render(request, 'vicodin/featured_products.html', context)

def latestProducts(request):
    one_month_ago = timezone.now() - timedelta(days=30)
    products = Product.objects.filter(created__gte=one_month_ago)

    products = products.annotate(avg_rating=Avg('review__stars'))

    for product in products:
        avg_rating = product.avg_rating or 0
        product.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]

    if request.method == 'POST':
        if 'add-to-cart' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-cart')
            add_product_to_cart(request, product_id)
        if 'add-to-wishlist' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-wishlist')
            add_product_to_wishlist(request, product_id)

    context = {
        'products' : products,
    }
    return render(request, 'vicodin/latest_products.html', context)

def trendingProducts(request):
    products = Product.objects.annotate(avg_rating=Avg('review__stars'))
    products = products.filter(avg_rating__gte=3)

    for product in products:
        avg_rating = product.avg_rating or 0
        product.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]

    if request.method == 'POST':
        if 'add-to-cart' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-cart')
            add_product_to_cart(request, product_id)
        if 'add-to-wishlist' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-wishlist')
            add_product_to_wishlist(request, product_id)

    one_month_ago = timezone.now() - timedelta(days=30)
    latestProducts = Product.objects.filter(created__gte=one_month_ago)
    context = {
        'products' : products,
        'latestProducts' : latestProducts,
    }
    return render(request, 'vicodin/trending_products.html', context)

def productDetail(request, pk):
    one_month_ago = timezone.now() - timedelta(days=30)

    product = get_object_or_404(Product, id=pk)
    products = Product.objects.annotate(avg_rating=Avg('review__stars'))
    latestProducts = products.filter(created__gte=one_month_ago)
    
    top_rated_products = products.order_by('-avg_rating')[:3]
    relatedProducts = products.filter(category=product.category).exclude(id=product.id)
    
    avg_rating = product.review_set.aggregate(Avg('stars'))['stars__avg'] or 0
    product.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]
    
    for p in top_rated_products:
        avg_rating = p.avg_rating or 0
        p.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]
    
    for p in relatedProducts:
        avg_rating = p.avg_rating or 0
        p.rating_binary_list = [1 if i < int(avg_rating) else 0 for i in range(5)]
    
    images = Images.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    review_count = reviews.count()
    
    if request.method == 'POST' and request.user.is_authenticated and request.user != product.host:
        stars = request.POST.get('rating')
        body = request.POST.get('body')
        if stars and body:
            Review.objects.create(
                user=request.user,
                product=product,
                stars=stars,
                body=body
            )
            return redirect('product-detail', pk=product.id)
        
        if 'add-to-cart' in request.POST:
            quantity = int(request.POST.get('qtybutton', 1))
            add_product_to_cart(request, product.id, quantity)
        if 'add-to-wishlist' in request.POST:
            add_product_to_wishlist(request, product.id)
    elif request.method == 'POST' and request.user == product.host:
        stars = None
        body = None
        messages.error(request, "You can't review your own product.")
    else:
        stars = None
        body = None
        messages.error(request, "You must be logged in to review a product.")
    
    context = {
        'product': product,
        'top_rated_products': top_rated_products,
        'relatedProducts': relatedProducts,
        'latestProducts': latestProducts,
        'reviews': reviews,
        'images': images,
        'review_count': review_count,
        'range': range(1, 6),
    }
    return render(request, 'vicodin/product-details.html', context)

def blogPage(request):
    blogs = Blog.objects.all()

    paginator = Paginator(blogs, 8)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:  
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'blogs': page_obj,
    }

    return render(request, 'vicodin/blog_page.html', context)

def detailBlogPage(request, pk):
    blog = Blog.objects.get(id=pk)
    comments = Comment.objects.filter(blog=blog)
    parent_comments = comments.filter(parent__isnull=True)
    comments_count = parent_comments.count()

    context = {
        'blog': blog,
        'comments': comments,
        'comments_count': comments_count
    }

    return render(request, 'vicodin/blog_details.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:  # noqa: E722
            messages.error(request, "User does not Exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password does not Exist.")

    return render(request, 'vicodin/login.html')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.name = user.first_name + ' ' + user.last_name
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration.")

    context = {'form': form}
    return render(request, 'vicodin/register.html', context)

def shopingPage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    one_month_ago = timezone.now() - timedelta(days=30)

    categories = Category.objects.all()
    products = Product.objects.annotate(
        review_count=Count('review'),
        avg_rating=Avg('review__stars')
    )
    latestProducts = Product.objects.filter(created__gte=one_month_ago)

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q) |
            Q(host__username__icontains=q)
        )

    if request.method == 'POST':
        sorting_option = request.POST.get('sorting_option')
        
        if 'add-to-cart' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-cart')
            add_product_to_cart(request, product_id)
        if 'add-to-wishlist' in request.POST and request.user.is_authenticated:
            product_id = request.POST.get('add-to-wishlist')
            add_product_to_wishlist(request, product_id)

        if sorting_option == 'popularity':
            products = products.order_by('-review_count')
        elif sorting_option == 'new_arrivals':
            products = products.order_by('-created')
        elif sorting_option == 'price_low_high':
            products = products.order_by('price')
        elif sorting_option == 'price_high_low':
            products = products.order_by('-price')
        else:
            pass


    if category_id:
        products = products.filter(category__id=category_id)
    
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    

    for product in products:
        product.avg_rating = product.avg_rating or 0
        product.rating_binary_list = [1 if i < int(product.avg_rating) else 0 for i in range(5)]



    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    start_index = (page_obj.number - 1) * paginator.per_page + 1
    end_index = start_index + len(page_obj.object_list) - 1 
    products_count = paginator.count

    context = {
        'products': page_obj,
        'latestProducts': latestProducts,
        'page_obj': page_obj,
        'categories': categories,
        'products_count': products_count,  
        'start_index': start_index,
        'end_index': end_index,
    }

    return render(request, 'vicodin/shoping.html', context)

# LOGIN REQUIRED VIEWS

@login_required(login_url='login')
def commentBlog(request, pk, type, id=None):
    blog = Blog.objects.get(id=pk)

    if type == 'blog':
        obj = blog
        parent_comment = None
    elif type == 'comment':
        obj = Comment.objects.get(id=id)
        parent_comment = obj
    else:
        return HttpResponse('Invalid type')

    form = CommentForm(request.POST)
    if request.method == 'POST' and request.user != blog.author:
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.parent = parent_comment
            comment.save()
        return redirect('blog-detail', pk=blog.id)
        messages.error(request, "Comment added successfully.")
    else:
        messages.error(request, "You can't comment on your own blog.")
        return redirect('blog-detail', pk=blog.id)
    

    context = {
        'obj': obj,
        'obj_class_name': obj.get_class_name(),
        'form': form,
    }

    return render(request, 'vicodin/comment_reply_form.html', context)

@login_required(login_url='login')
def CreateUpdateBlog(request, type, id=None):
    if request.method == 'POST':
        if type == 'create':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user
                blog.save()
                return redirect('blog-page')
        elif type == 'update' and id is not None:
            blog = Blog.objects.get(id=id)
            if blog.author != request.user:
                form = BlogForm(request.POST, request.FILES, instance=blog)
                if form.is_valid():
                    form.save()
                    return redirect('blog-detail', pk=blog.id)
                messages.error(request, "Blog updated successfully.")
            else:
                messages.error(request, "You can't update other's blog.")
                return redirect('blog-detail', pk=blog.id)
    else:
        if type == 'update' and id is not None:
            blog = Blog.objects.get(id=id)

            form = BlogForm(instance=blog)
        else:
            form = BlogForm()

    context = {
        'form': form
    }

    return render(request, 'vicodin/blog_create_update.html', context)

@login_required(login_url='login')
def DeleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)

    if request.method == 'POST' and request.user == blog.author:
        action = request.POST.get('action')
        if action == 'cancel':
            return redirect('blog-detail', pk=blog.id)
        else:
            blog.delete()
            return redirect('blog-page')
        messages.error(request, "Blog deleted successfully.")
    else :
        messages.error(request, "You can't delete other's blog.")
        return redirect('blog-detail', pk=blog.id)
    context = {
        'blog': blog,
    }

    return render(request, 'vicodin/delete_blog.html', context)

@login_required(login_url='login')
def EditCommentReply(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        messages.error(request, "You can't edit other's comment.")
        return redirect('blog-detail', pk=comment.blog.id)

    form = CommentForm(instance=comment)

    if request.method == 'POST' and request.user == comment.user:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog-detail', pk=comment.blog.id)
        messages.error(request, "Comment edited successfully.")
    else:
        messages.error(request, "You can't edit other's comment.")
        return redirect('blog-detail', pk=comment.blog.id)
    context = {
        'form': form,
        'comment': comment,
    }

    return render(request, 'vicodin/edit_comment.html', context)

@login_required(login_url='login')
def DeleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.method == 'POST' and request.user == comment.user:
        action = request.POST.get('action')
        if action == 'cancel':
            return redirect('blog-detail', pk=comment.blog.id)
        else:
            comment.delete()
            return redirect('blog-detail', pk=comment.blog.id)
        messages.error(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You can't delete other's comment.")
        return redirect('blog-detail', pk=comment.blog.id)
    context = {
        'comment': comment,
    }

    return render(request, 'vicodin/delete_comment.html', context)

@login_required(login_url='login')
def createProduct(request):
    categoryes = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            product.host = request.user
            product.category = category
            product.save()

            main_image = Images(product=product, image=product.main_image)
            main_image.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    Images.objects.create(product=product, image=image)
            return redirect('home')
    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=Images.objects.none())

    context = {
        'form': form,
        'formset': formset,
        'categoryes': categoryes,
    }

    return render(request, 'vicodin/create_product.html', context)

@login_required(login_url='login')
def updateProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categoryes = Category.objects.all()
    images = Images.objects.filter(product=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.filter(product=product))

        if 'delete-image' in request.POST:
            image_id = request.POST.get('image_id')
            Images.objects.get(id=image_id).delete()
            return redirect('update-product', pk=pk)

        if 'edit-image' in request.POST:
            image_id = request.POST.get('image_id')
            image = Images.objects.get(id=image_id)
            image_form = ImagesForm(request.POST, request.FILES, instance=image)
            if image_form.is_valid():
                image_form.save()
                return redirect('update-product', pk=pk)

        if form.is_valid():
            product = form.save(commit=False)
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            product.host = request.user
            product.category = category
            product.save()

            main_image = request.FILES.get('product_main_image')
            if main_image and product.main_image != main_image:
                Images.objects.delete(product=product, image=product.main_image)
                Images.objects.create(product=product, image=main_image)
                product.main_image = main_image
                product.save()



            return redirect('product-detail', pk=product.id)

    else:
        form = ProductForm(instance=product)
        formset = ImageFormSet(queryset=Images.objects.filter(product=product))

    context = {
        'form': form,
        'formset': formset,
        'categoryes': categoryes,
        'product': product,
        'images': images,
    }
    return render(request, 'vicodin/update_product.html', context)

@login_required(login_url='login')
def ImagesPage(request, pk, type, id=None):
    product = Product.objects.get(id=pk)
    image = None

    if type == 'add':
        form = ImagesForm()
        if request.method == 'POST':
            form = ImagesForm(request.POST, request.FILES)
            if form.is_valid():
                if 'add-image' in request.POST:
                    image = form.save(commit=False)
                    image.product = product
                    image.save()
                return redirect('update-product', pk=pk)
    else:
        image = Images.objects.get(id=id)
        if request.method == 'POST':
            form = ImagesForm(request.POST, request.FILES, instance=image)
            if form.is_valid():
                if 'delete-image' in request.POST:
                    image.delete()
                    return redirect('update-product', pk=pk)
                elif 'edit-image' in request.POST:
                    image.image = request.FILES.get('image')
                    image.save()
                    return redirect('update-product', pk=pk)
                form.save()
                return redirect('update-product', pk=pk)
        else:
            form = ImagesForm(instance=image)

    context = {
        'product': product,
        'image': image,
        'form': form,
    }

    return render(request, 'vicodin/image_form.html', context)

@login_required(login_url='login')
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)

    reviews = Review.objects.filter(product=product)
    review_count = reviews.count()

    
    if review_count > 0:
        avg_rating = reviews.aggregate(avg_rating=Avg('stars'))['avg_rating']
    else:
        avg_rating = 0

    rating_binary_list = [1] * int(avg_rating) + [0] * (5 - int(avg_rating))

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'cancel':
            return redirect('product-detail', pk=product.id)
        else:
            product.delete()
            return redirect('home')

    context = {
        'product': product,
        'reviews': reviews,
        'review_count': review_count,
        'rating_binary_list': rating_binary_list,
    }

    return render(request, 'vicodin/delete_product.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    wishList = WishList.objects.filter(user__id = pk)
    order_items = Order.objects.filter(user__id=pk)
    addresses = Address.objects.filter(user__id=pk)
    cards = Card.objects.filter(user=user)
    cardsCount = cards.count()
    addressesCount = addresses.count()

    for order in order_items:
        if order.status == Order.PENDING and timezone.now() > order.date + timedelta(days=7):
            order.status = Order.DELAYED
            order.save()
    

    if request.method == 'POST':
        if 'finish-order' in request.POST:
            order_to_finish = order_items.get(id=request.POST.get('finish-order-id'))
            order_to_finish.status = Order.APPROVED
            order_to_finish.save()
        elif 'cancel-order' in request.POST:
            order_to_cancel = order_items.get(id=request.POST.get('cancel-order-id'))
            order_to_cancel.delete()
        elif 'delete-wishlist' in request.POST:
            wish_to_delete = wishList.get(id=request.POST.get('delete-wishlist-id'))
            wish_to_delete.delete()
        elif 'delete-address' in request.POST:
            address_to_delete = addresses.get(id=request.POST.get('delete-address-id'))
            address_to_delete.delete()
        elif 'delete-card' in request.POST:
            card_to_delete = cards.get(id=request.POST.get('delete-card-id'))
            card_to_delete.delete()
        elif 'change-password' in request.POST:
            if user.check_password(request.POST.get('old_password')):
                if request.POST.get('new_password') == request.POST.get('confirm_password'):
                    user.set_password(request.POST.get('new_password'))
                    user.save()
                    messages.success(request, 'Password changed successfully.')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Old password is incorrect.')
        else:
            form = UserForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
        return redirect('user-profile', pk=pk)
    
    context = {
        'user': user,
        'form': form,
        'wishList': wishList,
        'order_items': order_items,
        'addresses': addresses,
        'cards': cards,
        'cardsCount': cardsCount,
        'addressesCount': addressesCount
    }

    return render(request, 'vicodin/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST' and request.user == user:
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
        messages.error(request, "An error occured during updating user.")
    else:
        messages.error(request, "You can't update other's profile.")
        return redirect('profile', pk=user.id)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def editReview(request, pk):
    review = Review.objects.get(id=pk)

    if request.user != review.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST' and review.user == request.user:
        stars = request.POST.get('rating')
        body = request.POST.get('body')

        if stars and body:
            review.stars = int(stars)
            review.body = body
            review.save()
        return redirect('product-detail', pk=review.product.id)
        messages.error(request, "Review edited successfully.")
    else:
        messages.error(request, "You can't edit other's review.")
        return redirect('product-detail', pk=review.product.id)
    
    context = {
        'review': review
    }

    return render(request, 'vicodin/edit_review.html', context)

@login_required(login_url='login')
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)

    if request.method == 'POST' and review.user == request.user:
        action = request.POST.get('action')
        if action == 'cancel':
            return redirect('product-details', pk=review.product.id)
        else:
            review.delete()
            return redirect('product-detail', pk=review.product.id)
        messages.error(request, "Review deleted successfully.")
    else:
        messages.error(request, "You can't delete other's review.")
        return redirect('product-detail', pk=review.product.id)
    
    context = {
        'review': review,
        'range' : range(1,6),
    }

    return render(request, 'vicodin/delete_review.html', context)

@login_required(login_url='login')
def cartPage(request):
    cart = Cart.objects.get(user=request.user)
    cartItems = CartItem.objects.filter(cart=cart)
    subtotal = cart.total_price + 15

    if request.method == 'POST' and cart.user == request.user:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('qtybutton'))
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            pass

        return redirect('cart')
        messages.error(request, "Cart updated successfully.")
    else:
        messages.error(request, "You can't update other's cart.")
        return redirect('cart')

    context = {
        'cart': cart,
        'cartItems': cartItems,
        'subtotal': subtotal
    }
    return render(request, 'vicodin/cart.html', context)

@login_required(login_url='login')
def CheckoutPage(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    cards = Card.objects.filter(user=user)
    cart = Cart.objects.get(user=user)
    form = OrderForm()

    if addresses and cards and cards.user == user and addresses.user == user:
        total_price = cart.total_price
        vat = 15 if cart.total_price > 100 else 100 if cart.total_price > 1000 else 0
        shipping = 0 if addresses[0].country == 'Georgia' else 25
        finish_total = total_price + vat + shipping

        choosen_card_id = request.GET.get('card_id')
        chosen_card = None
        if choosen_card_id:
            chosen_card = cards.get(id=choosen_card_id)

        if request.method == 'POST':
            selected_address_id = request.POST.get('selected_address')
            selected_card_id = request.POST.get('selected_card')

            if selected_address_id and selected_card_id:
                selected_address = Address.objects.get(id=selected_address_id)
                selected_card = cards.get(id=selected_card_id)

                messages.success(request, f'Selected address: {selected_address}')
                messages.success(request, f'Selected card: {selected_card}')

            for prod in cart.cartItems():
                form = OrderForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    order.user = user
                    order.product = prod.product
                    order.price = prod.item_price
                    order.status = Order.PENDING
                    order.save()
                    messages.success(request, 'Order placed successfully!')
            cart.clear_cart()
            messages.error(request, 'Payment successful!')
            return redirect('user-profile', pk=user.id)
    else:
        messages.error(request, 'You need to have at least one address and one card to checkout.')
        return redirect('user-profile', pk=user.id)

    context = {
        'user': user,
        'addresses': addresses,
        'cart': cart.cartItems,
        'vat': vat,
        'shipping': shipping,
        'finish_total': finish_total,
        'cards': cards,
        'chosen_card': chosen_card,
        'form': form,
        'messages': messages.get_messages(request)
    }

    return render(request, 'vicodin/payment.html', context)

@login_required(login_url='login')
def CreateCard(request):
    form = CardForm()
    cards = Card.objects.filter(user=request.user)

    if request.method == 'POST':
        if cards.count() < 3:
            form = CardForm(request.POST)
            if form.is_valid():
                card = form.save(commit=False)
                card.user = request.user
                card.save()
                return redirect('user-profile', pk=request.user.id)
        else:
            return messages.error(request, 'You can not add more than 3 cards.')

    context = {
        'form': form
    }

    return render(request, 'vicodin/create_card.html', context)

@login_required(login_url='login')
def CreateAddress(request):
    user = request.user
    form = AddressForm()
    addresses = Address.objects.filter(user=user)

    if request.method == 'POST':
        if addresses.count() < 3:
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = user
                address.save()
                return redirect('user-profile', pk=user.id)
        else:
            return messages.error(request, 'You can not add more than 3 Address.')

    context = {
        'form': form
    }

    return render(request, 'vicodin/create_address.html', context)
