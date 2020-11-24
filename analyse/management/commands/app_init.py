from django.contrib.auth.models import User , Group
from django.core.management.base import BaseCommand
from analyse.models import Profil ,Staff_Admin , GroupSanguin

class Command(BaseCommand):
    help = 'Create roles and first superuser'

    #def add_arguments(self, parser):
    #   parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        #total = kwargs['total']
        for sng in [ 'A positif', 'A negatif', 'B positif', 'B negatif', 'AB positif', 'AB negatif', 'O positif' ,'O negatif'] :
            instance = GroupSanguin(nom=sng)
            instance.save()
        Group.objects.create(name='Doctor')
        Group.objects.create(name='Patient')
        admin_gp = Group.objects.create(name='Admin')
        ##
        user = User.objects.create_user(username='root', email='', password='di*gi*20*20@' ,first_name='root_user' )
        admin_gp.user_set.add(user)
        ##
        admin = Staff_Admin(nom='root',nni='0000000',tel=000000,email='root@gmail.com', adresse='none')
        admin.poste = 'root' 
        admin.save()
        ##
        profil = Profil(user=user , with_account=admin.id, description='Admin')
        profil.save()
