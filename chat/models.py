from django.contrib.auth.models import User
from django.db import models
from analyse.models import Profil
'''
class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username
'''

class Message(models.Model):
    sender = models.ForeignKey(Profil, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content + ' - id : ' + str(self.pk)
    
    class Meta:
        db_table= "messsages"


class Chat(models.Model):
    user_to = models.ForeignKey(Profil, on_delete=models.CASCADE)
    user_from = models.ForeignKey(Profil, related_name='chats', on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, blank=True)
    last_message = models.ForeignKey(Message, related_name='last_message', on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return "{}".format(self.pk)
    
    class Meta:
        db_table= "Chats"