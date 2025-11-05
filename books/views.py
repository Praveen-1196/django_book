from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer
from rest_framework.parsers import JSONParser
import cloudinary.uploader

@csrf_exempt
def get_books(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def get_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "GET":
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def create_book(request):
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
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "DELETE":
        book.delete()
        return JsonResponse({"message": "Deleted"})
