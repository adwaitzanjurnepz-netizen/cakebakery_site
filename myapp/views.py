from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .cart import Cart
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from .models import Product
from decimal import Decimal
# Create your views here.
def home(request):
    return render(request,'home.html')
def cart(request):
    cart = Cart(request)

    cart_items = []
    total_price = 0

    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = float(item['price']) * item['quantity']
        total_price += subtotal

        cart_items.append({
            'product': product,
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    }) 
def about(request):
    return render(request,'about.html')
def help(request):
    return render(request,'contact.html')
def ajax_add_to_cart(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    cart.add(product_id=product.id, price=product.price)

    return JsonResponse({
        'success': True,
        'cart_count': sum(item['quantity'] for item in cart.cart.values())
    })


def ajax_remove_from_cart(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    cart.remove(product_id)

    return JsonResponse({'success': True})
def checkout(request):
    cart = Cart(request)

    if not cart.cart:
        return redirect('cart')

    if request.method == "POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']

        total_price = 0
        for item in cart.cart.values():
            total_price += float(item['price']) * item['quantity']

        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            total_price=total_price
        )

        for product_id, item in cart.cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        return render(request, 'order_success.html', {'order': order})

    return render(request, 'checkout.html')
# shop/views.py


def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart')

def clear(self):
    self.session['cart'] = {}
    self.session.modified = True
def increase_quantity(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product_id=product.id, price=product.price)
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = Cart(request)
    cart.decrease(product_id)
    return redirect('cart')


def checkout(request):
    cart = Cart(request)

    if not cart.cart:
        return redirect('cart')

    cart_items = []
    total_price = Decimal('0.00')

    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = Decimal(item['price']) * item['quantity']
        total_price += subtotal

        cart_items.append({
            'product': product,
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    if request.method == "POST":
        order = Order.objects.create(
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item['product'].name,
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        return render(request, 'order_success.html', {'order': order})

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
