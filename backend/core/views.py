from django.http import JsonResponse

def api_root(request):
    return JsonResponse({"status": "ok", "message": "Django API Running"})

def hello_world(request):
    return JsonResponse({"message": "Hello World from Django Backend!"})
