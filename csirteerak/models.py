from django.db import models
from pages.models import Page
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
import datetime


PAYMENT_METHODS=((2,'Credit card'),(3,'Transfer'),)

BAIEZ_CHOICES = ((1,'Bai'),(0,'Ez'))


class Irteera(models.Model):
    description = models.TextField(null=True,blank=True)
    needs= models.TextField(null=True,blank=True)
    begin_place = models.CharField(max_length=255,null=True, blank=True)
    end_place = models.CharField(max_length=255,null=True, blank=True)  
    page = models.ForeignKey(Page)
    prezio_orokorra = models.DecimalField(max_digits=10, decimal_places=2)
    iraupena=models.TimeField(null=True, blank=True)  
    bisitari_kopuru_mugatua = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Irteera'
        verbose_name_plural = 'Irteerak'    

    def __unicode__(self):
        return self.page.title()


class Agenda(models.Model):
    irteera = models.ForeignKey(Irteera)
    begin =models.DateTimeField(null=True,blank=True)
    end =models.DateTimeField(null=True,blank=True)
    blokeatuta = models.BooleanField(default=False)
    bertan_behera = models.BooleanField(default=False)

    def lekua_dago(self):
        if self.irteera.bisitari_kopuru_mugatua>=self.getDisponibilitatea():
           return True
        else:
           return False   

    def getDisponibilitatea(self):
        itemak = self.orderitem_set.all()
        okupatuta=0
        for item in itemak:
            okupatuta+=item.quantity
        return okupatuta

    def disponibilitatea(self):
         bisitari_kopurua = self.irteera.bisitari_kopuru_mugatua
         okupatuta = self.getDisponibilitatea()
         return "%d / %d"%(okupatuta,bisitari_kopurua)
         
    def getLibreak(self):
         bisitari_kopurua = self.irteera.bisitari_kopuru_mugatua
         okupatuta = self.getDisponibilitatea()
         return bisitari_kopurua - okupatuta                 
         
    def blokeatuta_dago(self):
        return self.blokeatuta

    def bertanbehera_dago(self):
        return self.bertan_behera

        
    class Meta:
        verbose_name = 'Irteeren agenda'
        verbose_name_plural = 'Irteeren agenda'

    def __unicode__(self):
        return '%s. %s:%s: %s'%(self.begin.date(), self.begin.hour,self.begin.minute,self.irteera.page.title())

   
class Event(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    begin =models.DateTimeField(null=True,blank=True)
    end =models.DateTimeField(null=True,blank=True)
    published = models.BooleanField("Argitaratuta?",choices=BAIEZ_CHOICES, default=0)

    def getTitle(self):
        return self.title

    class Meta:
        verbose_name = 'Ebentuen agenda'
        verbose_name_plural = 'Ebentuen agenda'      


class Order(models.Model):

    PAYMENT_PENDING = 1
    SUBMITED = 2
    CANCELLED = 3
    RETURNED = 4
    FREE = 5
    STATUS = ((PAYMENT_PENDING, 'Pendiente de pago'),
                    (SUBMITED, 'Pagado'),
                    (CANCELLED, 'Cancelado'),
                    (RETURNED, 'Devuelto'),
                    (FREE, 'Gratis'),
    )


    order_number = models.CharField(max_length=100,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=PAYMENT_PENDING)
    payment_method = models.IntegerField(choices=PAYMENT_METHODS, default=0)
    old_payment_method = models.IntegerField(choices=PAYMENT_METHODS, null=True, blank=True, default=0)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    certify = models.BooleanField("Ziurtatzen dut...")
    user = models.ForeignKey(User,null=True,blank=True)
    oharrak = models.TextField(null=True,blank=True)
    email_send = models.BooleanField("Ziurtatzen dut...")
    

    def get_order_items(self):
        return OrderItem.objects.filter(order=self)

    def get_total(self):
        subtotal = 0
        for item in self.get_order_items():
            subtotal +=  (item.price*item.quantity) + (item.price_murriztua*item.quantity_murriztua)
        return subtotal

    def set_order_number(self):
      order_number=str(self.id)+datetime.datetime.now().strftime('%Y%m%d') #date('ymdHis')
      self.order_number=str(order_number)
      self.save()   
      
    def create_order_number(self):
        try:
           id=Order.objects.all().order_by('-id')[0].id+1
           order_number=str(id)+datetime.datetime.now().strftime('%Y%m%d') #date('ymdHis')
        except:
           order_number=1   
        return order_number
 

    def getTPVAnswer(self):  
         return ''
                               
       
    def erosketa_ok_mail(self,language):
        for item in self.get_order_items():
           subject = render_to_string('order/email_ok_subject.txt',{'language':language})
           message = render_to_string('order/email_ok_body.txt',{'item':item,'language':language})
           send_mail(subject, message,settings.DEFAULT_FROM_EMAIL,  (self.email,), fail_silently=False)

    def erosketa_transf_mail(self,language):
        for item in self.get_order_items():
           subject = render_to_string('order/email_trans_subject.txt',{'language':language})
           message = render_to_string('order/email_trans_body.txt',{'item':item,'language':language})
           send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,  (self.email,), fail_silently=False)
        

    def erosketa_transf_ok_mail(self):
        for item in self.get_order_items():
           subject = render_to_string('order/email_trans_ok_subject.txt')
           message = render_to_string('order/email_trans_ok_body.txt',{'item':item,})
           send_mail(subject, message,settings.DEFAULT_FROM_EMAIL,  (self.email,), fail_silently=False)
           
    def __unicode__(self):
        return u'Pedido: %s' % self.id


def order_presave(sender, instance,**kwargs):
      if not instance.order_number:
         instance.order_number=instance.create_order_number()      
      return True

def order_postsave_send_mail(sender, created, instance,**kwargs):
    if instance.status==2 and instance.payment_method==3:
        instance.erosketa_transf_ok_mail()
    return True


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9,decimal_places=2,null=True,blank=True)
       
    def item_total(self):
        if self.order.status==3 or self.order.status==4 or self.order.status==5: #5 FREE da
           return 0
        else:           
           dena = (self.quantity*self.price)+(self.quantity_murriztua*self.price_murriztua)
           return dena
       
    def disponibilitatea(self):
        return self.product.disponibilitatea()

    def getTxartelarekin(self):
        if self.order.payment_method==2:
            return self.item_total()
        else:
            return '0'            

    def getTransferentziarekin(self):
        if self.order.payment_method==3:
            return self.item_total()
        else:
            return '0'   

    def __unicode__(self):
        try:
           return 'Order Item %d'%(self.id,)
        except:
           return '---'   

def admin_gorde(sender, instance, **kwargs):
    if not instance.price:
        instance.price=instance.product.irteera.prezio_orokorra
    return True    

pre_save.connect(admin_gorde,sender=OrderItem)    
pre_save.connect(order_presave,sender=Order)
post_save.connect(order_postsave_send_mail,sender=Order)        

class CartItem(models.Model):
    cart_id = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    irteera = models.ForeignKey(Agenda, unique=False)
    
    def augment_quantity(self,quantity=1):
        self.quantity += quantity
        self.save()

    def total(self):
        return self.irteera.irteera.prezio_orokorra * self.quantity

    def __unicode__(self):
        return '%s - %s: %s'%(self.irteera.begin, self.irteera.end, self.irteera.irteera.page.get_complete_slug())    
