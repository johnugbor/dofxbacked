from allauth.account.signals import user_signed_up
from django.core.mail import mail_admins, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from igmcaccount.models import User
from .models import Wallet


# # binding signal:
@receiver(post_save, sender=Wallet)
def send_mail_to_admin(sender, instance, created, **kwargs):
    # Send a copy via gmail to admin
    withraw_sender = User.objects.get(id=instance.user_id)
    email_subject = 'Withdrawal request from ' + withraw_sender.email
    email_body = withraw_sender.email + ' has placed a withdrawal request'

    from_email = 'mrjohnugbor@gmail.com'
    to_emails = ['mrjohnugbor@gmail.com']
    print("email  sent")
    send_mail(
        email_subject,
        email_body,
        from_email,
        to_emails,

        fail_silently=False
    )


# @receiver(user_signed_up, sender=User)
# def create_wallet_for_user(sender, instance, created, **kwargs):
#     wi = User.objects.get(id=instance.id)
#     Wallet.objects.create(user=wi)
# @receiver(user_signed_up)
# def after_user_signed_up(sender, request, user):
#     print(user)
#     wi = user.id
#     Wallet.objects.create(user=wi)


