from django.db.models import Model, TextChoices, AutoField, CharField, PositiveSmallIntegerField, ForeignKey, CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _

from app.models.load import Load
from app.models.loadhistoryevent import LoadHistoryEvent


class Accessorial(Model):
    class AccessorialReason(TextChoices):
        DETENTION = 'DETENTION', _('Detention')
        LAYOVER = 'LAYOVER', _('Layover')
        EXTRA_MILES = 'EXTRA MILES', _('Extra miles')

    id = AutoField(primary_key=True)
    reason = CharField(max_length=11, choices=AccessorialReason.choices)
    amount = PositiveSmallIntegerField()
    load = ForeignKey(Load, on_delete=CASCADE)


@receiver(post_save, sender=Accessorial)
def add_to_load_total(sender, instance, **kwargs):
    load = Load.objects.get(pk=instance.load.id)
    load.total += instance.amount
    load.save()


@receiver(post_save, sender=Accessorial)
def write_to_load_history(sender, instance, created, **kwargs):
    if created:
        text = 'Accessorial {} for order {} created'.format(instance.reason, instance.load)
        event = LoadHistoryEvent(load=instance.load, text=text)
        event.save()
