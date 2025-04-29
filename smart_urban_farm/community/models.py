from django.db import models

class EducationalContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)  # নতুন ফিল্ড যোগ করা

    def __str__(self):
        return self.title

class ForumPost(models.Model):
    user = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.created_at}"
    

class Reply(models.Model):
    post = models.ForeignKey(ForumPost, related_name='replies', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} replied to {self.post}"