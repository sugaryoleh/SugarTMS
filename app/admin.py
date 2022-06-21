from django.contrib import admin

from app.models.driver.driver import Driver
from app.models.driver.driverfile import DriverFile
from app.models.driver.ticket import Ticket
from app.models.load.accessorial import Accessorial
from app.models.load.load import Load
from app.models.load.loadfile import LoadFile
from app.models.load.loadhistoryevent import LoadHistoryEvent
from app.models.load.loadstage import LoadStage
from app.models.location.address import Address
from app.models.location.facility import Facility
from app.models.location.state import State
from app.models.parties.brokercompany import BrokerCompany
from app.models.parties.carriercompany import CarrierCompany
from app.models.unit.trailer import Trailer, TrailerModel, TrailerMake
from app.models.unit.trailerfile import TrailerFile
from app.models.unit.truck import Truck, TruckModel, TruckMake
from app.models.unit.truckfile import TruckFile
from app.models.users.profile import Profile
from app.models.users.role import Role

admin.site.register(Profile)
admin.site.register(Role)


admin.site.register(Driver)
admin.site.register(DriverFile)
admin.site.register(Ticket)


admin.site.register(Load)
admin.site.register(Accessorial)
admin.site.register(LoadStage)
admin.site.register(LoadHistoryEvent)
admin.site.register(LoadFile)


admin.site.register(State)
admin.site.register(Address)
admin.site.register(Facility)


admin.site.register(CarrierCompany)
admin.site.register(BrokerCompany)


admin.site.register(Truck)
admin.site.register(TruckModel)
admin.site.register(TruckMake)
admin.site.register(TruckFile)

admin.site.register(Trailer)
admin.site.register(TrailerModel)
admin.site.register(TrailerMake)
admin.site.register(TrailerFile)
