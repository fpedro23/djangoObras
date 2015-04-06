__author__ = 'Pedro'
from django.db.models import Q

from obras.models import *


class BuscarObras:
    def __init__(
            self, idtipoobra, iddependencias, estados, clasificaciones, inversiones, inauguradores, impactos,
            inaugurada,
            inversion_minima, inversion_maxima,
            fecha_inicio_primera, fecha_inicio_segunda,
            fecha_fin_primera, fecha_fin_segunda,
            denominacion,
    ):
        self.clasificaciones = clasificaciones
        self.estados = estados
        self.inaugurada = inaugurada
        self.impactos = impactos
        self.idTipoObra = idtipoobra
        self.dependencias = iddependencias
        self.inversiones = inversiones
        self.inauguradores = inauguradores
        self.inversion_minima = inversion_minima
        self.inversion_maxima = inversion_maxima

        self.fecha_inicio_primera = fecha_inicio_primera
        self.fecha_inicio_segunda = fecha_inicio_segunda
        self.fecha_fin_primera = fecha_fin_primera
        self.fecha_fin_segunda = fecha_fin_segunda

        self.denominacion = denominacion

    def buscar(self):

        query = Q()

        if self.idTipoObra is not None:
            query = Q(tipoObra__id__in=self.idTipoObra)

        if self.fecha_inicio_primera is not None and self.fecha_inicio_segunda is not None:
            query = query & Q(fechaInicio__range=(self.fecha_inicio_primera, self.fecha_inicio_segunda))

        if self.fecha_fin_primera is not None and self.fecha_fin_segunda is not None:
            query = query & Q(fechaTermino__range=(self.fecha_fin_primera, self.fecha_fin_segunda))

        if self.inversion_minima is not None and self.inversion_maxima is not None:
            query = query & Q(inversionTotal__range=(self.inversion_minima, self.inversion_maxima))

        if self.dependencias is not None:
            query = query & Q(dependencia__id__in=self.dependencias)

        if self.estados is not None:
            query = query & Q(estado__id__in=self.estados)

        if self.clasificaciones is not None:
            query = query & Q(tipoClasificacion__id__in=self.clasificaciones)

        if self.inversiones is not None:
            query = query & Q(tipoInversion__id__in=self.inversiones)

        if self.inauguradores is not None:
            query = query & Q(inaugurador__id__in=self.inauguradores)

        if self.inaugurada is not None:
            query = query & Q(inaugurada=self.inaugurada)

        if self.impactos is not None:
            query = query & Q(impacto__id__in=self.impactos)

        if self.denominacion is not None:
            query = query & Q(denominacion__contains=self.denominacion)

        if query is not None:
            obras = Obra.objects.filter(
                query
            )
        print obras