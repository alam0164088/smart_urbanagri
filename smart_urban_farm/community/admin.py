from django.contrib import admin
from .models import EducationalContent, ForumPost

@admin.register(EducationalContent)
class EducationalContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'url')  # লিস্টে দেখানোর জন্য
    fields = ('title', 'description', 'file', 'url')  # এডিটযোগ্য ফিল্ড
    # readonly_fields = ('created_at',)  # ঐচ্ছিক: শুধু দেখার জন্য

admin.site.register(ForumPost)