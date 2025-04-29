from django.contrib import admin
from .models import SensorData, CropHealth

admin.site.register(SensorData)
admin.site.register(CropHealth)