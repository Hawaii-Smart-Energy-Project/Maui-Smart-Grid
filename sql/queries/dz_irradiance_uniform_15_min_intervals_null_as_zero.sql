-- Provides averaged irradiance data over uniform intervals with nulls set to zero.
--
-- @author Daniel Zhang (張道博)

SELECT
    "_IrradianceFifteenMinIntervals".end_time,
    "_IrradianceFifteenMinIntervals".sensor_id,
    CASE
    WHEN (
        "AverageFifteenMinIrradianceData".irradiance_w_per_m2 IS NULL
    ) THEN
        (0.0) :: DOUBLE PRECISION
    ELSE
        "AverageFifteenMinIrradianceData".irradiance_w_per_m2
    END AS irradiance_w_per_m2
FROM
    (
            "_IrradianceFifteenMinIntervals"
            LEFT JOIN "AverageFifteenMinIrradianceData" ON (
            (
                (
                    "_IrradianceFifteenMinIntervals".end_time =
                    "AverageFifteenMinIrradianceData"."timestamp"
                )
                AND (
                    "_IrradianceFifteenMinIntervals".sensor_id =
                    "AverageFifteenMinIrradianceData".sensor_id
                )
            )
        )
            INNER JOIN "dz_count_of_15_min_irradiance_intervals" ON (date_trunc(
                                                                         'day',
                                                                         "_IrradianceFifteenMinIntervals".end_time)
                                                                     = day) AND
                                                                    cnt = 96
    )
WHERE
    (
        (
            "_IrradianceFifteenMinIntervals".end_time >= (
                SELECT
                    date_trunc(
                        'day' :: TEXT,
                        MIN(
                            "AverageFifteenMinIrradianceData"."timestamp"
                        )
                    ) AS date_trunc
                FROM
                    "AverageFifteenMinIrradianceData"
            )
        )
        AND (
            "_IrradianceFifteenMinIntervals".end_time <= (
                SELECT
                    date_trunc(
                        'day' :: TEXT,
                        MAX(
                            "AverageFifteenMinIrradianceData"."timestamp"
                        )
                    ) AS date_trunc
                FROM
                    "AverageFifteenMinIrradianceData"
            )
        )
    )
ORDER BY
    "_IrradianceFifteenMinIntervals".end_time,
    "_IrradianceFifteenMinIntervals".sensor_id
