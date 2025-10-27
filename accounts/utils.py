import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# def generate_otp():
#     """Return 6-digit OTP string."""
#     return f"{random.randint(100000, 999999):06d}"

# def send_otp_via_email(email, otp, subject="Your ARDAA Verification Code"):
#     """
#     Send OTP via Gmail SMTP with beautiful HTML design.
#     Returns True if successful, else False.
#     """
#     try:
#         # Context data for the template
#         context = {
#             'otp': otp,
#             'validity_minutes': 2,
#             'email': email,
#             'year': timezone.now().year,
# #             'subject': subject
# #         }
        
# #         # Render HTML and text versions
#         html_content = render_to_string('accounts/emails/otp_email.html', context)
#         text_content = render_to_string('accounts/emails/otp_email.txt', context)
        
#         # Create email message
#         email_msg = EmailMultiAlternatives(
#             subject=subject,
#             body=text_content,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[email],
#             reply_to=[getattr(settings, 'SUPPORT_EMAIL', settings.DEFAULT_FROM_EMAIL)]
#         )
#         email_msg.attach_alternative(html_content, "text/html")
        
#         # Send email
#         email_msg.send(fail_silently=False)
#         print(f"[INFO] OTP sent successfully to {email}")
#         return True
        
    # except Exception as e:
    #     print(f"[ERROR] Failed to send OTP to {email}. OTP: {otp}. Error: {e}")
    #     return False

def send_welcome_email(user):
    """
    Send welcome email to new user
    """
    subject = '🎉 Welcome to ARDAA - AI Resume Analyzer'
    
    # HTML content
    html_content = render_to_string('emails/welcome_email.html', {
        'user': user,
    })
    
    # Plain text content (fallback)
    text_content = f"""
    Welcome to ARDAA, {user.name}!

    Thank you for joining ARDAA - Your AI-powered Resume Analyzer!

    🚀 What you can do:
    - Analyze resumes with AI
    - Get ATS compatibility scores  
    - Receive improvement suggestions
    - Chat with ARDAA AI Assistant

    Get started: https://ai-resume-analyzer-debugger-builder.onrender.com/

    Best regards,
    The ARDAA Team
    """
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        print(f"✅ Welcome email sent to {user.email}")
        return True
    except Exception as e:
        print(f"❌ Welcome email failed: {e}")
        return False

# def otp_is_valid(otp_input, stored_otp, otp_created_at, validity_minutes=2):
#     """
#     Compare OTP strings and check expiry.
#     otp_created_at is a timezone-aware datetime or None
#     """
#     if not stored_otp or not otp_created_at:
#         return False
#     if str(otp_input).strip() != str(stored_otp).strip():
#         return False
#     now = timezone.now()
#     if now > otp_created_at + timezone.timedelta(minutes=validity_minutes):
#         return False

#     return True

