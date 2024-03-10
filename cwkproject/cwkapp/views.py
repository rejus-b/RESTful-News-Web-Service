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

    # Load JSON data from the request body
    data = json.loads(request.body.decode("utf-8"))
    username = data.get("username", "")
    password = data.get("password", "")

    # Now compare it
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Authentication successful, try to store the session info
        login(request=request, user=user)
        request.session.save()
        return JsonResponse({"result": "success", "message": "Succesful login"}, status=200)
    else:
        # Authentication failed
        return JsonResponse({"result": "error", "message": "Invalid credentials"}, status=401)
    

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
        return JsonResponse({"result": "success", "message": "Logged out"}, status=200)
    except:
         return JsonResponse({"result": "error", "message": "Error logging out"}, status=400)

    

@csrf_exempt
@login_required
def HandlePostRequest(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if POST
    if request.method != "POST":
        http_bad_response.content = "Only POST requests are allowed for this resource\n"
        http_bad_response.status_code = 405
        return http_bad_response
        
    data = json.loads(request.body.decode('utf-8'))
    headline = data.get('headline')
    category = data.get('category')
    region = data.get('region')
    details = data.get('details')
    

    if not all([headline, category, region, details]):
        return HttpResponse("Incomplete data. Please provide all required fields.", status=400)

    author = request.user
    print(author)

    news.objects.create(
        headline,
        category=category,
        region=region,
        details=details,
        author=author
        date=None#Figure this out 
    )

    return JsonResponse({"message": "Story posted successfully."}, status=201)
