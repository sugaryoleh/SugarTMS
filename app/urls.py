from django.urls import path

from app.views.location.address_view import AddressAdd, AddressDetail, AddressDelete, AddressList
from app.views.location.state_view import StateDetail, StateDelete, StateAdd, StateList

urlpatterns = [
    path('states/add/', StateAdd.as_view(), name='state-add'),
    path('states/<int:pk>/', StateDetail.as_view(), name='state-detail'),
    path('states/<int:pk>/delete', StateDelete.as_view(), name='state-delete'),
    path('states/', StateList.as_view(), name='state-list'),

    path('addresses/add/', AddressAdd.as_view(), name='address-add'),
    path('addresses/<int:pk>/', AddressDetail.as_view(), name='address-detail'),
    path('addresses/<int:pk>/delete', AddressDelete.as_view(), name='address-delete'),
    path('addresses/', AddressList.as_view(), name='address-list'),
]