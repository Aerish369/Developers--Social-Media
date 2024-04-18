from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .utils import searchProjects, paginateProjects 
from .forms import ProjectForm, ReviewForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required


def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context={
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)

def viewProject(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False) 
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount #! Updates vote count and ratio

        messages.success(request, 'Your review was successfully submitted !')
        return redirect('view-project', pk=projectObj.id)

    context = {
        'project': projectObj,
        'form': form,
    }
    return render(request, 'projects/view-project.html', context)

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