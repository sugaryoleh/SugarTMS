from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, TextField, AutoField, CharField, ManyToManyField, \
    TextChoices, BooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _


class Role(Model):

    class Department(TextChoices):
        DRM = 'DRM', _('Driver relationship management')
        SAFETY = 'SAFETY', _('Safety')
        OPERATIONS = 'OPERATIONS', _('Operations')
        SHOP = 'SHOP', _('Shop')
        ACCOUNTING = 'ACCOUNTING', _('Accounting')

    id = AutoField(primary_key=True)
    name = CharField(max_length=20, unique=True)
    department = CharField(max_length=10, choices=Department.choices)

    def __str__(self):
        return '{}/{}'.format(self.name, self.department)


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