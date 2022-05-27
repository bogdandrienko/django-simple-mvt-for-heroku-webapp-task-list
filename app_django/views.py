from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from . import models


# Create your views here.


def index(request):
    return HttpResponse("<h1>This is a Index Page</h1>")


def home(request):
    context = {
    }
    return render(request, 'pages/home.html', context)


def create(request):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        models.Task.objects.create(
            title=title,
            description=description,
            is_completed=False,
        )
        return redirect(reverse('app_name_task_list:read_list', args=()))
    context = {
    }
    return render(request, 'app_task_list/pages/task_create.html', context)


def read(request, task_id=None):
    task = models.Task.objects.get(id=task_id)
    context = {
        "task": task
    }
    return render(request, 'app_task_list/pages/task_detail.html', context)


def read_list(request):

    is_detail_view = request.GET.get("is_detail_view", True)
    if is_detail_view == "False":
        is_detail_view = False
    elif is_detail_view == "True":
        is_detail_view = True
    task_list = models.Task.objects.all()

    def paginate(objects, num_page):
        paginator = Paginator(objects, num_page)
        pages = request.GET.get('page')
        try:
            local_page = paginator.page(pages)
        except PageNotAnInteger:
            local_page = paginator.page(1)
        except EmptyPage:
            local_page = paginator.page(paginator.num_pages)
        return local_page

    page = paginate(objects=task_list, num_page=4)
    context = {
        "page": page,
        "is_detail_view": is_detail_view
    }
    return render(request, 'app_task_list/pages/task_list.html', context)


def update(request, task_id=None):
    if request.method == 'POST':
        task = models.Task.objects.get(id=task_id)
        is_completed = request.POST.get("is_completed", "")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        if is_completed:
            if is_completed == "False":
                task.is_completed = False
            elif is_completed == "True":
                task.is_completed = True
        if title and title != task.title:
            task.title = title
        if description and description != task.description:
            task.description = description
        task.updated = timezone.now()
        task.save()
        return redirect(reverse('app_name_task_list:read_list', args=()))
    task = models.Task.objects.get(id=task_id)
    context = {
        "task": task
    }
    return render(request, 'app_task_list/pages/task_change.html', context)


def delete(request, task_id=None):
    models.Task.objects.get(id=task_id).delete()
    return redirect(reverse('app_name_task_list:read_list', args=()))
