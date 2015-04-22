from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.contrib.admin import SimpleListFilter

from obras.models import *
from obras.forms import AddObraForm




# Register your models here.+

# Define an inline admin descriptor for Usuario model
# which acts a bit like a singleton
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Usuario'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dependencia":
            if request.user.usuario.rol == 'SA':
                kwargs["queryset"] = Dependencia.objects.all()
            if request.user.usuario.rol == 'AD':
                kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id=request.user.usuario.dependencia.id) |
                    Q(dependienteDe__id=request.user.usuario.dependencia.id))

        return super(
            UsuarioInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UsuarioInline, )
    list_display = ('username','first_name','last_name','email','get_dependencia',)

    def get_dependencia(self,obj):
        return obj.usuario.dependencia
    get_dependencia.short_description = 'Dependencia'

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.usuario.rol == 'SA':
            print 'Query Set Superadmin'
            return qs
        elif request.user.usuario.rol == 'AD':
            print 'Query Set Administrador dependencia'
            return qs.filter(
                Q(usuario__dependencia=request.user.usuario.dependencia) |
                Q(usuario__dependencia__dependienteDe=request.user.usuario.dependencia)
            )
        elif request.user.usuario.rol == 'US':
                print 'Query Set Usuario'
                return qs.filter(
                    Q(usuario__dependencia=request.user.usuario.dependencia)
                )


class InversionInLine(admin.StackedInline):
    model = TipoInversion
    extra = 3


class DependenciaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(DependenciaAdmin, self).queryset(request)
        if request.user.usuario.rol == 'SA':  # Secretaria tecnica
            return qs
        if request.user.usuario.rol == 'AD':  # Dependencia
            return qs.filter(
                Q(id=request.user.usuario.dependencia.id) |
                Q(dependienteDe__id=request.user.usuario.dependencia.id)
            )

        return qs.filter(Q(id=request.user.usuario.dependencia_id))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dependienteDe":
            if request.user.usuario.rol == 'SA':
                kwargs["queryset"] = Dependencia.objects.filter(dependienteDe=None)
                return super(DependenciaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            elif request.user.usuario.rol == 'AD':
                kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id=request.user.usuario.dependencia.id)
                )
                return super(DependenciaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ClasificacionInLine(admin.StackedInline):
    model = TipoClasificacion
    extra = 3


class DocumentoFuenteInline(admin.TabularInline):
    model = DocumentoFuente
    extra = 1


class DependenciaListFilter(SimpleListFilter):

    # USAGE
    # In your admin class, pass three filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Dependencias',)

    parameter_name = 'dependencia'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        if request.user.usuario.rol == 'SA':  # Secretaria tecnica
            dependencias = Dependencia.objects.all()
        if request.user.usuario.rol == 'AD':  # Dependencia
            dependencias =  Dependencia.objects.filter(
                Q(id=request.user.usuario.dependencia.id) |
                Q(dependienteDe__id=request.user.usuario.dependencia.id)
            )
        if request.user.usuario.rol == 'US':
            dependencias = Dependencia.objects.filter(
                Q(id=request.user.usuario.dependencia.id)
            )

        list_tuple = []
        for dependencia in dependencias:
            list_tuple.append((dependencia.id, dependencia.nombreDependencia))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value():
            return queryset.filter(dependencia__id=self.value())


def make_authorized(obrasadmin, request, queryset):
    queryset.update(autorizada=True)


make_authorized.short_description = "Autorizar las obras seleccionadas"


def make_unauthorized(obrasadmin, request, queryset):
    queryset.update(autorizada=False)


make_unauthorized.short_description = "No Autorizar las obras seleccionadas"


class ObrasAdmin(admin.ModelAdmin):
    form = AddObraForm
    inlinesInversion = [InversionInLine]
    inlinesClasificacion = [ClasificacionInLine]
    inlines = [DocumentoFuenteInline]
    list_display = (
        'identificador_unico',
        'denominacion',
        'autorizada',
        'tipoObra',
        'dependencia',
        'senalizacion',
        'inaugurada',
        'fechaInicio',
        'fechaTermino')
    list_filter = [DependenciaListFilter, 'autorizada']
    readonly_fields = ('identificador_unico',)
    actions = [make_authorized, make_unauthorized]

    # def get_fieldsets(self, request, obj=None):
    # fieldsets = [
    # ('Hacienda',
    #                         {'fields':
    #                             ['registroHacendario',
    #                              'montoRegistroHacendario'
    #                             ]
    #                          }
    #                     ),
    #                 ]
    #     return fieldsets

    def get_fields(self, request, obj=None):
        if request.user.usuario.rol == 'US':
            fields = ('identificador_unico',
                      'tipoObra',
                      'dependencia',
                      'instanciaEjecutora',
                      'estado',
                      'impacto',
                      'tipoInversion',
                      'tipoClasificacion',
                      'inaugurador',
                      'registroHacendario',
                      'montoRegistroHacendario',
                      'registroAuditoria',
                      'denominacion',
                      'descripcion',
                      'observaciones',
                      'fechaInicio',
                      'fechaTermino',
                      'inversionTotal',
                      'totalBeneficiarios',
                      'senalizacion',
                      'susceptibleInauguracion',
                      'porcentajeAvance',
                      'observaciones',
                      'fotoAntes',
                      'fotoDurante',
                      'fotoDespues',
                      'inaugurada',
                      'poblacionObjetivo',
                      'municipio',
                      'tipoMoneda',
                      )


        else:
            fields = ('identificador_unico',
                      'autorizada',
                      'tipoObra',
                      'instanciaEjecutora',
                      'dependencia',
                      'estado',
                      'impacto',
                      'tipoInversion',
                      'tipoClasificacion',
                      'inaugurador',
                      ('registroHacendario',
                       'montoRegistroHacendario',),
                      'registroAuditoria',
                      'denominacion',
                      'descripcion',
                      'observaciones',
                      'fechaInicio',
                      'fechaTermino',
                      'inversionTotal',
                      'totalBeneficiarios',
                      'senalizacion',
                      'susceptibleInauguracion',
                      'porcentajeAvance',
                      'observaciones',
                      'fotoAntes',
                      'fotoDurante',
                      'fotoDespues',
                      'inaugurada',
                      'poblacionObjetivo',
                      'municipio',
                      'tipoMoneda',
                      )
        return fields

    def get_actions(self, request):
        actions = super(ObrasAdmin, self).get_actions(request)
        if request.user.usuario.rol == 'US':
            del actions['make_authorized']
            del actions['make_unauthorized']
        return actions

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dependencia":
            if request.user.usuario.rol == 'SA':
                kwargs["queryset"] = Dependencia.objects.all()
            elif request.user.usuario.rol == 'AD':
                kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id=request.user.usuario.dependencia.id) |
                    Q(dependienteDe__id=request.user.usuario.dependencia.id))
            elif request.user.usuario.rol == 'US':
                    kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id=request.user.usuario.dependencia.id)
                    )

        return super(
            ObrasAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(ObrasAdmin, self).get_queryset(request)
        if request.user.usuario.rol == 'SA':
            print 'Query Set Superadmin'
            return qs
        elif request.user.usuario.rol == 'AD':
            print 'Query Set Administrador dependencia'
            return qs.filter(
                Q(dependencia=request.user.usuario.dependencia) |
                Q(dependencia__dependienteDe=request.user.usuario.dependencia)
            )
        elif request.user.usuario.rol == 'US':
                print 'Query Set Usuario'
                return qs.filter(
                Q(dependencia=request.user.usuario.dependencia)
                )



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(TipoObra)
admin.site.register(Dependencia, DependenciaAdmin)
admin.site.register(Estado)
admin.site.register(Impacto)
admin.site.register(Inaugurador)
admin.site.register(TipoMoneda)
admin.site.register(TipoInversion)
admin.site.register(TipoClasificacion)
admin.site.register(Obra, ObrasAdmin)
admin.site.register(InstanciaEjecutora)
