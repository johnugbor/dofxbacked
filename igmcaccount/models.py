'''
This module handles all user accounts types:

- `super user` or overall admin.
'''
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save,post_delete


from igmcaccount.managers import CustomManager


class User(AbstractBaseUser, PermissionsMixin):

    ''' Custom user model '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=60, unique=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    full_name =models.TextField(max_length=500)
    currency = models.CharField(max_length=3)
    phone_number=models.CharField(max_length=14)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    
    REQUIRED_FIELDS = []


    def get_wallet(self):
        """ Returns the users wallet.
        """
        return self.wallet if hasattr(self, 'wallet') else None


    # def get_full_name(self):

    #     return self.full_name
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

# class Profile(models.Model):

#     class Currency(models.TextChoices):
#         CAD = 'C$',_('CAD')
#         USD = '$',_('USD')
#         AUD = 'A$',_('AUD')
#         GBP = '£',_('GBP')
#         EUR = '€',_('EURO')
#         CHF = 'CHF',_('CHF')

    
#     full_name =models.TextField(max_length=500)
#     currency = models.CharField(max_length=3,choices=Currency.choices,default='',)
#     phone_number=models.CharField(max_length=14)
#     user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')

# def create_profile(sender, instance, created, **kwargs):

#     if created:
#         Profile.objects.create(user=instance)
# post_save.connect(create_profile, sender=User)

# def delete_user(sender, instance=None,**kwargs):

#     try:
#         instance.user
#     except User.DoestNotExist:
#         pass
#     else:
#         instance.user.delete()
# post_delete.connect(delete_user, sender=Profile)




    
