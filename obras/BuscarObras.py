__author__ = 'Pedro'
from django.db.models import Q
from django.db.models import Count, Sum
from obras.models import *


class BuscarObras:
    def __init__(
            self,
            idtipoobra,
            iddependencias,
            estados,
            clasificaciones,
            inversiones,
            inauguradores,
            impactos,
            inaugurada,
            inversion_minima,
            inversion_maxima,
            fecha_inicio_primera,
            fecha_inicio_segunda,
            fecha_fin_primera,
            fecha_fin_segunda,
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
            print query
            obras = Obra.objects.filter(
                query
            )

        #Reporte general
        obras_totales = obras.count()
        total_invertido = obras.aggregate(Sum('inversionTotal'))

        #Reporte Dependencia
        reporte_dependencia = Obra.objects.values('dependencia__nombreDependencia').annotate(numero_obras=Count('dependencia')).annotate(sumatotal=Sum('inversionTotal'))

        #Reporte Estado
        reporte_estado = Obra.objects.values('estado__nombreEstado').annotate(numero_obras=Count('estado')).annotate(sumatotal=Sum('inversionTotal'))

        reporte_general = {
            'obras_totales':obras_totales,
            'total_invertido': total_invertido,
        }

        reportes = {
            'obras': obras,
            'reporte_general': reporte_general,
            'reporte_dependencia': reporte_dependencia,
            'reporte_estado': reporte_estado,
        }

        return reportes

    def buscar_alt(self):

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
            print query
            obras = Obra.objects.filter(
                query
            )

        #Reporte general
        obras_totales = obras.count()
        total_invertido = 100

        #Reporte Dependencia
        reporte_dependencia = Obra.objects.annotate(numero_obras=200).annotate(sumatotal=100)

        #Reporte Estado
        reporte_estado = Obra.objects.values('estado__nombreEstado').annotate(numero_obras=Count('estado')).annotate(sumatotal=Sum('inversionTotal'))

        reporte_general = {
            'obras_totales':obras_totales,
            'total_invertido': total_invertido,
        }

        reportes = {
            'obras': obras,
            'reporte_general': reporte_general,
            'reporte_dependencia': reporte_dependencia,
            'reporte_estado': reporte_estado,
        }

        return reportes