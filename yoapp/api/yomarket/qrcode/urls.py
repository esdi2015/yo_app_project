from django.conf.urls import  url

from api.yomarket.qrcode.views import make_coupon,QRcouponsListView,QRcouponCheckView,QRcouponShortCheckView,QRcouponRedeemView,QRcouponShortRedeemView

urlpatterns = [
    url(r'^qr/redeem/(?P<uuid_id>.{12,50})/$', QRcouponRedeemView.as_view(), name='redeem_coupon'),
    url(r'^qr/redeem/(?P<id>.{0,12})/$', QRcouponShortRedeemView.as_view(), name='short_redeem_coupon'),

    url(r'^qr/check/(?P<uuid_id>.{12,50})/$', QRcouponCheckView.as_view(), name='check_coupon'),
    url(r'^qr/check/(?P<id>.{0,12})/$', QRcouponShortCheckView.as_view(), name='short_check_coupon'),

    url(r'^qr/list-coupons/',QRcouponsListView.as_view(),name='list_coupons'),
    url(r'^qr/make-coupon/', make_coupon, name='make_coupon'),

]