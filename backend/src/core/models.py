from django.db import models
from django.utils import timezone

class Debt(models.Model):
        DcID = models.CharField(max_length=255)
        UserName = models.CharField(max_length=255)
        Record = models.CharField(max_length=255)
        Account = models.CharField(max_length=255)
        PokerID = models.CharField(max_length=255)
        PokerID2 = models.CharField(max_length=255)
        Total = models.FloatField(default=0.0)
        #date = models.DateField(default=timezone.now)  #時間