__author__ = 'pedrocontreras'
import datetime

from django.db.models import Q
from django.db.models import Sum

from obras.models import *


class Reportes:
    def balance_general(self):
        start_date = datetime.date(2012, 12, 01)
        end_date = datetime.date(2013, 12, 31)
        obras2013 = Obra.objects.filter(
            Q(fechaTermino__range=(start_date, end_date)),
            Q(tipoObra=3)
        )

        total_obras_2013 = obras2013.count()
        total_invertido_2013 = obras2013.aggregate(Sum('inversionTotal'))

        print 'Total Obras 2013: ' + str(total_obras_2013)
        print 'Total Invertido 2013: ' + str(total_invertido_2013)

        start_date = datetime.date(2014, 01, 01)
        end_date = datetime.date(2014, 12, 31)
        obras2014 = Obra.objects.filter(
            Q(fechaTermino__range=(start_date, end_date)),
            Q(tipoObra=3)
        )

        total_obras_2014 = obras2014.count()
        total_invertido_2014 = obras2014.aggregate(Sum('inversionTotal'))

        print 'Total Obras 2014: ' + str(total_obras_2014)
        print 'Total Invertido 2014: ' + str(total_invertido_2014)

        obras_proceso = Obra.objects.filter(
            Q(tipoObra=2)
        )

        total_obras_proceso = obras_proceso.count()
        total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

        print 'Total Obras Proceso: ' + str(total_obras_proceso)
        print 'Total Invertido Proceso: ' + str(total_invertido_proceso)

        obras_proyectadas = Obra.objects.filter(
            Q(tipoObra=1)
        )

        total_obras_proyectadas = obras_proceso.count()
        total_invertido_proyectadas = obras_proceso.aggregate(Sum('inversionTotal'))

        print 'Total Obras Proyectadas: ' + str(total_obras_proyectadas)
        print 'Total Invertido Proyectadas: ' + str(total_invertido_proyectadas)

        total_obras = total_obras_2013 + total_obras_2014 + total_obras_proceso + total_obras_proyectadas
        # total_invertido = total_invertido_2013.get('inversionTotal__sum') + total_invertido_2014.get('inversionTotal__sum') + total_invertido_proceso.get('inversionTotal__sum') + total_invertido_proyectadas.get('inversionTotal__sum')

    def hipervinculo_informacion_general(self):

        obras_concluidas = Obra.objects.filter(
            Q(tipoObra=3)
        )

        obras_proceso = Obra.objects.filter(
            Q(tipoObra=2)
        )

        obras_proyectadas = Obra.objects.filter(
            Q(tipoObra=1)
        )

        total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))
        total_invertido_concluidas = obras_concluidas.aggregate(Sum('inversionTotal'))

        print 'Total Obras Proyectadas: ' + str(obras_proyectadas.count())
        print 'Total Invertido Proyectadas: ' + str(total_invertido_proyectadas)

        print 'Total Obras Proceso: ' + str(obras_proceso.count())
        print 'Total Invertido Proceso: ' + str(total_invertido_proceso)

        print 'Total Obras Concluidas: ' + str(obras_concluidas.count())
        print 'Total Invertido Concluidas: ' + str(total_invertido_concluidas)

    def hipervinculo_por_sector(self):

        start_date_2013 = datetime.date(2012, 12, 01)
        end_date_2013 = datetime.date(2013, 12, 31)

        start_date_2014 = datetime.date(2014, 01, 01)
        end_date_2014 = datetime.date(2014, 12, 31)

        for dependencia in Dependencia.objects.all():
            print dependencia.nombreDependencia

            obras_2013_concluidas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2013, end_date_2013)),
                Q(tipoObra=3),
                Q(dependencia=dependencia),
            )

            obras_2014_concluidas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2014, end_date_2014)),
                Q(tipoObra=3),
                Q(dependencia=dependencia),
            )

            obras_2014_proceso = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2014, end_date_2014)),
                Q(tipoObra=2),
                Q(dependencia=dependencia),
            )

            obras_2014_proyectadas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2014, end_date_2014)),
                Q(tipoObra=1),
                Q(dependencia=dependencia),
            )

            total_obras_concluidas_2013 = obras_2013_concluidas.count()
            total_obras_concluidas_2014 = obras_2014_concluidas.count()
            total_obras_proceso = obras_2014_proceso.count()
            total_obras_proyectadas = obras_2014_proyectadas.count()

            total_invertido_2013 = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
            total_invertido_2014 = obras_2014_concluidas.aggregate(Sum('inversionTotal'))
            total_invertido_proceso = obras_2014_proceso.aggregate(Sum('inversionTotal'))
            total_invertido_proyectadas = obras_2014_proyectadas.aggregate(Sum('inversionTotal'))

            print 'total_obras_concluidas_2013: ' + str(total_obras_concluidas_2013)
            print 'total_obras_concluidas_2014: ' + str(total_obras_concluidas_2014)
            print 'total_obras_proceso: ' + str(total_obras_proceso)
            print 'total_obras_proyectadas: ' + str(total_obras_proyectadas)

            print 'total_invertido_2013: ' + str(total_invertido_2013)
            print 'total_invertido_2014: ' + str(total_invertido_2014)
            print 'total_invertido_proceso: ' + str(total_invertido_proceso)
            print 'total_invertido_proyectadas: ' + str(total_invertido_proyectadas)

    def hipervinculo_por_entidad(self):

        start_date_2013 = datetime.date(2012, 12, 01)
        end_date_2013 = datetime.date(2013, 12, 31)

        start_date_2014 = datetime.date(2014, 01, 01)
        end_date_2014 = datetime.date(2014, 12, 31)

        start_date_2015 = datetime.date(2015, 01, 01)
        end_date_2015 = datetime.date(2015, 12, 31)

        start_date_2016 = datetime.date(2016, 01, 01)
        end_date_2016 = datetime.date(2016, 12, 31)

        start_date_2017 = datetime.date(2017, 01, 01)
        end_date_2017 = datetime.date(2017, 12, 31)

        start_date_2018 = datetime.date(2018, 01, 01)
        end_date_2018 = datetime.date(2018, 12, 31)

        for estado in Estado.objects.all():
            print estado.nombreEstado

            obras_2013_concluidas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2013, end_date_2013)),
                Q(tipoObra=3),
                Q(estado=estado),
            )

            obras_2014_concluidas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2014, end_date_2014)),
                Q(tipoObra=3),
                Q(estado=estado),
            )

            obras_proceso = Obra.objects.filter(
                Q(tipoObra=2),
                Q(estado=estado),
            )

            obras_2014_proyectadas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2014, end_date_2014)),
                Q(tipoObra=1),
                Q(estado=estado),
            )

            obras_2015_proyectadas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2015, end_date_2015)),
                Q(tipoObra=1),
                Q(estado=estado),
            )

            obras_2016_proyectadas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2016, end_date_2016)),
                Q(tipoObra=1),
                Q(estado=estado),
            )

            obras_2017_proyectadas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2017, end_date_2017)),
                Q(tipoObra=1),
                Q(estado=estado),
            )

            obras_2018_proyectadas = Obra.objects.filter(
                Q(fechaTermino__range=(start_date_2018, end_date_2018)),
                Q(tipoObra=1),
                Q(estado=estado),
            )

            total_obras_concluidas_2013 = obras_2013_concluidas.count()
            total_obras_concluidas_2014 = obras_2014_concluidas.count()
            total_obras_proceso = obras_proceso.count()
            total_obras_proyectadas_2014 = obras_2014_proyectadas.count()
            total_obras_proyectadas_2015 = obras_2015_proyectadas.count()
            total_obras_proyectadas_2016 = obras_2016_proyectadas.count()
            total_obras_proyectadas_2017 = obras_2017_proyectadas.count()
            total_obras_proyectadas_2018 = obras_2018_proyectadas.count()

            total_invertido_2013_concluidas = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
            total_invertido_2014_concluidas = obras_2014_concluidas.aggregate(Sum('inversionTotal'))
            total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

            total_invertido_proyectadas_2014 = obras_2014_proyectadas.aggregate(Sum('inversionTotal'))
            total_invertido_proyectadas_2015 = obras_2015_proyectadas.aggregate(Sum('inversionTotal'))
            total_invertido_proyectadas_2016 = obras_2016_proyectadas.aggregate(Sum('inversionTotal'))
            total_invertido_proyectadas_2017 = obras_2017_proyectadas.aggregate(Sum('inversionTotal'))
            total_invertido_proyectadas_2018 = obras_2018_proyectadas.aggregate(Sum('inversionTotal'))

            print 'total_obras_concluidas_2013: ' + str(total_obras_concluidas_2013)
            print 'total_obras_concluidas_2014: ' + str(total_obras_concluidas_2014)
            print 'total_obras_proceso: ' + str(total_obras_proceso)
            print 'total_obras_proyectadas_2014: ' + str(total_obras_proyectadas_2014)
            print 'total_obras_proyectadas_2015: ' + str(total_obras_proyectadas_2015)
            print 'total_obras_proyectadas_2016: ' + str(total_obras_proyectadas_2016)
            print 'total_obras_proyectadas_2017: ' + str(total_obras_proyectadas_2017)
            print 'total_obras_proyectadas_2018: ' + str(total_obras_proyectadas_2018)

            print 'total_invertido_2013_concluidas: ' + str(total_invertido_2013_concluidas)
            print 'total_invertido_2014_concluidas: ' + str(total_invertido_2014_concluidas)
            print 'total_invertido_proceso: ' + str(total_invertido_proceso)
            print 'total_invertido_proyectadas_2014: ' + str(total_invertido_proyectadas_2014)
            print 'total_invertido_proyectadas_2015: ' + str(total_invertido_proyectadas_2015)
            print 'total_invertido_proyectadas_2016: ' + str(total_invertido_proyectadas_2016)
            print 'total_invertido_proyectadas_2017: ' + str(total_invertido_proyectadas_2017)
            print 'total_invertido_proyectadas_2018: ' + str(total_invertido_proyectadas_2018)

    def hipervinculo_concluidas_proceso_proyectadas(self):

        start_date_2013 = datetime.date(2012, 12, 01)
        end_date_2013 = datetime.date(2013, 12, 31)

        start_date_2014 = datetime.date(2014, 01, 01)
        end_date_2014 = datetime.date(2014, 12, 31)

        obras_2013_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2013, end_date_2013)),
            Q(tipoObra=3),
        )

        obras_2014_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=3),
        )

        total_obras_concluidas_2013 = obras_2013_concluidas.count()
        total_invertido_2013_concluidas = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
        total_obras_concluidas_2014 = obras_2014_concluidas.count()
        total_invertido_2014_concluidas = obras_2014_concluidas.aggregate(Sum('inversionTotal'))

        print 'total_obras_concluidas_2013: ' + str(total_obras_concluidas_2013)
        print 'total_invertido_2013_concluidas: ' + str(total_invertido_2013_concluidas)
        print 'total_obras_concluidas_2014: ' + str(total_obras_concluidas_2014)
        print 'total_invertido_2014_concluidas: ' + str(total_invertido_2014_concluidas)

        obras_proceso = Obra.objects.filter(
            Q(tipoObra=2),
        )

        obras_totales_proceso = obras_proceso.count()
        total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

        print 'obras_totales_proceso: ' + str(obras_totales_proceso)
        print 'total_invertido_proceso: ' + str(total_invertido_proceso)

        obras_proyectadas = Obra.objects.filter(
            Q(tipoObra=1),
        )

        obras_totales_proyectadas = obras_proyectadas.count()
        total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))

        print 'obras_totales_proyectadas: ' + str(obras_totales_proyectadas)
        print 'total_invertido_proyectadas: ' + str(total_invertido_proyectadas)