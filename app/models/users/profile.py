from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, ManyToManyField, BooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models.users.role import Role


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    roles = ManyToManyField(Role)
    is_coordinator = BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
