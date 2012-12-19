from django.contrib import admin
from models import *


class AgendaAdmin(admin.ModelAdmin):
   list_display = ["begin","irteera_l","egingoda","block","lekua","dispon"]
   date_hierarchy = 'begin'
   search_fields = ('irteera','begin','end')

   list_filter = ('irteera',)
   custom_filter_spec = {'irteera': Irteera.objects.all()}

   ordering=("begin",)

   fieldsets = (
        ('Irteera', {
            'fields': ('irteera','begin','end')
        }),
        ('Datu gehigarriak', {
            'fields': ('blokeatuta','bertan_behera',)
        }),
    )                            

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
             
class IrteeraAdmin(admin.ModelAdmin):
   list_display = ["irteera_l",]
   
   def irteera_l(self,item):
       return item.page.title()[0:30]
   

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price','item_total','disponibilitatea')
    raw_id_fields = ('product',)
    extra = 0
    show_link = True

 
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','lastname','phone','status','payment_method','get_total','order_number',)
    list_filter = ('status','payment_method','date_added',)
    date_hierarchy = 'date_added'
    search_fields = ['email','name','lastname','order_number']
    inlines = [OrderItemInline,]
    readonly_fields=('get_total','order_number','getTPVAnswer',)

    fieldsets = (
        ('Basic', {'fields':('name','lastname','phone', 'email','city','state',)}),
        ('Oharrak', {'fields':('oharrak',)}),
        ('Payment',{'fields':('order_number','get_total','getTPVAnswer','payment_method','status',)}),
        )


admin.site.register(Order,OrderAdmin)
admin.site.register(Irteera,IrteeraAdmin)
admin.site.register(Agenda, AgendaAdmin)

