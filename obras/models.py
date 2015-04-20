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
    imagenDependencia = models.FileField(blank=True, null=True)
    dependienteDe = models.ForeignKey('self', null=True, blank=True)

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
            ans['imagenDependencia'] = self.imagenDependencia.name

        return ans


class Estado(models.Model):
    nombreEstado = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):  # __unicode__ on Python 2
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


class Obra(models.Model):
    #TODO agrupar semanticamente todos los campos de obras
    identificador_unico = models.SlugField(unique=True, null=True, )
    tipoObra = models.ForeignKey(TipoObra)
    dependencia = models.ForeignKey(Dependencia)
    estado = models.ForeignKey(Estado)
    impacto = models.ForeignKey(Impacto)
    tipoInversion = models.ManyToManyField(TipoInversion)
    tipoClasificacion = models.ManyToManyField(TipoClasificacion)
    inaugurador = models.ForeignKey(Inaugurador)
    registroHacendario = models.CharField(max_length=200)
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
    fotoAntes = models.FileField(blank=True, null=True)
    fotoDurante = models.FileField(blank=True, null=True)
    fotoDespues = models.FileField(blank=True, null=True)
    fechaModificacion = models.DateField(auto_now=True)
    inaugurada = models.BooleanField(default=False)
    poblacionObjetivo = models.CharField(max_length=200)
    municipio = models.CharField(max_length=200)
    tipoMoneda = models.ForeignKey(TipoMoneda, blank=True, null=True)
    autorizada = models.BooleanField(default=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.denominacion

    def to_serializable_dict(self):
        return model_to_dict(self)