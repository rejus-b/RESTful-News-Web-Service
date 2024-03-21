from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, backends
import json
from datetime import datetime

from cwkapp.models import Author, news

# Create your views here.

@csrf_exempt
def HandleLoginRequest(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if POST
    if request.method != "POST":
        http_bad_response.content = "Only POST requests are allowed for this resource."
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
        http_bad_response.content = "Only POST requests are allowed for this resource."
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
        http_bad_response.content = "Only POST requests are allowed for this resource."
        http_bad_response.status_code = 503 # Spec says only 503s
        return http_bad_response
        
    # Load JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))
    
    headline = data.get('headline')
    catergory = data.get('category')
    region = data.get('region')
    details = data.get('details')

    if not all([headline, catergory, region, details]):
        return HttpResponse("Incomplete data. Please provide all required fields.", status=400, content_type="text/plain")

    # Retrieve the Author obj of the logged in user
    try:
        author = Author.objects.get(user=request.user)
    except Exception as e:
         return HttpResponse(f"Error posting story. {e}", status=503, content_type="text/plain")
    
    date = datetime.now()
    
    try:
        news.objects.create(
            headline=headline,
            catergory=catergory,
            region=region,
            author=author,
            date=date,
            details=details,
        )

        return HttpResponse("Story posted successfully.", status=201, content_type="text/plain")
    except Exception as e:
        return HttpResponse(f"Error posting story. {e}", status=503, content_type="text/plain")
    

@csrf_exempt
# @login_required
def HandleGetStoriesRequest(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if GET
    if request.method != "GET":
        http_bad_response.content = "Only GET requests are allowed for this resource."
        http_bad_response.status_code = 503 # Spec says only 503s
        return http_bad_response
    
    # Extract parameters with default as wildcard
    story_cat = request.GET.get("story_cat", "*")
    story_region = request.GET.get("story_region", "*")
    story_date = request.GET.get("story_date", "*")

    # First get all stories and then filter them out
    stories = news.objects.all()

    if story_cat != "*":
        stories = stories.filter(catergory=story_cat)

    if story_region != "*":
        stories = stories.filter(region=story_region)

    if story_date != "*":
        try:
            # Extract datetime
            parsed_date = datetime.strptime(story_date, "%Y-%m-%d")
            # https://www.w3schools.com/django/ref_lookups_gte.php
            # Above link explains field lookups
            stories = stories.filter(date__gte=parsed_date)
        except ValueError:
            return HttpResponseBadRequest("Invalid date format. Please provide dates in YYYY-MM-DD format.", status_code=404)

    # Make payload
    payload = []
    for story in stories:
        story_data = {
            "key": str(story.uniquekey),
            "headline": story.headline,
            "story_cat": story.catergory,
            "story_region": story.region,
            "author": story.author.authorName,
            "story_date": str(story.date),
            "story_details": story.details
        }
        payload.append(story_data)

    if payload:
        return JsonResponse({"stories": payload}, status=200)
    else:
        return HttpResponse("Could not find any matching stories", status=404, content_type="text/plain")
    


@csrf_exempt
@login_required
def HandleDeleteRequest(request, key):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response["Content-Type"] = "text/plain"

    # Check if DELETE
    if request.method != "DELETE":
        http_bad_response.content = "Only DELETE requests are allowed for this resource."
        http_bad_response.status_code = 503 # Spec says only 503s
        return http_bad_response

    # Find the story with the matching key
    try:
        story = news.objects.get(uniquekey=key)
    except:
        return HttpResponseBadRequest("The key does not exist.", status_code=503)

    # Check that the user is the author of the story they want to delete
    if request.user != story.author.user:
        return HttpResponseBadRequest("You are not the author of the story.", status_code=503) 

    # Delete the story
    try:
        story.delete()
        return HttpResponse("Story deleted successfully.", status=200)
    except Exception as e:
        return HttpResponseBadRequest(f"Failed to delete story: {str(e)}", status=503)