from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from django.contrib import messages

from .forms import AddDeviceModel, UpdateProfileForm, UpdateUserForm, AddKeysModel
from .models import DeviceModel, Keys
from django.views.generic import DetailView, UpdateView, DeleteView
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
        print(device_lock)
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
    success_url = reverse_lazy('devices')
    context_object_name = 'data'
    

# !!! start of all work !!!
async def devices(request):
    """Renders and proccesing info the device page."""
    if request.method == 'POST':
        form = AddDeviceModel(request.POST)
        if await sync_to_async(form.is_valid)():
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


def keys(request, pk):
    """Renders and proccesing info the key`s page."""
    device_lock = DeviceModel.objects.get(id=pk)
    if request.method == 'POST':
        form = AddKeysModel({
            'key': request.POST['key'],
            'device': device_lock
            })
        if form.is_valid():
            if not Keys.objects.filter(key=request.POST['key']).exists():
                form.save()
    form = AddKeysModel()
    devices_numbers = Keys.objects.filter(device_id=pk)

    paginator = Paginator(devices_numbers, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'app/keys.html',
        {
            'title':'Your keys',
            'form': form,
            'year': datetime.now().year,
            'page_new': page_obj
        }
    )