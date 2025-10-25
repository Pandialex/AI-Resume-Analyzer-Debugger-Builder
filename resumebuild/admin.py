# resumebuild/admin.py

from django.contrib import admin
from .models import ResumeTemplate

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'is_active', 'created_at')
    list_filter = ('template_type', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'template_type', 'is_active')
        }),
        ('Files', {
            'fields': ('preview_image', 'html_file', 'css_file'),
            'description': "Upload the preview image, and the HTML/CSS files for the template. The HTML file should use Django template tags like `{{ data.full_name }}`."
        }),
    )