# resumebuild/models.py

from django.db import models
from django.urls import reverse

def get_template_html_path(instance, filename):
    return f"resume_templates/{instance.slug}/index.html"

def get_template_css_path(instance, filename):
    return f"resume_templates/{instance.slug}/style.css"

def get_template_preview_path(instance, filename):
    return f"template_previews/{instance.slug}/{filename}"

class ResumeTemplate(models.Model):
    # --- Added template_type for your frontend logic ---
    TYPE_EXPERIENCED = 'experienced'
    TYPE_FRESHER = 'fresher'
    TEMPLATE_TYPES = [
        (TYPE_EXPERIENCED, 'Experienced Professional'),
        (TYPE_FRESHER, 'Fresher/Student'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    template_type = models.CharField(
        max_length=20, 
        choices=TEMPLATE_TYPES, 
        default=TYPE_EXPERIENCED,
        help_text="Determines which form sections are shown."
    )
    
    # --- Added preview_image for the carousel ---
    preview_image = models.ImageField(
        upload_to=get_template_preview_path, 
        help_text="Image shown in the template selection carousel."
    )
    
    html_file = models.FileField(upload_to=get_template_html_path)
    css_file = models.FileField(upload_to=get_template_css_path, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resume Template"
        verbose_name_plural = "Resume Templates"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)