from django.db import models
from django.contrib.auth.models import User

#TODO agregar nombres verbose a los modelos

# Create your models here.
class TipoObra(models.Model):
    nombreTipoObra = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoObra


class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200)
    imagenDependencia = models.FileField(blank=True, null=True)
    dependienteDe = models.ForeignKey('self', null=True, blank=True)
    obraoprograma = models.CharField(max_length=1)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreDependencia


class Estado(models.Model):
    nombreEstado = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreEstado


class Impacto(models.Model):
    nombreImpacto = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreImpacto


class TipoInversion(models.Model):
    nombreTipoInversion = models.CharField(max_length=200)
    nombreTipoInversionCorta = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoInversion


class TipoClasificacion(models.Model):
    subclasificacionDe = models.ForeignKey('self', null=True, blank=True)
    nombreTipoClasificacion = models.CharField(max_length=200)
    nombreTipoClasificacionCorta = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoClasificacion


class Inaugurador(models.Model):
    nombreCargoInaugura = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreCargoInaugura


class TipoMoneda(models.Model):
    nombreTipoDeMoneda = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreTipoDeMoneda


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


class DocumentoFuente(models.Model):
    descripcion = models.TextField(blank=True, null=True)
    documento = models.FileField(blank=True, null=True)
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
