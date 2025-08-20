
from django.contrib import admin
from .models import Appointment
from django.contrib import admin
from django.core.mail import send_mail


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'status')

    def save_model(self, request, obj, form, change):
        old_status = None
        if obj.pk:
            old_status = Appointment.objects.get(pk=obj.pk).status
        super().save_model(request, obj, form, change)

       
        if old_status != obj.status and obj.status == "Approved":
            send_mail(
                'Appointment Approved',
                f"Hello {obj.name}, your appointment on {obj.date} at {obj.time} has been approved.",
                'nssreerag27@gmail.com',
                [obj.email],
                fail_silently=False,
            )