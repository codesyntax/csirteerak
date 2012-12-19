from models import *
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import datetime,timedelta

import cart
from models import *

def index(request):
    irteerak=Irteera.objects.all()
    orain=datetime.datetime.now()
    extra_context={'hileak':range(1,13),'gaur':orain,'ebentuak':Agenda.objects.all(),'irteerak':irteerak,'mota':''}

    return render_to_response('agenda/index.html',
                               extra_context,
                               context_instance=RequestContext(request))

def eguna(request,urtea,hilea,eguna):
    extra_context={}
    gaur=datetime.datetime(int(urtea), int(hilea), int(eguna))
    extra_context['gaur']=gaur
    bihar=datetime.datetime(int(urtea), int(hilea), int(eguna))+timedelta(1)
    extra_context['objs']=Agenda.objects.filter(begin__gte=gaur,begin__lte=bihar).order_by('begin')
    return render_to_response('agenda/show.html',
                               extra_context,
                               context_instance=RequestContext(request))  

def eguna_mota(request,urtea,hilea,eguna,mota):
    extra_context={}
    gaur=datetime.datetime(int(urtea), int(hilea), int(eguna))
    extra_context['gaur']=gaur
    bihar=datetime.datetime(int(urtea), int(hilea), int(eguna))+timedelta(1)
    extra_context['objs']=Agenda.objects.filter(begin__gte=gaur,begin__lte=bihar, irteera__id=mota).order_by('begin')
    return render_to_response('agenda/show.html',
                               extra_context,
                               context_instance=RequestContext(request))  
def irteera_item(request,id):
    extra_context={}
    itema=get_object_or_404(Agenda,pk=id)
    extra_context['gaur']=itema.begin
    extra_context['objs']=[itema,]
    return render_to_response('agenda/show.html',
                                             extra_context,
                                             context_instance=RequestContext(request)) 

def mota(request,id):
    irteerak=Irteera.objects.all()     
    extra_context={'mota':int(id), 'hileak':range(1,13),'gaur':datetime.datetime.now(),'ebentuak':Agenda.objects.filter(irteera__id=id),'irteerak':irteerak,'irteera_selected':int(id)}

    return render_to_response('agenda/index.html',
                                             extra_context,
                                              context_instance=RequestContext(request)) 

def add_product_to_cart(request):
    ebentua = request.GET.get('product_id', None)
    if not ebentua:
          messages.info(request, 'Error al anadir el producto')
          return HttpResponseRedirect("/")
    cart.add_to_cart(request, ebentua)

    messages.info(request, 'El producto se ha anadido correctamente')
    return HttpResponseRedirect(reverse('show_cart'))

def show_cart(request):
    cart_items = cart.get_cart_items(request)

    if request.method == 'POST':
        postdata = request.POST.copy()
        if 'update' in postdata.keys():
            cart.update_cart(request)
        if 'remove' in postdata.keys():
            cart.remove_from_cart(request)
            
    cart_subtotal = cart.get_cart_subtotal(request)
    total = cart_subtotal
    return render_to_response('cart/cart.html',locals(),context_instance=RequestContext(request))

def empty_cart(request):
   cart.empty_cart(request)
   return HttpResponseRedirect(reverse('show_cart'))
    
def update_cart(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        giltzak = [a for a in postdata.keys() if a.startswith('item_')]
        idak=[]
        for giltza in giltzak:
           id =giltza.split('_')[1]
           if not id in idak:
              idak.append(id)
              item_id=int(id)
              quantity=request.POST.get('item_%d_quantity'%(item_id),0)
              quantity_murriztua=request.POST.get('item_%d_quantity_murriztua'%(item_id),0)
              cart.update_cart(request, item_id, quantity, quantity_murriztua)
    return HttpResponseRedirect(reverse('show_cart'))

def update_cart_go(request):
    update_cart(request)
    return HttpResponseRedirect(reverse('checkout_index'))

def checkout_index(request):
    
    cart_items = cart.get_cart_items(request)
    total = cart.get_cart_subtotal(request)
    irteera_dict={}

    for item in cart_items:
       if item.irteera.irteera.id==3:
          irteera_aukera = item.irteera.irteera
       irteeran_okupatuta_n = item.irteera.getDisponibilitatea()
       irteeraren_muga = item.irteera.irteera.bisitari_kopuru_mugatua
       bisitan_honetan_datoz_n = item.quantity + item.quantity_murriztua
       totalean_bisitan = irteeran_okupatuta_n+bisitan_honetan_datoz_n

       if totalean_bisitan>irteeraren_muga:
          return render_to_response('order/muga.html',locals(),context_instance=RequestContext(request))

    if request.method == 'POST':
        postdata = request.POST.copy()
        postdata['user'] = request.user.id

        form = CheckOutForm(postdata)     

        if form.is_valid():

           item=form.save()
           item.set_order_number()
           request.session[ORDER_ID_SESSION_KEY]=item.id
           return HttpResponseRedirect(reverse("checkout_pay_method"))
        else:
           form =  CheckOutForm(postdata)
           return render_to_response('order/index.html',locals(),context_instance=RequestContext(request))

    form =  CheckOutForm()

    return render_to_response('order/index.html',locals(),context_instance=RequestContext(request))

def checkout_done(request):
    order = Order.objects.get(pk=request.session[ORDER_ID_SESSION_KEY])     
    cart_items=[] 

    order.save()

    for item in cart.get_cart_items(request):
        oi = OrderItem(product=item.irteera,quantity=item.quantity,
                       price=item.irteera.irteera.prezio_orokorra, 
                       order=order)
                                
        oi.save()

    cart_items = OrderItem.objects.filter(order=order)
    total=order.get_total()
    cart.end_session(request)
    return render_to_response('order/checkout_done.html',locals(),context_instance=RequestContext(request))
