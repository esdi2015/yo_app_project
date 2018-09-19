from django.db import models
from common.models import User
from yomarket.models import Offer,Shop


POINTS_TYPES = (
    ('user', 'User'),
    ('shop', 'Shop'),
    ('offer', 'Offer')
)

POINTS_EVENT_TYPES = (
    ('transaction', 'Successful transaction'),
    ('prize', 'Prize winnings'),
    ('payment', 'Payment of points'),
    ('daily', 'Daily points')

)



class Point(models.Model):
    points = models.SmallIntegerField(default=1, editable=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, choices=POINTS_TYPES, default=POINTS_TYPES[0][0])
    event_type = models.CharField(max_length=100, choices=POINTS_EVENT_TYPES, default=POINTS_EVENT_TYPES[0][0])

    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE,blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,blank=True, null=True)


