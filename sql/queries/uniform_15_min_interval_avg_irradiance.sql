-- Provide aggregated irradiance data over uniform daily intervals with nulls
-- set to zero.
--
-- @author Daniel Zhang (張道博)

SELECT
    "public"."_IrradianceFifteenMinIntervals".end_time,
    "public"."_IrradianceFifteenMinIntervals".sensor_id,
    (
        CASE
        WHEN "public"."AverageFifteenMinIrradianceData".irradiance_w_per_m2 IS
             NULL THEN
            0.0
        ELSE
            irradiance_w_per_m2
        END
    )
FROM "public"."_IrradianceFifteenMinIntervals"
    LEFT OUTER JOIN "public"."AverageFifteenMinIrradianceData" ON

                                                                   "public"."_IrradianceFifteenMinIntervals".end_time
                                                                   =
                                                                   "public"."AverageFifteenMinIrradianceData"."timestamp"

                                                                   AND

                                                                   "public"."_IrradianceFifteenMinIntervals".sensor_id
                                                                   =
                                                                   "public"."AverageFifteenMinIrradianceData".sensor_id

WHERE end_time BETWEEN (
    SELECT
        date_trunc(
            'day',
            MIN(
                "public"."AverageFifteenMinIrradianceData"."timestamp"
            )
        )
    FROM
        "AverageFifteenMinIrradianceData"
)
AND (
    SELECT
        date_trunc(
            'day',
            MAX(
                "public"."AverageFifteenMinIrradianceData"."timestamp"
            )
        )
    FROM
        "AverageFifteenMinIrradianceData"
)
ORDER BY "public"."_IrradianceFifteenMinIntervals".end_time ASC,
    "public"."_IrradianceFifteenMinIntervals".sensor_id ASC
