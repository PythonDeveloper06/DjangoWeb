from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import AddDeviceModel, UpdateProfileForm, UpdateUserForm, AddKeysModel
from .models import DeviceModel, Keys

from datetime import datetime


# !----- basic views -----!
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year': datetime.now().year,
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
            'year': datetime.now().year,
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
            'year': datetime.now().year,
        }
    )


def seld(request):
    """Renders the SELD page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'app/seld.html', {'title': 'SELD'})


# !----- devices -----!
# !!! start of all work !!!
class DevicesListView(LoginRequiredMixin, ListView):
    model = DeviceModel
    template_name = 'app/devices.html'
    context_object_name = 'data'
    from_class = AddDeviceModel
    paginate_by = 6

    def get_queryset(self):
        return DeviceModel.objects.filter(user=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = DeviceModel
    template_name = 'app/your_device.html'
    context_object_name = 'data'


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = DeviceModel
    template_name = 'app/update_form.html'
    form_class = AddDeviceModel

    def post(self, request, **kwargs):
        device_lock = self.model.objects.get(id=self.kwargs['pk'])

        request.POST = request.POST.copy()
        request.POST['serial_num'] = device_lock.serial_num
        request.POST['settings'] = device_lock.settings
        request.POST['admin'] = device_lock.admin
        request.POST['sync'] = device_lock.sync
        request.POST['user'] = self.request.user

        return super(DeviceUpdateView, self).post(request, **kwargs)
    

class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = DeviceModel
    template_name = 'app/delete_form.html'
    success_url = reverse_lazy('devices')
    context_object_name = 'data'


# !----- keys -----!
class KeysListView(LoginRequiredMixin, ListView, FormMixin):
    model = DeviceModel
    template_name = 'app/keys.html'
    context_object_name = 'data'
    paginate_by = 6
    form_class = AddKeysModel
    extra_context = {'title': 'Your keys'}

    def get_queryset(self):
        return Keys.objects.filter(device_id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        device_lock = DeviceModel.objects.get(id=self.kwargs['pk'])
        form = AddKeysModel({
            'key': request.POST['key'],
            'used': request.POST['used'],
            'time': request.POST['time'],
            'selection': request.POST['selection'],
            'device': device_lock
            })
        if form.is_valid():
            if not Keys.objects.filter(key=request.POST['key']):
                form.save()
            return HttpResponseRedirect(reverse_lazy('keys', args=[self.kwargs["pk"]]))
        return HttpResponseRedirect(reverse_lazy('devices'))


class KeyDeleteView(LoginRequiredMixin, DeleteView):
    model = Keys
    template_name = 'app/delete_key_form.html'
    context_object_name = 'data'

    def get_success_url(self):
        success_url = reverse_lazy('keys', args=[self.kwargs["device_id"]])
        return success_url


# !----- profile -----!
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


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'app/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')
    extra_context = {'year': datetime.now().year}
