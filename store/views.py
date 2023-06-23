from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import CustomerRegistrationForm, CheckoutForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
import json

def index(request):
    products = Product.objects.all()
    cart = None

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, completed=False)

    context = {"products": products, "cart": cart}
    return render(request, "index.html", context)


@login_required
def cart(request):
    cart = None
    cartitems = []
    cart, _ = Cart.objects.get_or_create(user=request.user, completed=False)
    cartitems = cart.cartitems.all()

    context = {"cart": cart, "items": cartitems}
    return render(request, "cart.html", context)




def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    num_of_item = 0

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        num_of_item = cart.num_of_items

    return JsonResponse(num_of_item, safe=False)


def remove_cart(request, cartitem_id):
    cartitem = get_object_or_404(CartItem, id=cartitem_id)

    if request.method == "POST" and request.user.is_authenticated:
        if cartitem.quantity > 1:
            cartitem.quantity -= 1
            cartitem.save()
        else:
            cartitem.delete()

        return redirect('cart')

    return JsonResponse({"message": "Invalid request."}, status=400)


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Congratulations! User registered successfully.')
            login(request, user) # Redirect to a success page or desired URL
        else:
            messages.warning(request, 'Invalid input data.')
            return render(request, 'customerregistration.html', {'form': form})


@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user)

    context = {'orders': orders}
    return render(request, 'content.html', context)


def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
           
            order = Order()
            order.user = request.user
            order.save()

            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            address = form.cleaned_data['address']
            town = form.cleaned_data['town']
            state = form.cleaned_data['state']
            card_number = form.cleaned_data['card_number']
            card_expiry = form.cleaned_data['card_expiry']
            cvv = form.cleaned_data['cvv']

            order.shipping_fname = fname
            order.shipping_lname = lname
            order.shipping_address = address
            order.shipping_town = town
            order.shipping_state = state
            order.payment_card_number = card_number
            order.payment_card_expiry = card_expiry
            order.payment_cvv = cvv

            order.save()

            cart = Cart.objects.get(user=request.user, completed=False)
            cart_items = cart.cartitems.all()
            for cart_item in cart_items:
                order_item = OrderItem(
                    product=cart_item.product,
                    order=order,
                    quantity=cart_item.quantity
                )
                order_item.save()

            cart.completed = True
            cart.save()

            messages.success(request, 'Congratulations! Order Placed Successfully.')
            return redirect('index')
    else:
        form = CheckoutForm()

    context = {'form': form}
    return render(request, 'checkout.html', context)



def logout_view(request):
    logout(request)
    return redirect('index')
