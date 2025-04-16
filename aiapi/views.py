from django.http import JsonResponse

# Create your views here.
def index(request):
    data = {
        "message": "Hello, this is a JSON response!",
        "status": "success"
    }
    return JsonResponse(data)