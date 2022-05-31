from django.shortcuts import render
from django.views.generic import ListView

from app.models.load.load import Load


class LoadListView(ListView):
    model = Load
