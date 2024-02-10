
from django.db import models

class TrackingData(models.Model):
    tag_id = models.CharField(max_length=32)
    temperature = models.FloatField()
    location = models.CharField(max_length=100)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.tag_id} - {self.time}"
    
class NfcTag(models.Model):
    """NFC tag model."""
    product_name = models.CharField(max_length=100)
    batch_no = models.CharField(max_length=100)
    model_no = models.CharField(max_length=100)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    source_address = models.CharField(max_length=100)
    destination_address = models.CharField(max_length=100)
    quantity = models.IntegerField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
