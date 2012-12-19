from django import forms
from django.forms import ModelForm
from django.conf import settings
from models import Order
from django.forms.util import ValidationError

PAYMENT_METHODS=getattr(settings, 'CSIRTEERAK_PAYMENT_METHODS',((1, 'Paypal'),(2,'Credit card'),(3,'Transfer')))

STATES=getattr(settings, 'CSIRTEERAK_PAYMENT_METHODS',(('-','-'),))


class CheckOutForm(ModelForm):
    name = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    city = forms.CharField(max_length=50)
    state =forms.TypedChoiceField(choices=STATES)
    certify=forms.CheckboxInput() 
    email_send=forms.CheckboxInput()
    payment_method = forms.TypedChoiceField(choices=PAYMENT_METHODS)
    
    def clean_phone(self):
        telefonoa = self.clean().get('phone','')
        if telefonoa.startswith('6') or telefonoa.startswith('+'):
           return telefonoa           
        else:
           raise ValidationError("Telefono mugikorra sartu mesedez / Introduzca un telefono movil por favor")
 
    def clean_certify(self):
        certify = self.clean().get('certify','')
        if not certify:
               raise ValidationError("Baldintza guztiak onartu behar ditiuzu")
        else: 
           return certify

    class Meta:
        model = Order
        exclude = ('payment_method','status','order_number','user') 
