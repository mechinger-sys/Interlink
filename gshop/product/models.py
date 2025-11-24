from django.db import models
from django import forms
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'image']
   
class ContactForm(forms.Form):
    username = forms.CharField(max_length=50)



class Messages(models.Model):
    chat_history = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:50]}'

    
class MessageForm(forms.ModelForm):    
    class Meta:
        model = Messages
        fields = [ 'message']   



    def __str__(self):
        return f'Settings for {self.project_name.name}'

