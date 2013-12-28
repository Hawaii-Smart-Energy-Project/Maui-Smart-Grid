-- Creates a table containing a series of intervals for analyzing irradiance
-- data using 15 min intervals. The intervals are created from the first
-- data point up to 1 year + 1 day past the last data point.
--
-- Sensor IDs are included.
--
-- @author Daniel Zhang (張道博)
DROP VIEW "public"."dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero";

DROP VIEW "public"."dz_count_of_fifteen_min_irradiance_intervals";

DROP VIEW "public"."z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero";

DROP TABLE "_IrradianceFifteenMinIntervals" CASCADE;

CREATE TABLE "_IrradianceFifteenMinIntervals" AS (
	WITH intervals AS (
		SELECT
			(
				(
					SELECT
						(
							MIN ("IrradianceData"."timestamp")
						) :: DATE AS MIN
					FROM
						"IrradianceData"
				) + ((n.n || ' minutes' :: TEXT)) :: INTERVAL
			) AS start_time,
			(
				(
					SELECT
						(
							MIN ("IrradianceData"."timestamp")
						) :: DATE AS MIN
					FROM
						"IrradianceData"
				) + (((n.n + 15) || ' minutes' :: TEXT)) :: INTERVAL
			) AS end_time
		FROM
			generate_series (
				0,
				(
					(
						SELECT
							MAX ("IrradianceData"."timestamp") :: DATE - MIN ("IrradianceData"."timestamp") :: DATE
						FROM
							"IrradianceData"
					) + 366
				) * 24 * 60,
				15
			) n (n)
	) SELECT
		generate_series (1, 4) AS sensor_id,
		*
	FROM
		intervals
);

CREATE VIEW "public"."z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero" AS SELECT
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
		(
			"_IrradianceFifteenMinIntervals"
			LEFT JOIN "AverageFifteenMinIrradianceData" ON (
				(
					(
						"_IrradianceFifteenMinIntervals".end_time = "AverageFifteenMinIrradianceData"."timestamp"
					)
					AND (
						"_IrradianceFifteenMinIntervals".sensor_id = "AverageFifteenMinIrradianceData".sensor_id
					)
				)
			)
		)
	)
WHERE
	(
		(
			"_IrradianceFifteenMinIntervals".end_time >= (
				SELECT
					date_trunc(
						'day' :: TEXT,
						MIN (
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
						MAX (
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
	"_IrradianceFifteenMinIntervals".sensor_id;

COMMENT ON VIEW "public"."z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero" IS 'Used internally. @author Daniel Zhang (張道博)';

CREATE VIEW "dz_count_of_fifteen_min_irradiance_intervals" AS SELECT
	COUNT (*) / 4 AS cnt,
	date_trunc('day', end_time) AS DAY
FROM
	"z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero"
GROUP BY
	DAY;

CREATE VIEW "public"."dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero" AS SELECT
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
		(
			"_IrradianceFifteenMinIntervals"
			LEFT JOIN "AverageFifteenMinIrradianceData" ON (
				(
					(
						"_IrradianceFifteenMinIntervals".end_time = "AverageFifteenMinIrradianceData"."timestamp"
					)
					AND (
						"_IrradianceFifteenMinIntervals".sensor_id = "AverageFifteenMinIrradianceData".sensor_id
					)
				)
			)
		)
		JOIN dz_count_of_fifteen_min_irradiance_intervals ON (
			(
				(
					date_trunc(
						'day' :: TEXT,
						"_IrradianceFifteenMinIntervals".end_time
					) = dz_count_of_fifteen_min_irradiance_intervals. DAY
				)
				AND (
					dz_count_of_fifteen_min_irradiance_intervals.cnt = 96
				)
			)
		)
	)
WHERE
	(
		(
			"_IrradianceFifteenMinIntervals".end_time >= (
				SELECT
					date_trunc(
						'day' :: TEXT,
						MIN (
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
						MAX (
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
	"_IrradianceFifteenMinIntervals".sensor_id;

COMMENT ON VIEW "public"."dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero" IS 'Transformed irradiance data for use in analysis. @author Daniel Zhang (張道博)';

GRANT DELETE,
 SELECT
	,
	REFERENCES,
	TRIGGER,
	INSERT,
	UPDATE,
	TRUNCATE ON dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO "sepgroup";

GRANT SELECT
	ON dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO "sepgroupreadonly";

