from django.conf.urls import  url
from .views import StatisticOwnerCategoryPie,\
                   StatisticOwnerOfferLikesAndViews,\
                   StatisticOwnerOfferTakenAndRedeemed,\
                   StatisticOwnerShopPie,\
                   StatisticOwnerOfferPie,\
                   StatisticGlobalCategoryPie,\
                   StatisticGlobalOfferPie,\
                   StatisticView
urlpatterns = [
    url(r'^statistic/owner/offers/$', StatisticOwnerOfferLikesAndViews.as_view(), name='statistic_owner_likes_views'),
    url(r'^statistic/owner/coupons/$', StatisticOwnerOfferTakenAndRedeemed.as_view(), name='statistic_owner_taken_redeemed'),
    url(r'^statistic/owner/category-pie/$', StatisticOwnerCategoryPie.as_view(), name='statistic_owner_category_pie'),
    url(r'^statistic/owner/shop-pie/$', StatisticOwnerShopPie.as_view(), name='statistic_owner_shop_pie'),
    url(r'^statistic/owner/offer-pie/$', StatisticOwnerOfferPie.as_view(), name='statistic_owner_offer_pie'),
    url(r'^statistic/global/category-pie/$', StatisticGlobalCategoryPie.as_view(), name='statistic_global_category_pie'),
    url(r'^statistic/global/offer-pie/$', StatisticGlobalOfferPie.as_view(), name='statistic_global_offer_pie'),
    url(r'^statistic/$', StatisticView.as_view(), name='statistic'),

]

