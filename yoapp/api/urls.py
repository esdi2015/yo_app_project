from .common.user.urls import urlpatterns as user_urls
from .common.category.urls import urlpatterns as category_urls
from .yomarket.offer.urls import urlpatterns as offer_urls
from .yomarket.shop.urls import urlpatterns as shop_urls
from .yomarket.qrcode.urls import urlpatterns as qr_urls


urlpatterns = []
urlpatterns = urlpatterns + user_urls + category_urls + offer_urls + shop_urls + qr_urls



