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
            instancia_ejecutora,
            limite_min,
            limite_max,
            busqueda_rapida,
            id_obra,
            susceptible_inauguracion,
            subclasificacion,
    ):
        self.clasificaciones = clasificaciones
        self.estados = estados
        self.inaugurada = inaugurada
        self.susceptible_inauguracion = susceptible_inauguracion
        self.impactos = impactos
        self.idTipoObra = idtipoobra
        self.dependencias = iddependencias
        self.inversiones = inversiones
        self.inauguradores = inauguradores
        self.inversion_minima = inversion_minima
        self.inversion_maxima = inversion_maxima
        self.id_obra = id_obra
        self.subclasificacion = subclasificacion

        self.fecha_inicio_primera = fecha_inicio_primera
        self.fecha_inicio_segunda = fecha_inicio_segunda
        self.fecha_fin_primera = fecha_fin_primera
        self.fecha_fin_segunda = fecha_fin_segunda

        self.denominacion = denominacion
        self.instancia_ejecutora = instancia_ejecutora
        self.limite_min = limite_min
        self.limite_max = limite_max

        self.busqueda_rapida = busqueda_rapida

    def buscar(self):

        query = Q(dependencia__id__in=self.dependencias) | Q(subdependencia__id__in=self.dependencias)

        if self.id_obra is not None:
            query = query & Q(identificador_unico=self.id_obra)
        elif self.busqueda_rapida is not None:
            query = query & Q(denominacion__icontains=self.busqueda_rapida) | Q(descripcion__icontains=self.busqueda_rapida)
        elif self.denominacion is not None:
            query = query & Q(denominacion__icontains=self.denominacion)

        else:

            if self.idTipoObra is not None:
                query = query & Q(tipoObra__id__in=self.idTipoObra)

            if self.fecha_inicio_primera is not None and self.fecha_inicio_segunda is not None:
                query = query & Q(fechaInicio__range=(self.fecha_inicio_primera, self.fecha_inicio_segunda))

            if self.fecha_fin_primera is not None and self.fecha_fin_segunda is not None:
                query = query & Q(fechaTermino__range=(self.fecha_fin_primera, self.fecha_fin_segunda))

            if self.inversion_minima is not None and self.inversion_maxima is not None:
                query = query & Q(inversionTotal__range=(self.inversion_minima, self.inversion_maxima))

            if self.estados is not None:
                query = query & Q(estado__id__in=self.estados)

            if self.clasificaciones is not None:
                query = query & Q(detalleclasificacion__tipoClasificacion__id__in=self.clasificaciones)

            if self.inversiones is not None:
                query = query & Q(tipoInversion__id__in=self.inversiones)

            if self.inauguradores is not None:
                query = query & Q(inaugurador__id__in=self.inauguradores)

            if self.inaugurada is not None:
                query = query & Q(inaugurada=self.inaugurada)

            if self.susceptible_inauguracion is not None:
                query = query & Q(susceptibleInauguracion=self.susceptible_inauguracion)

            if self.impactos is not None:
                query = query & Q(impacto__id__in=self.impactos)

            if self.instancia_ejecutora is not None:
                query = query & Q(instanciaEjecutora__id__in=self.instancia_ejecutora)

            if self.subclasificacion is not None:
                query = query & Q(detalleclasificacion__subclasificacion__id__in=self.subclasificacion)

        if query is not None:
            print query
            obras = Obra.objects.filter(query)
            obras = obras.order_by('identificador_unico')


        # Reporte general
        obras_totales = obras.count()
        total_invertido = obras.aggregate(Sum('inversionTotal'))

        #Reporte Dependencia
        reporte_dependencia = obras.values('dependencia__nombreDependencia','dependencia__orden_secretaria').annotate(
            numero_obras=Count('dependencia')).annotate(sumatotal=Sum('inversionTotal'))
        reporte_dependencia = reporte_dependencia.order_by('dependencia__orden_secretaria')

        #Reporte SubDependencia
        reporte_subdependencia = obras.values('dependencia__nombreDependencia','dependencia__orden_secretaria',
                                              'subdependencia__nombreDependencia').annotate(
            numero_obras=Count('dependencia')).annotate(sumatotal=Sum('inversionTotal'))

        reporte_subdependencia = reporte_subdependencia.order_by('subdependencia__nombreDependencia')

        #Reporte Estado
        reporte_estado = obras.values('estado__nombreEstado').annotate(numero_obras=Count('estado')).annotate(
            sumatotal=Sum('inversionTotal'))
        reporte_estado = reporte_estado.order_by('estado__nombreEstado')

        reporte_general = {
            'obras_totales': obras_totales,
            'total_invertido': total_invertido,
        }

        reportes = {
            'obras': obras[self.limite_min:self.limite_max],
            'reporte_general': reporte_general,
            'reporte_dependencia': reporte_dependencia,
            'reporte_estado': reporte_estado,
            'reporte_subdependencia': reporte_subdependencia,
        }

        return reportes


class BuscaObra:
    def __init__(
            self,
            identificador_unico,
    ):

        self.identificador_unico = identificador_unico


    def busca(self):
        obra_id = None
        query = Q()
        queryInversion = Q()
        queryClasificacion = Q()

        if self.identificador_unico is not None:
            query = Q(identificador_unico=self.identificador_unico)

        if query is not None:
            # print query
            obras = Obra.objects.filter(query)
            if obras and obras.count() > 0:
                obra_id = obras.first().id
                queryInversion = Q(obra__id=obra_id)
                queryClasificacion = Q(obra__id=obra_id)
                DInversion = DetalleInversion.objects.filter(queryInversion)
                DClasificacion = DetalleClasificacion.objects.filter(queryClasificacion).values('tipoClasificacion__id',
                                                                                                'subclasificacion__nombreTipoClasificacion')

        reporte = {
            'obras': obras,
            'DInversion': DInversion,
            'DClasificacion': DClasificacion,
        }

        return reporte