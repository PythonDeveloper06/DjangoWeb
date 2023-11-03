from datetime import datetime
from http.client import HTTPResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from django.contrib import messages

from .forms import AddDeviceModel, UpdateProfileForm, UpdateUserForm, AddKeysModel
from .models import DeviceModel, Keys
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# !!! basic views !!!
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

def seld(request):
    """Renders the SELD page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'app/seld.html', {'title': 'SELD'})


# !!! Class Basic Views !!!
class DeviceDetailView(DetailView):
    model = DeviceModel
    template_name = 'app/your_device.html'
    context_object_name = 'data'


class DeviceUpdateView(UpdateView):
    model = DeviceModel
    template_name = 'app/update_form.html'
    form_class = AddDeviceModel


    def get(self, request, pk):
        device_lock = self.model.objects.get(id=pk)
        form = self.form_class(initial=
                                   {
                                       'device_name': device_lock.device_name, 
                                       'serial_num': device_lock.serial_num, 
                                       'status': device_lock.status
                                   })
        form.fields['serial_num'].widget.attrs['readonly'] = True
        return render(request, 'app/update_form.html', {'title':'Update your device', 'form': form, 'year': datetime.now().year})
    

class DeviceDeleteView(DeleteView):
    model = DeviceModel
    template_name = 'app/delete_form.html'
    success_url = reverse_lazy('devices')
    context_object_name = 'data'


class KeyDeleteView(DeleteView):
    model = Keys
    template_name = 'app/delete_key_form.html'
    context_object_name = 'data'

    def get_success_url(self):
        success_url = reverse_lazy('keys', args=[self.kwargs["device_id"]])
        return success_url
    

# !!! start of all work !!!
class DevicesListView(ListView, FormMixin):
    model = DeviceModel
    template_name = 'app/devices.html'
    context_object_name = 'data'
    paginate_by = 3
    form_class = AddDeviceModel
    success_url = reverse_lazy('devices')

    def get_queryset(self):
        return DeviceModel.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if not self.model.objects.filter(serial_num=request.POST['serial_num']).exists():
                form.save()
            return HttpResponseRedirect(reverse_lazy('devices'))
        return HttpResponseRedirect(reverse_lazy('devices'))


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(data=request.POST, instance=request.user)
        profile_form = UpdateProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Wrong data')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'app/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'title': 'Profile', 'year': datetime.now().year})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'app/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')
    extra_context = {'year': datetime.now().year}


class KeysListView(ListView, FormMixin):
    model = DeviceModel
    template_name = 'app/keys.html'
    context_object_name = 'data'
    paginate_by = 3
    form_class = AddKeysModel
    extra_context = {'title': 'Your keys'}

    def get_queryset(self):
        return Keys.objects.filter(device_id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        device_lock = DeviceModel.objects.get(id=self.kwargs['pk'])
        form = AddKeysModel({
            'key': request.POST['key'],
            'device': device_lock
            })
        if form.is_valid():
            print(request.POST)
            if not Keys.objects.filter(device_id=device_lock).exists():
                form.save()
            return HttpResponseRedirect(reverse_lazy('keys', args=[self.kwargs["pk"]]))
        return HttpResponseRedirect(reverse_lazy('devices'))