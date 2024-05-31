from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver(post_save, sender=Profesor)
# def create_user_for_profesor(sender, instance, created, **kwargs):
#     if created:
#         email = instance.email
#         username = email.split('@')[0]
#         telefono = instance.telefono

#         user, user_created = User.objects.get_or_create(
#             username=username,
#             defaults={
#                 'email': email,
#                 'first_name': instance.apellidos_nombres.split(' ')[0],
#                 'last_name': ' '.join(instance.apellidos_nombres.split(' ')[1:]),
#                 'is_staff': True,
#                 'is_active': True,
#             }
#         )
#         if user_created:
#             user.set_password(telefono)
#             user.save()
#             Profile.objects.create(user=user, rol='P')
#         instance.user = user
#         instance.save()