from django.apps import AppConfig

class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'

    def ready(self):
        from .models import EducationalContent, ForumPost
        print("Community app is ready!")