# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from smart_selects.db_fields import ChainedForeignKey
from django.db import connection

# TODO agregar nombres verbose a los modelos


# Create your models here.
from django.db.models import Q
from django.forms import model_to_dict


@python_2_unicode_compatible
class TipoObra(models.Model):
    nombreTipoObra = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoObra

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


def content_file_dependencia(instance, filename):
    # print instance.identificador_unico
    # ext = filename.split('.')[-1]
    # filename = instance.identificador_unico + '_ANTES.'+ext
    return '/'.join(['imagenesDependencias', instance.nombreDependencia, filename])


@python_2_unicode_compatible
class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200)
    imagenDependencia = models.FileField(upload_to=content_file_dependencia, blank=True, null=True)

    dependienteDe = models.ForeignKey('self', null=True, blank=True, limit_choices_to={
        'obraoprograma': 'O',
    })

    obraoprograma = models.CharField(max_length=1, null=True, blank=True, default='O')
    fecha_ultima_modificacion = models.DateTimeField(null=True, blank=True)
    orden_secretaria = models.FloatField(null=True, blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreDependencia

    def get_contactos(self):
        return Usuario.objects.filter(Q(dependencia=self) & Q(rol='AD'))

    def to_serializable_dict(self):
        ans = {}

        ans['id'] = str(self.id)
        ans['nombreDependencia'] = str(self.nombreDependencia)
        if self.imagenDependencia is None or self.imagenDependencia.name == '' or self.imagenDependencia.name is None:
            ans['imagenDependencia'] = None
        else:
            ans['imagenDependencia'] = self.imagenDependencia.url

        if self.dependienteDe is None:
            ans['dependienteDe'] = None
        else:
            ans['dependienteDe'] = str(self.dependienteDe.id)

        if self.fecha_ultima_modificacion is None:
            ans['fecha_ultima_modificacion'] = None
        else:
            ans['fecha_ultima_modificacion'] = self.fecha_ultima_modificacion.__str__()

        return ans

    def get_tree(self):
        ans = {'dependencia': self.to_serializable_dict(), 'subdependencias': None}
        subdeps = Dependencia.objects.filter(dependienteDe__id=self.id)

        if subdeps and subdeps.count() > 0:
            ans['subdependencias'] = []
            for subdep in subdeps:
                ans['subdependencias'].append(subdep.get_tree())

        return ans

    def get_subdeps_flat(self):
        ans = None
        subdeps = Dependencia.objects.filter(dependienteDe__id=self.id)

        if subdeps and subdeps.count() > 0:
            ans = []
            for subdep in subdeps:
                subsubdeps = subdep.get_subdeps_flat()
                if subsubdeps:
                    ans.append(subsubdeps)

        return ans

    def get_obras(self):
        subdeps = self.get_subdeps_flat()
        if subdeps:
            return Obra.objects.filter(
                Q(dependencia=self) | Q(dependencia__in=subdeps) |
                Q(subdependencia__in=subdeps) | Q(subdependencia=self)
            )
        else:
            return Obra.objects.filter(dependencia=self)


@python_2_unicode_compatible
class Estado(models.Model):
    nombreEstado = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class Municipio (models.Model):
    nombreMunicipio = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.ForeignKey(Estado, null=False, blank=False)

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['estado'] = self.estado.nombreEstado
        return ans

    def __str__(self):
        return self.nombreMunicipio

    def __unicode__(self):
        return self.nombreMunicipio


@python_2_unicode_compatible
class Impacto(models.Model):

    class Meta:
        verbose_name = "Tipo de Impacto"
        verbose_name_plural = "Tipos de Impacto"

    nombreImpacto = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreImpacto

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


@python_2_unicode_compatible
class TipoInversion(models.Model):

    class Meta:
        verbose_name = "Tipo de Inversión"
        verbose_name_plural = "Tipos de Inversión"

    nombreTipoInversion = models.CharField(max_length=200)
    nombreTipoInversionCorta = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoInversion

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


@python_2_unicode_compatible
class TipoClasificacion(models.Model):

    class Meta:
        verbose_name_plural = "Tipos de Clasificación"
        verbose_name = "Tipo de Clasificación"

    subclasificacionDe = models.ForeignKey('self', null=True, blank=True,
                                           limit_choices_to={
                                               'subclasificacionDe': None,
                                           }
                                           )
    nombreTipoClasificacion = models.CharField(max_length=200)
    nombreTipoClasificacionCorta = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoClasificacion

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        if ans['subclasificacionDe'] is not None:
            ans['subclasificacionDe'] = str(self.subclasificacionDe_id)
        else:
            ans['subclasificacionDe'] = None
        return ans

    def get_tree(self):
        ans = {'tipoClasificacion': self, 'subclasificaciones': None}
        subclasificaciones = TipoClasificacion.objects.filter(subclasificacionDe__id=self.id)

        if subclasificaciones and subclasificaciones.count() > 0:
            ans['subclasificaciones'] = []
            for subclasificacion in subclasificaciones:
                ans.append(subclasificacion.get_tree())

        return ans

    def get_subclasificaciones_flat(self):
        ans = None
        subclasificaciones = TipoClasificacion.objects.filter(subclasificacionDe__id=self.id)

        if subclasificaciones and subclasificaciones.count() > 0:
            ans = []
            for subclasificacion in subclasificaciones:
                ans.append(subclasificacion)
                subsubclasificaciones = subclasificacion.get_subclasificaciones_flat()
                if subsubclasificaciones:
                    ans.extend(subsubclasificaciones)

        return ans


@python_2_unicode_compatible
class Inaugurador(models.Model):

    class Meta:
        verbose_name_plural = "Inauguradores"
        verbose_name = "Inaugurador"

    nombreCargoInaugura = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreCargoInaugura

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


@python_2_unicode_compatible
class TipoMoneda(models.Model):
    nombreTipoDeMoneda = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoDeMoneda

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class Usuario(models.Model):
    SUPERADMIN = 'SA'
    ADMIN = 'AD'
    USER = 'US'
    ROLES_CHOICES = (
        (SUPERADMIN, 'Administrador General'),
        (ADMIN, 'Administrador de Dependencia'),
        (USER, 'Usuario de Dependencia'),
    )
    rol = models.CharField(max_length=2, choices=ROLES_CHOICES, default=USER)
    user = models.OneToOneField(User)
    dependencia = models.ManyToManyField(Dependencia, blank=True, null=True, limit_choices_to={
        'dependienteDe': None,
        'obraoprograma': 'O',
    },
                                         )
    subdependencia = models.ManyToManyField(Dependencia, blank=True, null=True,
                                            limit_choices_to={'dependienteDe__isnull': False},
                                            related_name='Subdependencias')


@python_2_unicode_compatible
class InstanciaEjecutora(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


BOOL_CHOICES = ((True, 'Sí'), (False, 'No'))


def content_file_antes(instance, filename):
    print instance.identificador_unico
    ext = filename.split('.')[-1]
    filename = instance.identificador_unico + '_ANTES.' + ext
    return '/'.join(['imagenesObras', instance.identificador_unico, filename])


def content_file_durante(instance, filename):
    print instance.identificador_unico
    ext = filename.split('.')[-1]
    filename = instance.identificador_unico + '_DURANTE.' + ext
    return '/'.join(['imagenesObras', instance.identificador_unico, filename])


def content_file_despues(instance, filename):
    print instance.identificador_unico
    ext = filename.split('.')[-1]
    filename = instance.identificador_unico + '_DESPUES.' + ext
    return '/'.join(['imagenesObras', instance.identificador_unico, filename])


@python_2_unicode_compatible
class Obra(models.Model):
    # TODO agrupar semanticamente todos los campos de obras
    identificador_unico = models.SlugField(unique=True, null=True, verbose_name='Identificador Único')
    tipoObra = models.ForeignKey(TipoObra, verbose_name='Tipo de Obra')
    dependencia = models.ForeignKey(Dependencia, related_name='%(class)s_dependencia',
                                    limit_choices_to={
                                        'dependienteDe': None,
                                        'obraoprograma': 'O',
                                    })

    subdependencia = ChainedForeignKey(Dependencia,
                                       chained_field="dependencia",
                                       chained_model_field="dependienteDe",
                                       null=True,
                                       blank=True,
                                       )

    estado = models.ForeignKey(Estado)
    impacto = models.ForeignKey(Impacto, blank=True, null=True)
    instanciaEjecutora = models.ForeignKey(InstanciaEjecutora, blank=True, null=True)
    registroHacendario = models.CharField(max_length=200, blank=True, null=True)
    montoRegistroHacendario = models.FloatField(verbose_name="Recursos Federales Autorizados", blank=True, null=True)

    tipoInversion = models.ManyToManyField(TipoInversion,
                                           through='DetalleInversion',
                                           null=True,
                                           blank=True, )

    tipoClasificacion = models.ManyToManyField("self", TipoClasificacion,
                                               through='DetalleClasificacion',
                                               symmetrical=False,
                                               limit_choices_to={
                                                   'subclasificacionDe': None,
                                               },
                                               null=True,
                                               blank=True,

                                               )

    subclasificacion = ChainedForeignKey(TipoClasificacion,
                                         related_name='%(class)s_subclasificaciones',
                                         chained_field="tipoClasificacion",
                                         chained_model_field="subclasificacionDe",
                                         null=True,
                                         blank=True,
                                         )

    inaugurador = models.ForeignKey(Inaugurador, null=True, blank=True)
    denominacion = models.CharField(max_length=200, verbose_name='Denominación')
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField(verbose_name="Fecha de Inicio")
    fechaTermino = models.DateField(verbose_name="Fecha de Término")
    inversionTotal = models.FloatField()
    totalBeneficiarios = models.IntegerField()
    senalizacion = models.BooleanField(default=False, verbose_name='Señalización')
    susceptibleInauguracion = models.BooleanField(default=False)
    porcentajeAvance = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.CharField(max_length=200, null=True, blank=True)
    fotoAntes = models.FileField(blank=True, null=True, upload_to=content_file_antes)
    fotoDurante = models.FileField(blank=True, null=True, upload_to=content_file_durante)
    fotoDespues = models.FileField(blank=True, null=True, upload_to=content_file_despues)
    fechaModificacion = models.DateTimeField(auto_now=True, auto_now_add=True, verbose_name='Fecha de Modificación')
    inaugurada = models.BooleanField(choices=BOOL_CHOICES, blank=False, null=False, default=False)
    poblacionObjetivo = models.CharField(max_length=200)
    municipio = models.ForeignKey(Municipio)

    tipoMoneda = models.ForeignKey(TipoMoneda, blank=False, default=1)
    autorizada = models.BooleanField(default=False)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    id_Dependencia = models.CharField(verbose_name='Identificador Interno', max_length=200, null=True, blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.identificador_unico + " " + self.denominacion[0:30]

    def to_serializable_dict(self):
        map = {}

        map['identificador_unico'] = self.identificador_unico
        if self.tipoObra:
            map['tipoObra'] = self.tipoObra.to_serializable_dict()
        else:
            map['tipoObra'] = None
        if self.dependencia:
            map['dependencia'] = self.dependencia.to_serializable_dict()
        else:
            map['dependencia'] = None
        if self.subdependencia:
            map['subdependenencia'] = self.subdependencia.to_serializable_dict()
        else:
            map['subdependenencia'] = None
        if self.estado:
            map['estado'] = self.estado.to_serializable_dict()
        else:
            map['estado'] = None
        if self.impacto:
            map['impacto'] = self.impacto.to_serializable_dict()
        else:
            map['impacto'] = None
        if self.instanciaEjecutora:
            map['instanciaEjecutora'] = self.instanciaEjecutora.to_serializable_dict()
        else:
            map['instanciaEjecutora'] = None
        if self.municipio:
            map['municipio'] = self.municipio.nombreMunicipio
        else:
            map['municipio'] = None


        map['tipoInversion'] = []
        if self.tipoInversion:
            for tipoInversion in self.tipoInversion.all():
                map['tipoInversion'].append(tipoInversion.to_serializable_dict())

        map['tipoClasificacion'] = []
        try:
            detalles = DetalleClasificacion.objects.filter(obra__id=self.id)
            for detalleTipoClasificacion in detalles.all():
                map['tipoClasificacion'].append(detalleTipoClasificacion.tipoClasificacion.to_serializable_dict())

        except Exception as e:
            print e

        map['subclasificaciones'] = []
        if self.subclasificacion:
            for subclasificacion in self.subclasificacion.all():
                map['subclasificaciones'].append(subclasificacion.to_serializable_dict())

        if self.inaugurador:
            map['inaugurador'] = self.inaugurador.to_serializable_dict()
        else:
            map['inaugurador'] = None
        map['registroHacendario'] = self.registroHacendario
        map['denominacion'] = self.denominacion
        map['descripcion'] = self.descripcion
        map['observaciones'] = self.observaciones
        if self.fechaModificacion is None:
            map['fechaModificacion'] = None
        else:
            map['fechaModificacion'] = self.fechaModificacion.isoformat()
        if self.fechaInicio is None:
            map['fechaInicio'] = None
        else:
            map['fechaInicio'] = self.fechaInicio.__str__()
        if self.fechaTermino is None:
            map['fechaTermino'] = None
        else:
            map['fechaTermino'] = self.fechaTermino.__str__()
        if self.inversionTotal is None:
            map['inversionTotal'] = 0.0
        else:
            map['inversionTotal'] = float(self.inversionTotal)
        if self.totalBeneficiarios is None:
            map['totalBeneficiarios'] = 0
        else:
            map['totalBeneficiarios'] = int(self.totalBeneficiarios)
        map['senalizacion'] = self.senalizacion
        map['susceptibleInauguracion'] = self.susceptibleInauguracion
        if self.porcentajeAvance is None:
            map['porcentajeAvance'] = 0.0
        else:
            map['porcentajeAvance'] = float(self.porcentajeAvance)
        if self.fotoAntes is None:
            map['fotoAntes'] = None
        else:
            map['fotoAntes'] = self.fotoAntes.name
        if self.fotoDurante is None:
            map['fotoDurante'] = None
        else:
            map['fotoDurante'] = self.fotoDurante.name
        if self.fotoDespues is None:
            map['fotoDespues'] = None
        else:
            map['fotoDespues'] = self.fotoDespues.name
        map['inaugurada'] = self.inaugurada
        map['poblacionObjetivo'] = self.poblacionObjetivo

        if self.tipoMoneda is None:
            map['tipoMoneda'] = None
        else:
            map['tipoMoneda'] = self.tipoMoneda.to_serializable_dict()

        return map
    # static method to perform a parameter
    @staticmethod
    def searchList(p_tipoobra,p_dependencias,p_subdependencias,p_municipios,p_instancia_ejecutora,p_estados,inversion_minima,inversion_maxima,fecha_inicio_primera,fecha_inicio_segunda,fecha_fin_primera,fecha_fin_segunda,p_impactos,p_inauguradores,p_inversiones,p_clasificaciones,susceptible,inaugurada,denominacion):

        # create a cursor
        cur = connection.cursor()
        # execute the stored procedure passing in
        # A SOME parameters
        # '',p_dependencias,'','',0,0,'2010-08-01','2011-08-01','2020-08-01','2021-08-01','','','','','','','',
        cur.callproc('sp_listado', (p_tipoobra,p_dependencias,p_subdependencias,p_municipios,p_instancia_ejecutora,p_estados,inversion_minima,inversion_maxima,fecha_inicio_primera,fecha_inicio_segunda,fecha_fin_primera,fecha_fin_segunda,p_impactos,p_inauguradores,p_inversiones,p_clasificaciones,susceptible,inaugurada,denominacion,))
        # grab the results
        results = cur.fetchall()
        cur.close()

        # wrap the results up into Document domain objects
        #return [Obra(*row) for row in results]
        return results



def content_file_documento_fuente(instance, filename):
    # print instance.identificador_unico
    # ext = filename.split('.')[-1]
    # filename = instance.identificador_unico + '_ANTES.'+ext
    return '/'.join(['documentosFuente', instance.obra.identificador_unico, filename])


@python_2_unicode_compatible
class DocumentoFuente(models.Model):
    descripcion = models.CharField(max_length=50, )
    documento = models.FileField(upload_to=content_file_documento_fuente, )
    obra = models.ForeignKey('Obra', )

    def __str__(self):
        return self.descripcion

    def __unicode__(self):
        return self.descripcion

    def delete(self, using=None):
        self.documento.delete()
        super(DocumentoFuente, self).delete(using)


# modelo temporal para probar ubicaciones de obras en mapa
class Ubicacion(models.Model):
    nombre = models.SlugField(unique=True, null=True, )
    tipoObra = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    dependencia = models.CharField(max_length=100)
    # user = models.OneToOneField(User)  asi estaba debe ser foreign key

    def __str__(self):
        return self.nombre


class DetalleInversion(models.Model):
    obra = models.ForeignKey(Obra)
    tipoInversion = models.ForeignKey(TipoInversion,

                                      )
    monto = models.FloatField()

    class Meta:
        unique_together = [("obra", "tipoInversion")]

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class DetalleClasificacion(models.Model):
    class Meta:
        unique_together = [("obra", "tipoClasificacion")]

    obra = models.ForeignKey(Obra)
    tipoClasificacion = models.ForeignKey(TipoClasificacion,
                                          related_name="obra_clasificacion",
                                          limit_choices_to={
                                              'subclasificacionDe': None,
                                          },
                                          null=True,
                                          blank=True
                                          )

    subclasificacion = ChainedForeignKey(TipoClasificacion,
                                         related_name='obra_subclasificacion',
                                         chained_field='tipoClasificacion',
                                         chained_model_field='subclasificacionDe',
                                         null=True,
                                         blank=True,
                                         )

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


def get_subdependencias_as_list_flat(deps):
    if deps is None or deps.count() == 0:
        return None
    ans = []
    for dependencia in deps:
        ans.append(dependencia)
        subdeps = dependencia.get_subdeps_flat()
        if subdeps and subdeps.count() > 0:
            ans.extend(subdeps)
    return ans
