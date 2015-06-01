from django.db import models
from django.contrib.auth.models import User

#TODO agregar nombres verbose a los modelos


# Create your models here.
from django.forms import model_to_dict


class TipoObra(models.Model):
    nombreTipoObra = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoObra

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200)
    imagenDependencia = models.FileField(upload_to="./", blank=True, null=True)
    dependienteDe = models.ForeignKey('self', null=True, blank=True)
    obraoprograma = models.CharField(max_length=1)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreDependencia

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        if ans['dependienteDe'] is None:
            ans['dependienteDe'] = None
        else:
            ans['dependienteDe'] = str(self.dependienteDe_id)

        # We KNOW that this entry must be a FileField value
        # (therefore, calling its name attribute is safe),
        # so we need to mame it JSON serializable (Django objects
        # are not by default and its built-in serializer sucks),
        # namely, we only need the path
        if self.imagenDependencia is None or self.imagenDependencia.name == '' or self.imagenDependencia.name == '':
            ans['imagenDependencia'] = None
        else:
            ans['imagenDependencia'] = self.imagenDependencia.url

        return ans


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


class Impacto(models.Model):
    nombreImpacto = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreImpacto

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class TipoInversion(models.Model):
    nombreTipoInversion = models.CharField(max_length=200)
    nombreTipoInversionCorta = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoInversion

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans


class TipoClasificacion(models.Model):
    subclasificacionDe = models.ForeignKey('self', null=True, blank=True)
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

class Inaugurador(models.Model):
    nombreCargoInaugura = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreCargoInaugura

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        return ans



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
    dependencia = models.ForeignKey(Dependencia, blank=True, null=True)


class InstanciaEjecutora(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

    def to_serializable_dict(self):
        map = {'nombre': self.nombre}
        return map


class Obra(models.Model):
    #TODO agrupar semanticamente todos los campos de obras
    identificador_unico = models.SlugField(unique=True, null=True, )
    tipoObra = models.ForeignKey(TipoObra)
    dependencia = models.ForeignKey(Dependencia)
    estado = models.ForeignKey(Estado)
    impacto = models.ForeignKey(Impacto)
    instanciaEjecutora = models.ForeignKey(InstanciaEjecutora, blank=True, null=True)
    registroHacendario = models.CharField(max_length=200, blank=True, null=True)
    montoRegistroHacendario = models.FloatField(blank=True, null=True)
    tipoInversion = models.ManyToManyField(TipoInversion)
    tipoClasificacion = models.ManyToManyField(TipoClasificacion)
    inaugurador = models.ForeignKey(Inaugurador)
    registroAuditoria = models.CharField(max_length=200)
    denominacion = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200)
    fechaInicio = models.DateField()
    fechaTermino = models.DateField()
    inversionTotal = models.DecimalField(max_digits=19, decimal_places=10)
    totalBeneficiarios = models.DecimalField(max_digits=19, decimal_places=10)
    senalizacion = models.BooleanField(default=False)
    susceptibleInauguracion = models.BooleanField(default=False)
    porcentajeAvance = models.DecimalField(max_digits=3, decimal_places=2)
    observaciones = models.CharField(max_length=200)
    fotoAntes = models.FileField(upload_to="/", blank=True, null=True)
    fotoDurante = models.FileField(upload_to="/", blank=True, null=True)
    fotoDespues = models.FileField(upload_to="/", blank=True, null=True)
    fechaModificacion = models.DateTimeField(auto_now=True, auto_now_add=True)
    inaugurada = models.BooleanField(default=False)
    poblacionObjetivo = models.CharField(max_length=200)
    municipio = models.CharField(max_length=200)
    tipoMoneda = models.ForeignKey(TipoMoneda, blank=True, null=True)
    autorizada = models.BooleanField(default=False)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):  # __unicode__ on Python 2
        return self.denominacion

    def to_serializable_dict(self):
        map = {}

        map['identificador'] = self.identificador_unico
        map['tipoObra'] = self.tipoObra.to_serializable_dict()
        map['dependencia'] = self.dependencia.to_serializable_dict()
        map['estado'] = self.estado.to_serializable_dict()
        map['impacto'] = self.impacto.to_serializable_dict()
        map['instanciaEjecutora'] = self.instanciaEjecutora.to_serializable_dict()

        map['tipoInversion'] = []
        for tipoInversion in self.tipoInversion.all():
            tipo = tipoInversion.to_serializable_dict()
            map['tipoInversion'].append(tipo)

        map['tipoClasificacion'] = []
        for tipoClasificacion in self.tipoClasificacion.all():
            tipo = tipoClasificacion.to_serializable_dict()
            map['tipoClasificacion'].append(tipo)

        map['inaugurador'] = self.inaugurador.to_serializable_dict()
        map['registroHacendario'] = self.registroHacendario
        map['registroAuditoria'] = self.registroAuditoria
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



class DocumentoFuente(models.Model):
    descripcion = models.TextField(blank=True, null=True)
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