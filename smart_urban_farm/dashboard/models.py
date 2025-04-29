from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)  # যেমন "Water Pump"
    status = models.BooleanField(default=False)  # True = চালু, False = বন্ধ
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    soil_moisture = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    light_level = models.FloatField()

    def __str__(self):
        return f"Data at {self.timestamp}"

class CropHealth(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    disease_detected = models.BooleanField(default=False)
    yield_prediction = models.FloatField()

    def __str__(self):
        return f"Health at {self.timestamp}"
    
class ControlSystem(models.Model):
    irrigation = models.BooleanField(default=False)
    climate_control = models.CharField(max_length=10, choices=[('heat', 'Heat'), ('cool', 'Cool'), ('off', 'Off')], default='off')
    nutrient_delivery = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)