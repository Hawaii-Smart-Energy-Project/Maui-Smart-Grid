-- This provides the average temperature according to NOAA weather data
-- for fifteen minute intervals of irradiance readings.
--
-- @author Daniel Zhang (張道博)

SELECT
    i.start_time,

    avg(
        CASE
        WHEN (
            (w.dry_bulb_celsius) :: TEXT ~
            '(([1-9]+\.[0-9]*)|([1-9]*\.[0-9]+)|([1-9]+))([eE][-+]?[0-9]+)?' ::
            TEXT
        ) THEN
            (w.dry_bulb_celsius) :: DOUBLE PRECISION
        ELSE
            NULL :: DOUBLE PRECISION
        END
    )
FROM
        "WeatherNOAA" w,
        "_IrradianceFifteenMinIntervals" i

WHERE
    date_trunc('hour', i.start_time) = date_trunc('hour', w.datetime)
GROUP BY

    i.start_time

ORDER BY
    i.start_time

