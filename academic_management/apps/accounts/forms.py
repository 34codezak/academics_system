# from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
# from .models import User

from django.contrib.auth import get_user_model, password_validation

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    """Registration form for custom User model"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control input-field',
            'placeholder': 'you@institution.edu'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control input-field', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control input-field', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control input-field', 'placeholder': 'Last name'}),
            # 'role': forms.Select(attrs={'class': 'form-select input-field'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control input-field', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control input-field', 'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, **kwargs):  # Accept *args, **kwargs
        super().__init__(*args, **kwargs)  # Pass them to parent
        # Apply Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['password1', 'password2']:  # Already styled via Meta.widgets
                field.widget.attrs.update({
                    'class': 'form-control input-field',
                    'placeholder': field.label or ''
                })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Login form with custom styling"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control input-field',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-field',
            'placeholder': 'Password'
        })
    )

"""# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Your Name"
        })
    )

    email = forms.CharField(
            widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Your Email"
        })
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Subject"
        })
    )

    message = forms.CharField(
            widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "Your Message",
            'rows': 5
        })
    )

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters or more.')
        return message
"""

# Password change form
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current Password'
        })
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        })
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2
    
# 


