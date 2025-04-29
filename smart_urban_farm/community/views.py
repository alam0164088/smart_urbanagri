from django.shortcuts import render, redirect
from .models import EducationalContent, ForumPost

def community(request):
    resources = EducationalContent.objects.all()
    posts = ForumPost.objects.all()
    if request.method == 'POST':
        user = request.POST.get('user')
        content = request.POST.get('content')
        if user and content:
            ForumPost.objects.create(user=user, content=content)
            return redirect('community')
    return render(request, 'community.html', {'resources': resources, 'posts': posts})