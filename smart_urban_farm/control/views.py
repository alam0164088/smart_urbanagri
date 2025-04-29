from django.shortcuts import render

def control(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'irrigate':
            # Placeholder for IoT command
            print("Irrigation started!")
    return render(request, 'control.html')