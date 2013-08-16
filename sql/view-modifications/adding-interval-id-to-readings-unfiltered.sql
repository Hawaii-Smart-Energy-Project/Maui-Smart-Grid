-- Adding interval id to readings unfiltered view.
-- Ordering may not be correct during modification.
--
-- @author Daniel Zhang (張道博)

DROP VIEW "public"."dz_pv_readings_without_pv_service_point_ids";
DROP VIEW "public"."cd_energy_voltages_for_houses_with_pv";
DROP VIEW "public"."count_of_readings_and_meters_by_day";
DROP VIEW "public"."dz_pv_readings";
DROP VIEW "public"."readings_not_referenced_by_mlh";
DROP VIEW "public"."readings_unfiltered";


CREATE
VIEW "public"."readings_unfiltered" AS
    SELECT
        "Interval".end_time,
        "MeterData".meter_name,
        "Reading".channel,
        "Reading".raw_value,
        "Reading"."value",
        "Reading".uom,
        "IntervalReadData".start_time,
        "IntervalReadData".end_time AS ird_end_time,
        "MeterData".meter_data_id,
        "Reading".interval_id
    FROM "MeterData"
         INNER JOIN "IntervalReadData" ON "MeterData".meter_data_id = "IntervalReadData".meter_data_id
         INNER JOIN "Interval" ON "IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id
         INNER JOIN "Reading" ON "Interval".interval_id = "Reading".interval_id; COMMENT ON VIEW "public" . "readings_unfiltered" IS 'All readings along with their end times by meter. @author Daniel Zhang (張道博)' ;


CREATE
VIEW "public"."dz_pv_readings_without_pv_service_point_ids" AS
    SELECT
        nonpv_mlh.meter_name,
        nonpv_mlh.service_point_id,
        dz_pv_readings.end_time,
        dz_pv_readings.channel,
        dz_pv_readings.VALUE

    FROM (dz_pv_readings
          JOIN nonpv_mlh ON ((dz_pv_readings.meter_name = (nonpv_mlh.meter_name) : : bpchar))); COMMENT ON VIEW "public" . "dz_pv_readings_without_pv_service_point_ids" IS 'Working on reporting PV readings without PV Service Point IDs. @author Daniel Zhang (張道博)' ;


CREATE
VIEW "public"."cd_energy_voltages_for_houses_with_pv" AS
    SELECT
        cd_meter_ids_for_houses_with_pv_with_locations.device_util_id,
        view_readings_with_meter_id_unsorted.end_time,
        MAX (CASE WHEN (view_readings_with_meter_id_unsorted.channel = (1) : : SMALLINT) THEN
                  view_readings_with_meter_id_unsorted.VALUE

             ELSE
             NULL : : REAL
             END) AS "Energy to House kwH",
        zero_to_null (MAX (CASE WHEN (view_readings_with_meter_id_unsorted.channel = (4) : : SMALLINT) THEN
                                view_readings_with_meter_id_unsorted.VALUE

                           ELSE
                           NULL : : REAL
                           END)) AS "Voltage",
        MAX (cd_meter_ids_for_houses_with_pv_with_locations.service_pt_longitude) AS service_pt_longitude,
        MAX (cd_meter_ids_for_houses_with_pv_with_locations.service_pt_latitude) AS service_pt_latitude,
        MAX ((cd_meter_ids_for_houses_with_pv_with_locations.address1) : : TEXT ) AS address1
    FROM (cd_meter_ids_for_houses_with_pv_with_locations
          JOIN readings_unfiltered view_readings_with_meter_id_unsorted ON (((cd_meter_ids_for_houses_with_pv_with_locations.device_util_id) : : bpchar = view_readings_with_meter_id_unsorted.meter_name)))
    WHERE (
          (view_readings_with_meter_id_unsorted.channel = (1) : : SMALLINT) OR
          (view_readings_with_meter_id_unsorted.channel = (4) : : SMALLINT))
    GROUP BY
        cd_meter_ids_for_houses_with_pv_with_locations.device_util_id,
        view_readings_with_meter_id_unsorted.end_time; COMMENT ON VIEW "public" . "cd_energy_voltages_for_houses_with_pv" IS NULL ;


CREATE
VIEW "public"."count_of_readings_and_meters_by_day" AS
    SELECT
        date_trunc ('day' : : TEXT , view_readings_with_meter_id_unsorted . end_time ) AS "Day" , COUNT ( view_readings_with_meter_id_unsorted . VALUE ) AS "Reading Count" , COUNT ( DISTINCT view_readings_with_meter_id_unsorted . meter_name ) AS "Meter Count" , ( COUNT ( view_readings_with_meter_id_unsorted . VALUE )
/ COUNT ( DISTINCT view_readings_with_meter_id_unsorted . meter_name ) ) AS "Readings per Meter" FROM readings_unfiltered view_readings_with_meter_id_unsorted WHERE ( view_readings_with_meter_id_unsorted . channel = 1 ) GROUP BY date_trunc ( 'day' : : TEXT , view_readings_with_meter_id_unsorted . end_time ) ORDER BY date_trunc ( 'day' : : TEXT , view_readings_with_meter_id_unsorted . end_time ) ; COMMENT ON VIEW "public" . "count_of_readings_and_meters_by_day" IS 'Get counts of readings and meters per day. @author Daniel Zhang (張道博)' ;


CREATE
VIEW "public"."dz_pv_readings" AS
    SELECT
        readings_unfiltered.end_time,
        readings_unfiltered.meter_name,
        readings_unfiltered.channel,
        readings_unfiltered.VALUE,
        readings_unfiltered.meter_data_id
    FROM readings_unfiltered
    WHERE (
          (readings_unfiltered.channel = 2 : : SMALLINT) AND
          (readings_unfiltered.VALUE > 0 : : REAL)); COMMENT ON VIEW "public" . "dz_pv_readings" IS NULL ;


CREATE
VIEW "public"."readings_not_referenced_by_mlh" AS
    SELECT
        readings_by_meter_location_history_2.meter_name AS mlh_meter_name,
        readings_with_meter_data_id_unfiltered.meter_name AS full_meter_name,
        readings_by_meter_location_history_2.channel AS mlh_channel,
        readings_by_meter_location_history_2.VALUE AS mlh_value,
        readings_with_meter_data_id_unfiltered.channel AS full_channel,
        readings_with_meter_data_id_unfiltered.VALUE AS full_value,
        readings_by_meter_location_history_2.end_time AS mlh_end_time,
        readings_with_meter_data_id_unfiltered.end_time AS full_end_time,
        readings_with_meter_data_id_unfiltered.meter_data_id AS full_meter_data_id
    FROM (readings_unfiltered readings_with_meter_data_id_unfiltered
          LEFT JOIN readings_by_meter_location_history readings_by_meter_location_history_2 ON ((readings_with_meter_data_id_unfiltered.meter_data_id = readings_by_meter_location_history_2.meter_data_id)))
    WHERE (readings_by_meter_location_history_2.meter_data_id IS NULL); COMMENT ON VIEW "public" . "readings_not_referenced_by_mlh" IS 'Readings that are present in the DB but are not referenced by the Meter Location History. @author Daniel Zhang (張道博)' ;
