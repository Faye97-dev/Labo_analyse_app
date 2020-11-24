from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard', views.get_dashboard),
    path('analyse', views.get_analyses),
    path('analyse/medecin/<str:id>', views.get_analyses_medecin),
    path('analyse/patient/<str:id>', views.get_analyses_patient),
    path('add_analyse',views.add_analyse),
    path('existant_analyse',views.existant_analyse),
    path('edit_analyse',views.edit_analyse),
    path('delete_analyse/<str:id>',views.delete_analyse),
    ##
    path('compte_medecin', views.get_medecins),
    path('add_medecin', views.add_medecin),
    path('edit_medecin', views.edit_medecin),
    path('delete_medecin/<str:id>', views.delete_medecin),
    path('json_medecinUser/<str:id>', views.medecin_user_json),
    ##
    path('compte_patient', views.get_patients),
    path('compte_patient/medecin/<str:id>', views.get_patients_medecin),
    path('add_patient', views.add_patient),
    path('edit_patient', views.edit_patient),
    path('delete_patient/<str:id>', views.delete_patient),
    path('json_patientUser/<str:id>', views.patient_user_json),
    ##
    path('compte_admin', views.get_admin),
    path('add_admin', views.add_admin),
    path('edit_admin', views.edit_admin),
    path('delete_admin/<str:id>', views.delete_admin),
    path('json_adminUser/<str:id>', views.admin_user_json),
    ##
    path('profil-medecin', views.get_profil_medecin),
    path('edit_profil-medecin', views.edit_profil_medecin),
    ##
    path('profil-patient', views.get_profil_patient),
    path('edit_profil-patient', views.edit_profil_patient),
    ##
    path('profil-admin', views.get_profil_admin),
    path('edit_profil-admin', views.edit_profil_admin),
    ##
    path('view_send_analyse', views.get_send_analyse),
    path('json_patient/<str:id>', views.json_patient),
    path('send_analyse', views.sent_analyse), 
      
]
