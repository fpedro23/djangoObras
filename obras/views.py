import datetime

from django.http import HttpResponse
from django.db.models import Q

from obras.models import *


def index(request):
    data = "Respuesta = " + request.GET.get('id')
    return HttpResponse(data)


def balance_general(request):
    start_date = datetime.date(2012, 12, 01)
    end_date = datetime.date(2013, 12, 31)
    Obra.objects.filter(

        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)

    )