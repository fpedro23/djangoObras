from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect
from django.contrib import messages
from obras.models import *
from obras.forms import AddObraForm, DetalleInversionAddForm, DetalleClasificacionAddForm, DocumentoFuenteForm
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry

# Register your models here.+

# Define an inline admin descriptor for Usuario model
# which acts a bit like a singleton
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Usuario'
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        arreglo_dependencias = []

        for dependencia in request.user.usuario.dependencia.all():
            arreglo_dependencias.append(dependencia.id)

        if db_field.name == "dependencia":
            if request.user.usuario.rol == 'SA':
                kwargs["queryset"] = Dependencia.objects.all()
            if request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':
                kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id__in=arreglo_dependencias) |
                    Q(dependienteDe__id__in=arreglo_dependencias))

        return super(
            UsuarioInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UsuarioInline, )
    list_per_page = 8
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_dependencia', 'get_subdependencia')
    fieldsets = (
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('AuthInfo'), {'fields': ('username', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (('AuthInfo'), {'fields': ('username', 'password1', 'password2')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active',)}),
    )

    def response_add(self, request, obj, post_url_continue=None):

        if '_addanother' not in request.POST:
            return HttpResponseRedirect('/admin/auth/user')
        else:
            return super(UserAdmin, self).response_add(request, obj, post_url_continue)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        print obj.usuario
        usuario = obj
        usuario.save()

        print usuario.usuario
        if usuario.usuario.rol == 'SA':
            usuario.is_superuser = True
        elif usuario.usuario.rol == 'AD' or usuario.usuario.rol == 'UD':
            g = Group.objects.get(name='administrador_dependencia')
            g.user_set.add(usuario)
            print 'Definir permisos de administrador de dependencia'

        elif usuario.usuario.rol == 'US':
            g = Group.objects.get(name='usuario_dependencia')
            g.user_set.add(usuario)
            print 'Definir permisos para usuario'

        elif usuario.usuario.rol == 'FU':
            g = Group.objects.get(name='funcionario')
            g.user_set.add(usuario)
            print 'Definir permisos para funcionario'


        super(UserAdmin, self).save_model(request, obj, form, change)


    def delete_model(self, request, obj):
        self.message_user(request, "Usuario eliminado satisfactoriamente", )
        super(UserAdmin, self).delete_model(request, obj)


    def get_subdependencia(self, obj):
        return ",\n".join([dependencia.nombreDependencia for dependencia in obj.usuario.subdependencia.all()])

    def get_dependencia(self, obj):
        return ",\n".join([dependencia.nombreDependencia for dependencia in obj.usuario.dependencia.all()])

    get_dependencia.short_description = 'Dependencia'
    get_subdependencia.short_description = 'SubDependencia'

    def get_queryset(self, request):
        arreglo_dependencias = []

        for dependencia in request.user.usuario.dependencia.all():
            arreglo_dependencias.append(dependencia.id)

        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.usuario.rol == 'SA':
            print 'Query Set Superadmin'
            return qs
        elif request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':
            print 'Query Set Administrador dependenciasub'
            print arreglo_dependencias
            return qs.filter(
                Q(usuario__dependencia__id__in=arreglo_dependencias) |
                Q(usuario__dependencia__dependienteDe__id__in=arreglo_dependencias)
            )
        elif request.user.usuario.rol == 'US':
            print 'Query Set Usuario'
            return qs.filter(
                Q(usuario__dependencia=request.user.usuario.dependencia)
            )


class DependenciaAdmin(admin.ModelAdmin):
    exclude = ('fecha_ultima_modificacion', 'obraoprograma', 'orden_secretaria')

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(DependenciaAdmin, self).queryset(request)
        if request.user.usuario.rol == 'SA':  # Secretaria tecnica
            return qs
        if request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':  # Dependencia
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
            elif request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':
                kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id=request.user.usuario.dependencia.id)
                )
                return super(DependenciaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ClasificacionInLine(admin.StackedInline):
    model = TipoClasificacion
    extra = 4


class DocumentoFuenteInline(admin.TabularInline):
    model = DocumentoFuente
    extra = 2
    form = DocumentoFuenteForm


class DependenciaListFilter(SimpleListFilter):
    # USAGE
    # In your admin class, pass three filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Dependencia'

    parameter_name = 'dependencia'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        arreglo_dependencias = []
        for dependencia in request.user.usuario.dependencia.all():
            arreglo_dependencias.append(dependencia.id)

        if request.user.usuario.rol == 'SA':  # Secretaria tecnica
            dependencias = Dependencia.objects.filter(
                Q(obraoprograma='O') &
                Q(dependienteDe__isnull=True)
            )

        elif request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':  # Dependencia
            dependencias = Dependencia.objects.filter(
                Q(id__in=arreglo_dependencias) &
                Q(obraoprograma='O')

            )
        elif request.user.usuario.rol == 'US':
            dependencias = Dependencia.objects.filter(
                Q(id__in=arreglo_dependencias)
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


class SubDependenciaListFilter(SimpleListFilter):
    # USAGE
    # In your admin class, pass three filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Subdependencia'

    parameter_name = 'subdependencia'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        arreglo_dependencias = []
        for dependencia in request.user.usuario.dependencia.all():
            arreglo_dependencias.append(dependencia.id)

        if request.user.usuario.rol == 'SA':  # Secretaria tecnica
            dependencias = Dependencia.objects.filter(
                Q(obraoprograma='O') &
                Q(dependienteDe__isnull=False)
            )

        elif request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':  # Dependencia
            dependencias = Dependencia.objects.filter(
                Q(dependienteDe__id__in=arreglo_dependencias) &
                Q(obraoprograma='O')

            )
        elif request.user.usuario.rol == 'US':
            for dependencia in request.user.usuario.subdependencia.all():
                arreglo_dependencias.append(dependencia.id)

            dependencias = Dependencia.objects.filter(
                Q(dependienteDe__id__in=arreglo_dependencias)
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
            return queryset.filter(subdependencia__id=self.value())


class EstadoListFilter(SimpleListFilter):
    # USAGE
    # In your admin class, pass three filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Estado'

    parameter_name = 'estado'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        list_tuple = []
        for estado in Estado.objects.all():
            list_tuple.append((estado.id, estado.nombreEstado))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value():
            return queryset.filter(estado__id=self.value())

class MunicipioListFilter(SimpleListFilter):
    # USAGE
    # In your admin class, pass three filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Municipio'

    parameter_name = 'municipio'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        list_tuple = []
        for municipio in Municipio.objects.all():
            list_tuple.append((municipio.id, municipio.nombreMunicipio))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value():
            return queryset.filter(municipio__id=self.value())

def make_authorized(obrasadmin, request, queryset):
    queryset.update(autorizada=True)


make_authorized.short_description = "Autorizar las obras seleccionadas"


def make_unauthorized(obrasadmin, request, queryset):
    queryset.update(autorizada=False)


make_unauthorized.short_description = "No Autorizar las obras seleccionadas"


class DetalleInversionInline(admin.TabularInline):
    form = DetalleInversionAddForm
    model = DetalleInversion
    extra = 1
    can_delete = False


class DetalleClasificacionInline(admin.TabularInline):
    form = DetalleClasificacionAddForm
    model = DetalleClasificacion
    extra = 5
    can_delete = False


class ObrasAdmin(admin.ModelAdmin):
    form = AddObraForm
    inlinesClasificacion = [ClasificacionInLine]
    inlines = (DetalleInversionInline, DocumentoFuenteInline, DetalleClasificacionInline)

    readonly_fields = []

    list_display = (
        'identificador_unico',
        'estado',
        'denominacion',
        'autorizada',
        'tipoObra',
        'dependencia',
        'subdependencia',
        'fechaInicio',
        'fechaTermino',
        'fechaModificacion',
    )
    ordering = ['identificador_unico']

    list_filter = [DependenciaListFilter, 'autorizada', SubDependenciaListFilter, EstadoListFilter, MunicipioListFilter,]
    actions = [make_authorized, make_unauthorized]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('identificador_unico',)
        return readonly_fields

    def save_model(self, request, obj, form, change):
        print request.user.usuario.rol

        if change and request.user.usuario.rol == 'US':
            obj.autorizada = False

        if change:
            success_message = 'La obra \"%s\" se ha modificado exitosamente.' % obj.__str__()

            self.message_user(request, success_message, level=messages.SUCCESS)
        else:
            success_message = 'La obra \"%s\" se ha creado exitosamente.' % obj.__str__()

            self.message_user(request, success_message, level=messages.SUCCESS)

        super(ObrasAdmin, self).save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        if request.user.usuario.rol == 'US':
            fields = ('identificador_unico',
                      'id_Dependencia',
                      'denominacion',
                      'dependencia',
                      'subdependencia',
                      'instanciaEjecutora',
                      'estado',
                      'municipio',
                      'latitud',
                      'longitud',
                      'descripcion',
                      'porcentajeAvance',
                      'tipoObra',
                      'fechaInicio',
                      'fechaTermino',
                      'poblacionObjetivo',
                      'totalBeneficiarios',
                      'impacto',
                      'senalizacion',
                      'registroHacendario',
                      'montoRegistroHacendario',
                      'inversionTotal',
                      'tipoMoneda',
                      'susceptibleInauguracion',
                      'inaugurada',
                      'inaugurador',
                      'observaciones',
                      'fotoAntes',
                      'fotoDurante',
                      'fotoDespues',
                      # 'autorizada',
                      #'registroAuditoria',
                      )
        elif request.user.usuario.rol == 'UD':
            fields = ('identificador_unico',
                      'id_Dependencia',
                      'denominacion',
                      'dependencia',
                      'subdependencia',
                      'instanciaEjecutora',
                      'estado',
                      'municipio',
                      'latitud',
                      'longitud',
                      'descripcion',
                      'porcentajeAvance',
                      'tipoObra',
                      'fechaInicio',
                      'fechaTermino',
                      'poblacionObjetivo',
                      'totalBeneficiarios',
                      'impacto',
                      'senalizacion',
                      'registroHacendario',
                      'montoRegistroHacendario',
                      'inversionTotal',
                      'tipoMoneda',
                      'susceptibleInauguracion',
                      'inaugurada',
                      'inaugurador',
                      'observaciones',
                      'fotoAntes',
                      'fotoDurante',
                      'fotoDespues',
                      # 'autorizada',
                      )
        else:
            fields = ('identificador_unico',
                      'id_Dependencia',
                      'denominacion',
                      'dependencia',
                      'subdependencia',
                      'instanciaEjecutora',
                      'estado',
                      'municipio',
                      'latitud',
                      'longitud',
                      'descripcion',
                      'porcentajeAvance',
                      'tipoObra',
                      'fechaInicio',
                      'fechaTermino',
                      'poblacionObjetivo',
                      'totalBeneficiarios',
                      'impacto',
                      'senalizacion',
                      'registroHacendario',
                      'montoRegistroHacendario',
                      'inversionTotal',
                      'tipoMoneda',
                      'susceptibleInauguracion',
                      'inaugurada',
                      'inaugurador',
                      'observaciones',
                      'fotoAntes',
                      'fotoDurante',
                      'fotoDespues',
                      'autorizada',
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
            elif request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':
                arreglo_dependencias = []

                for dependencia in request.user.usuario.dependencia.all():
                    print(dependencia.id)
                    arreglo_dependencias.append(dependencia.id)

                kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id__in=arreglo_dependencias) |
                    Q(dependienteDe__id__in=arreglo_dependencias)
                )
            elif request.user.usuario.rol == 'US':
                arreglo_dependencias = []

                for dependencia in request.user.usuario.dependencia.all():
                    print(dependencia.id)
                    arreglo_dependencias.append(dependencia.id)

                kwargs["queryset"] = Dependencia.objects.filter(
                    Q(id__in=arreglo_dependencias)
                )

        return super(
            ObrasAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(ObrasAdmin, self).get_queryset(request)
        arreglo_dependencias = []

        for dependencia in request.user.usuario.dependencia.all():
            print(dependencia.id)
            arreglo_dependencias.append(dependencia.id)

        if request.user.usuario.rol == 'SA':
            print 'Query Set Superadmin'
            return qs

        elif request.user.usuario.rol == 'AD' or request.user.usuario.rol == 'FU' or request.user.usuario.rol == 'UD':
            print 'Query Set Administrador dependencia'
            a = request.user.usuario.dependencia.all()


            return qs.filter(
                Q(dependencia__id__in=arreglo_dependencias) |
                Q(dependencia__dependienteDe__id__in=arreglo_dependencias)
            )
        elif request.user.usuario.rol == 'US':
            print 'Query Set Usuario'
            for subdependencia in request.user.usuario.subdependencia.all():
                print(subdependencia.id)
                arreglo_dependencias.append(subdependencia.id)

            return qs.filter(
                Q(subdependencia__id__in=arreglo_dependencias)
            )




class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'


    list_filter = [
        'user__usuario__dependencia',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
        'change_message',
	'get_dependencia',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def get_dependencia(self, obj):
        return ",\n".join([dependencia.nombreDependencia for dependencia in obj.user.usuario.dependencia.all()])

    get_dependencia.short_description = 'Dependencia'


admin.site.register(LogEntry, LogEntryAdmin)



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
admin.site.register(Municipio)
