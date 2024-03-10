from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json

from cwkapp.models import Author

# Create your views here.

@csrf_exempt
def HandleLoginRequest(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if POST
    if request.method != "POST":
        http_bad_response.content = "Only POST requests are allowed for this resource\n" + str(request.method)
        return http_bad_response

    # Load JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))
    username = data.get("username", "")
    password = data.get("password", "")

    # Now compare it
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Authentication successful
        return JsonResponse({'result': 'success'}, status=200)
    else:
        # Authentication failed
        return JsonResponse({'result': 'error', 'message': 'Invalid credentials'}, status=400)