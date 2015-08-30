import json
from datetime import *
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q
from django.http import HttpResponse
from oauth2_provider.models import AccessToken
from oauth2_provider.views import ProtectedResourceView
from django.db.models import Count

from obras.BuscarObras import BuscarObras
from obras.models import Obra, Estado, Dependencia, Impacto, TipoClasificacion, TipoInversion, TipoObra, Inaugurador, \
    InstanciaEjecutora, get_subdependencias_as_list_flat
from obras.views import get_array_or_none


try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from xlsxwriter.workbook import Workbook
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse


def get_usuario_for_token(token):
    if token:
        return AccessToken.objects.get(token=token).user.usuario
    else:
        return None


class HoraUltimaActualizacion(ProtectedResourceView):
    def get(self, request):
        json_response = {}
        date = LogEntry.objects.filter(
            action_flag=ADDITION,
            content_type__id__exact=ContentType.objects.get_for_model(Obra).id
        ).order_by('action_time').last().action_time

        json_response['dia'] = date.day
        json_response['mes'] = date.month
        json_response['ano'] = date.year

        time = date.time
        json_response['hora'] = time.hour
        json_response['minuto'] = time.minute
        json_response['segundo'] = time.second


class HoraEndpoint(ProtectedResourceView):
    def get(self, request):
        json_response = {}
        date = datetime.now()
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
        usuario = get_usuario_for_token(request.GET.get('access_token'))

        query = Q(fechaInicio__lte=datetime.now().date()) & Q(tipoObra_id=1)
        if not (usuario.rol == 'SA'):
            subdependencias = get_subdependencias_as_list_flat(usuario.dependencia.all())
            query = query & (Q(dependencia__in=subdependencias) | Q(subdependencia__in=subdependencias))
        obras = Obra.objects.filter(query)

        json_ans = '['
        for obra in obras.values('id', 'identificador_unico', 'estado__nombreEstado', 'denominacion'):
            json_ans += '{"id":"'
            json_ans += str(obra['id'])

            json_ans += '","identificador_unico":"'
            json_ans += obra['identificador_unico']

            json_ans += '","estado__nombreEstado":"'
            json_ans += obra['estado__nombreEstado']

            json_ans += '","denominacion":"'
            json_ans += obra['denominacion']

            json_ans += '"},'
        json_ans = json_ans[:-1]
        json_ans += ']'

        return HttpResponse(json_ans, 'application/json')


class ObrasVencidasEndpoint(ProtectedResourceView):
    def get(self, request):
        usuario = get_usuario_for_token(request.GET.get('access_token'))

        query = Q(fechaTermino__lte=datetime.now().date()) & Q(tipoObra_id=2)
        if not usuario.rol == 'SA':
            subdependencias = get_subdependencias_as_list_flat(usuario.dependencia.all())
            query = query & (Q(dependencia__in=subdependencias) | Q(subdependencia__in=subdependencias))
        obras = Obra.objects.filter(query)

        the_list = []
        for obra in obras.values('id', 'identificador_unico', 'estado__nombreEstado', 'denominacion'):
            the_list.append(obra)

        return HttpResponse(json.dumps(the_list), 'application/json')


class ObrasForDependenciaEndpoint(ProtectedResourceView):
    def get(self, request):
        usuario = get_usuario_for_token(request.GET.get('access_token'))

        if usuario.rol == 'SA':
            obras = Obra.objects.all()
        else:
            obras = Obra.filter(dependencia__in=get_subdependencias_as_list_flat(usuario.dependencia.all()))

        the_list = []
        for obra in obras.values('id', 'identificador_unico', 'estado__nombreEstado', 'denominacion'):
            the_list.append(obra)

        return HttpResponse(json.dumps(the_list), 'application/json')


class DependenciasEndpoint(ProtectedResourceView):
    def get(self, request):
        token = request.GET.get('access_token')
        token_model = AccessToken.objects.get(token=token)

        if token_model.user.usuario.rol == 'SA':
            dicts = map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.filter(
                Q(obraoprograma='O')
            )
                        )

        elif token_model.user.usuario.rol == 'AD':
            dicts = map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.filter(
                Q(id__in=token_model.user.usuario.dependencia.all()) |
                Q(dependienteDe__in=token_model.user.usuario.dependencia.all()))
                        )
        else:
            dicts = map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.filter(
                Q(id__in=token_model.user.usuario.subdependencia.all()))
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
        usuario = get_usuario_for_token(request.GET.get('access_token'))

        if usuario.rol == 'SA':
            dependencias = Dependencia.objects.all()
        else:
            dependencias = usuario.dependencia.all()

        ans = []
        for dep in dependencias:
            ans.append(dep.get_tree())

        return HttpResponse(json.dumps(ans), 'application/json')


class DependenciasIdEndpoint(ProtectedResourceView):
    def get(self, request):
        usuario = get_usuario_for_token(request.GET.get('access_token'))
        idDep = request.GET.get('id')

        dependencias = Dependencia.objects.filter(id=idDep).all()

        ans = []
        for dep in dependencias:
            ans.append(dep.get_tree())

        return HttpResponse(json.dumps(ans), 'application/json')


class SubependenciasFlatEndpoint(ProtectedResourceView):
    def get(self, request):
        usuario = get_usuario_for_token(request.GET.get('access_token'))

        if usuario.rol == 'SA':
            dependencias = Dependencia.objects.all()
        else:
            dependencias = usuario.dependencia.all()

        ans = map(lambda dependencia: dependencia.to_serializable_dict(), dependencias)
        for dependencia in dependencias:
            subdeps = dependencia.get_subdeps_flat()
            if subdeps:
                ans.extend(map(lambda dep: dep.to_serializable_dict(), subdeps))

        return HttpResponse(json.dumps(ans), 'application/json')


class ClasificacionEndpoint(ProtectedResourceView):
    def get(self, request):
        if request.GET.get('id', False):
            clasificaciones = TipoClasificacion.objects.filter(subclasificacionDe_id=request.GET.get('id'))
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


class InstanciaEjecutoraEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(
            json.dumps(map(lambda instancia: instancia.to_serializable_dict(), InstanciaEjecutora.objects.all())),
            'application/json')


class TipoDeObraEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda tipo: tipo.to_serializable_dict(), TipoObra.objects.all())),
                            'application/json')


class IdUnicoEndpoint(ProtectedResourceView):
    def get(self, request):
        identificador_unico = request.GET.get('identificador_unico', None)
        obra_id = None
        if identificador_unico is not None:
            obra = Obra.objects.filter(identificador_unico=identificador_unico)
            if obra and obra.count() > 0:
                obra_id = obra.first().id

        return HttpResponse(json.dumps({'id': obra_id}), 'application/json')


class IdUnicoEndpointIpad(ProtectedResourceView):
    def get(self, request):
        identificador_unico = request.GET.get('identificador_unico', None)
        return HttpResponse(
            json.dumps(map(lambda obra: obra.to_serializable_dict(),
                           Obra.objects.filter(identificador_unico=identificador_unico))),
            'application/json')


class BuscadorEndpoint(ProtectedResourceView):
    def get(self, request):

        user = AccessToken.objects.get(token=request.GET.get('access_token')).user

        buscador = BuscarObras(
            idtipoobra=get_array_or_none(request.GET.get('tipoDeObra')),
            iddependencias=get_array_or_none(request.GET.get('dependencia')),
            estados=get_array_or_none(request.GET.get('estado')),
            clasificaciones=get_array_or_none(request.GET.get('clasificacion')),
            inversiones=get_array_or_none(request.GET.get('tipoDeInversion')),
            inauguradores=get_array_or_none(request.GET.get('inaugurador')),
            impactos=get_array_or_none(request.GET.get('impacto')),
            inaugurada=request.GET.get('inaugurada', None),
            inversion_minima=request.GET.get('inversionMinima', None),
            inversion_maxima=request.GET.get('inversionMaxima', None),
            fecha_inicio_primera=request.GET.get('fechaInicio', None),
            fecha_inicio_segunda=request.GET.get('fechaInicio', None),
            fecha_fin_primera=request.GET.get('fechaFin', None),
            fecha_fin_segunda=request.GET.get('fechaFinSegunda', None),
            denominacion=request.GET.get('denominacion', None),
            instancia_ejecutora=get_array_or_none(request.GET.get('instanciaEjecutora')),
            limite_min=request.GET.get("limiteMin"),
            limite_max=request.GET.get("limiteMax"),
            busqueda_rapida=request.GET.get("busquedaRapida", None),
            id_obra=request.GET.get("idObra", None),
            susceptible_inauguracion=request.GET.get("susceptible", None),
            subclasificacion=get_array_or_none(request.GET.get('subclasificacion')),

        )

        arreglo_dependencias = []

        if user.usuario.rol == 'SA' and get_array_or_none(request.GET.get('dependencia')) is None:
            buscador.dependencias = None

        elif user.usuario.rol == 'AD' and get_array_or_none(request.GET.get('dependencia')) is None:

            for dependencia in user.usuario.dependencia.all():
                arreglo_dependencias.append(dependencia.id)

            for subdependencia in user.usuario.subdependencia.all():
                arreglo_dependencias.append(subdependencia.id)

            buscador.dependencias = arreglo_dependencias

        elif user.usuario.rol == 'US' and get_array_or_none(request.GET.get('dependencia')) is None:
            for subdependencia in user.usuario.subdependencia.all():
                arreglo_dependencias.append(subdependencia.id)

            buscador.dependencias = arreglo_dependencias

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
                map['sumatotal'] = float(reporte['sumatotal'])
            json_map['reporte_dependencia'].append(map)

        json_map['reporte_subdependencia'] = []
        for reporteSub in resultados['reporte_subdependencia']:
            map = {}
            if reporteSub['subdependencia__nombreDependencia'] is not None:
                map['subdependencia'] = Dependencia.objects.get(
                    nombreDependencia=reporteSub['subdependencia__nombreDependencia']).to_serializable_dict()
            else:
                map['subdependencia'] = Dependencia.objects.get(
                    nombreDependencia=reporteSub['dependencia__nombreDependencia']).to_serializable_dict()
            map['numero_obras'] = reporteSub['numero_obras']
            if reporteSub['sumatotal'] is None:
                map['sumatotal'] = 0
            else:
                map['sumatotal'] = float(reporteSub['sumatotal'])
            json_map['reporte_subdependencia'].append(map)
        # json_map['obras'] = []
        #for obra in resultados['obras']:
        #    json_map['obras'].append(obra.to_serializable_dict())

        json_map['obras'] = []
        for obra in resultados['obras'].values('id', 'identificador_unico', 'estado__nombreEstado', 'denominacion',
                                               'latitud', 'longitud', 'dependencia__imagenDependencia'):
            json_map['obras'].append(obra)

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


class ListarEndpoint(ProtectedResourceView):
    def get(self, request):

        user = AccessToken.objects.get(token=request.GET.get('access_token')).user

        idtipoobra = get_array_or_none(request.GET.get('tipoDeObra')),
        iddependencias = get_array_or_none(request.GET.get('dependencia')),
        estados = get_array_or_none(request.GET.get('estado')),
        clasificaciones = get_array_or_none(request.GET.get('clasificacion')),
        inversiones = get_array_or_none(request.GET.get('tipoDeInversion')),
        inauguradores = get_array_or_none(request.GET.get('inaugurador')),
        impactos = get_array_or_none(request.GET.get('impacto')),
        inaugurada = request.GET.get('inaugurada', None),
        inversion_minima = request.GET.get('inversionMinima', None),
        inversion_maxima = request.GET.get('inversionMaxima', None),
        fecha_inicio_primera = request.GET.get('fechaInicio', None),
        fecha_inicio_segunda = request.GET.get('fechaInicio', None),
        fecha_fin_primera = request.GET.get('fechaFin', None),
        fecha_fin_segunda = request.GET.get('fechaFinSegunda', None),
        denominacion = request.GET.get('denominacion', None),
        instancia_ejecutora = get_array_or_none(request.GET.get('instanciaEjecutora')),
        busqueda_rapida = request.GET.get("busquedaRapida", None),
        id_obra = request.GET.get("idObra", None),
        susceptible_inauguracion = request.GET.get("susceptible", None),
        subclasificacion = get_array_or_none(request.GET.get('subclasificacion')),

        p_tipoobra = ","
        p_estados = ","
        p_clasificaciones = ","
        p_inversiones = ","
        p_inauguradores = ","
        p_impactos = ","
        p_instancia_ejecutora = ","
        p_subclasificacion = ","

        arreglo_dependencias = []
        p_dependencias = ""
        if user.usuario.rol == 'SA' and get_array_or_none(request.GET.get('dependencia')) is None:
            p_dependencias = ","

        elif user.usuario.rol == 'AD' and get_array_or_none(request.GET.get('dependencia')) is None:

            for dependencia in user.usuario.dependencia.all():
                arreglo_dependencias.append(dependencia.id)

            for subdependencia in user.usuario.subdependencia.all():
                arreglo_dependencias.append(subdependencia.id)

            iddependencias = arreglo_dependencias

        elif user.usuario.rol == 'US' and get_array_or_none(request.GET.get('dependencia')) is None:
            for subdependencia in user.usuario.subdependencia.all():
                arreglo_dependencias.append(subdependencia.id)

            iddependencias = arreglo_dependencias

        if iddependencias[0] is not None:
            for dependencia in iddependencias[0]:
                p_dependencias += str(dependencia) + ","

        if idtipoobra[0] is not None:
            p_tipoobra = ""
            for tipoobra in idtipoobra[0]:
                p_tipoobra += str(tipoobra) + ","

        if estados[0] is not None:
            p_estados = ""
            for estado in estados[0]:
                p_estados += str(estado) + ","

        if clasificaciones[0] is not None:
            p_clasificaciones = ""
            for clasificacion in clasificaciones[0]:
                p_clasificaciones += str(clasificacion) + ","

        if inversiones[0] is not None:
            p_inversiones = ""
            for inversion in inversiones[0]:
                p_inversiones += str(inversion) + ","

        if inauguradores[0] is not None:
            p_inauguradores = ""
            for inaugurador in inauguradores[0]:
                p_inauguradores += str(inaugurador) + ","

        if impactos[0] is not None:
            p_impactos = ""
            for impacto in impactos[0]:
                p_impactos += str(impacto) + ","

        if instancia_ejecutora[0] is not None:
            p_instancia_ejecutora = ""
            for instancia in instancia_ejecutora[0]:
                p_instancia_ejecutora += str(instancia) + ","

        p_inaugurada = ""
        p_inversion_minima = 0
        p_inversion_maxima = 999999999.99
        p_fecha_inicio_primera = ""
        p_fecha_inicio_segunda = ""
        p_fecha_fin_primera = ""
        p_fecha_fin_segunda = ""
        p_denominacion = ""

        if inaugurada[0] is None: p_inaugurada = ""
        if inversion_minima[0] is None:
            p_inversion_minima = 0
        else:
            p_inversion_minima = inversion_minima[0]
        if inversion_maxima[0] is None:
            p_inversion_maxima = 999999999.99
        else:
            p_inversion_maxima = inversion_maxima[0]
        if fecha_inicio_primera[0] is None:
            p_fecha_inicio_primera = "1900-01-01"
        else:
            p_fecha_inicio_primera = fecha_inicio_primera[0]
        if fecha_inicio_segunda[0] is None:
            p_fecha_inicio_segunda = "2100-12-31"
        else:
            p_fecha_inicio_segunda = fecha_inicio_segunda[0]
        if fecha_fin_primera[0] is None:
            p_fecha_fin_primera = "1900-01-01"
        else:
            p_fecha_fin_primera = fecha_fin_primera[0]
        if fecha_fin_segunda[0] is None:
            p_fecha_fin_segunda = "2100-12-31"
        else:
            p_fecha_fin_segunda = fecha_fin_segunda[0]
        if denominacion[0] is None:
            p_denominacion = ""
        else:
            p_denominacion = denominacion[0]

        results = Obra.searchList(p_tipoobra[:-1], p_dependencias[:-1], p_instancia_ejecutora[:-1], p_estados[:-1],
                                  p_inversion_minima, p_inversion_maxima, p_fecha_inicio_primera,
                                  p_fecha_inicio_segunda, p_fecha_fin_primera, p_fecha_fin_segunda, p_impactos[:-1],
                                  p_inauguradores[:-1], p_inversiones[:-1], p_clasificaciones[:-1],
                                  "", "", p_denominacion)

        output = StringIO.StringIO()
        book = Workbook(output)
        sheet = book.add_worksheet('obras')

        if results:
            # Add a bold format to use to highlight cells.
            bold = book.add_format({'bold': True})
            # encabezados
            sheet.write(0, 0, "Tipo de Obra", bold)
            sheet.write(0, 1, "id Unico", bold)
            sheet.write(0, 2, "Dependencia/Organismo", bold)
            sheet.write(0, 3, "Estado", bold)
            sheet.write(0, 4, "Denominacion", bold)
            sheet.write(0, 5, "Descripcion", bold)
            sheet.write(0, 6, "Municipio", bold)
            sheet.write(0, 7, "Fecha Inicio", bold)
            sheet.write(0, 8, "Fecha Termino", bold)
            sheet.write(0, 9, "Avance Fisico %", bold)
            sheet.write(0, 10, "F", bold)
            sheet.write(0, 11, "E", bold)
            sheet.write(0, 12, "M", bold)
            sheet.write(0, 13, "S", bold)
            sheet.write(0, 14, "P", bold)
            sheet.write(0, 15, "O", bold)
            sheet.write(0, 16, "Inversion Total", bold)
            sheet.write(0, 17, "Tipo Moneda MDP/MDD", bold)
            sheet.write(0, 18, "Poblacion Objetivo", bold)
            sheet.write(0, 19, "Beneficiarios", bold)
            sheet.write(0, 20, "Impacto", bold)
            sheet.write(0, 21, "CG", bold)
            sheet.write(0, 22, "PNG", bold)
            sheet.write(0, 23, "PM", bold)
            sheet.write(0, 24, "PNI", bold)
            sheet.write(0, 25, "CNCH", bold)
            sheet.write(0, 26, "OI", bold)
            sheet.write(0, 27, "Senalizacion", bold)
            sheet.write(0, 28, "Observaciones", bold)
            sheet.write(0, 29, "Inaugurado por:", bold)
            sheet.write(0, 30, "Susceptible de inaugurar", bold)
            sheet.write(0, 31, "Foto Antes", bold)
            sheet.write(0, 32, "Foto Durante", bold)
            sheet.write(0, 33, "Foto Despues", bold)

            i = 1
            for obra in results:
                id_unico = obra[0]
                sheet.write(i, 0, obra[0])
                sheet.write(i, 1, obra[1])
                sheet.write(i, 2, obra[2])
                sheet.write(i, 3, obra[3])
                sheet.write(i, 4, obra[4])
                sheet.write(i, 5, obra[5])
                sheet.write(i, 6, obra[6])
                sheet.write(i, 7, obra[7])
                sheet.write(i, 8, obra[8])
                sheet.write(i, 9, obra[9])

                sheet.write(i, 10, "NO")  #F
                sheet.write(i, 11, "NO")  #E
                sheet.write(i, 12, "NO")  #M
                sheet.write(i, 13, "NO")  #S
                sheet.write(i, 14, "NO")  #P
                sheet.write(i, 15, "NO")  #O
                for inv in (obra[10].split(',')):
                    if inv[0] == "F": sheet.write(i, 10, "SI")
                    if inv[0] == "E": sheet.write(i, 11, "SI")
                    if inv[0] == "M": sheet.write(i, 12, "SI")
                    if inv[0] == "S": sheet.write(i, 13, "SI")
                    if inv[0] == "P": sheet.write(i, 14, "SI")
                    if inv[0] == "O": sheet.write(i, 15, "SI")

                sheet.write(i, 16, obra[11])
                sheet.write(i, 17, obra[12])
                sheet.write(i, 18, obra[13])
                sheet.write(i, 19, obra[14])
                sheet.write(i, 20, obra[15])

                sheet.write(i, 21, "NO")  #CG
                sheet.write(i, 22, "NO")  #PNG
                sheet.write(i, 23, "NO")  #PM
                sheet.write(i, 24, "NO")  #PNI
                sheet.write(i, 25, "NO")  #CNCH
                sheet.write(i, 26, "NO")  #OI
                if obra[16] is not None:
                    for cla in (obra[16].split(',')):
                        sCla = ''.join(cla)
                        if sCla == 'CG':
                            if obra[17] is not None:
                                for subscla in (obra[17].split(',')):
                                    sSubCla = ''.join(subscla)
                                    if sSubCla[:2] == 'CG': sheet.write(i, 21, sSubCla)
                        if sCla == "PNG": sheet.write(i, 22, "SI")
                        if sCla == "PM": sheet.write(i, 23, "SI")
                        if sCla == "PNI":
                            sheet.write(i, 24, "SI")
                            if obra[17] is not None:
                                for subscla in (obra[17].split(',')):
                                    sSubCla = ''.join(subscla)
                                    if sSubCla[:3] == "PNI": sheet.write(i, 24, sSubCla)
                        if sCla == "CNCH": sheet.write(i, 25, "SI")
                        if sCla == "OI": sheet.write(i, 26, "SI")

                sheet.write(i, 27, obra[18])
                sheet.write(i, 28, obra[19])
                sheet.write(i, 29, obra[20])
                sheet.write(i, 30, obra[21])
                sheet.write(i, 31, obra[22])
                sheet.write(i, 32, obra[23])
                sheet.write(i, 33, obra[24])

                i += 1
            book.close()

            # construct response

            #output.seek(0)
            #response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            #response['Content-Disposition'] = "attachment; filename=test.xlsx"
        else:
            sheet.write(0, 0,
                        "Los filtros seleccionados no arrojaron informacion alguna sobre las obras, cambie los filtros para una nueva consulta.")
            book.close()

        response = StreamingHttpResponse(FileWrapper(output),
                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="listado_obras.xlsx"'
        response['Content-Length'] = output.tell()

        output.seek(0)

        return response



        # return HttpResponse(json.dumps(json_map), 'application/json')


class InauguradorEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(
            json.dumps(map(lambda inaugurador: inaugurador.to_serializable_dict(), Inaugurador.objects.all())),
            'application/json')


class NumeroObrasPendientes(ProtectedResourceView):
    def get(self, request):
        token = request.GET.get('access_token')
        token_model = AccessToken.objects.get(token=token)
        arreglo_dependencias = []
        total_obras = 0

        for dependencia in token_model.user.usuario.dependencia.all():
            arreglo_dependencias.append(dependencia.id)

        if token_model.user.usuario.rol == 'AD':
            dependencias = Dependencia.objects.filter(
                Q(id__in=arreglo_dependencias) |
                Q(dependienteDe__id__in=arreglo_dependencias)
            )

            for dependencia in dependencias:
                total_obras = total_obras + dependencia.obra_set.filter(autorizada=False).count()

        ans = {}

        ans['obrasTotalesPendientes'] = total_obras

        return HttpResponse(json.dumps(ans), 'application/json')


class ReporteInicioEndpoint(ProtectedResourceView):
    def rename_estado(self, obra):
        obra['estado'] = obra['estado__nombreEstado']
        del obra['estado__nombreEstado']

    def get(self, request):
        dependencias = get_usuario_for_token(request.GET.get('access_token')).dependencia.all()
        subdependencias = get_usuario_for_token(request.GET.get('access_token')).subdependencia.all()

        if dependencias and dependencias.count() > 0:
            if get_usuario_for_token(request.GET.get('access_token')).rol == 'US':
                obras = Obra.objects.filter(
                    Q(subdependencia__in=get_subdependencias_as_list_flat(subdependencias))
                )
            else:
                obras = Obra.objects.filter(
                    Q(dependencia__in=get_subdependencias_as_list_flat(dependencias)) |
                    Q(subdependencia__in=get_subdependencias_as_list_flat(dependencias))
                )
        else:
            obras = Obra.objects.all()

        reporte = {
            'reporte_total': {'obras_proceso': {}, 'obras_proyectadas': {}, 'obras_concluidas': {}},
            'reporte2015': {'obras_proceso': {}, 'obras_proyectadas': {}, 'obras_concluidas': {}},
            'reporte2014': {'obras_concluidas': {}},
            'reporte2013': {'obras_concluidas': {}},
            'reporte2012': {'obras_concluidas': {}},
        }

        # Grafico, obras totales
        obras_totales_proceso = obras.filter(tipoObra_id=2)
        the_list = []
        for obra in obras_totales_proceso.values('latitud', 'longitud', 'estado__nombreEstado'):
            self.rename_estado(obra)
            the_list.append(obra)

        obras_totales_proyectadas = obras.filter(tipoObra_id=1)
        the_list = []
        for obra in obras_totales_proyectadas.values('latitud', 'longitud', 'estado__nombreEstado'):
            self.rename_estado(obra)
            the_list.append(obra)

        obras_totales_concluidas = obras.filter(tipoObra_id=3)
        the_list = []
        for obra in obras_totales_concluidas.values('latitud', 'longitud', 'estado__nombreEstado'):
            self.rename_estado(obra)
            the_list.append(obra)

        reporte['reporte_total']['obras_proceso'] = obras_totales_proceso
        reporte['reporte_total']['obras_proyectadas'] = obras_totales_proyectadas
        reporte['reporte_total']['obras_concluidas'] = obras_totales_concluidas

        obras2015 = obras.filter(fechaInicio__year=2015)
        obras2015_proceso = obras2015.filter(tipoObra_id=2)
        the_list = []

        for obra in obras2015_proceso.values('latitud', 'longitud', 'estado__nombreEstado').annotate(
                numero_obras=Count('estado')):
            self.rename_estado(obra)
            the_list.append(obra)
        reporte['reporte2015']['obras_proceso']['obras'] = the_list
        reporte['reporte2015']['obras_proceso']['total'] = obras2015_proceso.count()

        obras2015_proyectadas = obras2015.filter(tipoObra_id=1)
        the_list = []
        for obra in obras2015_proyectadas.values('latitud', 'longitud', 'estado__nombreEstado').annotate(
                numero_obras=Count('estado')):
            self.rename_estado(obra)
            the_list.append(obra)
        reporte['reporte2015']['obras_proyectadas']['obras'] = the_list
        reporte['reporte2015']['obras_proyectadas']['total'] = obras2015_proyectadas.count()

        obras2015_concluidas = obras.filter(Q(fechaTermino__year=2015) & Q(tipoObra_id=3))
        the_list = []
        for obra in obras2015_concluidas.values('latitud', 'longitud', 'estado__nombreEstado').annotate(
                numero_obras=Count('estado')):
            self.rename_estado(obra)
            the_list.append(obra)
        reporte['reporte2015']['obras_concluidas']['obras'] = the_list
        reporte['reporte2015']['obras_concluidas']['total'] = obras2015_concluidas.count()

        # Obras Concluidas, barra inferior

        obras2014 = obras.filter(Q(fechaTermino__year=2014) & Q(tipoObra_id=3))
        the_list = []
        for obra in obras2014.values('latitud', 'longitud', 'estado__nombreEstado'):
            self.rename_estado(obra)
            the_list.append(obra)
        reporte['reporte2014']['obras_concluidas']['total'] = obras2014.count()

        obras2013 = obras.filter(Q(fechaTermino__year=2013) & Q(tipoObra_id=3))
        the_list = []
        for obra in obras2013.values('latitud', 'longitud', 'estado__nombreEstado'):
            self.rename_estado(obra)
            the_list.append(obra)
        reporte['reporte2013']['obras_concluidas']['obras'] = the_list
        reporte['reporte2013']['obras_concluidas']['total'] = obras2013.count()

        obras2012 = obras.filter(Q(fechaTermino__year=2012) & Q(tipoObra_id=3))
        the_list = []
        for obra in obras2012.values('latitud', 'longitud', 'estado__nombreEstado'):
            self.rename_estado(obra)
            the_list.append(obra)
        reporte['reporte2012']['obras_concluidas']['obra'] = the_list
        reporte['reporte2012']['obras_concluidas']['total'] = obras2012.count()

        return HttpResponse(json.dumps(reporte), 'application/json')


class ReporteNoTrabajoEndpoint(ProtectedResourceView):
    def get(self, request):
        comp_date = datetime.now() - timedelta(15)
        print "****"
        print comp_date
        dicts = map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.filter(
            Q(obraoprograma='O') &
            Q(fecha_ultima_modificacion__lt=comp_date)))

        return HttpResponse(json.dumps(dicts), 'application/json')


class ReporteObrasPorAutorizar(ProtectedResourceView):
    def get(self, request):
        dependencias = get_usuario_for_token(request.GET.get('access_token')).dependencia.all()
        subdependencias = get_usuario_for_token(request.GET.get('access_token')).subdependencia.all()

        if dependencias and dependencias.count() > 0:
            if get_usuario_for_token(request.GET.get('access_token')).rol == 'US':
                obras = Obra.objects.filter(
                    Q(subdependencia__in=get_subdependencias_as_list_flat(subdependencias))
                )
            else:
                obras = Obra.objects.filter(
                    Q(dependencia__in=get_subdependencias_as_list_flat(dependencias)) |
                    Q(subdependencia__in=get_subdependencias_as_list_flat(dependencias))
                )
        else:
            obras = Obra.objects.all()

        obras = obras.filter(autorizada=False).values('id', 'identificador_unico', 'estado__nombreEstado',
                                                      'denominacion', 'latitud', 'longitud',
                                                      'dependencia__imagenDependencia')

        the_list = []
        for obra in obras:
            the_list.append(obra)

        return HttpResponse(json.dumps(the_list), 'application/json')

