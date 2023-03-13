import random


NUMBERS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')


def new_code():
    rand_number = int(''.join(random.sample(NUMBERS, 4)))
    while len(str(rand_number)) != 4:
        rand_number = int(''.join(random.sample(NUMBERS, 4)))
    return rand_number


class DeviceMixin:
    def get_async_form(self, device_lock):
        form = self.form_class(initial=
                                   {
                                       'device_name': device_lock.device_name, 
                                       'serial_num': device_lock.serial_num, 
                                       'auth_key': device_lock.auth_key,
                                       'status': device_lock.status
                                   })
        form.fields['serial_num'].widget.attrs['readonly'] = True
        return form

