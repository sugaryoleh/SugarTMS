from django.db.models import Model, AutoField, CharField


class State(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    code = CharField(max_length=3)

    class Meta:
        unique_together = ('name', 'code')

    def __str__(self):
        return '{}'.format(self.code)