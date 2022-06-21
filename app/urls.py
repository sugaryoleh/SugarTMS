import inflect
from django.urls import path

from app.views.users.profile_view import ProfileAdd, ProfileDetail, ProfileDelete, ProfileList

from app.views.location.state_view import StateAdd, StateDetail, StateDelete, StateList

from app.views.location.address_view import AddressAdd, AddressDetail, AddressDelete, AddressList

from app.views.location.facility_view import FacilityAdd, FacilityDetail, FacilityDelete, FacilityList

from app.views.unit.trailer.trailer_make_view import TrailerMakeAdd, TrailerMakeDetail, TrailerMakeDelete, \
    TrailerMakeList
from app.views.unit.trailer.trailer_model_view import TrailerModelAdd, TrailerModelDetail, TrailerModelDelete, \
    TrailerModelList
from app.views.unit.trailer.trailer_view import TrailerAdd, TrailerDetail, TrailerDelete, TrailerList
from app.views.unit.trailer.trailer_group_view import TrailerGroupAdd, TrailerGroupDetail, TrailerGroupDelete, \
    TrailerGroupList

from app.views.unit.truck.truck_make_view import TruckMakeAdd, TruckMakeDetail, TruckMakeDelete, TruckMakeList
from app.views.unit.truck.truck_model_view import TruckModelAdd, TruckModelDetail, TruckModelDelete, TruckModelList
from app.views.unit.truck.truck_view import TruckAdd, TruckDetail, TruckDelete, TruckList
from app.views.unit.truck.truck_group_view import TruckGroupAdd, TruckGroupDetail, TruckGroupDelete, TruckGroupList

from app.views.parties.brokercompany_view import BrokerCompanyAdd, BrokerCompanyDetail, BrokerCompanyDelete, \
    BrokerCompanyList
from app.views.parties.carriercompany_view import CarrierCompanyAdd, CarrierCompanyDetail, CarrierCompanyDelete, \
    CarrierCompanyList

from app.views.driver.driver_view import DriverAdd, DriverDetail, DriverDelete, DriverList

from app.views.load.load_view import LoadAddView, LoadListView, LoadDetailView, Dispatch
from app.views.load.loadstage_view import LoadStageListAddView
from app.views.index import index


def make_urls(host, url_fields, ):
    engine = inflect.engine()
    urlbase = host + '/{}'
    urls = {name: urlbase.format(url) for (name, url) in
            zip(url_fields, (engine.plural(name.replace(' ', '')) for name in url_fields))}
    return urls


profile_views = [ProfileAdd, ProfileDetail, ProfileDelete, ProfileList]
state_views = [StateAdd, StateDetail, StateDelete, StateList]
address_views = [AddressAdd, AddressDetail, AddressDelete, AddressList]
facility_views = [FacilityAdd, FacilityDetail, FacilityDelete, FacilityList]
trailer_make_views = [TrailerMakeAdd, TrailerMakeDetail, TrailerMakeDelete, TrailerMakeList]
trailer_model_views = [TrailerModelAdd, TrailerModelDetail, TrailerModelDelete, TrailerModelList]
trailer_views = [TrailerAdd, TrailerDetail, TrailerDelete, TrailerList]
trailer_group_views = [TrailerGroupAdd, TrailerGroupDetail, TrailerGroupDelete, TrailerGroupList]
truck_make_views = [TruckMakeAdd, TruckMakeDetail, TruckMakeDelete, TruckMakeList]
truck_model_views = [TruckModelAdd, TruckModelDetail, TruckModelDelete, TruckModelList]
truck_views = [TruckAdd, TruckDetail, TruckDelete, TruckList]
truck_group_views = [TruckGroupAdd, TruckGroupDetail, TruckGroupDelete, TruckGroupList]
broker_company_views = [BrokerCompanyAdd, BrokerCompanyDetail, BrokerCompanyDelete, BrokerCompanyList]
carrier_company_views = [CarrierCompanyAdd, CarrierCompanyDetail, CarrierCompanyDelete, CarrierCompanyList]
driver_views = [DriverAdd, DriverDetail, DriverDelete, DriverList]

all_views = [state_views, address_views, facility_views, trailer_make_views, trailer_model_views, trailer_views,
             trailer_group_views, truck_make_views, truck_model_views, truck_views, truck_group_views,
             broker_company_views, carrier_company_views, driver_views, profile_views]

urlpatterns = []

for views in all_views:
    name = views[0].model._meta.verbose_name_raw.replace(' ', '')
    plural_name = views[0].model._meta.verbose_name_plural.replace(' ', '')
    urlpatterns.append(path('{}/add/'.format(plural_name), views[0].as_view(), name='{}-add'.format(name)))
    urlpatterns.append(path('{}/<int:pk>/'.format(plural_name), views[1].as_view(), name='{}-detail'.format(name)))
    urlpatterns.append(path('{}/<int:pk>/delete'.format(plural_name), views[2].as_view(), name='{}-delete'.format(name)))
    urlpatterns.append(path('{}/'.format(plural_name), views[3].as_view(), name='{}-list'.format(name)))

urlpatterns.append(path('loads/add',  LoadAddView.as_view(), name='load-add'))
urlpatterns.append(path('loads/',  LoadListView.as_view(), name='load-list'))
urlpatterns.append(path('loads/<int:pk>',  LoadDetailView.as_view(), name='load-detail'))
urlpatterns.append(path('loads/<int:load>/stages',  LoadStageListAddView.as_view(), name='load-stages'))
urlpatterns.append(path('loads/<int:load>/dispatch',  Dispatch.as_view(), name='load-dispatch'))
urlpatterns.append(path('',  index, name='index'))
