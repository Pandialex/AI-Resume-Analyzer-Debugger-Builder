from django.db import models
from django.conf import settings

class ResumeAnalysis(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    resume_text = models.TextField(blank=True)
    job_description = models.TextField(blank=True)
    ats_score = models.IntegerField(null=True, blank=True)
    matched_keywords = models.JSONField(default=list, blank=True)
    missing_keywords = models.JSONField(default=list, blank=True)
    grammar_issues = models.JSONField(default=list, blank=True)
    ai_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name or 'Unknown'} - {self.created_at:%Y-%m-%d %H:%M}"

class UsageTraker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    tokens_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user or self.session_key} - {self.tokens_used}"
