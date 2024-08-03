from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from .forms import AddDeviceModel, UpdateProfileForm, UpdateUserForm, AddKeysModel
from .models import DeviceModel, Keys
from .others import timepp

from datetime import datetime
from rest_framework import status


# !----- basic views -----!
def home(request) -> HttpResponse:
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def about(request) -> HttpResponse:
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


# !----- devices -----!
# !!! start of all work !!!
class DevicesListView(LoginRequiredMixin, ListView, FormMixin):
    form_class = AddDeviceModel
    model = DeviceModel
    template_name = 'app/devices.html'
    context_object_name = 'data'
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

        time_end = request.POST['time_end']
        slct = request.POST['selection']
        time_d = timepp(time_end, slct)

        form = AddKeysModel({
            'key': request.POST['key'],
            'used': request.POST['used'],
            'time_start': request.POST.get('time_start', timezone.make_aware(datetime.now())),
            'time_end': time_d,
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

    return render(request, 'app/profile.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'title': 'Profile',
                   'year': datetime.now().year})


# !----- htmx devices -----!
def change_device_name(request, pk):
    device = DeviceModel.objects.get(pk=pk)

    device.device_name = request.POST.get('device_name') if request.POST.get('device_name') else device.device_name
    print(device.device_name)
    device.save()

    return HttpResponse(device.device_name)


def change_status(request, pk):
    device = DeviceModel.objects.get(pk=pk)

    if device.status == 'Close':
        device.status = 'Open'
    else:
        device.status = 'Close'
    device.save()

    return HttpResponse(device.status)


def change_admin(request, pk):
    device = DeviceModel.objects.get(pk=pk)

    if device.admin == 'Off':
        device.admin = 'On'
    else:
        device.admin = 'Off'
    device.save()

    return HttpResponse(device.admin)


def delete_key(request, id, pk):
    Keys.objects.get(pk=id).delete()
    keys = Keys.objects.filter(device_id=pk)
    return HttpResponse('<p class="mb-0">Ключ удалён</p>')


# !----- download file apk -----!
def download_file(request):
    fl_path = 'app/static/app/mobile_app/app-debug.apk'
    filename = 'seld.apk'

    fl = open(fl_path, 'rb')
    response = HttpResponse(fl, content_type='application/force-download')
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response


# !----- own errors -----!
def handler_403(request, exception=None):
    return render(request, "errors_app/403.html", {'title': '403 - в доступе отказано!'},
                  status=status.HTTP_403_FORBIDDEN)


def handler_404(request, exception=None):
    return render(request, "errors_app/404.html", {'title': '404 - страница не найдена!'},
                  status=status.HTTP_404_NOT_FOUND)


def handler_500(request, exception=None):
    return render(request, "errors_app/500.html", {'title': '500 - ошибка сервера!'},
                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
