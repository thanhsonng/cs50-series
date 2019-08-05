from django.contrib.auth import authenticate, login, logout, models
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Cart, CartItem, RegularPizza, SicilianPizza, Topping, Sub, SubAddon, Pasta, Salad, DinnerPlatter

# Create your views here.
def index(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'auth/login.html', {'message': None})

    try:
        cart = user.cart
    except:
        cart = Cart.objects.create(user=user)

    context = {
        'user': user,
        'cart_size': cart.items.filter(parent=None).count(),
        'regular_pizzas': RegularPizza.objects.all(),
        'sicilian_pizzas': SicilianPizza.objects.all(),
        'toppings': Topping.objects.all(),
        'subs': Sub.objects.all(),
        'pastas': Pasta.objects.all(),
        'salads': Salad.objects.all(),
        'dinner_platters': DinnerPlatter.objects.all(),
    }
    return render(request, 'orders/index.html', context)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html', {'message': None})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'auth/login.html', {'message': 'Invalid credentials.'})

    login(request, user)
    return HttpResponseRedirect(reverse('index'))

def logout_view(request):
    logout(request)
    return render(request, 'auth/login.html', {'message': 'Logged out.'})

def signup_view(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html', {'message': None})

    username = request.POST['username']
    email    = request.POST['email']
    password = request.POST['password']

    try:
        user = models.User.objects.create_user(username, email, password)
    except IntegrityError:
        return render(request, 'auth/signup.html', {'message': 'Username taken.'})

    login(request, user)
    return HttpResponseRedirect(reverse('index'))

def regular_pizza(request):
    pass

def sicilian_pizza(request):
    pass

def sub(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'auth/login.html', {'message': None})

    name = request.POST['name']
    size = request.POST['size']
    addons = request.POST.getlist('addons')

    cart = user.cart
    sub = Sub.objects.get(name=name)
    cart_item = CartItem(
        cart=cart,
        product_object_id=sub.id,
        product_content_type=ContentType.objects.get_for_model(sub),
    )
    if size == 'small':
        cart_item.price = sub.small_price
    elif size == 'large':
        cart_item.price = sub.large_price
    cart_item.save()

    for addon in addons:
        sub_addon = SubAddon.objects.get(sub=sub, name=addon)
        CartItem.objects.create(
            cart=cart,
            price=sub_addon.price,
            product_object_id=sub_addon.id,
            product_content_type=ContentType.objects.get_for_model(sub_addon),
            parent=cart_item,
        )

    return HttpResponseRedirect(reverse('index'))

def pasta(request):
    pass

def salad(request):
    pass

def dinner_platter(request):
    pass
