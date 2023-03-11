"""
Definition of views.
"""

from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse_lazy
from django import forms
from .forms import AddDeviceModel, new_code
from .models import DeviceModel
from django.views.generic import DetailView, UpdateView, DeleteView

NUMBERS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')


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

 
class DeviceUpdateView(UpdateView):
    model = DeviceModel
    template_name = 'app/update_form.html'

    form_class = AddDeviceModel

    def post(self, request, *args, **kwargs):
        device_lock = DeviceModel.objects.get(id=self.kwargs['pk'])
        if 'update_something' in request.POST:
            form = self.form_class(request.POST)
            if form.is_valid():
                return super().post(request, *args, **kwargs)
        elif 'code' in request.POST:
            device_lock.auth_key = new_code()
            form = self.form_class(initial=
                                   {
                                       'device_name': device_lock.device_name, 
                                       'serial_num': device_lock.serial_num, 
                                       'auth_key': device_lock.auth_key,
                                       'status': device_lock.status
                                   })
            form.fields['serial_num'].widget.attrs['readonly'] = True
            return render(request, 'app/update_form.html', {'title':'Update your device', 'form': form, 'year': datetime.now().year})



class DeviceDeleteView(DeleteView):
    model = DeviceModel
    template_name = 'app/delete_form.html'
    success_url = reverse_lazy('devices')

    context_object_name = 'data'


def devices(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AddDeviceModel(request.POST)
        if form.is_valid():
            cleaned_info = form.cleaned_data
            print(cleaned_info)
            if not DeviceModel.objects.filter(device_name=cleaned_info['device_name']).exists():
                form.save()
    form = AddDeviceModel()
    devices_numbers = DeviceModel.objects.filter(user=request.user)
    return render(
        request,
        'app/devices.html',
        {
            'title':'Your devices',
            'form': form,
            'year': datetime.now().year,
            'data': devices_numbers,
        }
    )
