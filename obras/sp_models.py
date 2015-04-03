SEARCH_RESULT_FIELDS = (
    'id',
    'denominacion',
    'tipoObra_id',
    'nombreTipoObra',
    'dependencia_id',
    'nombreDependencia',
    'imagenDependencia',
    'estado_id',
    'nombreEstado',
    'latitud',
    'longitud',
    'impacto_id',
    'nombreImpacto',
    'listaIDInversiones',
    'listaInversiones',
    'listaIDclasificaciones',
    'listaClasificaciones',
    'inaugurador_id',
    'nombreCargoInaugura',
    'descripcion',
    'observaciones',
    'fechaInicio',
    'fechaTermino',
    'inversionTotal',
    'totalBeneficiarios',
    'senalizacion',
    'susceptibleInauguracion',
    'porcentajeAvance',
    'fotoAntes',
    'fotoDurante',
    'fotoDespues',
    'fechaModificacion',
    'nombreTipoDeMoneda',
    'inaugurada',
    'poblacionObjetivo',
    'municipio',
    'subclasificacionDe_id',
    'nombreTipoClasificacion'
)

DEPENDENCY_REPORT_FIELDS = (
    'dependencia_id',
    'nombreDependencia',
    'numeroObras',
    'totalInvertido'
)


def get_search_result_map(values):
    if len(values) == len(SEARCH_RESULT_FIELDS):
        return zip(SEARCH_RESULT_FIELDS, values)
    else:
        return None

def get_dependency_report(values):
    return None