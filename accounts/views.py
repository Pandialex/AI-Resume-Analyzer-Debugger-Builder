from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.urls import reverse

from .forms import UserRegisterForm, UserLoginForm, ForgetPasswordForm, ResetPasswordForm
from .utils import generate_otp, send_otp_via_email, otp_is_valid
from .models import UsageTracker

User = get_user_model()


# ---------- AJAX: send OTP for registration OR password reset ----------
def send_otp_ajax(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

    email = request.POST.get("email")
    if not email:
        return JsonResponse({"status": "error", "message": "Email required"}, status=400)

    otp = generate_otp()
    try:
        request.session['otp_for_email'] = email
        request.session['otp_value'] = otp
        request.session['otp_created_at'] = timezone.now().isoformat()

        user = User.objects.filter(email=email).first()
        if user:
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save(update_fields=['otp', 'otp_created_at'])

        sent = send_otp_via_email(email, otp)

        # ✅ Enforce Email Only
        if not sent:
            return JsonResponse({"status": "error", "message": "Failed to send OTP. Check SMTP settings."}, status=500)

        return JsonResponse({"status": "success", "message": "OTP sent to your email."})

    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Failed to generate/send OTP: {e}"}, status=500)


# ---------------- Register ----------------
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "accounts/register.html", {"form": form, "error": "Form invalid"})

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data['password']
        otp_input = form.cleaned_data.get('otp')

        session_otp = request.session.get('otp_value')
        otp_time_str = request.session.get('otp_created_at')
        otp_time = parse_datetime(otp_time_str) if otp_time_str else None

        user_obj = User.objects.filter(email=email).first()
        if user_obj and user_obj.is_active:
            return render(request, "accounts/register.html", {"form": form, "error": "Email already in use."})

        stored_otp = session_otp
        stored_otp_time = otp_time
        if user_obj and user_obj.otp and user_obj.otp_created_at:
            stored_otp = user_obj.otp
            stored_otp_time = user_obj.otp_created_at

        if not otp_is_valid(otp_input, stored_otp, stored_otp_time, validity_minutes=2):
            return render(request, "accounts/register.html", {"form": form, "error": "Invalid or expired OTP."})

        user = User.objects.create_user(email=email, name=name, phone=phone, password=password)
        user.is_active = True
        user.otp = None
        user.otp_created_at = None
        user.save(update_fields=['is_active', 'otp', 'otp_created_at'])

        UsageTracker.objects.create(user=user, tokens_used=5)

        for k in ['otp_value', 'otp_created_at', 'otp_for_email']:
            request.session.pop(k, None)

        messages.success(request, "Account created! Please log in.")
        return redirect("accounts:login")

    form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# ---------------- Login ----------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("ARDAA:index")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next")
            return redirect(next_url or "ARDAA:index")
        return render(request, "accounts/login.html", {"form": form, "error": "Invalid credentials"})

    form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


# ---------------- Logout ----------------
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


# ---------------- Forget Password request - send OTP ----------------
def forget_password_request(request):
    if request.method == "POST":
        form = ForgetPasswordForm(request.POST)
        if not form.is_valid():
            return render(request, "accounts/forget_password_request.html", {"form": form, "error": "Enter valid email"})

        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, "accounts/forget_password_request.html", {"form": form, "error": "Email not registered"})

        otp = generate_otp()
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save(update_fields=['otp', 'otp_created_at'])

        send_otp_via_email(email, otp, subject="ARDAA Password Reset OTP")

        request.session['fp_user_id'] = user.id
        request.session['fp_otp'] = otp
        request.session['fp_otp_created_at'] = timezone.now().isoformat()

        return redirect("accounts:forget_password_verify", user_id=user.id)

    form = ForgetPasswordForm()
    return render(request, "accounts/forget_password_request.html", {"form": form})


# ---------------- Forget Password Verify & Reset ----------------
def forget_password_verify(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect("accounts:forget_password_request")

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if not form.is_valid():
            return render(request, "accounts/forget_password_verify.html", {"form": form, "error": "Form invalid", "user": user})

        otp_input = form.cleaned_data.get("otp")
        new_password = form.cleaned_data.get("new_password")

        session_otp = request.session.get('fp_otp')
        otp_time_str = request.session.get('fp_otp_created_at')
        otp_time = parse_datetime(otp_time_str) if otp_time_str else None

        stored_otp = user.otp or session_otp
        stored_otp_time = user.otp_created_at or otp_time

        if not otp_is_valid(otp_input, stored_otp, stored_otp_time, validity_minutes=2):
            return render(request, "accounts/forget_password_verify.html", {"form": form, "error": "Invalid or expired OTP", "user": user})

        user.set_password(new_password)
        user.otp = None
        user.otp_created_at = None
        user.save()

        for k in ['fp_otp', 'fp_otp_created_at', 'fp_user_id']:
            request.session.pop(k, None)

        messages.success(request, "Password reset successfully. Please login.")
        return redirect("accounts:login")

    form = ResetPasswordForm()
    return render(request, "accounts/forget_password_verify.html", {"form": form, "user": user})


# ---------------- Profile ----------------
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    full_name = (user.name or "").strip()
    name_parts = full_name.split()
    first_name = " ".join(name_parts[:-1]) if len(name_parts) > 1 else full_name
    last_name = name_parts[-1] if len(name_parts) > 1 else ""

    return render(request, "accounts/profile.html", {"user": user, "first_name": first_name, "last_name": last_name})


# ---------------- Check resume access ----------------
from django.http import JsonResponse as JsonResp

def check_resume_access(request):
    if request.user.is_authenticated:
        tracker, created = UsageTracker.objects.get_or_create(user=request.user)
        return JsonResp({"allowed": True})
    else:
        if request.session.get("first_free_analysis_done", False):
            return JsonResp({"allowed": False, "redirect_url": "/accounts/register/"})
        request.session["first_free_analysis_done"] = True
        return JsonResp({"allowed": True})
