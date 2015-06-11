from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from smart_selects.db_fields import ChainedForeignKey

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


@python_2_unicode_compatible
class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200)
    imagenDependencia = models.FileField(upload_to="./", blank=True, null=True)
    dependienteDe = models.ForeignKey('self', null=True, blank=True)
    obraoprograma = models.CharField(max_length=1, null=True, blank=True, default='O')
    fecha_ultima_modificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreDependencia

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
            ans['dependienteDe'] = str(self.depenienteDe_id)

        # We KNOW that this entry must be a FileField value
        # (therefore, calling its name attribute is safe),
        # so we need to mame it JSON serializable (Django objects
        # are not by default and its built-in serializer sucks),
        # namely, we only need the path

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


@python_2_unicode_compatible
class Impacto(models.Model):
    nombreImpacto = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreImpacto

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


@python_2_unicode_compatible
class TipoInversion(models.Model):
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
    dependencia = models.ManyToManyField(Dependencia, blank=True, null=True)


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


BOOL_CHOICES = ((True, 'Si'), (False, 'No'), (None, 'Sin inauguracion'))


@python_2_unicode_compatible
class Obra(models.Model):
    # TODO agrupar semanticamente todos los campos de obras
    identificador_unico = models.SlugField(unique=True, null=True, )
    tipoObra = models.ForeignKey(TipoObra)
    dependencia = models.ForeignKey(Dependencia, related_name='%(class)s_dependencia',
                                    limit_choices_to={
                                        'dependienteDe': None,
                                    })

    subdependencia = ChainedForeignKey(Dependencia,
                                       chained_field="dependencia",
                                       chained_model_field="dependienteDe",
                                       null=True,
                                       blank=True,
                                       )

    estado = models.ForeignKey(Estado)
    impacto = models.ForeignKey(Impacto)
    instanciaEjecutora = models.ForeignKey(InstanciaEjecutora, blank=True, null=True)
    registroHacendario = models.CharField(max_length=200, blank=True, null=True)
    montoRegistroHacendario = models.FloatField(verbose_name="Recursos Federales Autorizados", blank=True, null=True)
    tipoInversion = models.ManyToManyField(TipoInversion, through='DetalleInversion')

    tipoClasificacion = models.ManyToManyField("self", TipoClasificacion,
                                               through='DetalleClasificacion',

                                               symmetrical=False,
                                               limit_choices_to={
                                                   'subclasificacionDe': None,
                                               }
                                               )


    inaugurador = models.ForeignKey(Inaugurador)
    denominacion = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField()
    fechaTermino = models.DateField(verbose_name="Fecha de Termino")
    inversionTotal = models.DecimalField(max_digits=19, decimal_places=10)
    totalBeneficiarios = models.DecimalField(max_digits=19, decimal_places=10)
    senalizacion = models.BooleanField(default=False)
    susceptibleInauguracion = models.BooleanField(default=False)
    porcentajeAvance = models.DecimalField(max_digits=3, decimal_places=2)
    observaciones = models.CharField(max_length=200)
    fotoAntes = models.FileField(blank=True, null=True)
    fotoDurante = models.FileField(blank=True, null=True)
    fotoDespues = models.FileField(blank=True, null=True)
    fechaModificacion = models.DateTimeField(auto_now=True, auto_now_add=True)
    inaugurada = models.NullBooleanField(choices=BOOL_CHOICES)
    poblacionObjetivo = models.CharField(max_length=200)
    municipio = models.CharField(max_length=200)
    tipoMoneda = models.ForeignKey(TipoMoneda, blank=False, default=1)
    autorizada = models.BooleanField(default=False)
    latitud = models.FloatField()
    longitud = models.FloatField()
    id_Dependencia = models.CharField(verbose_name='Identificador Interno' , max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.denominacion

    def to_serializable_dict(self):
        map = {}

        map['identificador'] = self.identificador_unico
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

        map['tipoInversion'] = []
        if self.tipoInversion:
            for tipoInversion in self.tipoInversion.all():
                map['tipoInversion'].append(tipoInversion.to_serializable_dict())

        map['tipoClasificacion'] = []
        if self.tipoClasificacion:
            for tipoClasificacion in self.tipoClasificacion.all():
                map['tipoClasificacion'].append(tipoClasificacion.to_serializable_dict())

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
            map['fotoAntes'] = None
        else:
            map['fotoAntes'] = self.fotoDurante.name
        if self.fotoDespues is None:
            map['fotoAntes'] = None
        else:
            map['fotoAntes'] = self.fotoDespues.name
        map['inaugurada'] = self.inaugurada
        map['poblacionObjetivo'] = self.poblacionObjetivo
        map['municipio'] = self.municipio
        if self.tipoMoneda is None:
            map['tipoMoneda'] = None
        else:
            map['tipoMoneda'] = self.tipoMoneda.to_serializable_dict()

        return map


@python_2_unicode_compatible
class DocumentoFuente(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    documento = models.FileField(upload_to="/", blank=True, null=True)
    obra = models.ForeignKey('Obra', blank=True, null=True)

    def __str__(self):
        return self.descripcion

    def __unicode__(self):
        return self.descripcion


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
    tipoInversion = models.ForeignKey(TipoInversion)
    monto = models.FloatField()


class DetalleClasificacion(models.Model):
    obra = models.ForeignKey(Obra)
    tipoClasificacion = models.ForeignKey(TipoClasificacion,
                                          limit_choices_to={
                                              'subclasificacionDe': None,
                                          }
                                          )

    subclasificacion = ChainedForeignKey(TipoClasificacion,
                                         related_name='%(class)s_subclasificaciones',
                                         chained_field='tipoClasificacion',
                                         chained_model_field='subclasificacionDe',
                                         null=True,
                                         blank=True,
                                         )
    
def get_subdependencias_as_list_flat(deps):
    ans = []
    for dependencia in deps:
        ans.append(dependencia)
        subdeps = dependencia.get_subdeps_flat()
        if subdeps and subdeps.count() > 0:
            ans.extend(subdeps)
    return ans