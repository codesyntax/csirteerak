# -*- coding: utf-8 -*-
import hashlib
import random
import string
import decimal

from django.contrib import messages

from irteerak.cart.models import CartItem
from irteerak.agenda.models import Agenda

CART_ID_SESSION_KEY = 'cart_id'

def end_session(request):
    request.session[CART_ID_SESSION_KEY]=_generate_cart_id()
    
def _generate_cart_id():
    return hashlib.sha384(''.join(random.sample(string.printable,40))).hexdigest()

def _cart_id(request):
    if not(request.session.get(CART_ID_SESSION_KEY,'')):
        request.session[CART_ID_SESSION_KEY]=_generate_cart_id()
    return request.session.get(CART_ID_SESSION_KEY)

def get_cart_item(request,item_id):
    return CartItem.objects.get(pk=item_id,cart_id=_cart_id(request))

def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))

def get_cart_items_count(request):
    return CartItem.objects.filter(cart_id=_cart_id(request)).count()

def get_cart_subtotal(request):
    cart_total = decimal.Decimal('0.00')
    cart_items = get_cart_items(request)
    for item in cart_items:
        cart_total += item.total()
    return cart_total

def add_to_cart(request, agenda_id):
    cart_items = get_cart_items(request)
    product_in_cart = False
    for cart_item in cart_items:        
        if str(cart_item.irteera) == agenda_id:
            product_in_cart = True                
            cart_item.augment_quantity()
            break
    if not product_in_cart:
        #try:
        if 1:
            product = Agenda.objects.get(pk=agenda_id)
            ci = CartItem(cart_id=_cart_id(request),quantity=1,irteera=product)
            ci.save()
        #except:
        else:
            messages.info(request,'No hemos podido añadir su pedido')

def update_cart(request, item_id, quantity, quantity_murriztua):
    cart_item = get_cart_item(request, item_id)
    try:
        quantity = int(quantity)
        quantity_murriztua=int(quantity_murriztua)
    except:
        messages.info(request,'La cantidad no es correcta')
        return 0

    
    if not quantity:
        quantity = 0
    if not quantity_murriztua:
       quantity_murriztua=0    
    cart_item.quantity = quantity
    cart_item.quantity_murriztua = quantity_murriztua
    cart_item.save()


def remove_from_cart(request):
    postdata = request.POST.copy()
    cart_item = get_cart_item(request, postdata.get('item_id'))
    cart_item.delete()
    

def empty_cart(request):
    user_cart = get_cart_items(request)
    user_cart.delete()
