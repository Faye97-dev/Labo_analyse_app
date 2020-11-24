# Generated by Django 3.1.3 on 2020-11-15 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff_Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
                ('nni', models.CharField(max_length=50, null=True)),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('tel', models.CharField(max_length=50, null=True)),
                ('poste', models.CharField(max_length=100, null=True)),
                ('user_created', models.CharField(max_length=100, null=True)),
                ('user_modified', models.CharField(max_length=100, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modifcation', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'admin',
            },
        ),
        migrations.AddField(
            model_name='profil',
            name='chat_reloading',
            field=models.IntegerField(null=True),
        ),
    ]
