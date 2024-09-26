from django import forms
from .models import Tweet,Profile
from django.contrib.auth.models import User

class  TweetForm(forms.ModelForm):
    class Meta:
        model=Tweet
        fields=['title','text','summary']


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}),
        label="Old Password",
        max_length=100
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label="New Password",
        max_length=100
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        label="Confirm New Password",
        max_length=100
    )

    # Validate that new password and confirm password match
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password do not match.")

        return cleaned_data



#contact forms
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        label='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        label='Your Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message'}),
        label='Your Message'
    )



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'profile_picture']  # Assuming you have these fields in your Profile model