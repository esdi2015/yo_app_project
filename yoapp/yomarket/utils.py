from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from yoapp.settings import DEFAULT_FROM_EMAIL
from fcm_django.models import FCMDevice
RANK_SYSTEM = {
    "1": (150, "Rank 1. 150 points."),
    "2": (250, "Rank 2. 250 points."),
    "3": (350, "Rank 3. 350 points."),
    "4": (450, "Rank 4. 450 points."),
    "5": (550, "Rank 5. 550 points."),
    "6": (650, "Rank 6. 650 points."),
    "7": (750, "Rank 7. 750 points."),
    "8": (850, "Rank 8. 850 points."),
    "9": (950, "Rank 9. 950 points."),
    "10": (1050, "Rank 10. 1050 points."),
    "11": (1150, "Rank 11. 1150 points."),
    "12": (1250, "Rank 12. 1250 points."),
    "13": (1350, "Rank 13. 1350 points."),
    "14": (1450, "Rank 14. 1450 points."),
    "15": (1550, "Rank 15. 1550 points."),
    "16": (1650, "Rank 16. 1650 points."),
    "17": (1750, "Rank 17. 1750 points."),
    "18": (1850, "Rank 18. 1850 points."),
    "19": (1950, "Rank 19. 1950 points."),
    "20": (2050, "Rank 20. 2050 points."),
    "21": (2150, "Rank 21. 2150 points."),
    "22": (2250, "Rank 22. 2250 points."),
    "23": (2350, "Rank 23. 2350 points."),
    "24": (2450, "Rank 24. 2450 points."),
    "25": (2550, "Rank 25. 2550 points."),
    "26": (2650, "Rank 26. 2650 points."),
    "27": (2750, "Rank 27. 2750 points."),
    "28": (2850, "Rank 28. 2850 points."),
    "29": (2950, "Rank 29. 2950 points."),
    "30": (3050, "Rank 30. 3050 points."),
    "31": (3150, "Rank 31. 3150 points."),
    "32": (3250, "Rank 32. 3250 points."),
    "33": (3350, "Rank 33. 3350 points."),
    "34": (3450, "Rank 34. 3450 points."),
    "35": (3550, "Rank 35. 3550 points."),
    "36": (3650, "Rank 36. 3650 points."),
    "37": (3750, "Rank 37. 3750 points."),
    "38": (3850, "Rank 38. 3850 points."),
    "39": (3950, "Rank 39. 3950 points."),
    "40": (4050, "Rank 40. 4050 points."),
    "41": (4150, "Rank 41. 4150 points."),
    "42": (4250, "Rank 42. 4250 points."),
    "43": (4350, "Rank 43. 4350 points."),
    "44": (4450, "Rank 44. 4450 points."),
    "45": (4550, "Rank 45. 4550 points."),
    "46": (4650, "Rank 46. 4650 points."),
    "47": (4750, "Rank 47. 4750 points."),
    "48": (4850, "Rank 48. 4850 points."),
    "49": (4950, "Rank 49. 4950 points."),
    "50": (5050, "Rank 50. 5050 points."),
    "51": (5150, "Rank 51. 5150 points."),
    "52": (5250, "Rank 52. 5250 points."),
    "53": (5350, "Rank 53. 5350 points."),
    "54": (5450, "Rank 54. 5450 points."),
    "55": (5550, "Rank 55. 5550 points."),
    "56": (5650, "Rank 56. 5650 points."),
    "57": (5750, "Rank 57. 5750 points."),
    "58": (5850, "Rank 58. 5850 points."),
    "59": (5950, "Rank 59. 5950 points."),
    "60": (6050, "Rank 60. 6050 points."),
    "61": (6150, "Rank 61. 6150 points."),
    "62": (6250, "Rank 62. 6250 points."),
    "63": (6350, "Rank 63. 6350 points."),
    "64": (6450, "Rank 64. 6450 points."),
    "65": (6550, "Rank 65. 6550 points."),
    "66": (6650, "Rank 66. 6650 points."),
    "67": (6750, "Rank 67. 6750 points."),
    "68": (6850, "Rank 68. 6850 points."),
    "69": (6950, "Rank 69. 6950 points."),
    "70": (7050, "Rank 70. 7050 points."),
    "71": (7150, "Rank 71. 7150 points."),
    "72": (7250, "Rank 72. 7250 points."),
    "73": (7350, "Rank 73. 7350 points."),
    "74": (7450, "Rank 74. 7450 points."),
    "75": (7550, "Rank 75. 7550 points."),
    "76": (7650, "Rank 76. 7650 points."),
    "77": (7750, "Rank 77. 7750 points."),
    "78": (7850, "Rank 78. 7850 points."),
    "79": (7950, "Rank 79. 7950 points."),
    "80": (8050, "Rank 80. 8050 points."),
    "81": (8150, "Rank 81. 8150 points."),
    "82": (8250, "Rank 82. 8250 points."),
    "83": (8350, "Rank 83. 8350 points."),
    "84": (8450, "Rank 84. 8450 points."),
    "85": (8550, "Rank 85. 8550 points."),
    "86": (8650, "Rank 86. 8650 points."),
    "87": (8750, "Rank 87. 8750 points."),
    "88": (8850, "Rank 88. 8850 points."),
    "89": (8950, "Rank 89. 8950 points."),
    "90": (9050, "Rank 90. 9050 points."),
    "91": (9150, "Rank 91. 9150 points."),
    "92": (9250, "Rank 92. 9250 points."),
    "93": (9350, "Rank 93. 9350 points."),
    "94": (9450, "Rank 94. 9450 points."),
    "95": (9550, "Rank 95. 9550 points."),
    "96": (9650, "Rank 96. 9650 points."),
    "97": (9750, "Rank 97. 9750 points."),
    "98": (9850, "Rank 98. 9850 points."),
    "99": (9950, "Rank 99. 9950 points."),
    "100": (10050, "Rank 100. 10050 points."),
}



def recalculate_rank(user):
    user_rank = 0
    next_rank = 0
    for rank in RANK_SYSTEM:
      if RANK_SYSTEM[rank][0]<user.profile.points:
        pass
      else:
          next_rank=rank
          user_rank=int(rank)-1
          break

    # i = str(next_rank)
    # points_to_next_rank=RANK_SYSTEM[i][0]-user.profile.points

    user.profile.rank=user_rank
    user.profile.save()
    return True


def send_invoice(order,user):
        devices = FCMDevice.objects.filter(user=user)

        if devices.exists():
            msg = {'data': {'extra': {"order_id": order.id},'title': 'Thanks you for order','message':" Thanks you for order"}}

        for device in devices:
            device.send_message(**msg)

        else:
            pass

        context = {'order':order,
                   'order_products':order.order_products.all()}

        email_html_message = render_to_string('invoice/email.html', context)
        email_plaintext_message = render_to_string('invoice/email.txt', context)

        msg = EmailMultiAlternatives("Thank you for order. HALAP",email_plaintext_message,from_email=DEFAULT_FROM_EMAIL,to=(user.email,))
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        return True