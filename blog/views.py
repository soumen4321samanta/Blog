from django.contrib.auth import authenticate,login,logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from .forms import CustomPasswordChangeForm,ContactForm
from .forms import UserUpdateForm, ProfileUpdateForm


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.decorators import login_required

from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404





# Create your views here.
def home(request):
    tweets = Tweet.objects.all()
    return render(request, 'blog/home.html', {'tweets': tweets})



# def tweet_list(request):
#     form=TweetForm()
#     tweets=Tweet.objects.all().order_by('-created_at')
#     return render(request,'home.html',{'twee':tweets,'form':form})

@login_required
def tweet_list(request):
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'blog/tweet_list.html', {'twee': tweets})


@login_required(login_url='signin')
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')  # Redirect to the tweet list or another view
    else:
        form = TweetForm()
    
    return render(request, 'blog/tweet_create.html', {'form': form})



def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)
    return render(request,'blog/tweet_create.html',{'form':form})


    


def tweet_delete(request, tweet_id):
    # Ensure that the tweet belongs to the logged-in user
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    
    # Only delete if the request method is POST
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    
    # Render the confirmation page if it's not a POST request
    return render(request, 'blog/tweet_con_delete.html', {'tweet': tweet})







def signup(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        # mobile = request.POST['mobile']
        password = request.POST['pass1']

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        # # Validate the mobile number
        # if len(mobile) != 10 or not mobile.isdigit():
        #     messages.error(request, 'Invalid mobile number')
        #     return redirect('signup')

        # Create new user
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password, 
            first_name=fullname,
        )
        user.save()

        # Generate a token
        auth_token = str(uuid.uuid4())  # Initialize outside of any conditional blocks

        # Check if a profile already exists for this user
        if not Profile.objects.filter(user=user).exists():
            profile = Profile.objects.create(
                user=user, 
                auth_token=auth_token, 
                # mobile=mobile  # Assuming you have a `mobile` field in your Profile model
            )
            profile.save()
        else:
            # This ensures that auth_token is always assigned
            profile = Profile.objects.get(user=user)
            profile.auth_token = auth_token  # Assign a new token or use an old one
            profile.save()

        # Send verification email with auth_token
        send_mail_after_registration(email, auth_token)

        return redirect('token_send')

    return render(request, 'blog/signup.html')





def signin(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists in the database
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, "User not found")
            return redirect('signin')
        
        # Check if the user's profile is verified
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if profile_obj is None or not profile_obj.is_verified:
            messages.error(request, "Profile is not verified. Please check your mail.")
            return redirect('signin')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('signin')

    return render(request, "blog/signin.html")




def signout(request):
    # Check if the user is an admin (superuser)
    if request.user.is_superuser:
        # If the user is admin, don't flush the session, just log them out
        messages.success(request, "Admin successfully logged out.")
        auth_logout(request)
        return redirect('home')  # Redirect admin to the admin index page
    else:
        # For normal users, log them out and flush the session
        auth_logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('home')





def success(request):
    return render(request,'blog/success.html')




def token_send(request):
    return render(request,'blog/token_send.html')



def send_mail_after_registration(email,auth_token):
    subject="Account Activation"
    message=f"Hi press the link to verified account http://127.0.0.1:8000/verify/{auth_token}/"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)




def verify(request, auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,"your account has been all ready verified")
                return redirect('signin')

            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,"your account has been verified")
            return redirect('signin')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)




def error(request):
    return render(request,'blog/error.html')




def request_reset_password(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
            send_reset_password_email(user.email, reset_link)
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('signin')
        else:
            messages.error(request, "Email address not found.")
            return redirect('request_reset_password')

    return render(request, 'blog/request_reset_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect('signin')
            else:
                messages.error(request, "Passwords do not match.")
                return redirect(f'reset_password', uidb64=uidb64, token=token)

        return render(request, 'blog/reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "Password reset link is invalid or has expired.")
        return redirect('request_reset_password')


def send_reset_password_email(email, reset_link):
    subject = "Password Reset Request"
    message = f"Hi,\n\nTo reset your password, click the link below:\n\n{reset_link}\n\nIf you did not request a password reset, please ignore this email."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@login_required(login_url='signin')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Construct email subject and message
            subject = f"New Contact Form Submission from {name}"
            message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Send email using send_mail
            send_mail(
                subject,  # Subject
                message_body,  # Message body
                email,  # From email (user's email)
                [settings.ADMIN_EMAIL],  # To email (your admin email)
            )

            # After sending the admin email, you can also send an email to the user
            send_mail(
                "Thank you for contacting us",
                "Hi {},\n\nThank you for reaching out. We will get back to you soon.".format(name),
                settings.DEFAULT_FROM_EMAIL,  # Your site email
                [email],  # Send back to user's email
            )

            # Optional: Display a success message or redirect
            return render(request, 'blog/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})

def about(request):
    return render(request, 'blog/about.html')





def custom_change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')

            # Check if the old password is correct
            user = authenticate(username=request.user.username, password=old_password)
            if user is not None:
                # Change the user's password
                request.user.set_password(new_password)
                request.user.save()

                # Update the session to avoid logging out the user
                update_session_auth_hash(request, request.user)

                messages.success(request, "Password has been changed successfully.")
                return redirect('home')
            else:
                messages.error(request, "Old password is incorrect.")
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'blog/change_password.html', {'form': form})






@login_required
def user_dashboard(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-dashboard')  # Redirect to prevent form resubmission
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/user_dashboard.html', context)


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile  # Assuming you have a related Profile model linked to User

    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'blog/profile.html', context)