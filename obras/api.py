import json
import datetime
from django.db.models import Q
from django.http import HttpResponse
from oauth2_provider.models import AccessToken
from oauth2_provider.views import ProtectedResourceView
from obras.BuscarObras import BuscarObras
from obras.models import Obra, Estado, Dependencia, Impacto, TipoClasificacion, TipoInversion, TipoObra, Inaugurador
from obras.views import get_array_or_none


class HoraEndpoint(ProtectedResourceView):
    def get(self, request):
        json_response = {}
        date = datetime.datetime.now()
        time = date.time()

        json_response['dia'] = date.day
        json_response['mes'] = date.month
        json_response['ano'] = date.year

        json_response['hora'] = time.hour
        json_response['minuto'] = time.minute
        json_response['segundo'] = time.second

        return HttpResponse(json.dumps(json_response), 'application/json')


class ObrasIniciadasEndpoint(ProtectedResourceView):
    def get(self, request):
        today = datetime.datetime.now().date()
        obras = Obra.objects.filter(Q(fechaInicio__lte=today)).all()

        return HttpResponse(json.dumps(map(lambda obra: obra.to_serializable_dict(), obras)), 'application/json')


class ObrasVencidasEndpoint(ProtectedResourceView):
    def get(self, request):
        today = datetime.datetime.now().date()
        obras = Obra.objects.filter(Q(fechaTermino__lte=today))

        return HttpResponse(json.dumps(map(lambda obra: obra.to_serializable_dict(), obras)), 'application/json')


class DependenciasEndpoint(ProtectedResourceView):
    def get(self, request):
        token = request.GET.get('access_token')
        print '*************' + token
        token_model = AccessToken.objects.get(token=token)
        print token_model.user

        if token_model.user.usuario.rol == 'SA':
            dicts = map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.all())

        elif token_model.user.usuario.rol == 'AD':
            dicts = map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.filter(
                Q(id=token_model.user.usuario.dependencia.id) |
                Q(dependienteDe__id=token_model.user.usuario.dependencia.id))
                        )

        else:
            dicts = map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.filter(
                Q(id=token_model.user.usuario.dependencia.id))
                        )

        return HttpResponse(json.dumps(dicts), 'application/json')


class ImpactosEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda impacto: impacto.to_serializable_dict(), Impacto.objects.all())),
                            'application/json')


class EstadosEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda estado: estado.to_serializable_dict(), Estado.objects.all())),
                            'application/json')


class DependenciasTreeEndpoint(ProtectedResourceView):
    def get(self, request):
        token = request.GET.get('access_token')
        token_model = AccessToken.objects.get(token=token)

        if request.GET.get('id', None):
            dependencia_id = request.GET.get('id')
        else:
            dependencia_id = token_model.user.usuario.dependencia_id

        dependencia = Dependencia.objects.get(id=dependencia_id)
        ans = dependencia.get_tree()

        return HttpResponse(json.dumps(ans), 'application/json')


class ClasificacionEndpoint(ProtectedResourceView):
    def get(self, request):
        if request.GET.get('id', False):
            clasificaciones = TipoClasificacion.objects.filter(subclasificacionDe_id=1)
        else:
            clasificaciones = TipoClasificacion.objects.filter(subclasificacionDe_id__isnull=True)

        return HttpResponse(
            json.dumps(map(lambda clasificacion: clasificacion.to_serializable_dict(), clasificaciones)),
            "application/json")


class InversionEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(
            json.dumps(map(lambda inversion: inversion.to_serializable_dict(), TipoInversion.objects.all())),
            'application/json')


class TipoDeObraEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda tipo: tipo.to_serializable_dict(), TipoObra.objects.all())),
                            'application/json')


class BuscadorEndpoint(ProtectedResourceView):
    def get(self, request):
        buscador = BuscarObras(idtipoobra=get_array_or_none(request.GET.get('tipoDeObra')),
                               iddependencias=get_array_or_none(request.GET.get('tipoDeObra')),
                               estados=get_array_or_none(request.GET.get('tipoDeObra')),
                               clasificaciones=get_array_or_none(request.GET.get('tipoDeObra')),
                               inversiones=get_array_or_none(request.GET.get('tipoDeObra')),
                               inauguradores=get_array_or_none(request.GET.get('tipoDeObra')),
                               impactos=get_array_or_none(request.GET.get('tipoDeObra')),
                               inaugurada=None,
                               inversion_minima=None,
                               inversion_maxima=None,
                               fecha_inicio_primera=None,
                               fecha_inicio_segunda=None,
                               fecha_fin_primera=None,
                               fecha_fin_segunda=None,
                               denominacion=None,
                               )
        resultados = buscador.buscar()

        json_map = {}
        json_map['reporte_dependencia'] = []
        for reporte in resultados['reporte_dependencia']:
            map = {}
            map['dependencia'] = Dependencia.objects.get(
                nombreDependencia=reporte['dependencia__nombreDependencia']).to_serializable_dict()
            map['numero_obras'] = reporte['numero_obras']
            if reporte['sumatotal'] is None:
                map['sumatotal'] = 0
            else:
                map['sumatotal'] = int(reporte['sumatotal'])
            json_map['reporte_dependencia'].append(map)

        json_map['obras'] = []
        for obra in resultados['obras']:
            json_map['obras'].append(obra.to_serializable_dict())

        json_map['reporte_estado'] = []
        for reporte_estado in resultados['reporte_estado']:
            map = {}
            if reporte_estado['sumatotal'] is None:
                map['sumatotal'] = 0.0
            else:
                map['sumatotal'] = float(reporte_estado['sumatotal'])
            map['estado'] = Estado.objects.get(
                nombreEstado=reporte_estado['estado__nombreEstado']).to_serializable_dict()
            map['numeroObras'] = reporte_estado['numero_obras']

            json_map['reporte_estado'].append(map)

        json_map['reporte_general'] = []
        map = {}
        total = resultados['reporte_general']['total_invertido']['inversionTotal__sum']
        if total is None:
            total = 0.0
        else:
            total = float(total)
        map['total_invertido'] = total

        map['obras_totales'] = resultados['reporte_general']['obras_totales']
        json_map['reporte_general'].append(map)

        return HttpResponse(json.dumps(json_map), 'application/json')


class InauguradorEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(
            json.dumps(map(lambda inaugurador: inaugurador.to_serializable_dict(), Inaugurador.objects.all())),
            'application/json')


class ReporteInicioEndpoint(ProtectedResourceView):
    def get(self, request):
        dependencia = AccessToken.objects.get(
            token=request.GET.get('access_token')).token_model.user.usuario.dependencia
        obras = dependencia.get_obras()
        start2015 = datetime.date(2015, 1, 1)
        reporte = {
            'reporte2015': {'obras_proceso': {}, 'obras_proyectadas': {}, 'obras_concluidas': {}},
            'reporte2014': {'obras_concluidas': {}},
            'reporte2013': {'obras_concluidas': {}},
            'reporte2012': {'obras_concluidas': {}},
        }

        reporte['reporte2015']['obras_proceso']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(Q(fechaInicio__lte=start2015) & Q(fechaTermino__gte=start2015)))
        reporte['reporte2015']['obras_proceso']['total'] = len(reporte['reporte2015']['obras_proceso']['obras'])

        reporte['reporte2015']['obras_proyectadas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaInicio__year=2015))
        reporte['reporte2015']['obras_proyectadas']['total'] = len(reporte['reporte2015']['obras_proyectadas']['obras'])

        reporte['reporte2015']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2015))
        reporte['reporte2015']['obras_concluidas']['total'] = len(reporte['reporte2015']['obras_concluidas']['obras'])

        reporte['reporte2014']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2014))
        reporte['reporte2014']['obras_concluidas']['total'] = len(reporte['reporte2014']['obras_concluidas']['obras'])

        reporte['reporte2013']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2013))
        reporte['reporte2013']['obras_concluidas']['total'] = len(reporte['reporte2013']['obras_concluidas']['obras'])

        reporte['reporte2012']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2012))
        reporte['reporte2012']['obras_concluidas']['total'] = len(reporte['reporte2012']['obras_concluidas']['obras'])

        # reporte2015 = {
        #     'obras_proceso': map(lambda obra: obra.to_serializable_dict(), obras.filter(Q(fechaInicio__lte=start2015) & Q(fechaTermino__gte=start2015))),
        #     'obras_proyectadas': map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaInicio__year=2015)),
        #     'obras_concluidas': map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2015))
        # }

        # reporte2012 = {'obras_concluidas': obras.filter(fechaTermino__year=2012)}
        # reporte2013 = {'obras_concluidas': obras.filter(fechaTermino__year=2013)}
        # reporte2014 = {'obras_concluidas': obras.filter(fechaTermino__year=2014)}

        return HttpResponse(json.dumps(reporte), 'application/json')


def inicio(request):
    # dependencia = AccessToken.objects.get(
    # token=request.GET.get('access_token')).token_model.user.usuario.dependencia
    dependencia = Dependencia.objects.first()
    obras = dependencia.get_obras()
    start2015 = datetime.date(2015, 1, 1)
    reporte = {
        'reporte2015': {'obras_proceso': {}, 'obras_proyectadas': {}, 'obras_concluidas': {}},
        'reporte2014': {'obras_concluidas': {}},
        'reporte2013': {'obras_concluidas': {}},
        'reporte2012': {'obras_concluidas': {}},
    }

    reporte['reporte2015']['obras_proceso']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(Q(fechaInicio__lte=start2015) & Q(fechaTermino__gte=start2015)))
    reporte['reporte2015']['obras_proceso']['total'] = len(reporte['reporte2015']['obras_proceso']['obras'])

    reporte['reporte2015']['obras_proyectadas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaInicio__year=2015))
    reporte['reporte2015']['obras_proyectadas']['total'] = len(reporte['reporte2015']['obras_proyectadas']['obras'])

    reporte['reporte2015']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2015))
    reporte['reporte2015']['obras_concluidas']['total'] = len(reporte['reporte2015']['obras_concluidas']['obras'])

    reporte['reporte2014']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2014))
    reporte['reporte2014']['obras_concluidas']['total'] = len(reporte['reporte2014']['obras_concluidas']['obras'])

    reporte['reporte2013']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2013))
    reporte['reporte2013']['obras_concluidas']['total'] = len(reporte['reporte2013']['obras_concluidas']['obras'])

    reporte['reporte2012']['obras_concluidas']['obras'] = map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2012))
    reporte['reporte2012']['obras_concluidas']['total'] = len(reporte['reporte2012']['obras_concluidas']['obras'])

    # reporte2015 = {
    #     'obras_proceso': map(lambda obra: obra.to_serializable_dict(), obras.filter(Q(fechaInicio__lte=start2015) & Q(fechaTermino__gte=start2015))),
    #     'obras_proyectadas': map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaInicio__year=2015)),
    #     'obras_concluidas': map(lambda obra: obra.to_serializable_dict(), obras.filter(fechaTermino__year=2015))
    # }

    # reporte2012 = {'obras_concluidas': obras.filter(fechaTermino__year=2012)}
    # reporte2013 = {'obras_concluidas': obras.filter(fechaTermino__year=2013)}
    # reporte2014 = {'obras_concluidas': obras.filter(fechaTermino__year=2014)}

    return HttpResponse(json.dumps(reporte), 'application/json')