from .common.user.urls import urlpatterns as user_urls
from .common.category.urls import urlpatterns as category_urls
from .common.city.urls import urlpatterns as city_urls
from .yomarket.offer.urls import urlpatterns as offer_urls
from .yomarket.shop.urls import urlpatterns as shop_urls
from .yomarket.qrcode.urls import urlpatterns as qr_urls
from .yomarket.transaction.urls import urlpatterns as transaction_urls

from .yomarket.schedule.urls import urlpatterns as schedule_urls

from .notification.urls import urlpatterns as notification_urls
from .account.urls import urlpatterns as account_urls
from .yomarket.wishlist.urls import urlpatterns as wishlist_urls
from .statistic.urls import urlpatterns as statistic_urls
from .common.smsreg.urls import urlpatterns as sms_reg_urls
from .history.urls import urlpatterns as history_urls
from .common.overview.urls import urlpatterns as overview_urls
from .yomarket.secondary_info.urls import urlpatterns as secondary_info_urls
from .targeting.urls import urlpatterns as targeting_urls

urlpatterns = []
urlpatterns = urlpatterns + \
              user_urls + \
              category_urls + \
              offer_urls + \
              shop_urls + \
              qr_urls + \
              transaction_urls + \
              notification_urls + \
              account_urls + \
              wishlist_urls + \
              statistic_urls + \
              city_urls + \
              sms_reg_urls + \
              schedule_urls + \
              history_urls + \
              overview_urls + \
              secondary_info_urls +\
              targeting_urls



