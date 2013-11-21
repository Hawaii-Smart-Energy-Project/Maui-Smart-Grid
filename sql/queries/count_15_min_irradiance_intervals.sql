-- Count 15-min irradiance intervals.
--
-- @author Daniel Zhang (張道博)

SELECT
	COUNT (*) / 4 AS cnt,
	date_trunc('day', end_time) AS DAY
FROM
	"dz_avg_irradiance_15_min_uniform_intervals_null_as_zero"
WHERE
	cnt = 96
GROUP BY
	DAY
