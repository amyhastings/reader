from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def error_500(request):
    return render(request, 'reader/500.html', status=500)