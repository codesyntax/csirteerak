from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
     url(r'^$','index', name="agenda_index"),
     url(r'^(?P<urtea>[0-9]+)-(?P<hilea>[0-9]+)-(?P<eguna>[0-9]+)/$','eguna', name="csirteerak_agenda_eguna"),
     url(r'^(?P<urtea>[0-9]+)-(?P<hilea>[0-9]+)-(?P<eguna>[0-9]+)/(?P<mota>[0-9]+)/$','eguna_mota', name="csirteerak_agenda_eguna_mota"),               
     url(r'^(?P<id>[0-9]+)/$','irteera_item',name="csirteerak_irteera_item"),     
     url(r'^mota/(?P<id>[0-9]+)/$','mota',name="csirteerak_agenda_mota"),
     url(r'^event/$','agenda_index',name="csirteerak_agenda_ebentuak"),     
     url(r'^event/(?P<id>[0-9]+)/$','agenda_show',name="csirteerak_agenda_ebentua"),

     url(r'^add_product/$','add_product_to_cart', name="csirteerak_add_to_cart"),
     url(r'^show_cart/$','show_cart', name="csirteerak_show_cart"),
     url(r'^empty_cart/$','empty_cart', name="csirteerak_empty_cart"),
     url(r'^update_cart/$','update_cart', name="csirteerak_update_cart"),
     url(r'^update_cart_go/$','update_cart_go', name="csirteerak_update_cart_go"),               


     url(r'^checkout$','checkout_index', name="csirteerak_checkout_index"), #METODOARI IZENA ALDATU DIOGU!
     url(r'^pay_method/$','pay_method', name="csirteerak_checkout_pay_method"),
     url(r'^checkout_done/$','checkout_done', name="csirteerak_checkout_done"),

                       
    )
urlpatterns += staticfiles_urlpatterns()    
