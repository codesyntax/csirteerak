from django import forms
from django.forms import ModelForm
from django.conf import settings
from models import Order
from django.forms.util import ValidationError

STATES=getattr(settings, 'CSIRTEERAK_PAYMENT_METHODS',(('-','-'),))


class CheckOutForm(ModelForm):
    name = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    city = forms.CharField(max_length=50)
    state =forms.TypedChoiceField(choices=STATES)
    certify=forms.CheckboxInput() 
    
    def clean_certify(self):
        certify = self.clean().get('certify','')
        if not certify:
               raise ValidationError("Baldintza guztiak onartu behar ditiuzu")
        else: 
           return certify

    class Meta:
        model = Order
        exclude = ('status','order_number') 
