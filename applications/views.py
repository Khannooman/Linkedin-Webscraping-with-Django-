from django.shortcuts import render
from .models import Job
from django.http import HttpResponse
from django.urls import reverse


def home(request):
    context = {
        'title': 'Find a Job',
        'link': reverse('linked_jobs')
    }
    return render(request, 'applications/home.html', context)


def linked_jobs(request):
    if request.method == 'GET':
        # Retrieve filter values from frontend
        location_filter = request.GET.get('location', '')

        # Apply filters to queryset
        deet = Job.objects.filter(
            Location__icontains=location_filter,

        )

    return render(request, "applications/job.html", {"details": deet})




