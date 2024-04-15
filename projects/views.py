from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .utils import searchProjects, paginateProjects 
from .forms import ProjectForm

from django.contrib.auth.decorators import login_required


def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 3)

    context={
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)

def viewProject(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/view-project.html', {'project': projectObj})

@login_required(login_url='login-page')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            return redirect('user-account')

    context = {'form': form}
    return render(request, "projects/projects_form.html", context)


@login_required(login_url='login-page')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save() 
            return redirect('user-account')

    context = {'form': form}
    return render(request, "projects/projects_form.html", context)


@login_required(login_url='login-page')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('user-account')
    context={'object':project}
    return render(request, 'delete_template.html', context)