from django.contrib import admin
from .models import Patient , Medecin , Analyse , GroupSanguin , Profil , Staff_Admin
# Register your models here.
admin.site.register(Patient)
admin.site.register(Analyse)
admin.site.register(Medecin)
admin.site.register(GroupSanguin)
admin.site.register(Profil)
admin.site.register(Staff_Admin)