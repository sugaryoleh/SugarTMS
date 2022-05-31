from django.db.models import BooleanField

from app.models.parties.logisticscompany import LogisticsCompany


class CarrierCompany(LogisticsCompany):
    is_main = BooleanField(default=False)

    def just_created(self):
        return not CarrierCompany.objects.filter(pk=self.pk).exists()

    def is_main_changed(self):
        if not self.just_created():
            return self.is_main != CarrierCompany.objects.get(pk=self.id).is_main

    @staticmethod
    def is_first():
        return not CarrierCompany.objects.all().exists()

    def save(self, *args, **kwargs):
        if self.is_first() and not self.is_main:
            raise Exception(_('The main Carrier Company must be created first'))
        elif (self.is_main and self.just_created()) or self.is_main_changed():
            raise Exception(_('The main Carrier Company must be set once'))
        super(LogisticsCompany, self).save(args, kwargs)
