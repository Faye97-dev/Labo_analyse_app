# Generated by Django 3.1.3 on 2020-11-11 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSanguin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, null=True)),
                ('descprition', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'group_sanguin',
            },
        ),
        migrations.CreateModel(
            name='Medecin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
                ('nni', models.CharField(max_length=50, null=True)),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('tel', models.CharField(max_length=50, null=True)),
                ('specialite', models.CharField(max_length=100, null=True)),
                ('clinique', models.CharField(max_length=50, null=True)),
                ('user_created', models.CharField(max_length=100, null=True)),
                ('user_modified', models.CharField(max_length=100, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modifcation', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'medecin',
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('with_account', models.IntegerField(null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profil',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
                ('nni', models.CharField(max_length=50, null=True)),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('tel', models.CharField(max_length=50, null=True)),
                ('poids', models.FloatField(null=True)),
                ('taille', models.FloatField(null=True)),
                ('age', models.IntegerField(null=True)),
                ('user_created', models.CharField(max_length=100, null=True)),
                ('user_modified', models.CharField(max_length=100, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modifcation', models.DateTimeField(auto_now=True, null=True)),
                ('group_sanguin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='analyse.groupsanguin')),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='Analyse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_analyse', models.DateField(null=True)),
                ('analyse_pdf', models.FileField(blank=True, null=True, upload_to='')),
                ('user_created', models.CharField(max_length=100, null=True)),
                ('user_modified', models.CharField(max_length=100, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modifcation', models.DateTimeField(auto_now=True, null=True)),
                ('medecin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='analyse.medecin')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='analyse.patient')),
            ],
            options={
                'db_table': 'analyse',
            },
        ),
    ]
