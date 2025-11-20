from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer
from rest_framework.parsers import JSONParser
import cloudinary.uploader
import jwt
from django.conf import settings
import datetime
import json


def validate_token(request):
    token = request.COOKIES.get("token")

    if not token:
        return None, JsonResponse({"error": "Unauthorized - No token"}, status=401)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload, None

    except jwt.ExpiredSignatureError:
        return None, JsonResponse({"error": "Token expired"}, status=401)

    except jwt.DecodeError:
        return None, JsonResponse({"error": "Invalid token"}, status=401)

    except Exception as e:
        return None, JsonResponse({"error": str(e)}, status=401)




@csrf_exempt
def get_books(request):
    payload, error = validate_token(request)
    if error:
        return error

    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def get_book(request, id):
    payload, error = validate_token(request)
    if error:
        return error
    

    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "GET":
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def create_book(request):
    payload, error = validate_token(request)
    if error:
        return error
    
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("image")

        image_url = None
        if image:
            upload = cloudinary.uploader.upload(image)
            image_url = upload["secure_url"]

        payload = {
            "name": data.get("name"),
            "author": data.get("author"),
            "quote": data.get("quote"),
            "image": image_url,
        }

        serializer = BookSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def update_book(request, id):

    payload, error = validate_token(request)
    if error:
        return error

    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def delete_book(request, id):


    payload, error = validate_token(request)
    if error:
        return error
    

    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "DELETE":
        book.delete()
        return JsonResponse({"message": "Deleted"})


# User Authentication Views
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )


    return JsonResponse({"message": "User registered successfully"})

@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=401)

    payload = {
        "id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    res = JsonResponse({"message": "Login successful"})
    res.set_cookie(
        "token",
        token,
        httponly=True,
        samesite="None",
        secure=False
    )
    return res
