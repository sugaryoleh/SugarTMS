from django.db.models import CASCADE, ForeignKey

from app.models.driver.driver import Driver
from app.models.file import File


class DriverFile(File):
    driver = ForeignKey(Driver, on_delete=CASCADE)
