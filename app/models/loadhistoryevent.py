import datetime as datetime
from django.db.models import Model, BigAutoField, DateTimeField, ForeignKey, CASCADE, CharField

from app.models.load import Load


class LoadHistoryEvent(Model):
    id = BigAutoField(primary_key=True)
    datetime = DateTimeField(default=datetime.datetime.now())
    load = ForeignKey(Load, on_delete=CASCADE)
    text = CharField(max_length=200)


class LoadHistoryEvents:
    @staticmethod
    def load_created(load):
        text = 'Load# {} created'.format(load.id)
        LoadHistoryEvent(load=load, text=text).save()

    @staticmethod
    def driver_assigned(load):
        text = 'Driver {}; Truck {} was assigned to the order.'.format(load.driver, load.driver.truck)
        LoadHistoryEvent(load=load, text=text).save()

    @staticmethod
    def driver_unassigned(load):
        text = 'Driver {}; Truck {} was unassigned from the order.'.format(load.driver, load.driver.truck)
        LoadHistoryEvent(load=load, text=text).save()

    @staticmethod
    def status_changed(load):
        text = 'Status changed to {}'.format(load.status)
        LoadHistoryEvent(load=load, text=text).save()

    @staticmethod
    def invoice_created(load):
        text = 'Invoice# {} generated'.format(load.id)
        LoadHistoryEvent(load=load, text=text).save()
