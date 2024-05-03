from django.http import HttpResponseNotFound

def custom_404_view(request, exception=None):
    return HttpResponseNotFound('<h1>Page not found</h1>')