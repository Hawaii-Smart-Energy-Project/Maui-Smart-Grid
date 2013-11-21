-- Creates a table containing a series of intervals for analyzing irradiance
-- data usin 15 min intervals. The intervals are created from the first
-- data point up to 1 year + 1 day past the last data point.
--
-- Sensor IDs are included.
--
-- Create aggregated temperature view using NOAA weather data.
--
-- @author Daniel Zhang (張道博)

DROP VIEW "public"."dz_average_temp_noaa_weather_per_15_min_irradiance_interval";
DROP TABLE "_IrradianceFifteenMinIntervals";

CREATE TABLE "_IrradianceFifteenMinIntervals" AS (
        WITH intervals AS (
            SELECT
                (
                    (
                        SELECT
                (
                    MIN("IrradianceData"."timestamp" - INTERVAL '1' DAY)
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
        ) SELECT
            generate_series(1,
                            4) AS sensor_id,
            *
        FROM
            intervals);

CREATE VIEW "public"."dz_average_temp_noaa_weather_per_15_min_irradiance_interval" AS
    SELECT
        i.start_time,
        AVG(
            CASE
            WHEN (
                (w.dry_bulb_celsius) :: TEXT ~
                '(([1-9]+\.[0-9]*)|([1-9]*\.[0-9]+)|([1-9]+))([eE][-+]?[0-9]+)?'
                :: TEXT
            ) THEN
                (w.dry_bulb_celsius) :: DOUBLE PRECISION
            ELSE
                NULL :: DOUBLE PRECISION
            END
        ) AS AVG
    FROM
            "WeatherNOAA" w,
            "_IrradianceFifteenMinIntervals" i
    WHERE
        (
            date_trunc('hour' :: TEXT, i.start_time) =
            date_trunc('hour' :: TEXT, w.datetime)
        )
    GROUP BY
        i.start_time
    ORDER BY
        i.start_time;
COMMENT ON VIEW "public"."dz_average_temp_noaa_weather_per_15_min_irradiance_interval" IS NULL;
