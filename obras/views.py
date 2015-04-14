# Create your views here.
import os
from django.forms import model_to_dict
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from oauth2_provider.views import ProtectedResourceView
from oauth2_provider.models import AccessToken
from pptx import Presentation
from obras.models import *
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from forms import AddUserForm
from forms import AddObraForm
from forms import AddAuthUserForm
from forms import UbicacionForm
import json
from obras.models import Obra
from django.contrib.auth.models import User
import datetime
import qsstats


def login(request):
    c = {}
    c.update(csrf(request))

    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('loggedin')
    else:
        return HttpResponseRedirect('invalid_login')


def loggedin(request):
    return render_to_response('loggedin.html', {'full_name': request.user.username})


def invalid_login(request):
    return render_to_response('invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')


def create_authuser(request):
    if request.method == 'POST':
        form_a = AddAuthUserForm(request.POST)
        form_b = UserCreationForm(request.POST)
        ufirst_name = request.POST.get('first_name', '')
        ulast_name = request.POST.get('last_name', '')
        uemail = request.POST.get('email', '')

        if form_a.is_valid() and form_b.is_valid():
            form_b.save()
            iduser = form_b.save()

            User.objects.filter(id=iduser.id).update(first_name=ufirst_name,
                                                     last_name=ulast_name,
                                                     email=uemail
                                                     )
            return HttpResponseRedirect('create_user')

    form_a = AddAuthUserForm()
    form_b = UserCreationForm()

    return render_to_response('register.html', {'form_a': form_a, 'form_b': form_b},
                              context_instance=RequestContext(request))


def create_user(request):
    if request.method == 'POST':
        form_c = AddUserForm(request.POST)
        if form_c.is_valid():
            form_c.save()
            return HttpResponseRedirect('register_success')

    args = {}
    args.update(csrf(request))

    args['form_c'] = AddUserForm()
    print args
    return render_to_response('registerperfil.html', args)


def register_success(request):
    return render_to_response('register_success.html')


def see_map(request):
    form = UbicacionForm()
    ubicaciones = Ubicacion.objects.all()

    return render_to_response('see_map.html', {'ubicaciones': ubicaciones, 'form': form}, context_instance=RequestContext(request))


def coords_save(request):
    if request.is_ajax():
        form = UbicacionForm(request.POST)
        print form.errors.as_data()
        print form.errors.as_json()
        if form.is_valid():
            form.save()
            ubicaciones = Ubicacion.objects.all()

            data = '<ul>'
            for ubicacion in ubicaciones:
                data += "<li>%s %s %s %s</li>" % (ubicacion.nombre, ubicacion.estado, ubicacion.lat, ubicacion.lng)

            data += '</ul>'

            return HttpResponse(json.dumps({'ok': True, 'msg': data}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'ok': False, 'msg': form.errors.as_data()}),
                                content_type="application/json")


def do_chart(request):

    GOOGLE_API_KEY = 'clave'

    qs = Ubicacion.objects.all()
    qss = qsstats.QuerySetStats(qs, 'fecha')

    hoy = datetime.date.today()
    hace_2_semanas = hoy - datetime.timedelta(weeks=2)

    users_stats = qss.time_series(hace_2_semanas, hoy)

    return render_to_response('reportes.html', locals(),
                              context_instance=RequestContext(request))


def create_obra(request):
    if request.method == 'POST':
        form = AddObraForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('register_success')

    args = {}
    args.update(csrf(request))

    args['form'] = AddObraForm()
    print args
    return render_to_response('create_obra.html', args)

from django.shortcuts import render_to_response

class EstadosEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda estado: model_to_dict(estado), Estado.objects.all()))
        return HttpResponse(json_response, 'application/json')


class DependenciasEndpoint(ProtectedResourceView):

    def get(self, request):
        token = request.GET.get('access_token')
        print '*************' + token
        token_model = AccessToken.objects.get(token=token)
        print token_model.user

        if token_model.user.usuario.rol == 'SA':
            dicts = map(lambda dependencia: model_to_dict(dependencia), Dependencia.objects.all())

        elif token_model.user.usuario.rol == 'AD':
            dicts = map(lambda dependencia: model_to_dict(dependencia), Dependencia.objects.filter(
                Q(id=token_model.user.usuario.dependencia.id) |
                Q(dependienteDe__id=token_model.user.usuario.dependencia.id))
            )

        else:
            dicts = map(lambda dependencia: model_to_dict(dependencia), Dependencia.objects.filter(
                Q(id=token_model.user.usuario.dependencia.id))
            )

        for dictionary in dicts:
            # We KNOW that this entry must be a FileField value
            # (therefore, calling its name attribute is safe),
            # so we need to mame it JSON serializable (Django objects
            # are not by default and its built-in serializer sucks),
            # namely, we only need the path
            if dictionary['imagenDependencia'].name == '' or dictionary['imagenDependencia'].name == '':
                dictionary['imagenDependencia'] = None
            else:
                dictionary['imagenDependencia'] = dictionary['imagenDependencia'].name

        json_response = json.dumps(dicts)
        return HttpResponse(json_response, 'application/json')


class ImpactosEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda impacto: model_to_dict(impacto), Impacto.objects.all()))
        return HttpResponse(json_response, 'application/json')


class InauguradorEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda inaugurador: model_to_dict(inaugurador), Inaugurador.objects.all()))
        return HttpResponse(json_response, 'application/json')


class ClasificacionEndpoint(ProtectedResourceView):

    def get(self, request):
        if request.GET.get('id', False):
            clasificaciones = TipoClasificacion.objects.filter(subclasificacionDe_id=1)
        else:
            clasificaciones = TipoClasificacion.objects.filter(subclasificacionDe_id__isnull=True)

        json_response = json.dumps(map(lambda clasificacion: model_to_dict(clasificacion), clasificaciones))
        return HttpResponse(json_response, 'application/json')



class InversionEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda inversion: model_to_dict(inversion), TipoInversion.objects.all()))
        return HttpResponse(json_response, 'application/json')


class TipoDeObraEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda x: model_to_dict(x), TipoObra.objects.all()))
        return HttpResponse(json_response, 'application/json')


def is_super_admin(user):
    return user.usuario.rol == 'SA'


@login_required()
@user_passes_test(is_super_admin)
def balance_general(request):
    start_date = datetime.date(2012, 12, 01)
    end_date = datetime.date(2013, 12, 31)
    obras2013 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2013 = obras2013.count()
    total_invertido_2013 = obras2013.aggregate(Sum('inversionTotal'))

    # print 'Total Obras 2013: ' + str(total_obras_2013)
    # print 'Total Invertido 2013: ' + str(total_invertido_2013)

    start_date = datetime.date(2014, 01, 01)
    end_date = datetime.date(2014, 12, 31)
    obras2014 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2014 = obras2014.count()
    total_invertido_2014 = obras2014.aggregate(Sum('inversionTotal'))

    # print 'Total Obras 2014: ' + str(total_obras_2014)
    # print 'Total Invertido 2014: ' + str(total_invertido_2014)

    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    total_obras_proceso = obras_proceso.count()
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

    # print 'Total Obras Proceso: ' + str(total_obras_proceso)
    # print 'Total Invertido Proceso: ' + str(total_invertido_proceso)

    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))

    # print 'Total Obras Proyectadas: ' + str(total_obras_proyectadas)
    # print 'Total Invertido Proyectadas: ' + str(total_invertido_proyectadas)

    total_obras = total_obras_2013 + total_obras_2014 + total_obras_proceso + total_obras_proyectadas
    total_invertido = total_invertido_2013.get('inversionTotal__sum') + total_invertido_2014.get(
        'inversionTotal__sum') + total_invertido_proceso.get('inversionTotal__sum') + total_invertido_proyectadas.get(
        'inversionTotal__sum')

    template = loader.get_template('reportes/balance_general.html')
    context = RequestContext(request, {
        'total_obras_2013': total_obras_2013,
        'total_invertido_2013': total_invertido_2013,
        'total_obras_2014': total_obras_2014,
        'total_invertido_2014': total_invertido_2014,
        'total_obras_proceso': total_obras_proceso,
        'total_invertido_proceso': total_invertido_proceso,
        'total_obras_proyectadas': total_obras_proyectadas,
        'total_invertido_proyectadas': total_invertido_proyectadas,
        'total_obras': total_obras,
        'total_invertido': total_invertido,
    })
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_informacion_general(request):
    obras_concluidas = Obra.objects.filter(
        Q(tipoObra=3)
    )

    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_obras_proceso = obras_proceso.count()
    total_obras_concluidas = obras_concluidas.count()

    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))
    total_invertido_concluidas = obras_concluidas.aggregate(Sum('inversionTotal'))

    template = loader.get_template('reportes/hipervinculo_informacion_general.html')
    context = RequestContext(request, {
        'total_obras_proyectadas': total_obras_proyectadas,
        'total_obras_proceso': total_obras_proceso,
        'total_obras_concluidas': total_obras_concluidas,
        'total_invertido_proyectadas': total_invertido_proyectadas,
        'total_invertido_proceso': total_invertido_proceso,
        'total_invertido_concluidas': total_invertido_concluidas,
    })
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_sector(request):
    start_date_2013 = datetime.date(2012, 12, 01)
    end_date_2013 = datetime.date(2013, 12, 31)

    start_date_2014 = datetime.date(2014, 01, 01)
    end_date_2014 = datetime.date(2014, 12, 31)
    dependencias = {}

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

        dependencias[dependencia.nombreDependencia] = {}
        dependencias[dependencia.nombreDependencia]['total_obras_concluidas_2013'] = total_obras_concluidas_2013
        dependencias[dependencia.nombreDependencia]['total_obras_concluidas_2014'] = total_obras_concluidas_2014
        dependencias[dependencia.nombreDependencia]['total_obras_proceso'] = total_obras_proceso
        dependencias[dependencia.nombreDependencia]['total_obras_proyectadas'] = total_obras_proyectadas

        dependencias[dependencia.nombreDependencia]['total_invertido_2013'] = total_invertido_2013
        dependencias[dependencia.nombreDependencia]['total_invertido_2014'] = total_invertido_2014
        dependencias[dependencia.nombreDependencia]['total_invertido_proceso'] = total_invertido_proceso
        dependencias[dependencia.nombreDependencia]['total_invertido_proyectadas'] = total_invertido_proyectadas

        print 'total_obras_concluidas_2013: ' + str(total_obras_concluidas_2013)
        print 'total_obras_concluidas_2014: ' + str(total_obras_concluidas_2014)
        print 'total_obras_proceso: ' + str(total_obras_proceso)
        print 'total_obras_proyectadas: ' + str(total_obras_proyectadas)

        print 'total_invertido_2013: ' + str(total_invertido_2013)
        print 'total_invertido_2014: ' + str(total_invertido_2014)
        print 'total_invertido_proceso: ' + str(total_invertido_proceso)
        print 'total_invertido_proyectadas: ' + str(total_invertido_proyectadas)

    template = loader.get_template('reportes/hipervinculo_informacion_sector.html')
    context = RequestContext(request, {
        'dependencias': dependencias,
    })
    print(dependencias)
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_entidad(request):
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
    estados = {}

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

        estados[estado.nombreEstado] = {}
        estados[estado.nombreEstado]['total_obras_concluidas_2013'] = total_obras_concluidas_2013
        estados[estado.nombreEstado]['total_obras_concluidas_2014'] = total_obras_concluidas_2014
        estados[estado.nombreEstado]['total_obras_proceso'] = total_obras_proceso
        estados[estado.nombreEstado]['total_obras_proyectadas_2014'] = total_obras_proyectadas_2014
        estados[estado.nombreEstado]['total_obras_proyectadas_2015'] = total_obras_proyectadas_2015
        estados[estado.nombreEstado]['total_obras_proyectadas_2016'] = total_obras_proyectadas_2016
        estados[estado.nombreEstado]['total_obras_proyectadas_2017'] = total_obras_proyectadas_2017
        estados[estado.nombreEstado]['total_obras_proyectadas_2018'] = total_obras_proyectadas_2018

        estados[estado.nombreEstado]['total_invertido_2013_concluidas'] = total_invertido_2013_concluidas
        estados[estado.nombreEstado]['total_invertido_2014_concluidas'] = total_invertido_2014_concluidas
        estados[estado.nombreEstado]['total_invertido_proceso'] = total_invertido_proceso

        estados[estado.nombreEstado]['total_invertido_proyectadas_2014'] = total_invertido_proyectadas_2014
        estados[estado.nombreEstado]['total_invertido_proyectadas_2015'] = total_invertido_proyectadas_2015
        estados[estado.nombreEstado]['total_invertido_proyectadas_2016'] = total_invertido_proyectadas_2016
        estados[estado.nombreEstado]['total_invertido_proyectadas_2017'] = total_invertido_proyectadas_2017
        estados[estado.nombreEstado]['total_invertido_proyectadas_2018'] = total_invertido_proyectadas_2018

    template = loader.get_template('reportes/hipervinculo_entidad.html')
    context = RequestContext(request, {
        'estados': estados,
    })
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_concluidas_proceso_proyectadas(request):
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

    template = loader.get_template('reportes/hipervinculo_concluidas_proceso_proyectadas.html')
    context = RequestContext(request, {
        'total_obras_concluidas_2013': total_obras_concluidas_2013,
        'total_invertido_2013_concluidas': total_invertido_2013_concluidas,
        'total_obras_concluidas_2014': total_obras_concluidas_2014,
        'total_invertido_2014_concluidas': total_invertido_2014_concluidas,
        'obras_totales_proceso': obras_totales_proceso,
        'total_invertido_proceso': total_invertido_proceso,
        'obras_totales_proyectadas': obras_totales_proyectadas,
        'total_invertido_proyectadas': total_invertido_proyectadas,
    })
    return HttpResponse(template.render(context))


@login_required()
def consulta_web(request):

    if request.user.usuario.rol == 'SA':
        dependencias = Dependencia.objects.all()
    elif request.user.usuario.rol == 'AD':
        dependencias = Dependencia.objects.filter(
                Q(id=request.user.usuario.dependencia.id) |
                Q(dependienteDe__id=request.user.usuario.dependencia.id))
    elif request.user.usuario.rol == 'US':
        dependencias = Dependencia.objects.filter(
                    Q(id=request.user.usuario.dependencia.id)
                    )
    template = loader.get_template('consultas/busqueda_general.html')
    context = RequestContext(request, {
        'dependencias': dependencias,
        'estados': Estado.objects.all(),
        'tipo_inversiones': TipoInversion.objects.all(),
        'impactos': Impacto.objects.all(),
        'clasificacion': TipoClasificacion.objects.all(),
        'inaugurador': Inaugurador.objects.all(),
    })
    return HttpResponse(template.render(context))

# reportes de power point ************************************************************************************

def reportes_predefinidos(request):
    return render_to_response('presentaciones.html', {'clases': ''}, context_instance=RequestContext(request))

def abrir_pptx(archivo):
    f = os.popen(archivo)
    #f.close()

def balance_general_ppt(request):
    prs = Presentation('obras/static/ppt/PRINCIPAL_BALANCE_GENERAL_APF.pptx')

    # informacion para el 2013
    start_date = datetime.date(2012, 12, 01)
    end_date = datetime.date(2013, 12, 31)
    obras2013 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2013 = obras2013.count()
    total_invertido_2013 = obras2013.aggregate(Sum('inversionTotal'))

    # informacion para el 2014
    start_date = datetime.date(2014, 01, 01)
    end_date = datetime.date(2014, 12, 31)
    obras2014 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2014 = obras2014.count()
    total_invertido_2014 = obras2014.aggregate(Sum('inversionTotal'))

    # informacion para obras en proceso
    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    total_obras_proceso = obras_proceso.count()
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

    # informacion para obras proyectadas
    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))

    # informacion para obras totales
    total_obras = total_obras_2013 + total_obras_2014 + total_obras_proceso + total_obras_proyectadas
    total_invertido = total_invertido_2013.get('inversionTotal__sum',0) + total_invertido_2014.get(
        'inversionTotal__sum',0) + total_invertido_proceso.get('inversionTotal__sum',0) + total_invertido_proyectadas.get(
        'inversionTotal__sum',0)


    prs.slides[0].shapes[15].text= '{0:,}'.format(total_obras_2013)
    prs.slides[0].shapes[16].text= '$ {0:,.2f}'.format(total_invertido_2013.get('inversionTotal__sum',0))
    prs.slides[0].shapes[17].text= '{0:,}'.format(total_obras_2014)
    prs.slides[0].shapes[18].text= '$ {0:,.2f}'.format(total_invertido_2014.get('inversionTotal__sum',0))
    prs.slides[0].shapes[21].text= '{0:,}'.format(total_obras_proceso)
    prs.slides[0].shapes[22].text= '$ {0:,.2f}'.format(total_invertido_proceso.get('inversionTotal__sum',0))
    prs.slides[0].shapes[23].text= '{0:,}'.format(total_obras_proyectadas)
    prs.slides[0].shapes[24].text= '$ {0:,.2f}'.format(total_invertido_proyectadas.get('inversionTotal__sum',0))
    prs.slides[0].shapes[19].text= '{0:,}'.format(total_obras)
    prs.slides[0].shapes[20].text= '$ {0:,.2f}'.format(total_invertido)


    prs.save('test.pptx')
    abrir_pptx('test.pptx')
    return render_to_response('presentaciones.html', {'clases': ''}, context_instance=RequestContext(request))

def hiper_info_general_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULO_INFORMACION_GENERAL.pptx')
    obras_concluidas = Obra.objects.filter(
        Q(tipoObra=3)
    )

    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_obras_proceso = obras_proceso.count()
    total_obras_concluidas = obras_concluidas.count()

    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))
    total_invertido_concluidas = obras_concluidas.aggregate(Sum('inversionTotal'))

    prs.slides[0].shapes[3].text= '{0:,}'.format(total_obras_concluidas)
    prs.slides[0].shapes[4].text= '$ {0:,.2f}'.format(total_invertido_concluidas.get('inversionTotal__sum',0))
    prs.slides[1].shapes[3].text= '{0:,}'.format(total_obras_proceso)
    prs.slides[1].shapes[4].text= '$ {0:,.2f}'.format(total_invertido_proceso.get('inversionTotal__sum',0))
    prs.slides[2].shapes[3].text= '{0:,}'.format(total_obras_proyectadas)
    prs.slides[2].shapes[4].text= '$ {0:,.2f}'.format(total_invertido_proyectadas.get('inversionTotal__sum',0))


    prs.save('hiper_info_general.pptx')
    abrir_pptx('hiper_info_general.pptx')
    return render_to_response('presentaciones.html', {'clases': ''}, context_instance=RequestContext(request))

def hiper_inauguradas_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULO_INAUGURADAS_SENALIZADAS.pptx')
    # falta implementar
    prs.save('hiper_inauguradas.pptx')
    abrir_pptx('hiper_inauguradas.pptx')
    return render_to_response('presentaciones.html', {'clases': ''}, context_instance=RequestContext(request))

def hiper_por_sector_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULO_POR_SECTOR.pptx')

    start_date_2013 = datetime.date(2012, 12, 01)
    end_date_2013 = datetime.date(2013, 12, 31)

    start_date_2014 = datetime.date(2014, 01, 01)
    end_date_2014 = datetime.date(2014, 12, 31)
    dependencias = {}

    for dependencia in Dependencia.objects.filter(
        Q(obraoprograma='O')
    ):
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



        if dependencia.nombreDependencia =='SEGOB': indiceSlide =0
        elif dependencia.nombreDependencia =='SEDESOL': indiceSlide =4
        elif dependencia.nombreDependencia =='SEMARNAT': indiceSlide = 8
        elif dependencia.nombreDependencia =='SAGARPA': indiceSlide = 12
        elif dependencia.nombreDependencia =='SCT': indiceSlide = 16
        elif dependencia.nombreDependencia =='SEP': indiceSlide = 20
        elif dependencia.nombreDependencia =='SS': indiceSlide = 24
        elif dependencia.nombreDependencia =='SEDATU': indiceSlide = 28
        elif dependencia.nombreDependencia =='SECTUR': indiceSlide = 32
        elif dependencia.nombreDependencia =='PEMEX': indiceSlide = 36
        elif dependencia.nombreDependencia =='CFE': indiceSlide = 40
        elif dependencia.nombreDependencia =='IMSS': indiceSlide = 44
        elif dependencia.nombreDependencia =='ISSSTE': indiceSlide = 48
        elif dependencia.nombreDependencia =='CONAGUA': indiceSlide = 52
        else: indiceSlide =56

        totalinvertidoproceso=0
        totalinvertido2013=0
        totalinvertido2014=0
        totalinvertidoproyectadas=0
        if str(total_invertido_2013.get('inversionTotal__sum',0)) != 'None': totalinvertido2013=total_invertido_2013.get('inversionTotal__sum',0)
        if str(total_invertido_2014.get('inversionTotal__sum',0)) != 'None': totalinvertido2014=total_invertido_2014.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas=total_invertido_proyectadas.get('inversionTotal__sum',0)
        if str(total_invertido_proceso.get('inversionTotal__sum',0)) != 'None': totalinvertidoproceso=total_invertido_proceso.get('inversionTotal__sum',0)

        TOTAL_INVERTIDO=totalinvertido2013+totalinvertido2014+totalinvertidoproceso+totalinvertidoproyectadas
        TOTAL_OBRAS=total_obras_concluidas_2013+total_obras_concluidas_2014+total_obras_proceso+total_obras_proyectadas

        prs.slides[indiceSlide].shapes[5].text= '{0:,}'.format(total_obras_concluidas_2013)
        prs.slides[indiceSlide].shapes[6].text= '$ {0:,.2f}'.format(totalinvertido2013)
        prs.slides[indiceSlide].shapes[7].text= '{0:,}'.format(total_obras_concluidas_2014)
        prs.slides[indiceSlide].shapes[8].text= '$ {0:,.2f}'.format(totalinvertido2014)
        prs.slides[indiceSlide].shapes[9].text= '{0:,}'.format(TOTAL_OBRAS)
        prs.slides[indiceSlide].shapes[10].text= '$ {0:,.2f}'.format(TOTAL_INVERTIDO)
        prs.slides[indiceSlide].shapes[11].text= '{0:,}'.format(total_obras_proceso)
        prs.slides[indiceSlide].shapes[12].text= '$ {0:,.2f}'.format(totalinvertidoproceso)
        prs.slides[indiceSlide].shapes[13].text= '{0:,}'.format(total_obras_proyectadas)
        prs.slides[indiceSlide].shapes[14].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas)


    prs.save('hiper_por_sector.pptx')
    abrir_pptx('hiper_por_sector.pptx')
    return render_to_response('presentaciones.html', {'clases': ''}, context_instance=RequestContext(request))

def hiper_por_entidad_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULOS_POR_ENTIDAD.pptx')

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
    indiceSlide=0
    estados = {}
    listaEstados = Estado.objects.exclude(nombreEstado='INTERESTATAL').exclude(nombreEstado='NACIONAL')
    listaEstados = listaEstados.order_by('nombreEstado')

    for estado in listaEstados:
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

        totalinvertido2013=0
        totalinvertido2014=0
        totalinvertidoproceso=0
        totalinvertidoproyectadas2014=0
        totalinvertidoproyectadas2015=0
        totalinvertidoproyectadas2016=0
        totalinvertidoproyectadas2017=0
        totalinvertidoproyectadas2018=0

        if str(total_invertido_2013_concluidas.get('inversionTotal__sum',0)) != 'None': totalinvertido2013=total_invertido_2013_concluidas.get('inversionTotal__sum',0)
        if str(total_invertido_2014_concluidas.get('inversionTotal__sum',0)) != 'None': totalinvertido2014=total_invertido_2014_concluidas.get('inversionTotal__sum',0)
        if str(total_invertido_proceso.get('inversionTotal__sum',0)) != 'None': totalinvertidoproceso=total_invertido_proceso.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2014.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2014=total_invertido_proyectadas_2014.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2015.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2015=total_invertido_proyectadas_2015.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2016.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2016=total_invertido_proyectadas_2016.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2017.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2017=total_invertido_proyectadas_2017.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2018.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2018=total_invertido_proyectadas_2018.get('inversionTotal__sum',0)

        totalObras14_18 = totalinvertidoproyectadas2014+totalinvertidoproyectadas2015+totalinvertidoproyectadas2016+totalinvertidoproyectadas2017+totalinvertidoproyectadas2018
        totalInvertido14_18 = total_obras_proyectadas_2014+total_obras_proyectadas_2015+total_obras_proyectadas_2016+total_obras_proyectadas_2017+total_obras_proyectadas_2018

        totalObrasGeneral = totalObras14_18+total_obras_concluidas_2013+total_obras_concluidas_2014+total_obras_proceso
        totalInvertidoGeneral = totalInvertido14_18+totalinvertido2013+totalinvertido2014+totalinvertidoproceso

        prs.slides[indiceSlide].shapes[9].text= '{0:,}'.format(total_obras_concluidas_2013)
        prs.slides[indiceSlide].shapes[10].text= '$ {0:,.2f}'.format(totalinvertido2013)
        prs.slides[indiceSlide].shapes[11].text= '{0:,}'.format(total_obras_concluidas_2014)
        prs.slides[indiceSlide].shapes[12].text= '$ {0:,.2f}'.format(totalinvertido2014)
        prs.slides[indiceSlide].shapes[13].text= '{0:,}'.format(total_obras_proceso)
        prs.slides[indiceSlide].shapes[14].text= '$ {0:,.2f}'.format(totalinvertidoproceso)
        prs.slides[indiceSlide].shapes[15].text= 'min1'
        prs.slides[indiceSlide].shapes[16].text= 'min2'
        prs.slides[indiceSlide].shapes[17].text= 'max1'
        prs.slides[indiceSlide].shapes[18].text= 'max2'

        prs.slides[indiceSlide].shapes[19].text= '{0:,}'.format(total_obras_proyectadas_2014)
        prs.slides[indiceSlide].shapes[20].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2014)
        prs.slides[indiceSlide].shapes[21].text= '{0:,}'.format(total_obras_proyectadas_2015)
        prs.slides[indiceSlide].shapes[22].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2015)
        prs.slides[indiceSlide].shapes[23].text= '{0:,}'.format(total_obras_proyectadas_2016)
        prs.slides[indiceSlide].shapes[24].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2016)
        prs.slides[indiceSlide].shapes[25].text= '{0:,}'.format(total_obras_proyectadas_2017)
        prs.slides[indiceSlide].shapes[26].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2017)
        prs.slides[indiceSlide].shapes[27].text= '{0:,}'.format(total_obras_proyectadas_2018)
        prs.slides[indiceSlide].shapes[28].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2018)
        prs.slides[indiceSlide].shapes[29].text= '{0:,}'.format(totalObras14_18)
        prs.slides[indiceSlide].shapes[30].text= '$ {0:,.2f}'.format(totalInvertido14_18)
        prs.slides[indiceSlide].shapes[31].text= '{0:,}'.format(totalObrasGeneral)
        #prs.slides[indiceSlide].shapes[32].text= '$ {0:,.2f}'.format(totalInvertidoGeneral)

        indiceSlide=indiceSlide+1

    prs.save('hiper_por_entidad.pptx')
    abrir_pptx('hiper_por_entidad.pptx')
    return render_to_response('presentaciones.html', {'clases': ''}, context_instance=RequestContext(request))


