from django.db.models import BigAutoField, BooleanField, Model, ForeignKey, CASCADE, PositiveSmallIntegerField, \
    DateTimeField, RESTRICT, TextField

from app.models.load.load import Load
from app.models.location.facility import Facility


class LoadStage(Model):
    id = BigAutoField(primary_key=True)
    type = BooleanField(default=False)
    load = ForeignKey(Load, on_delete=CASCADE)
    order_number = PositiveSmallIntegerField()
    time_from = DateTimeField()
    time_to = DateTimeField()
    actual_time_from = DateTimeField(null=True, blank=True)
    actual_time_to = DateTimeField(null=True, blank=True)
    facility = ForeignKey(Facility, on_delete=RESTRICT)
    note = TextField(max_length=50, null=True, blank=True)

    types = {
        True: 'Pick-up',
        False: 'Delivery'
    }

    class Meta:
        unique_together = [['load', 'order_number', 'type'], ]

    def save(self, *args, **kwargs):

        if self.time_from >= self.time_to:
            raise Exception('Time to cannot be earlier than time from')
        super(LoadStage, self).save(*args, **kwargs)

    def check_if_correct_order(self):
        stages = LoadStage.objects.filter(load=self.id).filter(type=self.type)
        if stages.exists():
            return all(self.order_number != s.order_number for s in stages)

    def __str__(self):
        return 'Order# {}|Stage# {}|{}|Facility: {}'.format(self.load.order_number, self.order_number,
                                                            self.types[self.type], self.facility)

    class LoadStageManager:

        @staticmethod
        def get_next_stage_order(load_stage, type=True):
            existing_stages = Load.LoadManager.get_load_stages(Load.objects.get(pk=load_stage.load.id), type=type)
            if not existing_stages:
                return 1
            else:
                last_stage = existing_stages[0]
                return last_stage.order_number + 1

        @staticmethod
        def clean_stage(load_stage):
            load_stage.actual_time_in = None
            load_stage.actual_time_in = None
            load_stage.save()

