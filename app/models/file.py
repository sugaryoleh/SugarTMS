from django.db.models import Model, AutoField, CharField, FileField, ForeignKey, SET_NULL

from app.models.file_router import route
from app.models.users.profile import Profile


class File(Model):
    id = AutoField(primary_key=True)
    file = FileField(upload_to=route)
    notes = CharField(max_length=20, null=True, blank=True)
    added_by = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=True)









