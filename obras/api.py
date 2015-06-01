import json
import datetime
from django.db.models import Q
from django.http import HttpResponse
from oauth2_provider.views import ProtectedResourceView
from obras.models import Obra


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
        json_response = []
        today = datetime.datetime.now().date()

        obras = Obra.objects.filter(Q(fechaInicio__lte=today)).all()

        for obra in obras:
            map = {}

            map['identificador'] = obra.identificador_unico
            map['tipoObra'] = obra.tipoObra.to_serializable_dict()
            map['dependencia'] = obra.dependencia.to_serializable_dict()
            map['estado'] = obra.estado.to_serializable_dict()
            map['impacto'] = obra.impacto.to_serializable_dict()

            map['tipoInversion'] = []
            for tipoInversion in obra.tipoInversion.all():
                tipo = tipoInversion.to_serializable_dict()
                map['tipoInversion'].append(tipo)

            map['tipoClasificacion'] = []
            for tipoClasificacion in obra.tipoClasificacion.all():
                tipo = tipoClasificacion.to_serializable_dict()
                map['tipoClasificacion'].append(tipo)

            map['inaugurador'] = obra.inaugurador.to_serializable_dict()
            map['registroHacendario'] = obra.registroHacendario
            map['registroAuditoria'] = obra.registroAuditoria
            map['denominacion'] = obra.denominacion
            map['descripcion'] = obra.descripcion
            map['observaciones'] = obra.observaciones
            if obra.fechaInicio is None:
                map['fechaInicio'] = None
            else:
                map['fechaInicio'] = obra.fechaInicio.__str__()
            if obra.fechaTermino is None:
                map['fechaTermino'] = None
            else:
                map['fechaTermino'] = obra.fechaTermino.__str__()
            if obra.inversionTotal is None:
                map['inversionTotal'] = 0.0
            else:
                map['inversionTotal'] = float(obra.inversionTotal)
            if obra.totalBeneficiarios is None:
                map['totalBeneficiarios'] = 0
            else:
                map['totalBeneficiarios'] = int(obra.totalBeneficiarios)
            map['senalizacion'] = obra.senalizacion
            map['susceptibleInauguracion'] = obra.susceptibleInauguracion
            if obra.porcentajeAvance is None:
                map['porcentajeAvance'] = 0.0
            else:
                map['porcentajeAvance'] = float(obra.porcentajeAvance)
            if obra.fotoAntes is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoAntes.name
            if obra.fotoDurante is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDurante.name
            if obra.fotoDespues is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDespues.name
            map['inaugurada'] = obra.inaugurada
            map['poblacionObjetivo'] = obra.poblacionObjetivo
            map['municipio'] = obra.municipio
            if obra.tipoMoneda is None:
                map['tipoMoneda'] = None
            else:
                map['tipoMoneda'] = obra.tipoMoneda.to_serializable_dict()

            json_response.append(map)

        return HttpResponse(json.dumps(json_response), 'application/json')


class ObrasVencidasEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = []
        today = datetime.datetime.now().date()

        obras = Obra.objects.filter(Q(fechaTermino__lte=today))

        for obra in obras:
            map = {}

            map['identificador'] = obra.identificador_unico
            map['tipoObra'] = obra.tipoObra.to_serializable_dict()
            map['dependencia'] = obra.dependencia.to_serializable_dict()
            map['estado'] = obra.estado.to_serializable_dict()
            map['impacto'] = obra.impacto.to_serializable_dict()

            map['tipoInversion'] = []
            for tipoInversion in obra.tipoInversion.all():
                tipo = tipoInversion.to_serializable_dict()
                map['tipoInversion'].append(tipo)

            map['tipoClasificacion'] = []
            for tipoClasificacion in obra.tipoClasificacion.all():
                tipo = tipoClasificacion.to_serializable_dict()
                map['tipoClasificacion'].append(tipo)

            map['inaugurador'] = obra.inaugurador.to_serializable_dict()
            map['registroHacendario'] = obra.registroHacendario
            map['registroAuditoria'] = obra.registroAuditoria
            map['denominacion'] = obra.denominacion
            map['descripcion'] = obra.descripcion
            map['observaciones'] = obra.observaciones
            if obra.fechaInicio is None:
                map['fechaInicio'] = None
            else:
                map['fechaInicio'] = obra.fechaInicio.__str__()
            if obra.fechaTermino is None:
                map['fechaTermino'] = None
            else:
                map['fechaTermino'] = obra.fechaTermino.__str__()
            if obra.inversionTotal is None:
                map['inversionTotal'] = 0.0
            else:
                map['inversionTotal'] = float(obra.inversionTotal)
            if obra.totalBeneficiarios is None:
                map['totalBeneficiarios'] = 0
            else:
                map['totalBeneficiarios'] = int(obra.totalBeneficiarios)
            map['senalizacion'] = obra.senalizacion
            map['susceptibleInauguracion'] = obra.susceptibleInauguracion
            if obra.porcentajeAvance is None:
                map['porcentajeAvance'] = 0.0
            else:
                map['porcentajeAvance'] = float(obra.porcentajeAvance)
            if obra.fotoAntes is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoAntes.name
            if obra.fotoDurante is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDurante.name
            if obra.fotoDespues is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDespues.name
            map['inaugurada'] = obra.inaugurada
            map['poblacionObjetivo'] = obra.poblacionObjetivo
            map['municipio'] = obra.municipio
            if obra.tipoMoneda is None:
                map['tipoMoneda'] = None
            else:
                map['tipoMoneda'] = obra.tipoMoneda.to_serializable_dict()

            json_response.append(map)

        return HttpResponse(json.dumps(json_response), 'application/json')
