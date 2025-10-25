from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import UsageTracker

User = get_user_model()


class UsageTrackerInline(admin.StackedInline):
    model = UsageTracker
    can_delete = False
    verbose_name_plural = 'Usage Tracker'
    fields = ('tokens_used', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 
        'name', 
        'phone', 
        'is_active', 
        'is_staff', 
        'is_superuser',
        'date_joined', 
        'last_login',
        'otp_status',
        'tokens_used',
        'password_status'
    )
    
    list_filter = (
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'date_joined',
    )
    
    search_fields = ('email', 'name', 'phone')
    
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'password_status_display')
        }),
        ('Personal Info', {
            'fields': ('name', 'phone')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('OTP Information', {
            'fields': ('otp', 'otp_created_at', 'otp_expiry_status'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = (
        'last_login', 
        'date_joined', 
        'password_status_display',
        'otp_expiry_status'
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2'),
        }),
    )
    
    inlines = [UsageTrackerInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('usagetracker_set')
    
    def otp_status(self, obj):
        if obj.otp and obj.otp_created_at:
            now = timezone.now()
            time_diff = now - obj.otp_created_at
            if time_diff.total_seconds() < 120:  # 2 minutes validity
                return format_html(
                    '<span style="color: orange; font-weight: bold;">Active</span>'
                )
            else:
                return format_html(
                    '<span style="color: red; font-weight: bold;">Expired</span>'
                )
        return format_html('<span style="color: green;">No OTP</span>')
    
    otp_status.short_description = 'OTP Status'
    
    def tokens_used(self, obj):
        try:
            tracker = obj.usagetracker_set.first()
            return tracker.tokens_used if tracker else 0
        except UsageTracker.DoesNotExist:
            return 0
    
    tokens_used.short_description = 'Tokens Used'
    
    def password_status(self, obj):
        if obj.has_usable_password():
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Set</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Not Set</span>'
        )
    
    password_status.short_description = 'Password'
    
    def password_status_display(self, obj):
        return self.password_status(obj)
    
    password_status_display.short_description = 'Password Status'
    
    def otp_expiry_status(self, obj):
        if obj.otp and obj.otp_created_at:
            now = timezone.now()
            time_diff = now - obj.otp_created_at
            minutes_ago = int(time_diff.total_seconds() / 60)
            if minutes_ago < 2:
                return f"Active ({minutes_ago}m ago)"
            else:
                return f"Expired ({minutes_minutes_ago}m ago)"
        return "No OTP"
    
    otp_expiry_status.short_description = 'OTP Expiry Status'
    
    def get_readonly_fields(self, request, obj=None):
        # Make email readonly when editing existing object
        if obj:
            return self.readonly_fields + ('email',)
        return self.readonly_fields
    
    actions = ['activate_users', 'deactivate_users', 'reset_passwords']
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated successfully.')
    
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated successfully.')
    
    deactivate_users.short_description = "Deactivate selected users"
    
    def reset_passwords(self, request, queryset):
        for user in queryset:
            # In a real scenario, you might want to send password reset emails
            # For now, we'll just set a temporary password
            user.set_password('temp123')
            user.save()
        self.message_user(request, f'{queryset.count()} user passwords reset to "temp123".')
    
    reset_passwords.short_description = "Reset passwords for selected users"


@admin.register(UsageTracker)
class UsageTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'tokens_used', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'tokens_used')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )