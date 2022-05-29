from django.contrib import admin

from app.models.accessorial import Accessorial
from app.models.address import State, Address
from app.models.driver import Driver
from app.models.facility import Facility
from app.models.files import DriverFile, Ticket, TrailerFile, TruckFile, LoadFile
from app.models.load import Load
from app.models.loadhistoryevent import LoadHistoryEvent
from app.models.loadstage import LoadStage
from app.models.parties import CarrierCompany, BrokerCompany
from app.models.units import TrailerMake, TrailerModel, TruckMake, TruckModel, Trailer, Truck
from app.models.profile import Profile, Role

admin.site.register(Profile)
admin.site.register(Role)


admin.site.register(State)
admin.site.register(Address)
admin.site.register(Facility)
admin.site.register(Driver)
admin.site.register(DriverFile)
admin.site.register(Ticket)
admin.site.register(TrailerFile)
admin.site.register(TruckFile)
admin.site.register(LoadFile)
admin.site.register(TrailerMake)
admin.site.register(TrailerModel)
admin.site.register(TruckMake)
admin.site.register(TruckModel)
admin.site.register(Trailer)
admin.site.register(Truck)

admin.site.register(CarrierCompany)
admin.site.register(BrokerCompany)

admin.site.register(Load)
admin.site.register(Accessorial)
admin.site.register(LoadStage)
admin.site.register(LoadHistoryEvent)


