-- Creates a table containing a series of intervals for analyzing irradiance
-- data usin 15 min intervals. The intervals are created from the first
-- data point up to 1 year + 1 day past the last data point.
--
-- @author Daniel Zhang (張道博)

CREATE TABLE "_IrradianceFifteenMinIntervals" AS

    SELECT
        (
            (
                SELECT
        (
            MIN("IrradianceData"."timestamp")
        ) :: DATE AS MIN
                FROM
                    "IrradianceData"
            ) + ((n.n || ' minutes' :: TEXT)) :: INTERVAL
        ) AS start_time,
        (
            (
                SELECT
        (
            MIN("IrradianceData"."timestamp")
        ) :: DATE AS MIN
                FROM
                    "IrradianceData"
            ) + (((n.n + 15) || ' minutes' :: TEXT)) :: INTERVAL
        ) AS end_time
    FROM
        generate_series(
            0,
            (
                (
                    SELECT
                        MAX("IrradianceData"."timestamp") :: DATE -
                        MIN("IrradianceData"."timestamp") :: DATE
                    FROM
                        "IrradianceData"
                ) + 366
            ) * 24 * 60,
            15
        ) n (n)
