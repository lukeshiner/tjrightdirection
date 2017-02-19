from django.db import models


class HitCounter(models.Model):

    page = models.CharField(max_length=255, editable=False)
    total = models.IntegerField(editable=False, default=0)
    trip = models.IntegerField(editable=False, default=0)

    def increment(self):
        self.total += 1
        self.trip += 1
        self.save()

    def reset_trip(self):
        self.trip = 0
        self.save()
