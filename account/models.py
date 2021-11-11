from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from api.vonage_api import VonageApi


class AccountManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            full_name=full_name,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, full_name, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Account(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Phone Number', unique=True, max_length=60)
    email = models.CharField(max_length=255, default=None)
    full_name = models.CharField(max_length=60, default=None)
    profile_image = models.ImageField(
        upload_to='files/profile_image', blank=True)
    account_type = models.IntegerField(
        default=0, help_text='0=normal user; 1=store owner;2=rider;')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    otp = reset_password_token.key
    msg = 'Your OTP is ' + otp
    smsStatus = VonageApi().sendMessage(
        reset_password_token.user.username, msg)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="E-TimerShop PH"),
        # message:
        "OTP: " + otp + "\nSMS:" + smsStatus,
        # from:
        "noreply@stephenwenceslao.com",
    )
