from django.conf.urls import  url

from api.yomarket.qrcode.views import qr_check, make_qrs, get_code, qr_checkout

urlpatterns = [
    url(r'^qr/check/(?P<uuid>.{0,50})$', qr_check,name='check_qr'),
    url(r'^qr/make_qrs/$', make_qrs,name='make_qr'),
    url(r'^qr/get_code/$',get_code,name='get_qr'),
    url(r'^qr/checkout/(?P<uuid>.{0,50})$', qr_checkout, name='checkout_qr'),

]