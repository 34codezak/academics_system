from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
# from .models import User
from django.contrib.auth import get_user_model

User = get_user_model() # This now references your custom User

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate until email is verified
            user.save()

            # Send verification email
            send_verification_email(request, user)

            messages.success(
                request,
                'Registration successful! Please check you email to verify your account.'
            )
            return redirect('login')
        
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = CustomUserCreationForm()
    
    return render(request, 'login.html', {'form': form})

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Email verified! You are now logged in.')
        return redirect('home')
    
    else:
        messages.error(request, 'Verification link is invalid or has expired.')
        return redirect('register')
    

@login_required
def resend_verification(request):
    if request.user.is_active:
        messages.info(request, 'Your account is already verified.')
        return redirect('home')
    
    send_verification_email(request, request.user)
    messages.success(request, 'Verification email sent! Please check your inbox.')
    return redirect('home')

def send_verification_email(request, user):
    uid= urlsafe_base64_decode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verification_link = request.build_absolute_url(
        f'/accounts/verify/{uid}/{token}/'
    )

    subject = "Verify Your Email Address"
    message = f'''
        Hello {user.username},

        Please click the link below to verify your email address:
        {verification_link}

        This link will expire in 24 hours.vars

        If you did not create an account please ignore this email.vars
        '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')

            # Redirect to next page or default
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

@login_required
def home_view(request):
    return render(request, 'templates/home.html')

def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect(request, 'login.html')
