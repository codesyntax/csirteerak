from django.contrib import admin
from models import *
from datetime import datetime
from filters import *


class AgendaAdmin(admin.ModelAdmin):
   list_display = ["begin","irteera_l","apuntatuak","egingoda","block","lekua","dispon"]
   #"bisita_gidatua",
   date_hierarchy = 'begin'
   search_fields = ('irteera','begin','end')

   list_filter = ('irteera',)
   custom_filter_spec = {'irteera': Irteera.objects.all()}

   ordering=("begin",)

   fieldsets = (
        ('Irteera', {
            'fields': ('irteera','begin','end')
        }),
        ('Irteera/Bukaera puntuak', {
            'fields': ('irteera_puntua','bukaera_puntua',)
        }),
        ('Datu gehigarriak', {
            'fields': ('blokeatuta','bertan_behera','euskaraz')
        }),
    )   
   
   def queryset(self, request):
         qs = super(AgendaAdmin, self).queryset(request)
         if request.GET.get('e','')=='1': #request.user.is_superuser:
            return qs.filter(begin__gte=datetime.now())
         else:
            return qs.all()
                         

   def lekua(self, item):
       return item.lekua_dago()
   lekua.boolean = True    

   def egingoda(self, item):
        return not item.bertan_behera
   egingoda.boolean = True

   def irteera_l(self,item):
       return item.irteera.page.title()[0:30]

   def bisita_gidatua(self,item):
       return item.irteera.page.parent.title()

   def block(sef, item):
       return item.blokeatuta_dago()
   block.boolean = True

   def dispon(self, item):
       return item.disponibilitatea()
   #dispon.boolean = True
   """ 
   def apuntatuak(self,item):
        """ """
        return '<a href="/irteerak/apuntatuak/%d/">Apuntatuak</a>' % item.id
           
   apuntatuak.short_description = 'Apuntatuak '
   apuntatuak.allow_tags = True    

   def ordainduak(self,item):
        """ """
        return '<a href="/irteerak/ordaindutakoak/%d/">Ordainduak</a>' % item.id
           
   ordainduak.short_description = 'Ordaindua '
   ordainduak.allow_tags = True
       
   class Media:
       js=('/static/js/bete_end.js',)
   """ 
             
class IrteeraAdmin(admin.ModelAdmin):
   list_display = ["irteera_l",]
   
   def irteera_l(self,item):
       return item.page.title()[0:30]
   """
   def estatistikak(self,item):
        """ """
        return '<a href="/irteerak/estadistikak/%d/">Estatistikak</a>' % item.id
           
   estatistikak.short_description = 'Estatistikak '
   estatistikak.allow_tags = True    
   """

class EventAdmin(admin.ModelAdmin):
   list_display = ["begin","getTitle"]
   

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price','item_total','disponibilitatea')
    raw_id_fields = ('product',)
    extra = 0
    #can_delete = True
    show_link = True

 
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','lastname','phone','status','payment_method','get_total','order_number','print_cert')
    list_filter = ('status','payment_method','date_added','user')
    date_hierarchy = 'date_added'
    search_fields = ['email','name','lastname','order_number']
    inlines = [OrderItemInline,]
    readonly_fields=('get_total','order_number','getTPVAnswer',)

    fieldsets = (
        ('Basic', {'fields':('name','lastname','phone', 'email','city','state','non_ezagutu','irteera_aukera')}),
        ('Oharrak', {'fields':('oharrak',)}),
        ('Payment',{'fields':('order_number','get_total','getTPVAnswer','payment_method','status','user')}),
        )

    """
    def print_cert(self, item):
        return '<a href="/payment/print/%s/">Deskargatu</a>' % str(item.order_number)
           
    print_cert.short_description = 'Erreziboa'
    print_cert.allow_tags = True   
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user.id
        return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)  

admin.site.register(Order,OrderAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Irteera,IrteeraAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(AgendaZarra, AgendaAdmin)
