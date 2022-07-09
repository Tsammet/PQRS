from django.shortcuts import render
from django.db.models import Q
from pqrs.models import piano
from django.core.paginator import Paginator



# Create your views here.


def inicioC(request):
    pianos = piano.objects.all().order_by('-id')

    paginator = Paginator(pianos, 2)
    page = request.GET.get('page')
    pianos = paginator.get_page(page)



    if request.method == "POST":
        busqueda = request.POST["buscar"]

        if busqueda:
            pianos = piano.objects.filter(
                Q(referencia_piano__icontains = busqueda) 
            ).distinct()


    return render(request, 'inicio/pianos.html', {"pianos":pianos})


def inicioA(request):
    return render(request, 'inicio/inicioA.html')
