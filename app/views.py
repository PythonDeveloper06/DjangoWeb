"""
Definition of views.
"""

from datetime import datetime
import asyncio

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse_lazy
from django import forms
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async

from .forms import AddDeviceModel
from .utils import new_code, DeviceMixin
from .models import DeviceModel
from django.views.generic import DetailView, UpdateView, DeleteView


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


class DeviceDetailView(DetailView):
    model = DeviceModel
    template_name = 'app/your_device.html'
    context_object_name = 'data'


class DeviceUpdateView(DeviceMixin, UpdateView):
    model = DeviceModel
    template_name = 'app/update_form.html'
    form_class = AddDeviceModel
    view_is_async = True

    async def get(self, request, *args, **kwargs):
        device_lock = await self.model.objects.aget(id=self.kwargs['pk'])
        form = self.get_async_form(device_lock)
        return await sync_to_async(render)(request, 'app/update_form.html', {'title':'Update your device', 'form': form, 'year': datetime.now().year})


    async def post(self, request, *args, **kwargs):
        device_lock = await self.model.objects.aget(id=self.kwargs['pk'])
        if 'update_something' in request.POST:
            form = self.form_class(request.POST)
            if form.is_valid():
                device_lock.device_name = request.POST['device_name']
                device_lock.serial_num = request.POST['serial_num']
                device_lock.auth_key = request.POST['auth_key']
                device_lock.status = request.POST['status']
                await sync_to_async(device_lock.save)()
                return await sync_to_async(redirect)(device_lock.get_absolute_url())
        elif 'code' in request.POST:
            device_lock.auth_key = new_code()
            form = self.get_async_form(device_lock)
            return await sync_to_async(render)(request, 'app/update_form.html', {'title':'Update your device', 'form': form, 'year': datetime.now().year})
    
    

class DeviceDeleteView(DeleteView):
    model = DeviceModel
    template_name = 'app/delete_form.html'
    success_url = reverse_lazy('devices')
    context_object_name = 'data'
    

async def devices(request):
    """Renders the about page."""
    if request.method == 'POST':
        form = AddDeviceModel(request.POST)
        if form.is_valid():
            if not await DeviceModel.objects.filter(device_name=form.cleaned_data['device_name']).aexists():
                await sync_to_async(form.save)()
    form = AddDeviceModel()
    devices_numbers = await sync_to_async(DeviceModel.objects.filter)(user=request.user)

    paginator = await sync_to_async(Paginator)(devices_numbers, 3)
    page_number = await sync_to_async(request.GET.get)('page')
    page_obj = await sync_to_async(paginator.get_page)(page_number)

    return await sync_to_async(render)(
        request,
        'app/devices.html',
        {
            'title':'Your devices',
            'form': form,
            'year': datetime.now().year,
            'page_new': page_obj
        }
    )