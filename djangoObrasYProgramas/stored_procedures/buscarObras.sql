-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `buscarObras`(
  inTipoObra            TEXT,
  inDependencia         TEXT,
  inEstado              TEXT,
  inRangoInversionMin   DOUBLE,
  inRangoInversionMax   DOUBLE,
  inFechaInicio         DATE,
  inFechaInicioSegunda  DATE,
  inFechaTermino        DATE,
  inFechaTerminoSegunda DATE,
  inImpacto             TEXT,
  inCargoInaugura       TEXT,
  inTipoInversion       TEXT,
  inTipoClasificacion   TEXT,
  inSusceptible         TEXT,
  inInaugurada          TEXT,
  inLimiteMin           INTEGER,
  inLimiteMax           INTEGER,
  inDenominacion        TEXT,
  inSubclasificacion    TEXT,
  inValorDolar          DOUBLE
)
  BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS resultados
      AS
        SELECT
          Obra.id,
          Obra.denominacion,
          Obra.tipoObra_id,
          TipoObra.nombreTipoObra,


          Obra.dependencia_id,
          Dependencia.nombreDependencia,
          Dependencia.imagenDependencia,

          Obra.estado_id,
          Estado.nombreEstado,
          Estado.latitud,
          Estado.longitud,


          Obra.impacto_id,
          Impacto.nombreImpacto,

          GROUP_CONCAT(DISTINCT TipoInversion.id)                          AS listaIDInversiones,
          GROUP_CONCAT(DISTINCT TipoInversion.nombreTipoInversion)         AS listaInversiones,

          GROUP_CONCAT(DISTINCT TipoClasificacion.id)                      AS listaIDclasificaciones,
          GROUP_CONCAT(DISTINCT TipoClasificacion.nombreTipoClasificacion) AS listaClasificaciones,

          Obra.inaugurador_id,
          Inaugurador.nombreCargoInaugura,

          Obra.descripcion,
          Obra.observaciones,
          Obra.fechaInicio,
          Obra.fechaTermino,
          Obra.inversionTotal,
          Obra.totalBeneficiarios,
          Obra.senalizacion,
          Obra.susceptibleInauguracion,
          Obra.porcentajeAvance,
          Obra.fotoAntes,
          Obra.fotoDurante,
          Obra.fotoDespues,
          Obra.fechaModificacion,
          Moneda.nombreTipoDeMoneda,
          Obra.inaugurada,
          Obra.poblacionObjetivo,
          Obra.municipio,
          TipoClasificacion.subclasificacionDe_id, # D:
          TipoClasificacion.nombreTipoClasificacion


        FROM
          obras_obra Obra
          LEFT JOIN
          obras_obra_tipoInversion RelTipoInversion ON Obra.id = RelTipoInversion.obra_id

          LEFT JOIN
          obras_tipoinversion TipoInversion ON RelTipoInversion.tipoinversion_id = TipoInversion.id

          LEFT JOIN
          obras_tipoobra TipoObra ON Obra.tipoObra_id = TipoObra.id

          LEFT JOIN
          obras_dependencia Dependencia ON Obra.dependencia_id = Dependencia.id

          LEFT JOIN
          obras_estado Estado ON Obra.estado_id = Estado.id

          LEFT JOIN
          obras_impacto Impacto ON Obra.impacto_id = Impacto.id

          LEFT JOIN
          obras_inaugurador Inaugurador ON Obra.inaugurador_id = Inaugurador.id

          LEFT JOIN
          obras_obra_tipoClasificacion RelTipoClasificacion ON Obra.id = RelTipoClasificacion.obra_id

          LEFT JOIN
          obras_tipoclasificacion TipoClasificacion ON RelTipoClasificacion.tipoclasificacion_id = TipoClasificacion.id

          LEFT JOIN
          obras_tipoclasificacion ON obras_tipoclasificacion.id = obras_tipoclasificacion.subclasificacionDe_id

          LEFT JOIN
          obras_tipomoneda Moneda ON Moneda.id = Obra.tipoMoneda_id
        WHERE
          (inTipoObra IS NULL OR FIND_IN_SET(Obra.tipoObra_id, inTipoObra) > 0) AND
          (inDependencia IS NULL OR FIND_IN_SET(Obra.dependencia_id, inDependencia) > 0) AND

          (inEstado IS NULL OR FIND_IN_SET(Obra.estado_id, inEstado) > 0) AND

          (inTipoClasificacion IS NULL OR
           FIND_IN_SET(RelTipoClasificacion.tipoclasificacion_id, inTipoClasificacion) > 0) AND

          (inTipoInversion IS NULL OR FIND_IN_SET(RelTipoInversion.tipoinversion_id, inTipoInversion) > 0) AND


          (inCargoInaugura IS NULL OR FIND_IN_SET(Obra.inaugurador_id, inCargoInaugura) > 0) AND

          (inInaugurada IS NULL OR FIND_IN_SET(Obra.inaugurada, inInaugurada) > 0) AND


          (inImpacto IS NULL OR FIND_IN_SET(Obra.impacto_id, inImpacto) > 0) AND
          (inSusceptible IS NULL OR FIND_IN_SET(Obra.susceptibleInauguracion, inSusceptible) > 0) AND

          (Obra.denominacion LIKE CASE WHEN inDenominacion IS NULL THEN Obra.denominacion
                               ELSE CONCAT('%', inDenominacion, '%') END) AND

          (inSubclasificacion IS NULL OR
           FIND_IN_SET(TipoClasificacion.id, inSubclasificacion) > 0) AND


          (inRangoInversionMin IS NULL OR inRangoInversionMax IS NULL OR
           (inRangoInversionMin IS NOT NULL AND inRangoInversionMax IS NOT NULL AND
            Obra.inversionTotal BETWEEN inRangoInversionMin AND inRangoInversionMax)) AND


          (inFechaInicio IS NULL OR inFechaInicioSegunda IS NULL OR
           (inFechaInicio IS NOT NULL AND inFechaInicioSegunda IS NOT NULL AND
            Obra.fechaInicio BETWEEN inFechaInicio AND inFechaInicioSegunda)) AND


          (inFechaTermino IS NULL OR inFechaTerminoSegunda IS NULL OR
           (inFechaTermino IS NOT NULL AND inFechaTerminoSegunda IS NOT NULL AND
            Obra.fechaTermino BETWEEN inFechaTermino AND inFechaTerminoSegunda))

        GROUP BY Obra.id;

    SELECT
      *
    FROM resultados
    LIMIT inLimiteMin, inLimiteMax;


    SELECT
      obras_obra.dependencia_id,
      obras_dependencia.nombreDependencia,
      count(*)            AS numeroObras,
      SUM(obras_obra.inversionTotal * CASE obras_tipomoneda.nombreTipoDeMoneda WHEN 'MDP' THEN 1 WHEN 'MDD' THEN inValorDolar END) AS totalInvertido
    FROM resultados
    GROUP BY obras_dependencia.nombreDependencia;

    SELECT
      obras_estado.id,
      obras_estado.nombreEstado,
      obras_estado.latitud,
      obras_estado.longitud,
      count(*)            AS numeroObras,
      SUM(obras_obra.inversionTotal * CASE obras_tipomoneda.nombreTipoDeMoneda WHEN 'MDP' THEN 1 WHEN 'MDD' THEN inValorDolar END) AS totalInvertido
    FROM resultados
    GROUP BY obras_estado.nombreEstado;

    SELECT
      count(*)            AS numeroObras,
      SUM(obras_obra.inversionTotal * CASE obras_tipomoneda.nombreTipoDeMoneda WHEN 'MDP' THEN 1 WHEN 'MDD' THEN inValorDolar END) AS totalInvertido
    FROM resultados;


    DROP TABLE resultados;
  END