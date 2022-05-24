from django.contrib import admin

from app.models.address import State, Address
from app.models.driver import Driver
from app.models.files import DriverFile, Ticket, TrailerFile, TruckFile
from app.models.parties import CarrierCompany
from app.models.units import TrailerMake, TrailerModel, TruckMake, TruckModel, Trailer, Truck
from app.models.profile import Profile, Role

admin.site.register(State)
admin.site.register(Address)
admin.site.register(Driver)
admin.site.register(DriverFile)
admin.site.register(Ticket)
admin.site.register(TrailerFile)
admin.site.register(TruckFile)
admin.site.register(TrailerMake)
admin.site.register(TrailerModel)
admin.site.register(TruckMake)
admin.site.register(TruckModel)
admin.site.register(Trailer)
admin.site.register(Truck)
admin.site.register(Role)
admin.site.register(Profile)

admin.site.register(CarrierCompany)

