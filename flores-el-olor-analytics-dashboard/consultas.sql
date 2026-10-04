/* ============================================================
1. PRODUCCIÓN VS PÉRDIDAS POR FINCA
============================================================ */

SELECT
    f.nombre AS finca,

    SUM(e.tallos_exportacion) AS tallos_exportados,

    SUM(lp.esquejes_sembrados) -
    SUM(e.tallos_exportacion)
        AS perdidas,

    ROUND(
        (
            (
                SUM(lp.esquejes_sembrados) -
                SUM(e.tallos_exportacion)
            ) * 100.0
        )
        /
        SUM(lp.esquejes_sembrados),
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
2. COSTO POR TALLO EXPORTADO
============================================================ */

SELECT
    f.nombre AS finca,

    SUM(c.costo_total_cop)
        AS costo_total,

    SUM(e.tallos_exportacion)
        AS tallos_exportados,

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
3. DEPENDENCIA COMERCIAL
============================================================ */

SELECT

    p.pais,

    SUM(ex.valor_facturado_usd)
        AS valor_facturado,

    ROUND(
        (
            SUM(ex.valor_facturado_usd)
            * 100.0
        )
        /
        SUM(
            SUM(ex.valor_facturado_usd)
        ) OVER (),
        2
    )
    AS porcentaje

FROM exportaciones ex

JOIN pedidos p
    ON ex.id_pedido = p.id_pedido

GROUP BY p.pais

ORDER BY valor_facturado DESC;

/* ============================================================
4. VARIEDADES PROBLEMÁTICAS
============================================================ */

SELECT

    v.nombre AS v*riedad,

    SUM(
        lp.esque*es_sembrados
    ) -
    SUM(
    *   e.tallos_exportacion
    )
    *S perdidas,

    SUM(
        ex.v*lor_facturado_usd
    )
    AS ing*eso_generado

FROM variedades v

J*IN lotes_produccion lp
    ON v.id*variedad = lp.id_variedad

JOIN em*aque e
    ON lp.id_lote = e.id_lo*e

LEFT JOIN pedidos p
    ON p.id_variedad = v.id_variedad

LEFT JOIN exportaciones ex
    ON ex.id_pedido = p.id_pedido

GROUP BY v.nombre

ORDER BY perdidas DESC;

/* ============================================================
5. TOP MERCADOS
============================================================ */

SELECT

    p.pais,

    SUM(ex*valor_facturado_usd)
        AS va*or_facturado,

    SUM(ex.tallos)
*       AS tallos,

    ROUND(
    *   SUM(ex.valor_facturado_usd)
        /
        NULLIF(
            SUM(ex.tallos),
            0
        ),
        2
    )
    AS ingreso_por_tallo

FROM exportaciones ex

JOIN pedidos p
    ON ex.id_pedido = p.id_pedido

GROUP BY p.pais

ORDER BY valor_facturado DESC;

/* ============================================================
6. DEMANDA HISTÓRICA
============================================================ */

SELECT

    month(fecha_pedid*)
        AS mes,

    SUM(cantidad_tallos)
        AS demanda_total

FROM pedidos

GROUP BY month(fecha_pedido)

ORDER BY mes;


/* ============================================================
7. CALIDAD DEL CORTE POR FINCA
============================================================ */

SELECT

    f.nombre AS finca,
*    SUM(c.calidad_a)
        AS ca*idad_a,

    SUM(c.calidad_b)
    *   AS calidad_b,

    SUM(c.rechaz*das)
        AS rechazadas,

    R*UND(
        SUM(c.rechazadas)
   *    * 100.0
        /
        SUM(*.cantidad_reportada),
        2
  * )
    AS porcentaje_rechazo

FROM*cortes c

JOIN fincas f
    ON c.i*_finca = f.id_finca

GROUP BY f.no*bre

ORDER BY porcentaje_rechazo D*SC;