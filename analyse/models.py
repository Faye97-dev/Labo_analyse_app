from django.db import models
from django.contrib.auth.models import User

class Staff_Admin(models.Model):
    nom = models.CharField(max_length=200,null=True)
    nni = models.CharField(max_length=50,null=True)
    adresse = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=50,null=True)
    tel = models.CharField(max_length=50,null=True)
    poste = models.CharField(max_length=100,null=True)
    
    user_created = models.CharField(max_length=100,null=True)
    user_modified = models.CharField(max_length=100,null=True)
    date_creation = models.DateTimeField(auto_now_add=True,null=True)
    date_modifcation = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        db_table= "admin"

class Medecin(models.Model):
    nom = models.CharField(max_length=200,null=True)
    nni = models.CharField(max_length=50,null=True)
    adresse = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=50,null=True)
    tel = models.CharField(max_length=50,null=True)
    specialite = models.CharField(max_length=100,null=True)
    clinique = models.CharField(max_length=50,null=True)
    #history = HistoricalRecords(table_name='history_medecin', excluded_fields=['id'])
    ##
    user_created = models.CharField(max_length=100,null=True)
    user_modified = models.CharField(max_length=100,null=True)
    date_creation = models.DateTimeField(auto_now_add=True,null=True)
    date_modifcation = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        db_table= "medecin"

class GroupSanguin(models.Model):
    nom = models.CharField(max_length=50,null=True)
    descprition = models.CharField(max_length=100,null=True)

    class Meta:
        db_table= "group_sanguin"

class Patient(models.Model):
    nom = models.CharField(max_length=200,null=True)
    nni = models.CharField(max_length=50,null=True)
    adresse = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=50,null=True)
    tel = models.CharField(max_length=50,null=True)
    ##
    group_sanguin = models.ForeignKey(GroupSanguin, on_delete=models.CASCADE,null=True)
    poids = models.FloatField(null=True)
    taille = models.FloatField(null=True)
    age = models.IntegerField(null=True)
    ##
    user_created = models.CharField(max_length=100,null=True)
    user_modified = models.CharField(max_length=100,null=True)
    date_creation = models.DateTimeField(auto_now_add=True,null=True)
    date_modifcation = models.DateTimeField(auto_now=True,null=True)
    
    class Meta:
        db_table= "patient"

class Analyse(models.Model):
    date_analyse = models.DateField(null=True)
    analyse_pdf = models.FileField(null=True,blank=True)
    medecin  = models.ForeignKey(Medecin, on_delete=models.CASCADE,null=True)
    patient  = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    ##
    user_created = models.CharField(max_length=100,null=True)
    user_modified = models.CharField(max_length=100,null=True)
    date_creation = models.DateTimeField(auto_now_add=True,null=True)
    date_modifcation = models.DateTimeField(auto_now=True,null=True)
    
    class Meta:
        db_table= "analyse"

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    with_account = models.IntegerField(null=True)
    description = models.CharField(max_length=200, null =True)
    chat_reloading = models.IntegerField(null=True)
    class Meta:
        db_table= "profil"

    def __str__(self):
        return self.user.username + ' : ' + self.description