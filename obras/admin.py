from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from obras.models import *


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


class ClasificacionInLine(admin.StackedInline):
    model = TipoClasificacion
    extra = 3

class DependenciaListFilter(SimpleListFilter):

    # USAGE
    # In your admin class, pass three filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)


    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Dependencias')

    parameter_name = 'dependencia'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = []
        dependencia = Dependencia.objects.get(id=1)
        #print category
        list_tuple.append((dependencia.id, dependencia.nombreDependencia))
        return list_tuple


    def queryset(self, request, queryset):
        return queryset.filter(id=1)




class ObrasAdmin(admin.ModelAdmin):

    inlinesInversion = [InversionInLine]
    inlinesClasificacion = [ClasificacionInLine]
    list_display = (
        'denominacion', 'autorizada', 'tipoObra', 'dependencia', 'senalizacion', 'inaugurada', 'inaugurador', 'fechaInicio',
        'fechaTermino')
    list_filter =[DependenciaListFilter,]

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


    def get_form(self, request, obj=None, **kwargs):
        print request.user.usuario.rol
        if request.user.usuario.rol == 'US':
            self.exclude = ('autorizada',)
        else:
            print 'No excluir'
        return super(ObrasAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(ObrasAdmin, self).get_queryset(request)
        if request.user.usuario.rol == 'SA':
            return qs
        elif request.user.usuario.rol == 'AD':
            return qs.filter(
                Q(dependencia=request.user.usuario.dependencia) |
                Q(dependencia__dependienteDe=request.user.usuario.dependencia)
            )
        elif request.user.usuario.rol == 'US':
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
