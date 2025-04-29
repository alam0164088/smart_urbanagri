from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SensorData, CropHealth, Device
from community.models import EducationalContent, ForumPost
import json
from datetime import datetime

# AI ফাংশন (সিম্পল উদাহরণ)
def predict_watering_schedule(sensor_data):
    if sensor_data and sensor_data.soil_moisture < 300:
        return "Water Now"
    return "No Water Needed"

def predict_crop_health(sensor_data):
    if sensor_data and sensor_data.temperature > 35 and sensor_data.humidity < 40:
        return "Potential Heat Stress Detected"
    return "Healthy"

@login_required
def dashboard(request):
    # সর্বশেষ সেন্সর ডাটা
    latest_data = SensorData.objects.latest('timestamp') if SensorData.objects.exists() else None
    sensor_data = SensorData.objects.all().order_by('-timestamp')[:10]  # গ্রাফের জন্য ১০টি ডাটা
    devices = Device.objects.all()

    # AI প্রেডিকশন
    watering_schedule = predict_watering_schedule(latest_data) if latest_data else "No Data"
    crop_health_status = predict_crop_health(latest_data) if latest_data else "No Data"

    # অ্যালার্ট
    alerts = []
    if latest_data:
        if latest_data.soil_moisture < 300:
            alerts.append("Low Soil Moisture - Water Needed!")
        if latest_data.temperature > 35:
            alerts.append("High Temperature - Cooling Required!")
        if latest_data.light_level < 100:
            alerts.append("Low Light Level - Check Lighting!")

    context = {
        'data': latest_data,
        'sensor_data': sensor_data,  # গ্রাফের জন্য
        'devices': devices,
        'watering_schedule': watering_schedule,
        'crop_health_status': crop_health_status,
        'alerts': alerts,
    }
    return render(request, 'dashboard.html', context)

@login_required
def analytics(request):
    latest_health = CropHealth.objects.latest('timestamp') if CropHealth.objects.exists() else None
    
    total_contents = EducationalContent.objects.count()
    total_views = sum(content.views for content in EducationalContent.objects.all())
    total_posts = ForumPost.objects.count()
    recent_contents = EducationalContent.objects.order_by('-created_at')[:5]
    
    # সেন্সর ডাটা অ্যানালিটিক্স
    sensor_data = SensorData.objects.all().order_by('-timestamp')[:50]
    avg_temp = sum(d.temperature for d in sensor_data) / len(sensor_data) if sensor_data else 0
    avg_humidity = sum(d.humidity for d in sensor_data) / len(sensor_data) if sensor_data else 0
    
    context = {
        'health': latest_health,
        'total_contents': total_contents,
        'total_views': total_views,
        'total_posts': total_posts,
        'recent_contents': recent_contents,
        'avg_temp': round(avg_temp, 2),
        'avg_humidity': round(avg_humidity, 2),
    }
    return render(request, 'analytics.html', context)

@login_required
def control(request):
    latest_data = SensorData.objects.latest('timestamp') if SensorData.objects.exists() else None
    devices = Device.objects.all()
    
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        action = request.POST.get('action')
        device = Device.objects.get(id=device_id)
        if action == 'turn_on':
            device.status = True
        elif action == 'turn_off':
            device.status = False
        device.save()
        return redirect('control')

    total_contents = EducationalContent.objects.count()
    total_views = sum(content.views for content in EducationalContent.objects.all())
    total_posts = ForumPost.objects.count()
    recent_contents = EducationalContent.objects.order_by('-created_at')[:5]
    
    context = {
        'latest_data': latest_data,
        'devices': devices,
        'total_contents': total_contents,
        'total_views': total_views,
        'total_posts': total_posts,
        'recent_contents': recent_contents,
    }
    return render(request, 'control.html', context)

def community(request):
    return render(request, 'community.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('community')


def community(request):
    sensor_data = SensorData.objects.all().order_by('-timestamp')[:5]
    educational_contents = EducationalContent.objects.all()
    forum_posts = ForumPost.objects.all().order_by('-created_at')
    
    context = {
        'sensor_data': sensor_data,
        'resources': educational_contents,
        'posts': forum_posts,
    }
    return render(request, 'community.html', context)