from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from .utils import searchProfiles,  paginateProfiles
from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

from django.contrib import messages



# Create Your Views Here

def loginUser(request):
    """
    Logs in a user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the user is already authenticated, redirects to the home page.
    - If the request method is POST and the username and password are valid, logs in the user and redirects to the home page.
    - If the username is not found or the password is incorrect, displays an error message.
    - Otherwise, renders the login page.

    """
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, "Username Not found")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home') #! Redirects to the page the user was trying to access before logging in
        else:
            messages.error(request, "Username or Password is incorrect")


    return render(request, 'users/login-page.html')


def logoutUser(request):
    logout(request)
    return redirect('login-page')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.error(request, "An error has occurred during registration!!!")

    
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login-page.html', context)


def home(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'users/home.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description = "")
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url="login-page")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context= {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'users/account.html', context)

@login_required(login_url="login-page")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user-account')

    context = {
        'form':form,
    }
    return render(request, 'users/edit-account.html', context)


@login_required(login_url='login-page')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            messages.success(request, "Skill added successfully!")

            return redirect('user-account')

    context = {
        'form': form,
    }
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login-page')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()

            messages.success(request, "Skill updated successfully!")
            
            return redirect('user-account')

    context = {
        'form': form,
    }
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login-page')
def deleteSkill(request, pk):
    """This function is used to delete a specific skill from a user's profile.

    Parameters:
    request (HttpRequest): The request object from the client.
    pk (int): The primary key of the skill to be deleted.

    Returns:
    HttpResponse: A redirect to the 'user-account' page if the skill is successfully deleted, 
    or a render of the 'delete_template.html' page with the skill context if the request method is not POST.

    The function first retrieves the profile of the currently logged in user and then the specific skill 
    associated with that profile using the provided primary key (pk). 

    If the request method is POST, it deletes the skill, sends a success message, and redirects the user 
    to the 'user-account' page.

    If the request method is not POST, it prepares a context with the skill to be deleted and renders 
    the 'delete_template.html' page with this context."""
    
    profile = request.user.profile
    skill=profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()

        messages.success(request, "Skill deleted successfully!")
        return redirect('user-account')
    
    context = {
        'object':skill,
    }
    return render(request, 'delete_template.html', context)


@login_required(login_url="login-page")
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()

    context = {
        'messageRequest': messageRequest,
        'unreadCount': unreadCount,
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login-page")
def viewMessages(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {
        'message': message,
    }
    return render(request, 'users/message.html', context)


def createMessage(request, pk ):
    recipient = Profile.objects.get(id=pk)

    context = {
        'recipient': recipient,
    }
    return render(request, 'users/message_form.html', context)