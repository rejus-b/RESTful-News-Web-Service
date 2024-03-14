from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, backends
import json


from cwkapp.models import Author, news

# Create your views here.

@csrf_exempt
def HandleLoginRequest(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if POST
    if request.method != "POST":
        http_bad_response.content = "Only POST requests are allowed for this resource\n"
        http_bad_response.status_code = 405
        return http_bad_response

    # Load form data from the request
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    # Now compare it
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Authentication successful, try to store the session info
        login(request=request, user=user)
        request.session.save()
        return HttpResponse("Successful login", status=200, content_type="text/plain")
    else:
        # Authentication failed
        return HttpResponse("Invalid credentials", status=401, content_type="text/plain")
    

@csrf_exempt
def HandleLogoutRequest(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if POST
    if request.method != "POST":
        http_bad_response.content = "Only POST requests are allowed for this resource\n"
        http_bad_response.status_code = 405
        return http_bad_response
    
    try:
        # Try logout the session
        logout(request=request)
        return HttpResponse("Logged out", status=200, content_type="text/plain")
    except:
        return HttpResponse("Error logging out", status=400, content_type="text/plain")

    

@csrf_exempt
@login_required
def HandlePostRequest(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if POST
    if request.method != "POST":
        http_bad_response.content = "Only POST requests are allowed for this resource\n"
        http_bad_response.status_code = 503 # Spec says only 503s
        return http_bad_response
        
    headline = request.POST.get('headline')
    category = request.POST.get('category')
    region = request.POST.get('region')
    details = request.POST.get('details')

    if not all([headline, category, region, details]):
        return HttpResponse("Incomplete data. Please provide all required fields.", status=400, content_type="text/plain")

    author = request.user
    print(author)
    return HttpResponse("Story posted successfully.", status=201, content_type="text/plain")
    # try:
    #     news.objects.create(
    #         headline,
    #         category=category,
    #         region=region,
    #         details=details,
    #         author=author
    #         date=None#Figure this out 
    #     )

    #     return HttpResponse("Story posted successfully.", status=201, content_type="text/plain")
    # except:
    #     return HttpResponse("Error posting story.", status=503, content_type="text/plain")