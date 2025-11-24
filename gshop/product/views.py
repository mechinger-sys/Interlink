import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from .models import Project, ProjectForm, ContactForm, Messages, MessageForm
    
def create_project(request):
    username = request.session.get('username')
    if not username:
        return HttpResponse('get out')

    user, _ = User.objects.get_or_create(username=username)
    user_dic = {'user': user.username}
    json_str = json.dumps(user_dic)
    
    project = None  # initialize project
    form = None

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = user
            project.save()
            request.session['username'] = user.username
    else:
        form = ProjectForm()

       

    return render(request, 'create_project.html', {
        'form': form,
        'username': username,
        'json_str': json_str,
        'is_valid': True,
    })

def main_page(request):
    # prefer authenticated user, fall back to a session-stored username
    if request.user.is_authenticated:
        user = request.user
        username = user.username
    else:
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()

    if not user:
        return render(request, 'failure.html')

    projects = Project.objects.filter(user=user)

    return render(request, 'main_page.html', {
        'name': username,
        'projects': projects,
        'is_valid': True,
        'projectnumber': not projects.exists()
    })#676767676767767767676767676t767!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11    


def login(request):
    user = None
    username = request.session.get('username', 'unknown')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():          
            username = form.cleaned_data['username']
            user, created = User.objects.get_or_create(username=username)
            auth_login(request, user)
            # ensure session is set so create_project can use it
            request.session['username'] = username
            # redirect to create_project with username
    else:
        form = ContactForm()

    return render(request, 'login.html', {'form': form,
    'username': username, 
    'user': user, 'appear':
    True, 'approval': True,
    'is_valid': True})
    
def index(request):
    return render(request, 'homepage.html', { 'other_valid': True, 'is_valid': True})


def chats(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # prefer authenticated user
    if request.user.is_authenticated:
        user = request.user
    else:
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()

    if not user:
        return HttpResponse("User not found")

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.chat_history = project
            msg.user = user
            msg.save()
            form = MessageForm()  # reset form after sending
    else:
        form = MessageForm()

    # Get all messages for this project
    messages = project.messages.all().order_by('id')  # oldest first

    return render(request, 'chats.html', {
        'form': form,
        'project': project,
        'messages': messages,
        'is_valid': True
    })

def project_settings(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    try:

        if request.method == 'POST':
            project.delete()  # Delete the project
    except Project.DoesNotExist:
        return HttpResponse("Project not found")
      
    return render(request, 'projectsetting.html', {
        'project': project,
        'is_valid': True
    })




def invites(request):
   return render(request, 'Invites.html', {'is_valid': True})