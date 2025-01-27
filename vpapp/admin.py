from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'video_file', 'upload_date', 'uploaded_by')
    search_fields = ('title',)
