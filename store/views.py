from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import datetime
from .utilits import cookie_cart, cart_data, guest_order


def store(request):
    products = Product.objects.all()

    data = cart_data(request)
    cart_item = data['cartItems']

    context = {
        'products': products,
        'cart_item': cart_item
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cart_data(request)

    cart_item = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_item': cart_item
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cart_data(request)

    cart_item = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_item': cart_item
    }
    return render(request, 'store/checkout.html', context)


def update_user_order(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('sending data', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data_json = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data_json)

    total = float(data_json['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_items_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data_json['shipping']['address'],
            city=data_json['shipping']['city'],
            state=data_json['shipping']['state'],
            zipcode=data_json['shipping']['zipcode'],
        )
    return JsonResponse('Transaction...', safe=False)
