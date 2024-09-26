from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

# Create your9 models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)
    about = models.TextField(blank=True)
    profile_picture = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')
    # mobile = models.CharField(
    #     max_length=15,  # Adjust length according to your needs
    #     null=True,
    #     validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid mobile number")]
    # )
    # mobile = models.BigIntegerField(null=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

class Tweet(models.Model):
    title = models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(max_length=1000)
    summary = models.TextField()
    # photo=models.ImageField(upload_to="myimage")
    # photo=models.ImageField(upload_to='tweets/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'
