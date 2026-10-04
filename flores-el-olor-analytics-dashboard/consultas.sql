/* ============================================================
Consultas ejecutadas en Amazon Athena para generar
los archivos CSV consumidos por el dashboard.
============================================================ */


/* ============================================================
Comparar producción exportable y pérdidas por finca.
============================================================ */

SELECT
    f.nombre AS finca,

    SUM(e.tallos_exportacion) AS tallos_exportados,

    (
        SUM(lp.esquejes_sembrados)
        -
        SUM(e.tallos_exportacion)
    ) AS perdidas,

    ROUND(
        (
            (
                SUM(lp.esquejes_sembrados)
                -
                SUM(e.tallos_exportacion)
            )
            * 100.0
        )
        /
        NULLIF(
            SUM(lp.esquejes_sembrados),
            0
        ),
        2
    ) AS porcentaje_perdida

FROM lotes_produccion lp

JOIN fincas f
    ON lp.id_finca = f.id_finca

JOIN empaque e
    ON lp.id_lote = e.id_lote

GROUP BY f.nombre

ORDER BY porcentaje_perdida DESC;


/* ============================================================
Calcular costo promedio por tallo exportado.
============================================================ */

SELECT
    f.nombre AS finca,

    SUM(c.costo_total_cop) AS costo_total,

    SUM(e.tallos_exportacion) AS tallos_exportados,

    ROUND(
        SUM(c.costo_total_cop)
        /
        NULLIF(
            SUM(e.tallos_exportacion),
            0
        ),
        2
    ) AS costo_por_tallo

FROM costos c

JOIN fincas f
    ON c.id_finca = f.id_finca

JOIN empaque e
    ON c.id_lote = e.id_lote

GROUP BY f.nombre

ORDER BY costo_por_tallo DESC;


/* ============================================================
Analizar participación por país comprador.
============================================================ */

SELECT

    p.pais,

    SUM(ex.valor_facturado_usd)
        AS valor_facturado,

    ROUND(
        (
            SUM(ex.valor_facturado_usd) * 100.0
        )
        /
        SUM(
            SUM(ex.valor_facturado_usd)
        ) OVER (),
        2
    ) AS porcentaje

FROM exportaciones ex

JOIN pedidos p
    ON ex.id_pedido = p.id_pedido

GROUP BY p.pais

ORDER BY valor_facturado DESC;


/* ============================================================
Detectar variedades con alto nivel de pérdidas y
bajo aporte económico.
============================================================ */

SELECT

    v.nombre AS variedad,

    (
        SUM(lp.esquejes_sembrados)
        -
        SUM(e.tallos_exportacion)
    ) AS perdidas,

    COALESCE(
        SUM(ex.valor_facturado_usd),
        0
    ) AS ingreso_generado

FROM variedades v

JOIN lotes_produccion lp
    ON v.id_variedad = lp.id_variedad

JOIN empaque e
    ON lp.id_lote = e.id_lote

LEFT JOIN pedidos p
    ON p.id_variedad = v.id_variedad

LEFT JOIN exportaciones ex
    ON ex.id_pedido = p.id_pedido

GROUP BY v.nombre

ORDER BY perdidas DESC;


/* ============================================================
Comparar producción proyectada y demanda proyectada.
============================================================ */

SELECT

    month AS mes,

    SUM(produccion_proyectada_tallos)
        AS produccion_proyectada,

    SUM(demanda_proyectada_tallos)
        AS demanda_proyectada

FROM forecast_2027

GROUP BY month

ORDER BY month;


/* ============================================================
VALIDACIÓN DE DATOS
============================================================ */

SELECT COUNT(*) AS fincas
FROM fincas;

SELECT COUNT(*) AS lotes
FROM lotes_produccion;

SELECT COUNT(*) AS cortes
FROM cortes;

SELECT COUNT(*) AS empaques
FROM empaque;

SELECT COUNT(*) AS pedidos
FROM pedidos;

SELECT COUNT(*) AS exportaciones
FROM exportaciones;

SELECT COUNT(*) AS costos
FROM costos;

SELECT COUNT(*) AS forecast
FROM forecast_2027;
