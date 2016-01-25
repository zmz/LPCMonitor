from django.shortcuts import render

# Create your views here.

def index(request):
    context          = {}
    context['lenovo'] = 'Lenovo Private Cloud'
    return render(request, 'index.html', context)