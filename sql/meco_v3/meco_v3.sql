--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: meco_v3; Type: COMMENT; Schema: -; Owner: sepgroup
--

COMMENT ON DATABASE meco_v3 IS 'This is version 3 of the MECO database that is being developed for adding the event data to the database.';


--
-- Name: az; Type: SCHEMA; Schema: -; Owner: ashkan
--

CREATE SCHEMA az;


ALTER SCHEMA az OWNER TO ashkan;

--
-- Name: cd; Type: SCHEMA; Schema: -; Owner: christian
--

CREATE SCHEMA cd;


ALTER SCHEMA cd OWNER TO christian;

--
-- Name: dw; Type: SCHEMA; Schema: -; Owner: dave
--

CREATE SCHEMA dw;


ALTER SCHEMA dw OWNER TO dave;

--
-- Name: dz; Type: SCHEMA; Schema: -; Owner: daniel
--

CREATE SCHEMA dz;


ALTER SCHEMA dz OWNER TO daniel;

--
-- Name: SCHEMA dz; Type: COMMENT; Schema: -; Owner: daniel
--

COMMENT ON SCHEMA dz IS 'Schema for Daniel Zhang.';


--
-- Name: ep; Type: SCHEMA; Schema: -; Owner: eileen
--

CREATE SCHEMA ep;


ALTER SCHEMA ep OWNER TO eileen;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: plpythonu; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpythonu WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpythonu; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpythonu IS 'PL/PythonU untrusted procedural language';


SET search_path = dz, pg_catalog;

--
-- Name: meco_readings_dupe_count(); Type: FUNCTION; Schema: dz; Owner: postgres
--

CREATE FUNCTION meco_readings_dupe_count() RETURNS integer
    LANGUAGE plpythonu
    AS $$
	from sys import path
	path.append('/home/daniel/fork-of-github-maui-smart-grid/src')
	from msg_data_verifier import MSGDataVerifier
	return MSGDataVerifier().mecoReadingDupes()
$$;


ALTER FUNCTION dz.meco_readings_dupe_count() OWNER TO postgres;

SET search_path = public, pg_catalog;

--
-- Name: zero_to_null(real); Type: FUNCTION; Schema: public; Owner: daniel
--

CREATE FUNCTION zero_to_null(real) RETURNS real
    LANGUAGE sql
    AS $_$select case when $1 < 1e-3 then null else $1 end;$_$;


ALTER FUNCTION public.zero_to_null(real) OWNER TO daniel;

--
-- Name: FUNCTION zero_to_null(real); Type: COMMENT; Schema: public; Owner: daniel
--

COMMENT ON FUNCTION zero_to_null(real) IS 'Change float4 value to null if it is less than 1e-3. @author Daniel Zhang (張道博)';


--
-- Name: zero_to_null(double precision); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION zero_to_null(double precision) RETURNS double precision
    LANGUAGE sql
    AS $_$select case when $1 < 1e-3 then null else $1 end;$_$;


ALTER FUNCTION public.zero_to_null(double precision) OWNER TO postgres;

SET search_path = dw, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: MeterLocationHistory_deprecated; Type: TABLE; Schema: dw; Owner: dave; Tablespace: 
--

CREATE TABLE "MeterLocationHistory_deprecated" (
    meter_name character varying,
    mac_address character varying,
    installed timestamp(6) without time zone,
    uninstalled timestamp(6) without time zone,
    location character varying,
    address character varying,
    city character varying,
    latitude double precision,
    longitude double precision,
    old_service_point_id character varying,
    service_point_height double precision,
    service_point_latitude double precision,
    service_point_longitude double precision,
    notes character varying,
    service_point_id character varying
);


ALTER TABLE dw."MeterLocationHistory_deprecated" OWNER TO dave;

SET search_path = public, pg_catalog;

--
-- Name: MeterProgramChanges; Type: TABLE; Schema: public; Owner: dave; Tablespace: 
--

CREATE TABLE "MeterProgramChanges" (
    meter_name character varying NOT NULL,
    date_changed timestamp without time zone NOT NULL,
    program_id integer NOT NULL
);


ALTER TABLE public."MeterProgramChanges" OWNER TO dave;

SET search_path = dw, pg_catalog;

--
-- Name: MeterProgramHistory_backup; Type: VIEW; Schema: dw; Owner: dave
--

CREATE VIEW "MeterProgramHistory_backup" AS
    SELECT "MeterProgramChanges".meter_name, "MeterProgramChanges".date_changed, "MeterProgramChanges".program_id FROM public."MeterProgramChanges";


ALTER TABLE dw."MeterProgramHistory_backup" OWNER TO dave;

SET search_path = public, pg_catalog;

--
-- Name: Interval; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Interval" (
    interval_read_data_id bigint NOT NULL,
    interval_id bigint NOT NULL,
    block_sequence_number smallint NOT NULL,
    end_time timestamp without time zone NOT NULL,
    gateway_collected_time timestamp without time zone NOT NULL,
    interval_sequence_number smallint NOT NULL
);


ALTER TABLE public."Interval" OWNER TO sepgroup;

--
-- Name: TABLE "Interval"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "Interval" IS 'Part of the Reading branch for MECO energy data. --Daniel Zhang (張道博)';


--
-- Name: IntervalReadData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "IntervalReadData" (
    interval_read_data_id bigint NOT NULL,
    meter_data_id bigint NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    interval_length smallint NOT NULL,
    number_intervals integer NOT NULL
);


ALTER TABLE public."IntervalReadData" OWNER TO sepgroup;

--
-- Name: TABLE "IntervalReadData"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "IntervalReadData" IS 'Part of the Reading branch for MECO energy data. --Daniel Zhang (張道博)';


--
-- Name: MeterData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "MeterData" (
    meter_data_id bigint NOT NULL,
    mac_id character(23) NOT NULL,
    meter_name character(8) NOT NULL,
    util_device_id character(8) NOT NULL,
    created timestamp without time zone
);


ALTER TABLE public."MeterData" OWNER TO sepgroup;

--
-- Name: TABLE "MeterData"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "MeterData" IS 'Root table for MECO energy data. This table is set to cascade delete so that deletions here are propagated through the MECO energy data branches. --Daniel Zhang (張道博)';


--
-- Name: COLUMN "MeterData".created; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON COLUMN "MeterData".created IS 'timestamp for when data is inserted';


--
-- Name: MeterLocationHistory; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "MeterLocationHistory" (
    meter_name character varying NOT NULL,
    mac_address character varying,
    installed timestamp(6) without time zone NOT NULL,
    uninstalled timestamp(6) without time zone,
    location character varying,
    address character varying,
    city character varying,
    latitude double precision,
    longitude double precision,
    old_service_point_id character varying,
    service_point_height double precision,
    service_point_latitude double precision,
    service_point_longitude double precision,
    notes character varying,
    service_point_id character varying
);


ALTER TABLE public."MeterLocationHistory" OWNER TO sepgroup;

--
-- Name: TABLE "MeterLocationHistory"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "MeterLocationHistory" IS 'Links meters to service points and provides a history of meter installations and uninstallations. --Daniel Zhang (張道博)';


--
-- Name: PVServicePointIDs; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "PVServicePointIDs" (
    old_pv_service_point_id character varying,
    old_house_service_point_id character varying,
    "PV_Mod_size_kW" double precision,
    inverter_model character varying,
    "size_kW" real,
    "system_cap_kW" real,
    bat character varying,
    sub character varying,
    circuit smallint,
    date_uploaded timestamp without time zone DEFAULT '2014-01-19 19:53:55.497375'::timestamp without time zone,
    has_meter smallint,
    has_separate_pv_meter smallint,
    "add_cap_kW" real,
    upgraded_total_kw real,
    street character varying,
    city character varying,
    state character varying,
    zip integer,
    month_installed integer,
    year_installed integer,
    notes character varying,
    pv_service_point_id character varying,
    house_service_point_id character varying,
    new_spid character varying(50),
    new_spid_pv character varying(50),
    nem_agreement_date date
);


ALTER TABLE public."PVServicePointIDs" OWNER TO sepgroup;

--
-- Name: TABLE "PVServicePointIDs"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "PVServicePointIDs" IS 'Contains service point data for one-meter and two-meter PV installations. --Daniel Zhang (張道博)';


--
-- Name: Reading; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Reading" (
    interval_id bigint NOT NULL,
    reading_id bigint NOT NULL,
    block_end_value real,
    channel smallint NOT NULL,
    raw_value smallint NOT NULL,
    uom character varying,
    value real
);


ALTER TABLE public."Reading" OWNER TO sepgroup;

--
-- Name: TABLE "Reading"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "Reading" IS 'Part of the Reading branch for MECO energy data. --Daniel Zhang (張道博)';


--
-- Name: nonpv_service_point_ids; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW nonpv_service_point_ids AS
    SELECT "MeterLocationHistory".service_point_id, "MeterLocationHistory".meter_name, "MeterLocationHistory".installed, "MeterLocationHistory".uninstalled FROM "MeterLocationHistory" WHERE ((NOT (EXISTS (SELECT "PVServicePointIDs".pv_service_point_id FROM "PVServicePointIDs" WHERE (("PVServicePointIDs".pv_service_point_id)::text = ("MeterLocationHistory".service_point_id)::text)))) OR (NOT (EXISTS (SELECT "PVServicePointIDs".house_service_point_id FROM "PVServicePointIDs" WHERE (("PVServicePointIDs".house_service_point_id)::text = ("MeterLocationHistory".service_point_id)::text)))));


ALTER TABLE public.nonpv_service_point_ids OWNER TO postgres;

--
-- Name: VIEW nonpv_service_point_ids; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW nonpv_service_point_ids IS 'Service Point IDs, in the MLH,  that are not PV Service Point IDs. @author Daniel Zhang (張道博)';


--
-- Name: readings_by_meter_location_history; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW readings_by_meter_location_history AS
    SELECT "MeterLocationHistory".meter_name, "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_latitude, "MeterLocationHistory".service_point_longitude, "MeterLocationHistory".location, "MeterLocationHistory".address, "MeterLocationHistory".latitude, "MeterLocationHistory".longitude, "MeterLocationHistory".installed, "MeterLocationHistory".uninstalled, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "Interval".end_time, "MeterData".meter_data_id FROM (((("MeterLocationHistory" JOIN "MeterData" ON ((("MeterLocationHistory".meter_name)::bpchar = "MeterData".meter_name))) JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (((("Interval".interval_id = "Reading".interval_id) AND ("Interval".end_time >= "MeterLocationHistory".installed)) AND CASE WHEN ("MeterLocationHistory".uninstalled IS NULL) THEN true ELSE ("Interval".end_time < "MeterLocationHistory".uninstalled) END)));


ALTER TABLE public.readings_by_meter_location_history OWNER TO eileen;

SET search_path = dw, pg_catalog;

--
-- Name: test_monthly_energy_summary_for_nonpv_service_points; Type: VIEW; Schema: dw; Owner: dave
--

CREATE VIEW test_monthly_energy_summary_for_nonpv_service_points AS
    SELECT max((readings_by_meter_location_history.service_point_id)::text) AS service_point_id, sum(CASE WHEN (readings_by_meter_location_history.channel = (1)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS total_energy_to_house_kwh, sum(CASE WHEN (readings_by_meter_location_history.channel = (2)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS total_energy_from_house_kwh, sum(CASE WHEN (readings_by_meter_location_history.channel = (3)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS total_net_energy_kwh, avg(CASE WHEN (readings_by_meter_location_history.channel = (4)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS avg, to_char(date_trunc('month'::text, readings_by_meter_location_history.end_time), 'yyyy-mm'::text) AS service_month, max(readings_by_meter_location_history.service_point_latitude) AS sp_latitude, max(readings_by_meter_location_history.service_point_longitude) AS sp_longitude, max((readings_by_meter_location_history.location)::text) AS location_id, max((readings_by_meter_location_history.address)::text) AS address, max(readings_by_meter_location_history.latitude) AS location_latitude, max(readings_by_meter_location_history.longitude) AS location_longitude, ((count(readings_by_meter_location_history.end_time) / 4) / 24) AS count_day FROM ((public.readings_by_meter_location_history JOIN public.nonpv_service_point_ids ON (((readings_by_meter_location_history.service_point_id)::text = (nonpv_service_point_ids.service_point_id)::text))) JOIN public."MeterProgramChanges" ON ((((readings_by_meter_location_history.meter_name)::text = ("MeterProgramChanges".meter_name)::text) AND (date_trunc('month'::text, readings_by_meter_location_history.end_time) = date_trunc('month'::text, "MeterProgramChanges".date_changed))))) GROUP BY readings_by_meter_location_history.service_point_id, to_char(date_trunc('month'::text, readings_by_meter_location_history.end_time), 'yyyy-mm'::text);


ALTER TABLE dw.test_monthly_energy_summary_for_nonpv_service_points OWNER TO dave;

SET search_path = dz, pg_catalog;

--
-- Name: _IrradianceFifteenMinIntervals; Type: TABLE; Schema: dz; Owner: postgres; Tablespace: 
--

CREATE TABLE "_IrradianceFifteenMinIntervals" (
    sensor_id integer,
    start_time timestamp without time zone,
    end_time timestamp without time zone
);


ALTER TABLE dz."_IrradianceFifteenMinIntervals" OWNER TO postgres;

--
-- Name: TABLE "_IrradianceFifteenMinIntervals"; Type: COMMENT; Schema: dz; Owner: postgres
--

COMMENT ON TABLE "_IrradianceFifteenMinIntervals" IS 'Used by the 15-min aggregation scripts. --Daniel Zhang (張道博)';


SET search_path = public, pg_catalog;

--
-- Name: Event; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Event" (
    event_name character varying,
    event_time timestamp without time zone,
    event_text character varying,
    event_data_id bigint,
    event_id bigint NOT NULL
);


ALTER TABLE public."Event" OWNER TO sepgroup;

--
-- Name: EventData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "EventData" (
    end_time timestamp without time zone,
    number_events smallint,
    start_time timestamp without time zone,
    meter_data_id bigint,
    event_data_id bigint NOT NULL
);


ALTER TABLE public."EventData" OWNER TO sepgroup;

SET search_path = dz, pg_catalog;

--
-- Name: count_of_event_duplicates; Type: VIEW; Schema: dz; Owner: daniel
--

CREATE VIEW count_of_event_duplicates AS
    SELECT "Event".event_time, "MeterData".meter_data_id, "EventData".event_data_id, (count(*) - 1) AS "Duplicate Count" FROM ((public."MeterData" JOIN public."EventData" ON (("MeterData".meter_data_id = "EventData".meter_data_id))) JOIN public."Event" ON (("EventData".event_data_id = "Event".event_data_id))) GROUP BY "Event".event_time, "MeterData".meter_data_id, "EventData".event_data_id HAVING ((count(*) - 1) > 0) ORDER BY "Event".event_time;


ALTER TABLE dz.count_of_event_duplicates OWNER TO daniel;

--
-- Name: readings_by_meter_location_history; Type: VIEW; Schema: dz; Owner: daniel
--

CREATE VIEW readings_by_meter_location_history AS
    SELECT "MeterLocationHistory".meter_name, "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_latitude, "MeterLocationHistory".service_point_longitude, "MeterLocationHistory".location, "MeterLocationHistory".address, "MeterLocationHistory".latitude, "MeterLocationHistory".longitude, "MeterLocationHistory".installed, "MeterLocationHistory".uninstalled, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "Interval".end_time, "MeterData".meter_data_id FROM ((((public."MeterLocationHistory" JOIN public."MeterData" ON ((("MeterLocationHistory".meter_name)::bpchar = "MeterData".meter_name))) JOIN public."IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN public."Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN public."Reading" ON (((("Interval".interval_id = "Reading".interval_id) AND ("Interval".end_time >= "MeterLocationHistory".installed)) AND CASE WHEN ("MeterLocationHistory".uninstalled IS NULL) THEN true ELSE ("Interval".end_time < "MeterLocationHistory".uninstalled) END)));


ALTER TABLE dz.readings_by_meter_location_history OWNER TO daniel;

--
-- Name: deprecated_readings_by_mlh_transposed_columns_opt1; Type: VIEW; Schema: dz; Owner: daniel
--

CREATE VIEW deprecated_readings_by_mlh_transposed_columns_opt1 AS
    SELECT readings_by_meter_location_history.service_point_id, max(CASE WHEN (readings_by_meter_location_history.channel = (1)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "Energy to House kwH", max(CASE WHEN (readings_by_meter_location_history.channel = (2)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "Energy from House kwH(rec)", max(CASE WHEN (readings_by_meter_location_history.channel = (3)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "Net Energy to House KwH", max(CASE WHEN (readings_by_meter_location_history.channel = (4)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "voltage at house", max(readings_by_meter_location_history.service_point_latitude) AS service_point_latitude, max(readings_by_meter_location_history.service_point_longitude) AS service_point_longitude, max((readings_by_meter_location_history.location)::text) AS "location_ID", max((readings_by_meter_location_history.address)::text) AS address, max(readings_by_meter_location_history.latitude) AS location_latitude, max(readings_by_meter_location_history.longitude) AS location_longitude, max(readings_by_meter_location_history.end_time) AS end_time FROM readings_by_meter_location_history GROUP BY readings_by_meter_location_history.service_point_id;


ALTER TABLE dz.deprecated_readings_by_mlh_transposed_columns_opt1 OWNER TO daniel;

--
-- Name: VIEW deprecated_readings_by_mlh_transposed_columns_opt1; Type: COMMENT; Schema: dz; Owner: daniel
--

COMMENT ON VIEW deprecated_readings_by_mlh_transposed_columns_opt1 IS 'NEEDS GROUP BY END TIME. Invalid optimization 1 for readings by MLH. Channels are transposed to columns. End time sorting is removed.';


SET search_path = public, pg_catalog;

--
-- Name: EgaugeEnergyAutoload; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "EgaugeEnergyAutoload" (
    egauge_id integer NOT NULL,
    datetime timestamp(6) without time zone NOT NULL,
    use_kw double precision,
    gen_kw double precision,
    grid_kw double precision,
    ac_kw double precision,
    acplus_kw double precision,
    clotheswasher_kw double precision,
    clotheswasher_usage_kw double precision,
    dhw_kw double precision,
    dishwasher_kw double precision,
    dryer_kw double precision,
    dryer_usage_kw double precision,
    fan_kw double precision,
    garage_ac_kw double precision,
    garage_ac_usage_kw double precision,
    large_ac_kw double precision,
    large_ac_usage_kw double precision,
    microwave_kw double precision,
    oven_kw double precision,
    oven_usage_kw double precision,
    range_kw double precision,
    range_usage_kw double precision,
    refrigerator_kw double precision,
    refrigerator_usage_kw double precision,
    rest_of_house_usage_kw double precision,
    solarpump_kw double precision,
    stove_kw double precision,
    upload_date timestamp(6) without time zone,
    oven_and_microwave_kw double precision,
    oven_and_microwave_plus_kw double precision,
    house_kw double precision,
    shop_kw double precision,
    addition_kw double precision,
    dhw_load_control double precision,
    pv_system_kw double precision,
    solar_plus_kw double precision
);


ALTER TABLE public."EgaugeEnergyAutoload" OWNER TO sepgroup;

--
-- Name: TABLE "EgaugeEnergyAutoload"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "EgaugeEnergyAutoload" IS 'Data that is autoloaded by the MSG eGauge Service. @author Daniel Zhang (張道博)';


SET search_path = dz, pg_catalog;

--
-- Name: outlier_test; Type: VIEW; Schema: dz; Owner: postgres
--

CREATE VIEW outlier_test AS
    SELECT "EgaugeEnergyAutoload".egauge_id, "EgaugeEnergyAutoload".datetime, "EgaugeEnergyAutoload".use_kw AS "use_kw (whole house)", "EgaugeEnergyAutoload".ac_kw, "EgaugeEnergyAutoload".addition_kw, "EgaugeEnergyAutoload".clotheswasher_kw, "EgaugeEnergyAutoload".dhw_load_control, "EgaugeEnergyAutoload".dryer_kw, "EgaugeEnergyAutoload".garage_ac_kw, "EgaugeEnergyAutoload".gen_kw, "EgaugeEnergyAutoload".large_ac_kw, "EgaugeEnergyAutoload".oven_and_microwave_kw, "EgaugeEnergyAutoload".oven_kw, "EgaugeEnergyAutoload".range_kw, "EgaugeEnergyAutoload".refrigerator_usage_kw, "EgaugeEnergyAutoload".shop_kw, "EgaugeEnergyAutoload".stove_kw FROM public."EgaugeEnergyAutoload" WHERE ((((((((((((((("EgaugeEnergyAutoload".use_kw IS NULL) OR ("EgaugeEnergyAutoload".use_kw < (20)::double precision)) AND (("EgaugeEnergyAutoload".ac_kw IS NULL) OR ("EgaugeEnergyAutoload".ac_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".addition_kw IS NULL) OR ("EgaugeEnergyAutoload".addition_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".clotheswasher_kw IS NULL) OR ("EgaugeEnergyAutoload".clotheswasher_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".dhw_load_control IS NULL) OR ("EgaugeEnergyAutoload".dhw_load_control < (10)::double precision))) AND (("EgaugeEnergyAutoload".dryer_kw IS NULL) OR ("EgaugeEnergyAutoload".dryer_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".garage_ac_kw IS NULL) OR ("EgaugeEnergyAutoload".garage_ac_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".large_ac_kw IS NULL) OR ("EgaugeEnergyAutoload".large_ac_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".oven_and_microwave_kw IS NULL) OR ("EgaugeEnergyAutoload".oven_and_microwave_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".oven_kw IS NULL) OR ("EgaugeEnergyAutoload".oven_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".range_kw IS NULL) OR ("EgaugeEnergyAutoload".range_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".refrigerator_usage_kw IS NULL) OR ("EgaugeEnergyAutoload".refrigerator_usage_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".shop_kw IS NULL) OR ("EgaugeEnergyAutoload".shop_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".shop_kw IS NULL) OR ("EgaugeEnergyAutoload".shop_kw < (10)::double precision)));


ALTER TABLE dz.outlier_test OWNER TO postgres;

--
-- Name: reading_dupes; Type: VIEW; Schema: dz; Owner: daniel
--

CREATE VIEW reading_dupes AS
    SELECT "Interval".end_time, "MeterData".meter_name, "Reading".channel, (count(*) - 1) AS dupe_cnt FROM (((public."MeterData" JOIN public."IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN public."Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN public."Reading" ON (("Interval".interval_id = "Reading".interval_id))) GROUP BY "MeterData".meter_name, "Interval".end_time, "Reading".channel;


ALTER TABLE dz.reading_dupes OWNER TO daniel;

--
-- Name: readings_by_mlh_new_spid_for_ashkan_from_2013-07-01; Type: VIEW; Schema: dz; Owner: daniel
--

CREATE VIEW "readings_by_mlh_new_spid_for_ashkan_from_2013-07-01" AS
    SELECT readings_by_meter_location_history.service_point_id, max(CASE WHEN (readings_by_meter_location_history.channel = (1)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "Energy to House kwH", max(CASE WHEN (readings_by_meter_location_history.channel = (2)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "Energy from House kwH(rec)", max(CASE WHEN (readings_by_meter_location_history.channel = (3)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "Net Energy to House KwH", max(CASE WHEN (readings_by_meter_location_history.channel = (4)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS "voltage at house", max((readings_by_meter_location_history.address)::text) AS address, readings_by_meter_location_history.end_time FROM readings_by_meter_location_history WHERE ((readings_by_meter_location_history.end_time >= '2013-07-01 00:00:00'::timestamp without time zone) AND (readings_by_meter_location_history.end_time <= '2014-02-01 00:00:00'::timestamp without time zone)) GROUP BY readings_by_meter_location_history.service_point_id, readings_by_meter_location_history.end_time;


ALTER TABLE dz."readings_by_mlh_new_spid_for_ashkan_from_2013-07-01" OWNER TO daniel;

SET search_path = public, pg_catalog;

--
-- Name: readings_unfiltered; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW readings_unfiltered AS
    SELECT "Interval".end_time, "MeterData".meter_name, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "IntervalReadData".start_time, "IntervalReadData".end_time AS ird_end_time, "MeterData".meter_data_id, "Reading".interval_id FROM ((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id)));


ALTER TABLE public.readings_unfiltered OWNER TO postgres;

--
-- Name: VIEW readings_unfiltered; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW readings_unfiltered IS 'All readings along with their end times by meter. @author Daniel Zhang (張道博)';


SET search_path = dz, pg_catalog;

--
-- Name: readings_not_referenced_by_mlh_deprecated; Type: VIEW; Schema: dz; Owner: postgres
--

CREATE VIEW readings_not_referenced_by_mlh_deprecated AS
    SELECT readings_by_meter_location_history_new_spid_2.meter_name AS mlh_meter_name, readings_with_meter_data_id_unfiltered.meter_name AS full_meter_name, readings_by_meter_location_history_new_spid_2.channel AS mlh_channel, readings_by_meter_location_history_new_spid_2.value AS mlh_value, readings_with_meter_data_id_unfiltered.channel AS full_channel, readings_with_meter_data_id_unfiltered.value AS full_value, readings_by_meter_location_history_new_spid_2.end_time AS mlh_end_time, readings_with_meter_data_id_unfiltered.end_time AS full_end_time, readings_with_meter_data_id_unfiltered.meter_data_id AS full_meter_data_id FROM (public.readings_unfiltered readings_with_meter_data_id_unfiltered LEFT JOIN public.readings_by_meter_location_history readings_by_meter_location_history_new_spid_2 ON ((readings_with_meter_data_id_unfiltered.meter_data_id = readings_by_meter_location_history_new_spid_2.meter_data_id))) WHERE (readings_by_meter_location_history_new_spid_2.meter_data_id IS NULL);


ALTER TABLE dz.readings_not_referenced_by_mlh_deprecated OWNER TO postgres;

--
-- Name: VIEW readings_not_referenced_by_mlh_deprecated; Type: COMMENT; Schema: dz; Owner: postgres
--

COMMENT ON VIEW readings_not_referenced_by_mlh_deprecated IS 'Readings that are present in the DB but are not referenced by the Meter Location History. @author Daniel Zhang (張道博)';


--
-- Name: readings_unfiltered; Type: VIEW; Schema: dz; Owner: daniel
--

CREATE VIEW readings_unfiltered AS
    SELECT "Interval".end_time, "MeterData".meter_name, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "IntervalReadData".start_time, "IntervalReadData".end_time AS ird_end_time, "MeterData".meter_data_id, "Reading".interval_id FROM (((public."MeterData" JOIN public."IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN public."Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN public."Reading" ON (("Interval".interval_id = "Reading".interval_id)));


ALTER TABLE dz.readings_unfiltered OWNER TO daniel;

--
-- Name: readings_with_pv_service_point_id_deprecated; Type: VIEW; Schema: dz; Owner: postgres
--

CREATE VIEW readings_with_pv_service_point_id_deprecated AS
    SELECT readings_by_meter_location_history_new_spid.meter_name, readings_by_meter_location_history_new_spid.end_time, max((readings_by_meter_location_history_new_spid.location)::text) AS location_id, max(("PVServicePointIDs".old_pv_service_point_id)::text) AS pv_service_point_id, max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS pv_channel_1, max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (2)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS pv_channel_2, max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (3)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS pv_channel_3, public.zero_to_null(max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END)) AS pv_channel_4_voltage FROM (public."PVServicePointIDs" JOIN public.readings_by_meter_location_history readings_by_meter_location_history_new_spid ON ((("PVServicePointIDs".old_pv_service_point_id)::text = (readings_by_meter_location_history_new_spid.service_point_id)::text))) GROUP BY readings_by_meter_location_history_new_spid.meter_name, readings_by_meter_location_history_new_spid.end_time;


ALTER TABLE dz.readings_with_pv_service_point_id_deprecated OWNER TO postgres;

--
-- Name: VIEW readings_with_pv_service_point_id_deprecated; Type: COMMENT; Schema: dz; Owner: postgres
--

COMMENT ON VIEW readings_with_pv_service_point_id_deprecated IS 'Readings that have an associated PV Service Point ID. @author Daniel Zhang (張道博)';


--
-- Name: test_readings_by_meter_location_history; Type: VIEW; Schema: dz; Owner: daniel
--

CREATE VIEW test_readings_by_meter_location_history AS
    SELECT "MeterLocationHistory".meter_name, "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_latitude, "MeterLocationHistory".service_point_longitude, "MeterLocationHistory".location, "MeterLocationHistory".address, "MeterLocationHistory".latitude, "MeterLocationHistory".longitude, "MeterLocationHistory".installed, "MeterLocationHistory".uninstalled, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "Interval".end_time, "MeterData".meter_data_id FROM ((((public."MeterLocationHistory" JOIN public."MeterData" ON ((("MeterLocationHistory".meter_name)::bpchar = "MeterData".meter_name))) JOIN public."IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN public."Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN public."Reading" ON (((("Interval".interval_id = "Reading".interval_id) AND ("Interval".end_time >= "MeterLocationHistory".installed)) AND CASE WHEN ("MeterLocationHistory".uninstalled IS NULL) THEN true ELSE ("Interval".end_time < "MeterLocationHistory".uninstalled) END)));


ALTER TABLE dz.test_readings_by_meter_location_history OWNER TO daniel;

SET search_path = public, pg_catalog;

--
-- Name: raw_meter_readings; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW raw_meter_readings AS
    SELECT "Interval".end_time, "MeterData".meter_name, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "MeterData".util_device_id FROM ((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) ORDER BY "Interval".end_time, "MeterData".meter_name, "Reading".channel;


ALTER TABLE public.raw_meter_readings OWNER TO postgres;

SET search_path = ep, pg_catalog;

--
-- Name: dates_raw_meter_readings; Type: VIEW; Schema: ep; Owner: eileen
--

CREATE VIEW dates_raw_meter_readings AS
    SELECT min(raw_meter_readings.end_time) AS min, max(raw_meter_readings.end_time) AS max, raw_meter_readings.meter_name, raw_meter_readings.util_device_id FROM public.raw_meter_readings GROUP BY raw_meter_readings.meter_name, raw_meter_readings.util_device_id;


ALTER TABLE ep.dates_raw_meter_readings OWNER TO eileen;

--
-- Name: egauge4913; Type: VIEW; Schema: ep; Owner: eileen
--

CREATE VIEW egauge4913 AS
    SELECT "EgaugeEnergyAutoload".egauge_id, "EgaugeEnergyAutoload".datetime, "EgaugeEnergyAutoload".use_kw, "EgaugeEnergyAutoload".gen_kw, "EgaugeEnergyAutoload".dryer_kw, "EgaugeEnergyAutoload".dryer_usage_kw, "EgaugeEnergyAutoload".clotheswasher_usage_kw, "EgaugeEnergyAutoload".clotheswasher_kw FROM public."EgaugeEnergyAutoload" WHERE (("EgaugeEnergyAutoload".egauge_id = 4913) AND ("EgaugeEnergyAutoload".datetime > '2014-04-01 00:00:00'::timestamp without time zone));


ALTER TABLE ep.egauge4913 OWNER TO eileen;

--
-- Name: meter115651channel2; Type: VIEW; Schema: ep; Owner: eileen
--

CREATE VIEW meter115651channel2 AS
    SELECT raw_meter_readings.end_time, raw_meter_readings.meter_name, raw_meter_readings.channel, raw_meter_readings.value FROM public.raw_meter_readings WHERE (raw_meter_readings.channel = 2);


ALTER TABLE ep.meter115651channel2 OWNER TO eileen;

SET search_path = public, pg_catalog;

--
-- Name: readings_unfiltered_columns; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW readings_unfiltered_columns AS
    SELECT readings_unfiltered.meter_name, readings_unfiltered.end_time, max(CASE WHEN (readings_unfiltered.channel = (1)::smallint) THEN readings_unfiltered.value ELSE NULL::real END) AS energy_tohouse_kwh, max(CASE WHEN (readings_unfiltered.channel = (2)::smallint) THEN readings_unfiltered.value ELSE NULL::real END) AS energy_fromhouse_kwh, max(CASE WHEN (readings_unfiltered.channel = (3)::smallint) THEN readings_unfiltered.value ELSE NULL::real END) AS net_energy_kwh, max(CASE WHEN (readings_unfiltered.channel = (4)::smallint) THEN readings_unfiltered.value ELSE NULL::real END) AS voltage FROM readings_unfiltered GROUP BY readings_unfiltered.meter_name, readings_unfiltered.end_time;


ALTER TABLE public.readings_unfiltered_columns OWNER TO eileen;

SET search_path = ep, pg_catalog;

--
-- Name: readings_meter_changes; Type: VIEW; Schema: ep; Owner: eileen
--

CREATE VIEW readings_meter_changes AS
    SELECT "MeterProgramChanges".meter_name, "MeterProgramChanges".date_changed, "MeterProgramChanges".program_id, readings_unfiltered_columns.end_time, readings_unfiltered_columns.energy_tohouse_kwh, readings_unfiltered_columns.energy_fromhouse_kwh, readings_unfiltered_columns.net_energy_kwh, readings_unfiltered_columns.voltage FROM (public."MeterProgramChanges" JOIN public.readings_unfiltered_columns ON ((("MeterProgramChanges".meter_name)::bpchar = readings_unfiltered_columns.meter_name))) WHERE (readings_unfiltered_columns.end_time > '2014-02-01 00:00:00'::timestamp without time zone);


ALTER TABLE ep.readings_meter_changes OWNER TO eileen;

--
-- Name: voltage_data_for_lesson_Mel_3D; Type: VIEW; Schema: ep; Owner: eileen
--

CREATE VIEW "voltage_data_for_lesson_Mel_3D" AS
    SELECT readings_by_meter_location_history.service_point_id, readings_by_meter_location_history.end_time, readings_by_meter_location_history.address, readings_by_meter_location_history.value, readings_by_meter_location_history.latitude, readings_by_meter_location_history.longitude FROM public.readings_by_meter_location_history WHERE (((readings_by_meter_location_history.channel = 4) AND (readings_by_meter_location_history.end_time > '2013-11-30 23:59:00'::timestamp without time zone)) AND (readings_by_meter_location_history.end_time < '2013-12-15 01:01:00'::timestamp without time zone));


ALTER TABLE ep."voltage_data_for_lesson_Mel_3D" OWNER TO eileen;

SET search_path = public, pg_catalog;

--
-- Name: AsBuilt; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "AsBuilt" (
    owner character(100),
    address character(200),
    spid integer NOT NULL,
    ihd character(125),
    pct character(125),
    load_control character(125),
    repeater character(125)
);


ALTER TABLE public."AsBuilt" OWNER TO sepgroup;

--
-- Name: AverageFifteenMinCircuitData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "AverageFifteenMinCircuitData" (
    circuit integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    amp_a integer,
    amp_b integer,
    amp_c integer,
    mvar double precision,
    mw double precision,
    upload_date date
);


ALTER TABLE public."AverageFifteenMinCircuitData" OWNER TO postgres;

--
-- Name: AverageFifteenMinEgaugeEnergyAutoload; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "AverageFifteenMinEgaugeEnergyAutoload" (
    egauge_id integer NOT NULL,
    datetime timestamp(6) without time zone NOT NULL,
    use_kw double precision,
    gen_kw double precision,
    grid_kw double precision,
    ac_kw double precision,
    acplus_kw double precision,
    clotheswasher_kw double precision,
    clotheswasher_usage_kw double precision,
    dhw_kw double precision,
    dishwasher_kw double precision,
    dryer_kw double precision,
    dryer_usage_kw double precision,
    fan_kw double precision,
    garage_ac_kw double precision,
    garage_ac_usage_kw double precision,
    large_ac_kw double precision,
    large_ac_usage_kw double precision,
    microwave_kw double precision,
    oven_kw double precision,
    oven_usage_kw double precision,
    range_kw double precision,
    range_usage_kw double precision,
    refrigerator_kw double precision,
    refrigerator_usage_kw double precision,
    rest_of_house_usage_kw double precision,
    solarpump_kw double precision,
    stove_kw double precision,
    upload_date timestamp(6) without time zone,
    oven_and_microwave_kw double precision,
    oven_and_microwave_plus_kw double precision,
    house_kw double precision,
    shop_kw double precision,
    addition_kw double precision,
    dhw_load_control double precision,
    pv_system_kw double precision,
    solar_plus_kw double precision
);


ALTER TABLE public."AverageFifteenMinEgaugeEnergyAutoload" OWNER TO postgres;

--
-- Name: AverageFifteenMinIrradianceData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "AverageFifteenMinIrradianceData" (
    sensor_id integer NOT NULL,
    irradiance_w_per_m2 double precision,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public."AverageFifteenMinIrradianceData" OWNER TO postgres;

--
-- Name: TABLE "AverageFifteenMinIrradianceData"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE "AverageFifteenMinIrradianceData" IS 'Static table generated by aggregate-irradiance-data.sh. --Daniel Zhang (張道博)';


--
-- Name: AverageFifteenMinKiheiSCADATemperatureHumidity; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "AverageFifteenMinKiheiSCADATemperatureHumidity" (
    "timestamp" timestamp without time zone NOT NULL,
    met_air_temp_degf double precision,
    met_rel_humid_pct double precision
);


ALTER TABLE public."AverageFifteenMinKiheiSCADATemperatureHumidity" OWNER TO postgres;

--
-- Name: BatteryWailea; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "BatteryWailea" (
    "timestamp" timestamp without time zone,
    kvar double precision,
    kw double precision,
    soc double precision,
    pwr_ref_volt double precision,
    upload_date timestamp without time zone DEFAULT now()
);


ALTER TABLE public."BatteryWailea" OWNER TO sepgroup;

--
-- Name: TABLE "BatteryWailea"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "BatteryWailea" IS 'KVAR – This is the var output of the battery system (- is absorbing vars, + is discharging vars)
KW – This is the kilowatt output of the battery system (- is absorbing kW, + is discharging kW)
SOC – This is the state of charge for the battery system (100% is full charged, 0% is fully discharged)
PWR_REF/VOLT – This is the measurement of voltage (volts) at the protection relay for circuit breaker 1517.';


--
-- Name: CircuitData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "CircuitData" (
    circuit integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    amp_a integer,
    amp_b integer,
    amp_c integer,
    mvar double precision,
    mw double precision,
    upload_date date DEFAULT now()
);


ALTER TABLE public."CircuitData" OWNER TO sepgroup;

--
-- Name: EgaugeInfo; Type: TABLE; Schema: public; Owner: eileen; Tablespace: 
--

CREATE TABLE "EgaugeInfo" (
    svc_pt_id character varying,
    address character varying,
    egauge character varying,
    egauge_id integer
);


ALTER TABLE public."EgaugeInfo" OWNER TO eileen;

--
-- Name: ExportHistory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "ExportHistory" (
    "timestamp" timestamp without time zone NOT NULL,
    name text,
    url text,
    size integer
);


ALTER TABLE public."ExportHistory" OWNER TO postgres;

--
-- Name: TABLE "ExportHistory"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE "ExportHistory" IS 'Used for keeping track of DB exports.';


--
-- Name: IrradianceData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "IrradianceData" (
    sensor_id integer NOT NULL,
    irradiance_w_per_m2 double precision,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public."IrradianceData" OWNER TO sepgroup;

--
-- Name: IrradianceSensorInfo; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "IrradianceSensorInfo" (
    sensor_id integer NOT NULL,
    latitude double precision,
    longitude double precision,
    manufacturer character varying,
    model character varying,
    name character varying
);


ALTER TABLE public."IrradianceSensorInfo" OWNER TO sepgroup;

--
-- Name: KiheiSCADATemperatureHumidity; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "KiheiSCADATemperatureHumidity" (
    "timestamp" timestamp without time zone NOT NULL,
    met_air_temp_degf double precision,
    met_rel_humid_pct double precision
);


ALTER TABLE public."KiheiSCADATemperatureHumidity" OWNER TO postgres;

--
-- Name: LocationRecords; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "LocationRecords" (
    load_device_type character varying,
    load_action character varying,
    device_util_id character varying NOT NULL,
    device_serial_no character varying,
    device_status character varying,
    device_operational_status character varying,
    install_date timestamp without time zone,
    remove_date timestamp without time zone,
    cust_account_no character varying,
    cust_name character varying,
    service_point_util_id character varying,
    service_type character varying,
    meter_phase character varying,
    cust_billing_cycle character varying,
    location_code character varying,
    voltage_level character varying,
    voltage_phase character varying,
    service_pt_height character varying,
    service_pt_longitude real,
    service_pt_latitude real,
    device_pt_ratio character varying,
    device_ct_ratio character varying,
    premise_util_id character varying,
    premise_type character varying,
    premise_description character varying,
    address1 character varying,
    address2 character varying,
    city character varying,
    cross_street character varying,
    state character(2),
    post_code character varying,
    country character varying,
    timezone character varying,
    region_code character varying,
    map_page_no character varying,
    map_coord character varying,
    longitude real,
    latitude real
);


ALTER TABLE public."LocationRecords" OWNER TO sepgroup;

--
-- Name: MSG_PV_Data; Type: TABLE; Schema: public; Owner: eileen; Tablespace: 
--

CREATE TABLE "MSG_PV_Data" (
    util_device_id character varying(64) NOT NULL,
    map integer,
    no integer,
    pv_mod_size_kw double precision,
    inverter_model character varying(40),
    inverter_size_kw real,
    system_cap_kw real,
    add_cap_kw real,
    upg_date real,
    battery character varying(10),
    substation character varying(20),
    circuit real,
    upload_date timestamp without time zone
);


ALTER TABLE public."MSG_PV_Data" OWNER TO eileen;

--
-- Name: COLUMN "MSG_PV_Data".util_device_id; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".util_device_id IS 'meter id number';


--
-- Name: COLUMN "MSG_PV_Data".map; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".map IS 'referencing map from Mel Gehrs';


--
-- Name: COLUMN "MSG_PV_Data".no; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".no IS 'net energy metering number from MECO';


--
-- Name: COLUMN "MSG_PV_Data".pv_mod_size_kw; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".pv_mod_size_kw IS 'total capacity of all the modules (panels)';


--
-- Name: COLUMN "MSG_PV_Data".inverter_model; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".inverter_model IS 'Inverter make and model number';


--
-- Name: COLUMN "MSG_PV_Data".inverter_size_kw; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".inverter_size_kw IS 'total inverter capacity';


--
-- Name: COLUMN "MSG_PV_Data".system_cap_kw; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".system_cap_kw IS 'System capacity: smaller of the two - either module size or inverter size';


--
-- Name: COLUMN "MSG_PV_Data".add_cap_kw; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".add_cap_kw IS 'can extra capacity be added? Installation with microinverters can easily add capacity';


--
-- Name: COLUMN "MSG_PV_Data".upg_date; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".upg_date IS 'last date of an upgrade of system capacity';


--
-- Name: COLUMN "MSG_PV_Data".battery; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".battery IS 'if there is a battery (none in Maui Meadows in 2013)';


--
-- Name: COLUMN "MSG_PV_Data".substation; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".substation IS 'substation ID';


--
-- Name: COLUMN "MSG_PV_Data".circuit; Type: COMMENT; Schema: public; Owner: eileen
--

COMMENT ON COLUMN "MSG_PV_Data".circuit IS 'circuit ID number';


--
-- Name: MeterRecords; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "MeterRecords" (
    type character varying,
    action character varying,
    did_sub_type character varying,
    device_util_id character varying NOT NULL,
    device_serial_no character varying,
    device_status character varying,
    device_operational_status character varying,
    device_name character varying,
    device_description character varying,
    device_mfg character varying,
    device_mfg_date timestamp(6) without time zone,
    device_mfg_model character varying,
    device_sw_ver_no character varying,
    device_sw_rev_no character varying,
    device_sw_patch_no character varying,
    device_sw_config character varying,
    device_hw_ver_no character varying,
    device_hw_rev_no character varying,
    device_hw_patch_no character varying,
    device_hw_config character varying,
    meter_form_type character varying,
    meter_base_type character varying,
    max_amp_class character varying,
    rollover_point character varying,
    volt_type character varying,
    nic_mac_address character varying,
    nic_serial_no character varying,
    nic_rf_channel character varying,
    nic_network_identifier character varying,
    nic_model character varying,
    nic_sw_ver_no character varying,
    nic_sw_rev_no character varying,
    nic_sw_patch_no character varying,
    nic_released_date character varying,
    nic_sw_config character varying,
    nic_hw_ver_no character varying,
    nic_hw_rev_no character varying,
    nic_hw_patch_no character varying,
    nic_hw_config character varying,
    master_password character varying,
    reader_password character varying,
    cust_password character varying,
    meter_mode character varying,
    timezone_region character varying,
    battery_mfg_name character varying,
    battery_model_no character varying,
    battery_serial_no character varying,
    battery_mfg_date character varying,
    battery_exp_date character varying,
    battery_installed_date character varying,
    battery_lot_no character varying,
    battery_last_tested_date character varying,
    price_program character varying,
    catalog_number character varying,
    program_seal character varying,
    meter_program_id character varying,
    device_attribute_1 character varying,
    device_attribute_2 character varying,
    device_attribute_3 character varying,
    device_attribute_4 character varying,
    device_attribute_5 character varying,
    nic_attribute_1 character varying,
    nic_attribute_2 character varying,
    nic_attribute_3 character varying,
    nic_attribute_4 character varying,
    nic_attribute_5 character varying
);


ALTER TABLE public."MeterRecords" OWNER TO sepgroup;

--
-- Name: NotificationHistory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "NotificationHistory" (
    "notificationType" character varying NOT NULL,
    "notificationTime" timestamp without time zone NOT NULL
);


ALTER TABLE public."NotificationHistory" OWNER TO postgres;

--
-- Name: TABLE "NotificationHistory"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE "NotificationHistory" IS 'Used for tracking automatic notifications. @author Daniel Zhang (張道博)';


--
-- Name: PowerMeterEvents; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "PowerMeterEvents" (
    dtype text,
    id bigint NOT NULL,
    event_category integer,
    el_epoch_num text,
    el_seq_num text,
    event_ack_status text,
    event_text text,
    event_time timestamp without time zone NOT NULL,
    generic_col_1 text,
    generic_col_2 text,
    generic_col_3 text,
    generic_col_4 text,
    generic_col_5 text,
    generic_col_6 text,
    generic_col_7 text,
    generic_col_8 text,
    generic_col_9 text,
    generic_col_10 text,
    insert_ts timestamp without time zone,
    job_id text,
    event_key integer,
    nic_reboot_count text,
    seconds_since_reboot text,
    event_severity text,
    source_id integer,
    update_ts timestamp without time zone,
    updated_by_user text,
    event_ack_note text
);


ALTER TABLE public."PowerMeterEvents" OWNER TO sepgroup;

--
-- Name: Register; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Register" (
    tier_id bigint NOT NULL,
    register_id bigint NOT NULL,
    cumulative_demand real,
    demand_uom character varying,
    number smallint NOT NULL,
    summation real,
    summation_uom character varying
);


ALTER TABLE public."Register" OWNER TO sepgroup;

--
-- Name: RegisterData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "RegisterData" (
    meter_data_id bigint NOT NULL,
    register_data_id bigint NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    number_reads smallint NOT NULL
);


ALTER TABLE public."RegisterData" OWNER TO sepgroup;

--
-- Name: RegisterRead; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "RegisterRead" (
    register_data_id bigint NOT NULL,
    register_read_id bigint NOT NULL,
    gateway_collected_time timestamp without time zone NOT NULL,
    read_time timestamp without time zone NOT NULL,
    register_read_source character varying NOT NULL,
    season smallint NOT NULL
);


ALTER TABLE public."RegisterRead" OWNER TO sepgroup;

--
-- Name: TapData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "TapData" (
    "timestamp" timestamp without time zone,
    tap_setting real,
    substation character varying(20) DEFAULT 'wailea'::character varying,
    transformer character varying(4) DEFAULT '4'::character varying
);


ALTER TABLE public."TapData" OWNER TO sepgroup;

--
-- Name: Tier; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Tier" (
    register_read_id bigint NOT NULL,
    tier_id bigint NOT NULL,
    number smallint NOT NULL
);


ALTER TABLE public."Tier" OWNER TO sepgroup;

--
-- Name: TransformerData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "TransformerData" (
    transformer character varying NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    vlt_a double precision,
    vlt_b double precision,
    vlt_c double precision,
    volt double precision,
    upload_date date DEFAULT now()
);


ALTER TABLE public."TransformerData" OWNER TO sepgroup;

--
-- Name: TABLE "TransformerData"; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON TABLE "TransformerData" IS 'Data from MECO scada data extract (comes with circuit data and irradiance data)
vlt_a, vlt_b, and vlt_c = kV (1,000 volts) measured phase to neutral
volt (e.g. 121.5) = reference voltage measurement (measured in volts) for the load tap changer
';


--
-- Name: TransformerDataNREL; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "TransformerDataNREL" (
    "timestamp" timestamp without time zone NOT NULL,
    quality character varying,
    v1_phasor_magnitude double precision,
    v1_phase_angle double precision,
    v2_phasor_magnitude double precision,
    v2_phase_angle double precision,
    v12_phasor_magnitude double precision,
    v12_phase_angle double precision,
    i1_phasor_magnitude double precision,
    i1_phase_angle double precision,
    i2_phasor_magnitude double precision,
    i2_phase_angle double precision,
    in_phasor_magnitude double precision,
    in_phase_angle double precision,
    frequency double precision,
    v1_rms double precision,
    v2_rms double precision,
    v12_rms double precision,
    i1_rms double precision,
    i2_rms double precision,
    in_rms double precision,
    apparent_power_magnitude_s double precision,
    real_power_p double precision,
    reactive_power_q double precision,
    power_factor double precision,
    meter_internal_temperature double precision,
    transformer_housing_temperature double precision,
    device_name character varying NOT NULL
);


ALTER TABLE public."TransformerDataNREL" OWNER TO sepgroup;

--
-- Name: TransformerDataNRELST; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "TransformerDataNRELST" (
    "timestamp" timestamp without time zone NOT NULL,
    quality character varying,
    va_phasor_magnitude double precision,
    va_phasor_angle double precision,
    vb_phasor_magnitude double precision,
    vb_phasor_angle double precision,
    vc_phasor_magnitude double precision,
    vc_phasor_angle double precision,
    ia_phasor_magnitude double precision,
    ia_phasor_angle double precision,
    ib_phasor_magnitude double precision,
    ib_phasor_angle double precision,
    ic_phasor_magnitude double precision,
    ic_phasor_angle double precision,
    frequency double precision,
    va_rms double precision,
    vb_rms double precision,
    vc_rms double precision,
    ia_rms double precision,
    ib_rms double precision,
    ic_rms double precision,
    apparent_power_magnitude_s double precision,
    phase_a_apparent_power_magnitude_s double precision,
    phase_b_apparent_power_magnitude_s double precision,
    phase_c_apparent_power_magnitude_s double precision,
    real_power_p double precision,
    phase_a_real_power_p double precision,
    phase_b_real_power_p double precision,
    phase_c_real_power_p double precision,
    reactive_power_q double precision,
    phase_a_reactive_power_q double precision,
    phase_b_reactive_power_q double precision,
    phase_c_reactive_power_q double precision,
    power_factor double precision,
    meter_internal_temperature double precision,
    transformer_housing_temperature double precision,
    device_name character varying NOT NULL
);


ALTER TABLE public."TransformerDataNRELST" OWNER TO sepgroup;

--
-- Name: WeatherNOAA; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE "WeatherNOAA" (
    wban character varying NOT NULL,
    datetime timestamp(6) without time zone NOT NULL,
    station_type smallint,
    sky_condition character varying,
    sky_condition_flag character varying,
    visibility character varying,
    visibility_flag character varying,
    weather_type character varying,
    weather_type_flag character varying,
    dry_bulb_farenheit character varying,
    dry_bulb_farenheit_flag character varying,
    dry_bulb_celsius character varying,
    dry_bulb_celsius_flag character varying,
    wet_bulb_farenheit character varying,
    wet_bulb_farenheit_flag character varying,
    wet_bulb_celsius character varying,
    wet_bulb_celsius_flag character varying,
    dew_point_farenheit character varying,
    dew_point_farenheit_flag character varying,
    dew_point_celsius character varying,
    dew_point_celsius_flag character varying,
    relative_humidity character varying,
    relative_humidity_flag character varying,
    wind_speed character varying,
    wind_speed_flag character varying,
    wind_direction character varying,
    wind_direction_flag character varying,
    value_for_wind_character character varying,
    value_for_wind_character_flag character varying,
    station_pressure character varying,
    station_pressure_flag character varying,
    pressure_tendency character varying,
    pressure_tendency_flag character varying,
    pressure_change character varying,
    pressure_change_flag character varying,
    sea_level_pressure character varying,
    sea_level_pressure_flag character varying,
    record_type character varying NOT NULL,
    record_type_flag character varying,
    hourly_precip character varying,
    hourly_precip_flag character varying,
    altimeter character varying,
    altimeter_flag character varying,
    created timestamp(6) with time zone NOT NULL
);


ALTER TABLE public."WeatherNOAA" OWNER TO daniel;

--
-- Name: COLUMN "WeatherNOAA".created; Type: COMMENT; Schema: public; Owner: daniel
--

COMMENT ON COLUMN "WeatherNOAA".created IS 'Time that record was created.';


--
-- Name: _IrradianceFifteenMinIntervals; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "_IrradianceFifteenMinIntervals" (
    sensor_id integer,
    start_time timestamp without time zone,
    end_time timestamp without time zone
);


ALTER TABLE public."_IrradianceFifteenMinIntervals" OWNER TO postgres;

--
-- Name: TABLE "_IrradianceFifteenMinIntervals"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE "_IrradianceFifteenMinIntervals" IS 'Private table used by 15 min aggregation operations. --Daniel Zhang (張道博)';


--
-- Name: az_ashkan1; Type: VIEW; Schema: public; Owner: christian
--

CREATE VIEW az_ashkan1 AS
    SELECT DISTINCT avg("IrradianceData".irradiance_w_per_m2) AS "irradiance w/m2", date_trunc('hour'::text, "IrradianceData"."timestamp") AS "time hr", avg("KiheiSCADATemperatureHumidity".met_air_temp_degf) AS temperature, avg("KiheiSCADATemperatureHumidity".met_rel_humid_pct) AS "humidity pct" FROM ("IrradianceData" JOIN "KiheiSCADATemperatureHumidity" ON (("IrradianceData"."timestamp" = "KiheiSCADATemperatureHumidity"."timestamp"))) GROUP BY "IrradianceData"."timestamp" ORDER BY date_trunc('hour'::text, "IrradianceData"."timestamp") LIMIT 1000;


ALTER TABLE public.az_ashkan1 OWNER TO christian;

--
-- Name: az_houses_all_with_smart_meter; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW az_houses_all_with_smart_meter AS
    SELECT "MeterLocationHistory".address, "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_id AS new_service_point_id FROM "MeterLocationHistory" WHERE ("MeterLocationHistory".uninstalled IS NULL);


ALTER TABLE public.az_houses_all_with_smart_meter OWNER TO eileen;

--
-- Name: az_houses_with_no_pv; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW az_houses_with_no_pv AS
    SELECT az_houses_all_with_smart_meter.address, az_houses_all_with_smart_meter.service_point_id FROM (az_houses_all_with_smart_meter JOIN "PVServicePointIDs" ON ((("PVServicePointIDs".old_house_service_point_id)::text = (az_houses_all_with_smart_meter.service_point_id)::text))) WHERE ((az_houses_all_with_smart_meter.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text);


ALTER TABLE public.az_houses_with_no_pv OWNER TO eileen;

--
-- Name: az_houses_with_pv_and_pv_meter; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW az_houses_with_pv_and_pv_meter AS
    SELECT "PVServicePointIDs".old_pv_service_point_id AS pv_service_point_id, "PVServicePointIDs".old_house_service_point_id AS house_service_point_id, "PVServicePointIDs".has_meter, "PVServicePointIDs".has_separate_pv_meter, "PVServicePointIDs".street FROM "PVServicePointIDs" WHERE (("PVServicePointIDs".has_meter = 1) AND ("PVServicePointIDs".has_separate_pv_meter = 1));


ALTER TABLE public.az_houses_with_pv_and_pv_meter OWNER TO eileen;

--
-- Name: az_houses_with_pv_no_extra_meter; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW az_houses_with_pv_no_extra_meter AS
    SELECT "PVServicePointIDs".old_pv_service_point_id AS pv_service_point_id, "PVServicePointIDs".old_house_service_point_id AS house_service_point_id, "PVServicePointIDs".has_meter, "PVServicePointIDs".has_separate_pv_meter, "PVServicePointIDs".street FROM "PVServicePointIDs" WHERE (("PVServicePointIDs".has_meter = 1) AND ("PVServicePointIDs".has_separate_pv_meter = 0));


ALTER TABLE public.az_houses_with_pv_no_extra_meter OWNER TO eileen;

--
-- Name: az_noaa_weather_data; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW az_noaa_weather_data AS
    SELECT "WeatherNOAA".datetime, "WeatherNOAA".dry_bulb_farenheit, "WeatherNOAA".relative_humidity FROM "WeatherNOAA" WHERE ((("WeatherNOAA".dry_bulb_farenheit)::text <> 'M'::text) AND (("WeatherNOAA".relative_humidity)::text <> 'M'::text)) ORDER BY "WeatherNOAA".datetime;


ALTER TABLE public.az_noaa_weather_data OWNER TO eileen;

--
-- Name: cd_readings_channel_as_columns_by_service_point; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW cd_readings_channel_as_columns_by_service_point AS
    SELECT readings_by_meter_location_history_new_spid.service_point_id, max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "Energy to House kwH", max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (2)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "Energy from House kwH(rec)", max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (3)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "Net Energy to House KwH", max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "voltage at house", readings_by_meter_location_history_new_spid.end_time, max(readings_by_meter_location_history_new_spid.service_point_latitude) AS service_point_latitude, max(readings_by_meter_location_history_new_spid.service_point_longitude) AS service_point_longitude, max((readings_by_meter_location_history_new_spid.location)::text) AS "location_ID", max((readings_by_meter_location_history_new_spid.address)::text) AS address, max(readings_by_meter_location_history_new_spid.latitude) AS location_latitude, max(readings_by_meter_location_history_new_spid.longitude) AS location_longitude FROM readings_by_meter_location_history readings_by_meter_location_history_new_spid GROUP BY readings_by_meter_location_history_new_spid.service_point_id, readings_by_meter_location_history_new_spid.end_time;


ALTER TABLE public.cd_readings_channel_as_columns_by_service_point OWNER TO eileen;

--
-- Name: az_readings_channel_as_columns_by_spid; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW az_readings_channel_as_columns_by_spid AS
    SELECT cd_readings_channel_as_columns_by_service_point.service_point_id, cd_readings_channel_as_columns_by_service_point."Energy to House kwH", cd_readings_channel_as_columns_by_service_point."Energy from House kwH(rec)", cd_readings_channel_as_columns_by_service_point."Net Energy to House KwH", cd_readings_channel_as_columns_by_service_point."voltage at house", cd_readings_channel_as_columns_by_service_point.end_time, cd_readings_channel_as_columns_by_service_point.address FROM cd_readings_channel_as_columns_by_service_point WHERE ((cd_readings_channel_as_columns_by_service_point.service_point_id)::text = '98751'::text);


ALTER TABLE public.az_readings_channel_as_columns_by_spid OWNER TO eileen;

--
-- Name: readings_channel_as_columns_by_new_spid; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW readings_channel_as_columns_by_new_spid AS
    SELECT readings_by_meter_location_history_new_spid.service_point_id, max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "Energy to House kwH", max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (2)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "Energy from House kwH(rec)", max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (3)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "Net Energy to House KwH", max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "voltage at house", readings_by_meter_location_history_new_spid.end_time, max(readings_by_meter_location_history_new_spid.service_point_latitude) AS service_point_latitude, max(readings_by_meter_location_history_new_spid.service_point_longitude) AS service_point_longitude, max((readings_by_meter_location_history_new_spid.location)::text) AS "location_ID", max((readings_by_meter_location_history_new_spid.address)::text) AS address, max(readings_by_meter_location_history_new_spid.latitude) AS location_latitude, max(readings_by_meter_location_history_new_spid.longitude) AS location_longitude FROM readings_by_meter_location_history readings_by_meter_location_history_new_spid GROUP BY readings_by_meter_location_history_new_spid.service_point_id, readings_by_meter_location_history_new_spid.end_time;


ALTER TABLE public.readings_channel_as_columns_by_new_spid OWNER TO eileen;

--
-- Name: az_readings_channels_as_columns_new_spid; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW az_readings_channels_as_columns_new_spid AS
    SELECT readings_channel_as_columns_by_new_spid.service_point_id, readings_channel_as_columns_by_new_spid."Energy to House kwH", readings_channel_as_columns_by_new_spid."Energy from House kwH(rec)", readings_channel_as_columns_by_new_spid."Net Energy to House KwH", readings_channel_as_columns_by_new_spid."voltage at house", readings_channel_as_columns_by_new_spid.end_time, readings_channel_as_columns_by_new_spid.address FROM readings_channel_as_columns_by_new_spid;


ALTER TABLE public.az_readings_channels_as_columns_new_spid OWNER TO eileen;

--
-- Name: az_transformer_and_pumping_station; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW az_transformer_and_pumping_station AS
    SELECT i.sensor_id, i.irradiance_w_per_m2, td."timestamp", td.real_power_p, td.reactive_power_q, td.device_name FROM ("TransformerDataNREL" td JOIN "IrradianceData" i ON (((td."timestamp" = i."timestamp") AND (i.sensor_id = ANY (ARRAY[2])))));


ALTER TABLE public.az_transformer_and_pumping_station OWNER TO dave;

--
-- Name: az_transformer_only; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW az_transformer_only AS
    SELECT "TransformerDataNREL".real_power_p, "TransformerDataNREL".reactive_power_q, "TransformerDataNREL".device_name, "TransformerDataNREL"."timestamp" FROM "TransformerDataNREL";


ALTER TABLE public.az_transformer_only OWNER TO dave;

--
-- Name: cd_20130706-20130711; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW "cd_20130706-20130711" AS
    SELECT "TransformerData".transformer, "TransformerData"."timestamp", "TransformerData".vlt_a FROM "TransformerData" WHERE (("TransformerData"."timestamp" >= '2013-07-06 17:03:00'::timestamp without time zone) AND ("TransformerData"."timestamp" <= '2013-07-11 14:32:00'::timestamp without time zone));


ALTER TABLE public."cd_20130706-20130711" OWNER TO eileen;

--
-- Name: cd_20130709-20130710; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW "cd_20130709-20130710" AS
    SELECT "TransformerData".transformer, "TransformerData"."timestamp", "TransformerData".vlt_a FROM "TransformerData" WHERE (("TransformerData"."timestamp" >= '2013-07-07 17:00:00'::timestamp without time zone) AND ("TransformerData"."timestamp" <= '2013-07-10 17:00:00'::timestamp without time zone));


ALTER TABLE public."cd_20130709-20130710" OWNER TO eileen;

--
-- Name: cd_meter_ids_for_houses_with_pv_with_locations; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW cd_meter_ids_for_houses_with_pv_with_locations AS
    SELECT "LocationRecords".device_util_id, "LocationRecords".service_pt_longitude, "LocationRecords".service_pt_latitude, "LocationRecords".address1 FROM ("LocationRecords" LEFT JOIN "MSG_PV_Data" ON ((("LocationRecords".device_util_id)::text = ("MSG_PV_Data".util_device_id)::text))) WHERE ("MSG_PV_Data".util_device_id IS NOT NULL);


ALTER TABLE public.cd_meter_ids_for_houses_with_pv_with_locations OWNER TO eileen;

--
-- Name: cd_energy_voltages_for_houses_with_pv; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW cd_energy_voltages_for_houses_with_pv AS
    SELECT cd_meter_ids_for_houses_with_pv_with_locations.device_util_id, view_readings_with_meter_id_unsorted.end_time, max(CASE WHEN (view_readings_with_meter_id_unsorted.channel = (1)::smallint) THEN view_readings_with_meter_id_unsorted.value ELSE NULL::real END) AS "Energy to House kwH", zero_to_null(max(CASE WHEN (view_readings_with_meter_id_unsorted.channel = (4)::smallint) THEN view_readings_with_meter_id_unsorted.value ELSE NULL::real END)) AS "Voltage", max(cd_meter_ids_for_houses_with_pv_with_locations.service_pt_longitude) AS service_pt_longitude, max(cd_meter_ids_for_houses_with_pv_with_locations.service_pt_latitude) AS service_pt_latitude, max((cd_meter_ids_for_houses_with_pv_with_locations.address1)::text) AS address1 FROM (cd_meter_ids_for_houses_with_pv_with_locations JOIN readings_unfiltered view_readings_with_meter_id_unsorted ON (((cd_meter_ids_for_houses_with_pv_with_locations.device_util_id)::bpchar = view_readings_with_meter_id_unsorted.meter_name))) WHERE ((view_readings_with_meter_id_unsorted.channel = (1)::smallint) OR (view_readings_with_meter_id_unsorted.channel = (4)::smallint)) GROUP BY cd_meter_ids_for_houses_with_pv_with_locations.device_util_id, view_readings_with_meter_id_unsorted.end_time;


ALTER TABLE public.cd_energy_voltages_for_houses_with_pv OWNER TO postgres;

--
-- Name: cd_houses_with_pv_no_pv_meter; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW cd_houses_with_pv_no_pv_meter AS
    SELECT "PVServicePointIDs".old_pv_service_point_id AS pv_service_point_id, "PVServicePointIDs".old_house_service_point_id AS house_service_point_id, "PVServicePointIDs"."PV_Mod_size_kW", "PVServicePointIDs".inverter_model, "PVServicePointIDs"."size_kW", "PVServicePointIDs"."system_cap_kW", "PVServicePointIDs".bat, "PVServicePointIDs".sub, "PVServicePointIDs".circuit, "PVServicePointIDs".date_uploaded, "PVServicePointIDs".has_meter, "PVServicePointIDs".has_separate_pv_meter, "PVServicePointIDs"."add_cap_kW", "PVServicePointIDs".upgraded_total_kw, "PVServicePointIDs".street, "PVServicePointIDs".city, "PVServicePointIDs".state, "PVServicePointIDs".zip, "PVServicePointIDs".month_installed, "PVServicePointIDs".year_installed, "PVServicePointIDs".notes FROM "PVServicePointIDs" WHERE (("PVServicePointIDs".old_pv_service_point_id IS NULL) AND ("PVServicePointIDs".old_house_service_point_id IS NOT NULL));


ALTER TABLE public.cd_houses_with_pv_no_pv_meter OWNER TO eileen;

--
-- Name: cd_monthly_summary; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW cd_monthly_summary AS
    SELECT cd_readings_channel_as_columns_by_service_point.service_point_id, sum(cd_readings_channel_as_columns_by_service_point."Energy to House kwH") AS total_energy_to_house_kwh, sum(cd_readings_channel_as_columns_by_service_point."Energy from House kwH(rec)") AS total_energy_from_house_kwh, sum(cd_readings_channel_as_columns_by_service_point."Net Energy to House KwH") AS total_net_energy_kwh, avg(cd_readings_channel_as_columns_by_service_point."voltage at house") AS avg, date_trunc('month'::text, cd_readings_channel_as_columns_by_service_point.end_time) AS month, max(cd_readings_channel_as_columns_by_service_point.service_point_latitude) AS sp_latitude, max(cd_readings_channel_as_columns_by_service_point.service_point_longitude) AS sp_longtidue, max(cd_readings_channel_as_columns_by_service_point."location_ID") AS location_id, max(cd_readings_channel_as_columns_by_service_point.address) AS address, max(cd_readings_channel_as_columns_by_service_point.location_latitude) AS location_latitude, max(cd_readings_channel_as_columns_by_service_point.location_longitude) AS location_longitude, (((count(cd_readings_channel_as_columns_by_service_point.end_time))::double precision / (4)::double precision) / (24)::double precision) AS count_day FROM cd_readings_channel_as_columns_by_service_point GROUP BY cd_readings_channel_as_columns_by_service_point.service_point_id, date_trunc('month'::text, cd_readings_channel_as_columns_by_service_point.end_time);


ALTER TABLE public.cd_monthly_summary OWNER TO eileen;

--
-- Name: count_of_meters_not_in_mlh; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW count_of_meters_not_in_mlh AS
    SELECT abs(((SELECT count(DISTINCT "MeterData".meter_name) AS count FROM "MeterData") - (SELECT count(DISTINCT "MeterLocationHistory".meter_name) AS count FROM "MeterLocationHistory"))) AS meter_count_not_in_mlh;


ALTER TABLE public.count_of_meters_not_in_mlh OWNER TO postgres;

--
-- Name: VIEW count_of_meters_not_in_mlh; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW count_of_meters_not_in_mlh IS 'Counts all meters not in MLH. The result should be zero. @author Daniel Zhang (張道博)';


--
-- Name: readings_after_uninstall; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW readings_after_uninstall AS
    SELECT "MeterLocationHistory".meter_name, "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_latitude, "MeterLocationHistory".service_point_longitude, "MeterLocationHistory".location, "MeterLocationHistory".address, "MeterLocationHistory".latitude, "MeterLocationHistory".longitude, "MeterLocationHistory".installed, "MeterLocationHistory".uninstalled, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "Interval".end_time, "MeterData".meter_data_id FROM (((("MeterLocationHistory" JOIN "MeterData" ON ((("MeterLocationHistory".meter_name)::bpchar = "MeterData".meter_name))) JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON ((("Interval".interval_id = "Reading".interval_id) AND ("Interval".end_time >= "MeterLocationHistory".uninstalled))));


ALTER TABLE public.readings_after_uninstall OWNER TO postgres;

--
-- Name: VIEW readings_after_uninstall; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW readings_after_uninstall IS 'Readings that have been recorded after a meter''s uninstall date. @author Daniel Zhang (張道博)';


--
-- Name: readings_before_install; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW readings_before_install AS
    SELECT "MeterLocationHistory".meter_name, "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_latitude, "MeterLocationHistory".service_point_longitude, "MeterLocationHistory".location, "MeterLocationHistory".address, "MeterLocationHistory".latitude, "MeterLocationHistory".longitude, "MeterLocationHistory".installed, "MeterLocationHistory".uninstalled, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "Interval".end_time, "MeterData".meter_data_id FROM (((("MeterLocationHistory" JOIN "MeterData" ON ((("MeterLocationHistory".meter_name)::bpchar = "MeterData".meter_name))) JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON ((("Interval".interval_id = "Reading".interval_id) AND ("Interval".end_time < "MeterLocationHistory".installed))));


ALTER TABLE public.readings_before_install OWNER TO postgres;

--
-- Name: VIEW readings_before_install; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW readings_before_install IS 'Readings that have been recorded before a meter''s install date. @author Daniel Zhang (張道博)';


--
-- Name: count_of_non_mlh_readings; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW count_of_non_mlh_readings AS
    SELECT ((SELECT count(*) AS count FROM readings_before_install) + (SELECT count(*) AS count FROM readings_after_uninstall));


ALTER TABLE public.count_of_non_mlh_readings OWNER TO postgres;

--
-- Name: VIEW count_of_non_mlh_readings; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW count_of_non_mlh_readings IS 'Counts readings not in MLH. @author Daniel Zhang (張道博)';


--
-- Name: count_of_readings_and_meters_by_day; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW count_of_readings_and_meters_by_day AS
    SELECT date_trunc('day'::text, view_readings_with_meter_id_unsorted.end_time) AS "Day", count(view_readings_with_meter_id_unsorted.value) AS "Reading Count", count(DISTINCT view_readings_with_meter_id_unsorted.meter_name) AS "Meter Count", (count(view_readings_with_meter_id_unsorted.value) / count(DISTINCT view_readings_with_meter_id_unsorted.meter_name)) AS "Readings per Meter" FROM readings_unfiltered view_readings_with_meter_id_unsorted WHERE (view_readings_with_meter_id_unsorted.channel = 1) GROUP BY date_trunc('day'::text, view_readings_with_meter_id_unsorted.end_time) ORDER BY date_trunc('day'::text, view_readings_with_meter_id_unsorted.end_time);


ALTER TABLE public.count_of_readings_and_meters_by_day OWNER TO postgres;

--
-- Name: VIEW count_of_readings_and_meters_by_day; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW count_of_readings_and_meters_by_day IS 'Get counts of readings and meters per day. @author Daniel Zhang (張道博)';


--
-- Name: count_of_register_duplicates; Type: VIEW; Schema: public; Owner: daniel
--

CREATE VIEW count_of_register_duplicates AS
    SELECT "Register".number, "MeterData".meter_name, "RegisterRead".read_time, (count(*) - 1) AS "Duplicate Count" FROM (((("MeterData" JOIN "RegisterData" ON (("MeterData".meter_data_id = "RegisterData".meter_data_id))) JOIN "RegisterRead" ON (("RegisterData".register_data_id = "RegisterRead".register_data_id))) JOIN "Tier" ON (("RegisterRead".register_read_id = "Tier".register_read_id))) JOIN "Register" ON (("Tier".tier_id = "Register".tier_id))) GROUP BY "Register".number, "MeterData".meter_name, "RegisterRead".read_time HAVING ((count(*) - 1) > 0) ORDER BY "RegisterRead".read_time DESC, (count(*) - 1) DESC;


ALTER TABLE public.count_of_register_duplicates OWNER TO daniel;

--
-- Name: VIEW count_of_register_duplicates; Type: COMMENT; Schema: public; Owner: daniel
--

COMMENT ON VIEW count_of_register_duplicates IS 'Count of duplicates in the Register branch. @author Daniel Zhang (張道博)';


--
-- Name: dates_az_readings_channels_as_columns_new_spid; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW dates_az_readings_channels_as_columns_new_spid AS
    SELECT az_readings_channels_as_columns_new_spid.service_point_id, az_readings_channels_as_columns_new_spid.address, min(az_readings_channels_as_columns_new_spid.end_time) AS start, max(az_readings_channels_as_columns_new_spid.end_time) AS "end" FROM az_readings_channels_as_columns_new_spid GROUP BY az_readings_channels_as_columns_new_spid.service_point_id, az_readings_channels_as_columns_new_spid.address;


ALTER TABLE public.dates_az_readings_channels_as_columns_new_spid OWNER TO eileen;

--
-- Name: dates_egauge_energy_autoload; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW dates_egauge_energy_autoload AS
    SELECT "EgaugeEnergyAutoload".egauge_id, min("EgaugeEnergyAutoload".datetime) AS "E Start Date", max("EgaugeEnergyAutoload".datetime) AS "E Latest Date", ((count(*) / 60) / 24) AS "Days of Data" FROM "EgaugeEnergyAutoload" GROUP BY "EgaugeEnergyAutoload".egauge_id ORDER BY "EgaugeEnergyAutoload".egauge_id;


ALTER TABLE public.dates_egauge_energy_autoload OWNER TO eileen;

--
-- Name: dates_irradiance_data; Type: TABLE; Schema: public; Owner: eileen; Tablespace: 
--

CREATE TABLE dates_irradiance_data (
    sensor_id integer,
    latitude double precision,
    longitude double precision,
    count bigint,
    "Earliest Date" timestamp without time zone,
    "Latest Date" timestamp without time zone,
    name character varying
);


ALTER TABLE public.dates_irradiance_data OWNER TO eileen;

--
-- Name: dates_kihei_scada_temp_hum; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW dates_kihei_scada_temp_hum AS
    SELECT min("KiheiSCADATemperatureHumidity"."timestamp") AS "Earliest date", max("KiheiSCADATemperatureHumidity"."timestamp") AS "Latest date" FROM "KiheiSCADATemperatureHumidity";


ALTER TABLE public.dates_kihei_scada_temp_hum OWNER TO eileen;

--
-- Name: dates_meter_read_with_uninstall; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW dates_meter_read_with_uninstall AS
    SELECT DISTINCT "MeterData".util_device_id, min("Interval".end_time) AS earliest_date, max("IntervalReadData".end_time) AS latest_date, CASE WHEN (max("MeterLocationHistory".uninstalled) > max("MeterLocationHistory".installed)) THEN "MeterLocationHistory".uninstalled ELSE NULL::timestamp without time zone END AS "Max Uninstalled > Max Installed", CASE WHEN ((max("IntervalReadData".end_time) > max("MeterLocationHistory".uninstalled)) AND (NOT (max("MeterLocationHistory".uninstalled) > max("MeterLocationHistory".installed)))) THEN 'Problem.'::text ELSE NULL::text END AS "Max latest_date > Max Uninstalled" FROM ((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "MeterLocationHistory" ON (("MeterData".util_device_id = ("MeterLocationHistory".meter_name)::bpchar))) GROUP BY "MeterData".util_device_id, "MeterLocationHistory".uninstalled;


ALTER TABLE public.dates_meter_read_with_uninstall OWNER TO dave;

--
-- Name: dates_powermeterevents; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW dates_powermeterevents AS
    SELECT min("PowerMeterEvents".event_time) AS "First event in data", max("PowerMeterEvents".event_time) AS "Last event in data" FROM "PowerMeterEvents";


ALTER TABLE public.dates_powermeterevents OWNER TO eileen;

--
-- Name: dates_tap_data; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW dates_tap_data AS
    SELECT "TapData".substation, "TapData".transformer, min("TapData"."timestamp") AS "earliest date", max("TapData"."timestamp") AS "latest date" FROM "TapData" GROUP BY "TapData".substation, "TapData".transformer;


ALTER TABLE public.dates_tap_data OWNER TO eileen;

--
-- Name: dates_transformer_data; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW dates_transformer_data AS
    SELECT min("TransformerData"."timestamp") AS "earliest date", max("TransformerData"."timestamp") AS "latest date" FROM "TransformerData";


ALTER TABLE public.dates_transformer_data OWNER TO eileen;

--
-- Name: deprecated_meter_ids_for_houses_without_pv; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW deprecated_meter_ids_for_houses_without_pv AS
    SELECT "LocationRecords".device_util_id FROM ("LocationRecords" LEFT JOIN "MSG_PV_Data" ON ((("LocationRecords".device_util_id)::text = ("MSG_PV_Data".util_device_id)::text))) WHERE ("MSG_PV_Data".util_device_id IS NULL);


ALTER TABLE public.deprecated_meter_ids_for_houses_without_pv OWNER TO postgres;

--
-- Name: VIEW deprecated_meter_ids_for_houses_without_pv; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW deprecated_meter_ids_for_houses_without_pv IS 'Meter IDs for houses that do not have PV. @author Daniel Zhang (張道博)';


--
-- Name: z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero AS
    SELECT "_IrradianceFifteenMinIntervals".end_time, "_IrradianceFifteenMinIntervals".sensor_id, CASE WHEN ("AverageFifteenMinIrradianceData".irradiance_w_per_m2 IS NULL) THEN (0.0)::double precision ELSE "AverageFifteenMinIrradianceData".irradiance_w_per_m2 END AS irradiance_w_per_m2 FROM ("_IrradianceFifteenMinIntervals" LEFT JOIN "AverageFifteenMinIrradianceData" ON ((("_IrradianceFifteenMinIntervals".end_time = "AverageFifteenMinIrradianceData"."timestamp") AND ("_IrradianceFifteenMinIntervals".sensor_id = "AverageFifteenMinIrradianceData".sensor_id)))) WHERE (("_IrradianceFifteenMinIntervals".end_time >= (SELECT date_trunc('day'::text, min("AverageFifteenMinIrradianceData"."timestamp")) AS date_trunc FROM "AverageFifteenMinIrradianceData")) AND ("_IrradianceFifteenMinIntervals".end_time <= (SELECT date_trunc('day'::text, max("AverageFifteenMinIrradianceData"."timestamp")) AS date_trunc FROM "AverageFifteenMinIrradianceData"))) ORDER BY "_IrradianceFifteenMinIntervals".end_time, "_IrradianceFifteenMinIntervals".sensor_id;


ALTER TABLE public.z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero OWNER TO postgres;

--
-- Name: VIEW z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero IS 'Used internally for aggregating irradiance data. @author Daniel Zhang (張道博)';


--
-- Name: dz_count_of_fifteen_min_irradiance_intervals; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_count_of_fifteen_min_irradiance_intervals AS
    SELECT (count(*) / 4) AS cnt, date_trunc('day'::text, z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero.end_time) AS day FROM z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero GROUP BY date_trunc('day'::text, z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero.end_time);


ALTER TABLE public.dz_count_of_fifteen_min_irradiance_intervals OWNER TO postgres;

--
-- Name: dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero AS
    SELECT "_IrradianceFifteenMinIntervals".end_time, "_IrradianceFifteenMinIntervals".sensor_id, CASE WHEN ("AverageFifteenMinIrradianceData".irradiance_w_per_m2 IS NULL) THEN (0.0)::double precision ELSE "AverageFifteenMinIrradianceData".irradiance_w_per_m2 END AS irradiance_w_per_m2 FROM (("_IrradianceFifteenMinIntervals" LEFT JOIN "AverageFifteenMinIrradianceData" ON ((("_IrradianceFifteenMinIntervals".end_time = "AverageFifteenMinIrradianceData"."timestamp") AND ("_IrradianceFifteenMinIntervals".sensor_id = "AverageFifteenMinIrradianceData".sensor_id)))) JOIN dz_count_of_fifteen_min_irradiance_intervals ON (((date_trunc('day'::text, "_IrradianceFifteenMinIntervals".end_time) = dz_count_of_fifteen_min_irradiance_intervals.day) AND (dz_count_of_fifteen_min_irradiance_intervals.cnt = 96)))) WHERE (("_IrradianceFifteenMinIntervals".end_time >= (SELECT date_trunc('day'::text, min("AverageFifteenMinIrradianceData"."timestamp")) AS date_trunc FROM "AverageFifteenMinIrradianceData")) AND ("_IrradianceFifteenMinIntervals".end_time <= (SELECT date_trunc('day'::text, max("AverageFifteenMinIrradianceData"."timestamp")) AS date_trunc FROM "AverageFifteenMinIrradianceData"))) ORDER BY "_IrradianceFifteenMinIntervals".end_time, "_IrradianceFifteenMinIntervals".sensor_id;


ALTER TABLE public.dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero OWNER TO postgres;

--
-- Name: VIEW dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero IS 'Transformed irradiance data for use in analysis. @author Daniel Zhang (張道博)';


--
-- Name: dz_energy_voltages_for_houses_without_pv; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_energy_voltages_for_houses_without_pv AS
    SELECT readings_by_meter_location_history_new_spid.meter_name, readings_by_meter_location_history_new_spid.end_time, max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS "Energy to House kwH", zero_to_null(max(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END)) AS "Voltage", max(readings_by_meter_location_history_new_spid.service_point_longitude) AS service_pt_longitude, max(readings_by_meter_location_history_new_spid.service_point_latitude) AS service_pt_latitude, max((readings_by_meter_location_history_new_spid.address)::text) AS address FROM (deprecated_meter_ids_for_houses_without_pv meter_ids_for_houses_without_pv JOIN readings_by_meter_location_history readings_by_meter_location_history_new_spid ON (((meter_ids_for_houses_without_pv.device_util_id)::text = (readings_by_meter_location_history_new_spid.meter_name)::text))) WHERE ((readings_by_meter_location_history_new_spid.channel = (1)::smallint) OR (readings_by_meter_location_history_new_spid.channel = (4)::smallint)) GROUP BY readings_by_meter_location_history_new_spid.meter_name, readings_by_meter_location_history_new_spid.end_time;


ALTER TABLE public.dz_energy_voltages_for_houses_without_pv OWNER TO postgres;

--
-- Name: VIEW dz_energy_voltages_for_houses_without_pv; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_energy_voltages_for_houses_without_pv IS 'Energy and voltages for houses without PV limited by Meter Location History. @author Daniel Zhang (張道博)';


--
-- Name: dz_irradiance_fifteen_min_intervals_plus_one_year; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_irradiance_fifteen_min_intervals_plus_one_year AS
    SELECT ((SELECT (min("IrradianceData"."timestamp"))::date AS min FROM "IrradianceData") + ((n.n || ' minutes'::text))::interval) AS start_time, ((SELECT (min("IrradianceData"."timestamp"))::date AS min FROM "IrradianceData") + (((n.n + 15) || ' minutes'::text))::interval) AS end_time FROM generate_series(0, ((((SELECT ((max("IrradianceData"."timestamp"))::date - (min("IrradianceData"."timestamp"))::date) FROM "IrradianceData") + 366) * 24) * 60), 15) n(n);


ALTER TABLE public.dz_irradiance_fifteen_min_intervals_plus_one_year OWNER TO postgres;

--
-- Name: dz_monthly_energy_summary_double_pv_meter; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_monthly_energy_summary_double_pv_meter AS
    SELECT max((readings_by_meter_location_history_new_spid.service_point_id)::text) AS service_point_id, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_to_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (2)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_from_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (3)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_net_energy_kwh, avg(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS avg, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text) AS service_month, max(readings_by_meter_location_history_new_spid.service_point_latitude) AS sp_latitude, max(readings_by_meter_location_history_new_spid.service_point_longitude) AS sp_longitude, max((readings_by_meter_location_history_new_spid.location)::text) AS location_id, max((readings_by_meter_location_history_new_spid.address)::text) AS address, max(readings_by_meter_location_history_new_spid.latitude) AS location_latitude, max(readings_by_meter_location_history_new_spid.longitude) AS location_longitude, ((count(readings_by_meter_location_history_new_spid.end_time) / 4) / 24) AS count_day FROM (readings_by_meter_location_history readings_by_meter_location_history_new_spid JOIN "PVServicePointIDs" ON ((((readings_by_meter_location_history_new_spid.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text) OR ((readings_by_meter_location_history_new_spid.service_point_id)::text = ("PVServicePointIDs".old_pv_service_point_id)::text)))) WHERE ("PVServicePointIDs".old_pv_service_point_id IS NOT NULL) GROUP BY readings_by_meter_location_history_new_spid.service_point_id, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text);


ALTER TABLE public.dz_monthly_energy_summary_double_pv_meter OWNER TO postgres;

--
-- Name: VIEW dz_monthly_energy_summary_double_pv_meter; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_monthly_energy_summary_double_pv_meter IS 'Monthly energy summary for service points that have PV with a second PV meter. @author Daniel Zhang (張道博)';


--
-- Name: dz_monthly_energy_summary_for_nonpv_service_points; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_monthly_energy_summary_for_nonpv_service_points AS
    SELECT max((readings_by_meter_location_history_new_spid.service_point_id)::text) AS service_point_id, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_to_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (2)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_from_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (3)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_net_energy_kwh, avg(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS avg, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text) AS service_month, max(readings_by_meter_location_history_new_spid.service_point_latitude) AS sp_latitude, max(readings_by_meter_location_history_new_spid.service_point_longitude) AS sp_longitude, max((readings_by_meter_location_history_new_spid.location)::text) AS location_id, max((readings_by_meter_location_history_new_spid.address)::text) AS address, max(readings_by_meter_location_history_new_spid.latitude) AS location_latitude, max(readings_by_meter_location_history_new_spid.longitude) AS location_longitude, ((count(readings_by_meter_location_history_new_spid.end_time) / 4) / 24) AS count_day FROM (readings_by_meter_location_history readings_by_meter_location_history_new_spid JOIN nonpv_service_point_ids nonpv_service_point_ids_v2 ON (((readings_by_meter_location_history_new_spid.service_point_id)::text = (nonpv_service_point_ids_v2.service_point_id)::text))) GROUP BY readings_by_meter_location_history_new_spid.service_point_id, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text);


ALTER TABLE public.dz_monthly_energy_summary_for_nonpv_service_points OWNER TO postgres;

--
-- Name: VIEW dz_monthly_energy_summary_for_nonpv_service_points; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_monthly_energy_summary_for_nonpv_service_points IS 'Monthly energy summary for Non-PV service points. @author Daniel Zhang (張道博)';


--
-- Name: dz_monthly_energy_summary_single_pv_meter; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_monthly_energy_summary_single_pv_meter AS
    SELECT max((readings_by_meter_location_history_new_spid.service_point_id)::text) AS service_point_id, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_to_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (2)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_from_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (3)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_net_energy_kwh, avg(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS avg, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text) AS service_month, max(readings_by_meter_location_history_new_spid.service_point_latitude) AS sp_latitude, max(readings_by_meter_location_history_new_spid.service_point_longitude) AS sp_longitude, max((readings_by_meter_location_history_new_spid.location)::text) AS location_id, max((readings_by_meter_location_history_new_spid.address)::text) AS address, max(readings_by_meter_location_history_new_spid.latitude) AS location_latitude, max(readings_by_meter_location_history_new_spid.longitude) AS location_longitude, ((count(readings_by_meter_location_history_new_spid.end_time) / 4) / 24) AS count_day FROM (readings_by_meter_location_history readings_by_meter_location_history_new_spid JOIN "PVServicePointIDs" ON (((readings_by_meter_location_history_new_spid.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text))) WHERE ("PVServicePointIDs".old_pv_service_point_id IS NULL) GROUP BY readings_by_meter_location_history_new_spid.service_point_id, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text);


ALTER TABLE public.dz_monthly_energy_summary_single_pv_meter OWNER TO postgres;

--
-- Name: VIEW dz_monthly_energy_summary_single_pv_meter; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_monthly_energy_summary_single_pv_meter IS 'Monthly energy summary for service points that have PV but NO second PV meter. @author Daniel Zhang (張道博)';


--
-- Name: dz_nonpv_addresses_service_points; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_nonpv_addresses_service_points AS
    SELECT DISTINCT mlh.service_point_id, mlh.address, mlh.uninstalled, mlh.installed FROM "MeterLocationHistory" mlh WHERE ((mlh.uninstalled IS NULL) AND (NOT (EXISTS (SELECT "PVServicePointIDs".pv_service_point_id FROM "PVServicePointIDs" WHERE ((("PVServicePointIDs".pv_service_point_id)::text = (mlh.service_point_id)::text) OR (("PVServicePointIDs".house_service_point_id)::text = (mlh.service_point_id)::text))))));


ALTER TABLE public.dz_nonpv_addresses_service_points OWNER TO postgres;

--
-- Name: nonpv_mlh; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW nonpv_mlh AS
    SELECT "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_height, "MeterLocationHistory".service_point_latitude, "MeterLocationHistory".service_point_longitude, "MeterLocationHistory".notes, "MeterLocationHistory".longitude, "MeterLocationHistory".latitude, "MeterLocationHistory".city, "MeterLocationHistory".address, "MeterLocationHistory".location, "MeterLocationHistory".uninstalled, "MeterLocationHistory".installed, "MeterLocationHistory".mac_address, "MeterLocationHistory".meter_name FROM "MeterLocationHistory" WHERE (NOT (EXISTS (SELECT "PVServicePointIDs".pv_service_point_id FROM "PVServicePointIDs" WHERE (("PVServicePointIDs".pv_service_point_id)::text = ("MeterLocationHistory".service_point_id)::text))));


ALTER TABLE public.nonpv_mlh OWNER TO postgres;

--
-- Name: VIEW nonpv_mlh; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW nonpv_mlh IS 'This is the Meter Location History for nonPV service points. @author Daniel Zhang (張道博)';


--
-- Name: dz_pv_interval_ids; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_pv_interval_ids AS
    SELECT readings_unfiltered.interval_id, readings_unfiltered.value, readings_unfiltered.channel, readings_unfiltered.end_time, readings_unfiltered.meter_name FROM (nonpv_mlh JOIN readings_unfiltered ON (((nonpv_mlh.meter_name)::bpchar = readings_unfiltered.meter_name))) WHERE ((readings_unfiltered.channel = 2::smallint) AND (readings_unfiltered.value > 0::real));


ALTER TABLE public.dz_pv_interval_ids OWNER TO postgres;

--
-- Name: VIEW dz_pv_interval_ids; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_pv_interval_ids IS 'Provides interval IDs for readings where channel 2 has energy > 0.0. @author Daniel Zhang (張道博)';


--
-- Name: dz_pv_readings_in_nonpv_mlh; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_pv_readings_in_nonpv_mlh AS
    SELECT nonpv_mlh.service_point_id, readings_unfiltered.end_time, readings_unfiltered.meter_name, readings_unfiltered.channel, readings_unfiltered.raw_value, readings_unfiltered.value, readings_unfiltered.uom, readings_unfiltered.start_time, readings_unfiltered.ird_end_time, readings_unfiltered.meter_data_id, readings_unfiltered.interval_id FROM ((dz_pv_interval_ids JOIN readings_unfiltered ON ((dz_pv_interval_ids.interval_id = readings_unfiltered.interval_id))) JOIN nonpv_mlh ON ((dz_pv_interval_ids.meter_name = (nonpv_mlh.meter_name)::bpchar)));


ALTER TABLE public.dz_pv_readings_in_nonpv_mlh OWNER TO postgres;

--
-- Name: VIEW dz_pv_readings_in_nonpv_mlh; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_pv_readings_in_nonpv_mlh IS 'A report of readings that are in the MLH but do not have PV service points IDs. @author Daniel Zhang (張道博)';


--
-- Name: dz_summary_pv_readings_in_nonpv_mlh; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW dz_summary_pv_readings_in_nonpv_mlh AS
    SELECT dz_pv_readings_in_nonpv_mlh.meter_name, dz_pv_readings_in_nonpv_mlh.service_point_id, min(dz_pv_readings_in_nonpv_mlh.end_time) AS first_reading_time, max(dz_pv_readings_in_nonpv_mlh.end_time) AS last_reading_time FROM dz_pv_readings_in_nonpv_mlh GROUP BY dz_pv_readings_in_nonpv_mlh.meter_name, dz_pv_readings_in_nonpv_mlh.service_point_id;


ALTER TABLE public.dz_summary_pv_readings_in_nonpv_mlh OWNER TO postgres;

--
-- Name: VIEW dz_summary_pv_readings_in_nonpv_mlh; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW dz_summary_pv_readings_in_nonpv_mlh IS 'Summary of service points and meters in the MLH that have PV readings but do not have PV Service Point IDs. @author Daniel Zhang (張道博)';


--
-- Name: egauge_15min_find_outliers; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW egauge_15min_find_outliers AS
    SELECT "AverageFifteenMinEgaugeEnergyAutoload".egauge_id, "AverageFifteenMinEgaugeEnergyAutoload".datetime, "AverageFifteenMinEgaugeEnergyAutoload".use_kw, "AverageFifteenMinEgaugeEnergyAutoload".gen_kw, "AverageFifteenMinEgaugeEnergyAutoload".ac_kw, "AverageFifteenMinEgaugeEnergyAutoload".addition_kw, "AverageFifteenMinEgaugeEnergyAutoload".clotheswasher_kw, "AverageFifteenMinEgaugeEnergyAutoload".dhw_load_control, "AverageFifteenMinEgaugeEnergyAutoload".dryer_kw, "AverageFifteenMinEgaugeEnergyAutoload".garage_ac_kw, "AverageFifteenMinEgaugeEnergyAutoload".large_ac_kw, "AverageFifteenMinEgaugeEnergyAutoload".oven_and_microwave_kw, "AverageFifteenMinEgaugeEnergyAutoload".oven_kw, "AverageFifteenMinEgaugeEnergyAutoload".range_kw, "AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw, "AverageFifteenMinEgaugeEnergyAutoload".stove_kw, "AverageFifteenMinEgaugeEnergyAutoload".shop_kw, "AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw FROM "AverageFifteenMinEgaugeEnergyAutoload" WHERE (((((((((((((((("AverageFifteenMinEgaugeEnergyAutoload".use_kw > (20)::double precision) OR ("AverageFifteenMinEgaugeEnergyAutoload".gen_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".ac_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".addition_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".clotheswasher_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".dhw_load_control > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".dryer_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".garage_ac_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".large_ac_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".oven_and_microwave_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".oven_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".range_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".stove_kw > (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".shop_kw > (10)::double precision));


ALTER TABLE public.egauge_15min_find_outliers OWNER TO eileen;

--
-- Name: egauge_energy_15min_with_filter_for_outliers; Type: VIEW; Schema: public; Owner: sepgroup
--

CREATE VIEW egauge_energy_15min_with_filter_for_outliers AS
    SELECT "AverageFifteenMinEgaugeEnergyAutoload".egauge_id, "AverageFifteenMinEgaugeEnergyAutoload".datetime, "AverageFifteenMinEgaugeEnergyAutoload".use_kw AS use_kw_whole_house, "AverageFifteenMinEgaugeEnergyAutoload".ac_kw, "AverageFifteenMinEgaugeEnergyAutoload".addition_kw, "AverageFifteenMinEgaugeEnergyAutoload".clotheswasher_kw, "AverageFifteenMinEgaugeEnergyAutoload".dhw_load_control, "AverageFifteenMinEgaugeEnergyAutoload".dryer_kw, "AverageFifteenMinEgaugeEnergyAutoload".garage_ac_kw, "AverageFifteenMinEgaugeEnergyAutoload".gen_kw, "AverageFifteenMinEgaugeEnergyAutoload".large_ac_kw, "AverageFifteenMinEgaugeEnergyAutoload".oven_and_microwave_kw, "AverageFifteenMinEgaugeEnergyAutoload".oven_kw, "AverageFifteenMinEgaugeEnergyAutoload".range_kw, CASE WHEN ((("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw > (10)::double precision)) AND (("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw > (10)::double precision))) THEN NULL::double precision WHEN ((("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw > (10)::double precision)) AND (("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw <= (10)::double precision))) THEN "AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw ELSE "AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw END AS refrigerator_kw, "AverageFifteenMinEgaugeEnergyAutoload".shop_kw, "AverageFifteenMinEgaugeEnergyAutoload".stove_kw FROM "AverageFifteenMinEgaugeEnergyAutoload" WHERE ((((((((((((((("AverageFifteenMinEgaugeEnergyAutoload".use_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".use_kw < (20)::double precision)) AND (("AverageFifteenMinEgaugeEnergyAutoload".ac_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".ac_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".addition_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".addition_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".clotheswasher_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".clotheswasher_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".dhw_load_control IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".dhw_load_control < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".dryer_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".dryer_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".garage_ac_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".garage_ac_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".large_ac_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".large_ac_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".oven_and_microwave_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".oven_and_microwave_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".oven_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".oven_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".range_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".range_kw < (10)::double precision))) AND (((("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_kw < (10)::double precision)) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw IS NULL)) OR ("AverageFifteenMinEgaugeEnergyAutoload".refrigerator_usage_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".shop_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".shop_kw < (10)::double precision))) AND (("AverageFifteenMinEgaugeEnergyAutoload".shop_kw IS NULL) OR ("AverageFifteenMinEgaugeEnergyAutoload".shop_kw < (10)::double precision)));


ALTER TABLE public.egauge_energy_15min_with_filter_for_outliers OWNER TO sepgroup;

--
-- Name: egauge_energy_autoload_dates; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW egauge_energy_autoload_dates AS
    SELECT "EgaugeEnergyAutoload".egauge_id, min("EgaugeEnergyAutoload".datetime) AS "E Start Date", max("EgaugeEnergyAutoload".datetime) AS "E Latest Date", ((count(*) / 60) / 24) AS "Days of Data" FROM "EgaugeEnergyAutoload" GROUP BY "EgaugeEnergyAutoload".egauge_id ORDER BY "EgaugeEnergyAutoload".egauge_id;


ALTER TABLE public.egauge_energy_autoload_dates OWNER TO postgres;

--
-- Name: VIEW egauge_energy_autoload_dates; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW egauge_energy_autoload_dates IS 'Used by the MSG eGauge Service. @author Daniel Zhang (張道博)';


--
-- Name: egauge_energy_autoload_with_outlier_filter; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW egauge_energy_autoload_with_outlier_filter AS
    SELECT "EgaugeEnergyAutoload".egauge_id, "EgaugeEnergyAutoload".datetime, "EgaugeEnergyAutoload".use_kw AS use_kw_whole_house, "EgaugeEnergyAutoload".ac_kw, "EgaugeEnergyAutoload".addition_kw, "EgaugeEnergyAutoload".clotheswasher_kw, "EgaugeEnergyAutoload".dhw_load_control, "EgaugeEnergyAutoload".dryer_kw, "EgaugeEnergyAutoload".garage_ac_kw, "EgaugeEnergyAutoload".gen_kw, "EgaugeEnergyAutoload".large_ac_kw, "EgaugeEnergyAutoload".oven_and_microwave_kw, "EgaugeEnergyAutoload".oven_kw, "EgaugeEnergyAutoload".range_kw, CASE WHEN ((("EgaugeEnergyAutoload".refrigerator_kw IS NULL) OR ("EgaugeEnergyAutoload".refrigerator_kw > (10)::double precision)) AND (("EgaugeEnergyAutoload".refrigerator_usage_kw IS NULL) OR ("EgaugeEnergyAutoload".refrigerator_usage_kw > (10)::double precision))) THEN NULL::double precision WHEN ((("EgaugeEnergyAutoload".refrigerator_kw IS NULL) OR ("EgaugeEnergyAutoload".refrigerator_kw > (10)::double precision)) AND (("EgaugeEnergyAutoload".refrigerator_usage_kw IS NULL) OR ("EgaugeEnergyAutoload".refrigerator_usage_kw <= (10)::double precision))) THEN "EgaugeEnergyAutoload".refrigerator_usage_kw ELSE "EgaugeEnergyAutoload".refrigerator_kw END AS refrigerator_kw, "EgaugeEnergyAutoload".shop_kw, "EgaugeEnergyAutoload".stove_kw FROM "EgaugeEnergyAutoload" WHERE ((((((((((((((("EgaugeEnergyAutoload".use_kw IS NULL) OR ("EgaugeEnergyAutoload".use_kw < (20)::double precision)) AND (("EgaugeEnergyAutoload".ac_kw IS NULL) OR ("EgaugeEnergyAutoload".ac_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".addition_kw IS NULL) OR ("EgaugeEnergyAutoload".addition_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".clotheswasher_kw IS NULL) OR ("EgaugeEnergyAutoload".clotheswasher_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".dhw_load_control IS NULL) OR ("EgaugeEnergyAutoload".dhw_load_control < (10)::double precision))) AND (("EgaugeEnergyAutoload".dryer_kw IS NULL) OR ("EgaugeEnergyAutoload".dryer_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".garage_ac_kw IS NULL) OR ("EgaugeEnergyAutoload".garage_ac_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".large_ac_kw IS NULL) OR ("EgaugeEnergyAutoload".large_ac_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".oven_and_microwave_kw IS NULL) OR ("EgaugeEnergyAutoload".oven_and_microwave_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".oven_kw IS NULL) OR ("EgaugeEnergyAutoload".oven_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".range_kw IS NULL) OR ("EgaugeEnergyAutoload".range_kw < (10)::double precision))) AND (((("EgaugeEnergyAutoload".refrigerator_kw IS NULL) OR ("EgaugeEnergyAutoload".refrigerator_kw < (10)::double precision)) OR ("EgaugeEnergyAutoload".refrigerator_usage_kw IS NULL)) OR ("EgaugeEnergyAutoload".refrigerator_usage_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".shop_kw IS NULL) OR ("EgaugeEnergyAutoload".shop_kw < (10)::double precision))) AND (("EgaugeEnergyAutoload".shop_kw IS NULL) OR ("EgaugeEnergyAutoload".shop_kw < (10)::double precision)));


ALTER TABLE public.egauge_energy_autoload_with_outlier_filter OWNER TO dave;

--
-- Name: egauge_view; Type: VIEW; Schema: public; Owner: sepgroup
--

CREATE VIEW egauge_view AS
    SELECT "EgaugeEnergyAutoload".egauge_id, "EgaugeEnergyAutoload".use_kw AS "use_kw whole house", "EgaugeEnergyAutoload".datetime, "EgaugeEnergyAutoload".ac_kw, "EgaugeEnergyAutoload".addition_kw, "EgaugeEnergyAutoload".clotheswasher_kw, "EgaugeEnergyAutoload".dhw_load_control, "EgaugeEnergyAutoload".dryer_kw, "EgaugeEnergyAutoload".garage_ac_kw, "EgaugeEnergyAutoload".gen_kw, "EgaugeEnergyAutoload".large_ac_kw, "EgaugeEnergyAutoload".oven_and_microwave_kw, "EgaugeEnergyAutoload".oven_kw, "EgaugeEnergyAutoload".range_kw, "EgaugeEnergyAutoload".refrigerator_usage_kw, "EgaugeEnergyAutoload".shop_kw, "EgaugeEnergyAutoload".stove_kw FROM "EgaugeEnergyAutoload" WHERE ((((((((((((((("EgaugeEnergyAutoload".use_kw < (20)::double precision) AND ("EgaugeEnergyAutoload".ac_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".addition_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".clotheswasher_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".dhw_load_control < (10)::double precision)) AND ("EgaugeEnergyAutoload".dryer_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".garage_ac_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".gen_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".large_ac_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".oven_and_microwave_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".oven_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".range_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".refrigerator_usage_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".shop_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".stove_kw < (10)::double precision));


ALTER TABLE public.egauge_view OWNER TO sepgroup;

--
-- Name: egauge_view_since_aug1; Type: VIEW; Schema: public; Owner: sepgroup
--

CREATE VIEW egauge_view_since_aug1 AS
    SELECT "EgaugeEnergyAutoload".egauge_id, "EgaugeEnergyAutoload".use_kw AS "use_kw whole house", "EgaugeEnergyAutoload".datetime, "EgaugeEnergyAutoload".ac_kw, "EgaugeEnergyAutoload".addition_kw, "EgaugeEnergyAutoload".clotheswasher_kw, "EgaugeEnergyAutoload".dhw_load_control, "EgaugeEnergyAutoload".dryer_kw, "EgaugeEnergyAutoload".garage_ac_kw, "EgaugeEnergyAutoload".gen_kw, "EgaugeEnergyAutoload".large_ac_kw, "EgaugeEnergyAutoload".oven_and_microwave_kw, "EgaugeEnergyAutoload".oven_kw, "EgaugeEnergyAutoload".range_kw, "EgaugeEnergyAutoload".refrigerator_usage_kw, "EgaugeEnergyAutoload".shop_kw, "EgaugeEnergyAutoload".stove_kw FROM "EgaugeEnergyAutoload" WHERE (((((((((((((((("EgaugeEnergyAutoload".use_kw < (20)::double precision) AND ("EgaugeEnergyAutoload".ac_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".addition_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".clotheswasher_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".dhw_load_control < (10)::double precision)) AND ("EgaugeEnergyAutoload".dryer_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".garage_ac_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".gen_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".large_ac_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".oven_and_microwave_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".oven_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".range_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".refrigerator_usage_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".shop_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".stove_kw < (10)::double precision)) AND ("EgaugeEnergyAutoload".datetime > '2014-08-01 00:00:00'::timestamp without time zone));


ALTER TABLE public.egauge_view_since_aug1 OWNER TO sepgroup;

--
-- Name: event_data_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE event_data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.event_data_id_seq OWNER TO sepgroup;

--
-- Name: event_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE event_data_id_seq OWNED BY "EventData".event_data_id;


--
-- Name: event_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.event_id_seq OWNER TO sepgroup;

--
-- Name: event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE event_id_seq OWNED BY "Event".event_id;


--
-- Name: event_table_view; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW event_table_view AS
    SELECT DISTINCT "Event".event_name, "Event".event_time, "Event".event_text, "Event".event_data_id, "Event".event_id FROM "Event";


ALTER TABLE public.event_table_view OWNER TO eileen;

--
-- Name: interval_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE interval_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.interval_id_seq OWNER TO sepgroup;

--
-- Name: interval_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE interval_id_seq OWNED BY "Interval".interval_id;


--
-- Name: intervalreaddata_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE intervalreaddata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.intervalreaddata_id_seq OWNER TO sepgroup;

--
-- Name: intervalreaddata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE intervalreaddata_id_seq OWNED BY "IntervalReadData".interval_read_data_id;


--
-- Name: irradiance_data; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW irradiance_data AS
    SELECT "IrradianceData".irradiance_w_per_m2, "IrradianceData".sensor_id, "IrradianceData"."timestamp", "IrradianceSensorInfo".latitude, "IrradianceSensorInfo".longitude, "IrradianceSensorInfo".name FROM ("IrradianceData" JOIN "IrradianceSensorInfo" ON (("IrradianceData".sensor_id = "IrradianceSensorInfo".sensor_id))) WHERE ("IrradianceData".irradiance_w_per_m2 > (0)::double precision);


ALTER TABLE public.irradiance_data OWNER TO eileen;

--
-- Name: locations_with_pv_service_points_ids; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW locations_with_pv_service_points_ids AS
    SELECT DISTINCT "MeterLocationHistory".location FROM ("PVServicePointIDs" JOIN "MeterLocationHistory" ON ((("PVServicePointIDs".old_pv_service_point_id)::text = ("MeterLocationHistory".old_service_point_id)::text)));


ALTER TABLE public.locations_with_pv_service_points_ids OWNER TO postgres;

--
-- Name: nonpv_mlh_v2; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW nonpv_mlh_v2 AS
    SELECT "MeterLocationHistory".service_point_id, "MeterLocationHistory".service_point_height, "MeterLocationHistory".service_point_latitude, "MeterLocationHistory".service_point_longitude, "MeterLocationHistory".notes, "MeterLocationHistory".longitude, "MeterLocationHistory".latitude, "MeterLocationHistory".city, "MeterLocationHistory".address, "MeterLocationHistory".location, "MeterLocationHistory".uninstalled, "MeterLocationHistory".installed, "MeterLocationHistory".mac_address, "MeterLocationHistory".meter_name FROM "MeterLocationHistory" WHERE (NOT (EXISTS (SELECT "PVServicePointIDs".pv_service_point_id FROM "PVServicePointIDs" WHERE ((("PVServicePointIDs".pv_service_point_id)::text = ("MeterLocationHistory".service_point_id)::text) OR (("PVServicePointIDs".house_service_point_id)::text = ("MeterLocationHistory".service_point_id)::text)))));


ALTER TABLE public.nonpv_mlh_v2 OWNER TO postgres;

--
-- Name: VIEW nonpv_mlh_v2; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW nonpv_mlh_v2 IS 'This is the Meter Location History for nonPV service points. @author Daniel Zhang (張道博)';


--
-- Name: meter_ids_for_service_points_without_pv; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW meter_ids_for_service_points_without_pv AS
    SELECT nonpv_mlh_v2.meter_name, nonpv_mlh_v2.uninstalled, nonpv_mlh_v2.installed FROM nonpv_mlh_v2;


ALTER TABLE public.meter_ids_for_service_points_without_pv OWNER TO postgres;

--
-- Name: VIEW meter_ids_for_service_points_without_pv; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW meter_ids_for_service_points_without_pv IS 'These are the nonPV meters. @author Daniel Zhang (張道博)';


--
-- Name: meterdata_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE meterdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meterdata_id_seq OWNER TO sepgroup;

--
-- Name: meterdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE meterdata_id_seq OWNED BY "MeterData".meter_data_id;


--
-- Name: monthly_energy_summary_all_meters; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW monthly_energy_summary_all_meters AS
    SELECT cd_readings_channel_as_columns_by_service_point.service_point_id, sum(cd_readings_channel_as_columns_by_service_point."Energy to House kwH") AS total_energy_to_house_kwh, sum(cd_readings_channel_as_columns_by_service_point."Energy from House kwH(rec)") AS total_energy_from_house_kwh, sum(cd_readings_channel_as_columns_by_service_point."Net Energy to House KwH") AS total_net_energy_kwh, avg(cd_readings_channel_as_columns_by_service_point."voltage at house") AS "avg voltage", date_trunc('month'::text, cd_readings_channel_as_columns_by_service_point.end_time) AS month, max(cd_readings_channel_as_columns_by_service_point.service_point_latitude) AS sp_latitude, max(cd_readings_channel_as_columns_by_service_point.service_point_longitude) AS sp_longtidue, max(cd_readings_channel_as_columns_by_service_point."location_ID") AS location_id, max(cd_readings_channel_as_columns_by_service_point.address) AS address, max(cd_readings_channel_as_columns_by_service_point.location_latitude) AS location_latitude, max(cd_readings_channel_as_columns_by_service_point.location_longitude) AS location_longitude, (((count(cd_readings_channel_as_columns_by_service_point.end_time))::double precision / (4)::double precision) / (24)::double precision) AS count_day FROM cd_readings_channel_as_columns_by_service_point GROUP BY cd_readings_channel_as_columns_by_service_point.service_point_id, date_trunc('month'::text, cd_readings_channel_as_columns_by_service_point.end_time);


ALTER TABLE public.monthly_energy_summary_all_meters OWNER TO eileen;

--
-- Name: readings_by_meter_location_history_old_program; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW readings_by_meter_location_history_old_program AS
    SELECT readings_by_meter_location_history.meter_name, readings_by_meter_location_history.service_point_id, readings_by_meter_location_history.service_point_latitude, readings_by_meter_location_history.service_point_longitude, readings_by_meter_location_history.location, readings_by_meter_location_history.address, readings_by_meter_location_history.latitude, readings_by_meter_location_history.longitude, readings_by_meter_location_history.installed, readings_by_meter_location_history.uninstalled, readings_by_meter_location_history.channel, readings_by_meter_location_history.raw_value, readings_by_meter_location_history.value, readings_by_meter_location_history.uom, readings_by_meter_location_history.end_time, readings_by_meter_location_history.meter_data_id FROM (readings_by_meter_location_history JOIN "MeterProgramChanges" ON ((("MeterProgramChanges".meter_name)::text = (readings_by_meter_location_history.meter_name)::text))) WHERE (NOT (((readings_by_meter_location_history.meter_name)::text IN (SELECT DISTINCT "MeterProgramChanges".meter_name FROM "MeterProgramChanges")) AND (readings_by_meter_location_history.end_time > "MeterProgramChanges".date_changed)));


ALTER TABLE public.readings_by_meter_location_history_old_program OWNER TO dave;

--
-- Name: monthly_energy_summary_double_pv_meter; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW monthly_energy_summary_double_pv_meter AS
    SELECT max((readings_by_meter_location_history.service_point_id)::text) AS service_point_id, sum(CASE WHEN (readings_by_meter_location_history.channel = (1)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS total_energy_to_house_kwh, sum(CASE WHEN (readings_by_meter_location_history.channel = (2)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS total_energy_from_house_kwh, sum(CASE WHEN (readings_by_meter_location_history.channel = (3)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS total_net_energy_kwh, avg(CASE WHEN (readings_by_meter_location_history.channel = (4)::smallint) THEN readings_by_meter_location_history.value ELSE NULL::real END) AS avg, to_char(date_trunc('month'::text, readings_by_meter_location_history.end_time), 'yyyy-mm'::text) AS service_month, max(readings_by_meter_location_history.service_point_latitude) AS sp_latitude, max(readings_by_meter_location_history.service_point_longitude) AS sp_longitude, max((readings_by_meter_location_history.location)::text) AS location_id, max((readings_by_meter_location_history.address)::text) AS address, max(readings_by_meter_location_history.latitude) AS location_latitude, max(readings_by_meter_location_history.longitude) AS location_longitude, ((count(readings_by_meter_location_history.end_time) / 4) / 24) AS count_day FROM (readings_by_meter_location_history_old_program readings_by_meter_location_history JOIN "PVServicePointIDs" ON ((((readings_by_meter_location_history.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text) OR ((readings_by_meter_location_history.service_point_id)::text = ("PVServicePointIDs".old_pv_service_point_id)::text)))) WHERE ("PVServicePointIDs".old_pv_service_point_id IS NOT NULL) GROUP BY readings_by_meter_location_history.service_point_id, to_char(date_trunc('month'::text, readings_by_meter_location_history.end_time), 'yyyy-mm'::text);


ALTER TABLE public.monthly_energy_summary_double_pv_meter OWNER TO dave;

--
-- Name: readings_by_meter_location_history_new_program; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW readings_by_meter_location_history_new_program AS
    SELECT readings_by_meter_location_history.meter_name, readings_by_meter_location_history.service_point_id, readings_by_meter_location_history.service_point_latitude, readings_by_meter_location_history.service_point_longitude, readings_by_meter_location_history.location, readings_by_meter_location_history.address, readings_by_meter_location_history.latitude, readings_by_meter_location_history.longitude, readings_by_meter_location_history.installed, readings_by_meter_location_history.uninstalled, readings_by_meter_location_history.channel, readings_by_meter_location_history.raw_value, readings_by_meter_location_history.value, readings_by_meter_location_history.uom, readings_by_meter_location_history.end_time, readings_by_meter_location_history.meter_data_id FROM (readings_by_meter_location_history JOIN "MeterProgramChanges" ON ((("MeterProgramChanges".meter_name)::text = (readings_by_meter_location_history.meter_name)::text))) WHERE (NOT (((readings_by_meter_location_history.meter_name)::text IN (SELECT DISTINCT "MeterProgramChanges".meter_name FROM "MeterProgramChanges")) AND (readings_by_meter_location_history.end_time < "MeterProgramChanges".date_changed)));


ALTER TABLE public.readings_by_meter_location_history_new_program OWNER TO dave;

--
-- Name: monthly_energy_summary_double_pv_meter_program_2; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW monthly_energy_summary_double_pv_meter_program_2 AS
    SELECT max((readings_by_meter_location_history_new_program.service_point_id)::text) AS service_point_id, sum(CASE WHEN (readings_by_meter_location_history_new_program.channel = (1)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS max_voltage, sum(CASE WHEN (readings_by_meter_location_history_new_program.channel = (2)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS energy_delivered_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_program.channel = (3)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS avg_voltage, avg(CASE WHEN (readings_by_meter_location_history_new_program.channel = (4)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS min_voltage, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_program.end_time), 'yyyy-mm'::text) AS service_month, max(readings_by_meter_location_history_new_program.service_point_latitude) AS sp_latitude, max(readings_by_meter_location_history_new_program.service_point_longitude) AS sp_longitude, max((readings_by_meter_location_history_new_program.location)::text) AS location_id, max((readings_by_meter_location_history_new_program.address)::text) AS address, max(readings_by_meter_location_history_new_program.latitude) AS location_latitude, max(readings_by_meter_location_history_new_program.longitude) AS location_longitude, ((count(readings_by_meter_location_history_new_program.end_time) / 4) / 24) AS count_day FROM (readings_by_meter_location_history_new_program JOIN "PVServicePointIDs" ON ((((readings_by_meter_location_history_new_program.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text) OR ((readings_by_meter_location_history_new_program.service_point_id)::text = ("PVServicePointIDs".old_pv_service_point_id)::text)))) WHERE ("PVServicePointIDs".old_pv_service_point_id IS NOT NULL) GROUP BY readings_by_meter_location_history_new_program.service_point_id, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_program.end_time), 'yyyy-mm'::text);


ALTER TABLE public.monthly_energy_summary_double_pv_meter_program_2 OWNER TO dave;

--
-- Name: monthly_energy_summary_houses_with_pv; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW monthly_energy_summary_houses_with_pv AS
    SELECT cd_readings_channel_as_columns_by_service_point.service_point_id, sum(cd_readings_channel_as_columns_by_service_point."Energy to House kwH") AS total_energy_to_house_kwh, sum(cd_readings_channel_as_columns_by_service_point."Energy from House kwH(rec)") AS total_energy_from_house_kwh, sum(cd_readings_channel_as_columns_by_service_point."Net Energy to House KwH") AS total_net_energy_kwh, avg(cd_readings_channel_as_columns_by_service_point."voltage at house") AS avg, date_trunc('month'::text, cd_readings_channel_as_columns_by_service_point.end_time) AS month, max(cd_readings_channel_as_columns_by_service_point.service_point_latitude) AS sp_latitude, max(cd_readings_channel_as_columns_by_service_point.service_point_longitude) AS sp_longtidue, max(cd_readings_channel_as_columns_by_service_point."location_ID") AS location_id, max(cd_readings_channel_as_columns_by_service_point.address) AS address, max(cd_readings_channel_as_columns_by_service_point.location_latitude) AS location_latitude, max(cd_readings_channel_as_columns_by_service_point.location_longitude) AS location_longitude, (((count(cd_readings_channel_as_columns_by_service_point.end_time))::double precision / (4)::double precision) / (24)::double precision) AS count_day FROM (cd_readings_channel_as_columns_by_service_point JOIN "PVServicePointIDs" ON (((cd_readings_channel_as_columns_by_service_point.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text))) WHERE ((cd_readings_channel_as_columns_by_service_point.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text) GROUP BY cd_readings_channel_as_columns_by_service_point.service_point_id, date_trunc('month'::text, cd_readings_channel_as_columns_by_service_point.end_time);


ALTER TABLE public.monthly_energy_summary_houses_with_pv OWNER TO eileen;

--
-- Name: monthly_energy_summary_single_pv_meter; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW monthly_energy_summary_single_pv_meter AS
    SELECT max((readings_by_meter_location_history_new_spid.service_point_id)::text) AS service_point_id, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (1)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_to_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (2)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_energy_from_house_kwh, sum(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (3)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS total_net_energy_kwh, avg(CASE WHEN (readings_by_meter_location_history_new_spid.channel = (4)::smallint) THEN readings_by_meter_location_history_new_spid.value ELSE NULL::real END) AS avg, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text) AS service_month, max(readings_by_meter_location_history_new_spid.service_point_latitude) AS sp_latitude, max(readings_by_meter_location_history_new_spid.service_point_longitude) AS sp_longitude, max((readings_by_meter_location_history_new_spid.location)::text) AS location_id, max((readings_by_meter_location_history_new_spid.address)::text) AS address, max(readings_by_meter_location_history_new_spid.latitude) AS location_latitude, max(readings_by_meter_location_history_new_spid.longitude) AS location_longitude, ((count(readings_by_meter_location_history_new_spid.end_time) / 4) / 24) AS count_day FROM (readings_by_meter_location_history readings_by_meter_location_history_new_spid JOIN "PVServicePointIDs" ON (((readings_by_meter_location_history_new_spid.service_point_id)::text = ("PVServicePointIDs".old_house_service_point_id)::text))) WHERE ("PVServicePointIDs".old_pv_service_point_id IS NULL) GROUP BY readings_by_meter_location_history_new_spid.service_point_id, to_char(date_trunc('month'::text, readings_by_meter_location_history_new_spid.end_time), 'yyyy-mm'::text);


ALTER TABLE public.monthly_energy_summary_single_pv_meter OWNER TO dave;

--
-- Name: name_address_service_point_id; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW name_address_service_point_id AS
    SELECT "LocationRecords".cust_name, "LocationRecords".service_point_util_id, "LocationRecords".address1, "LocationRecords".address2 FROM "LocationRecords";


ALTER TABLE public.name_address_service_point_id OWNER TO eileen;

--
-- Name: power_meter_events_with_spid; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW power_meter_events_with_spid AS
    SELECT pme.dtype, mlh.service_point_id, pme.id AS event_id, pme.event_category, pme.el_epoch_num, pme.el_seq_num, pme.event_ack_status, pme.event_text, pme.event_time, pme.generic_col_1 AS trap_recorded_epoch, pme.generic_col_2 AS event_is_a_swell, pme.generic_col_3 AS voltage_at_measurement_time, pme.generic_col_4, pme.generic_col_5, pme.generic_col_6, pme.generic_col_7, pme.generic_col_8, pme.generic_col_9, pme.generic_col_10, pme.insert_ts, pme.job_id, pme.event_key, pme.nic_reboot_count, pme.seconds_since_reboot, pme.event_severity, pme.source_id, pme.update_ts, pme.updated_by_user, pme.event_ack_note FROM ("PowerMeterEvents" pme JOIN "MeterLocationHistory" mlh ON (((((mlh.mac_address)::text = substr(pme.event_text, 11, 23)) AND (mlh.installed <= pme.event_time)) AND CASE WHEN (mlh.uninstalled IS NULL) THEN true ELSE (pme.event_time < mlh.uninstalled) END)));


ALTER TABLE public.power_meter_events_with_spid OWNER TO dave;

--
-- Name: pv_service_points_specifications_view; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW pv_service_points_specifications_view AS
    SELECT "PVServicePointIDs".old_pv_service_point_id AS pv_service_point_id, "PVServicePointIDs".old_house_service_point_id AS house_service_point_id, "PVServicePointIDs"."PV_Mod_size_kW", "PVServicePointIDs".inverter_model, "PVServicePointIDs"."size_kW", "PVServicePointIDs"."system_cap_kW", "PVServicePointIDs".bat, "PVServicePointIDs".sub, "PVServicePointIDs".circuit, "PVServicePointIDs".has_meter, "PVServicePointIDs".has_separate_pv_meter, "PVServicePointIDs"."add_cap_kW", "PVServicePointIDs".upgraded_total_kw, "PVServicePointIDs".street, "PVServicePointIDs".city, "PVServicePointIDs".state, "PVServicePointIDs".zip FROM "PVServicePointIDs" WHERE (("PVServicePointIDs".has_meter = 1) OR ("PVServicePointIDs".has_separate_pv_meter = 1));


ALTER TABLE public.pv_service_points_specifications_view OWNER TO eileen;

--
-- Name: reading_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE reading_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reading_id_seq OWNER TO sepgroup;

--
-- Name: reading_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE reading_id_seq OWNED BY "Reading".reading_id;


--
-- Name: readings_channel_as_columns_by_new_program; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW readings_channel_as_columns_by_new_program AS
    SELECT readings_by_meter_location_history_new_program.service_point_id, max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (1)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS max_voltage_in_interval, max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (2)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS energy_delivered_kwh, max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (3)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS avg_voltage_in_interval, max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (4)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS min_voltage_in_interval, readings_by_meter_location_history_new_program.end_time, max(readings_by_meter_location_history_new_program.service_point_latitude) AS service_point_latitude, max(readings_by_meter_location_history_new_program.service_point_longitude) AS service_point_longitude, max((readings_by_meter_location_history_new_program.location)::text) AS "location_ID", max((readings_by_meter_location_history_new_program.address)::text) AS address, max(readings_by_meter_location_history_new_program.latitude) AS location_latitude, max(readings_by_meter_location_history_new_program.longitude) AS location_longitude FROM readings_by_meter_location_history_new_program GROUP BY readings_by_meter_location_history_new_program.service_point_id, readings_by_meter_location_history_new_program.end_time;


ALTER TABLE public.readings_channel_as_columns_by_new_program OWNER TO dave;

--
-- Name: readings_channel_as_columns_by_old_program; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW readings_channel_as_columns_by_old_program AS
    SELECT readings_by_meter_location_history_old_program.service_point_id, max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (1)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END) AS "Energy to House kwH", max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (2)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END) AS "Energy from House kwH(rec)", max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (3)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END) AS "Net Energy to House KwH", max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (4)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END) AS "voltage at house", readings_by_meter_location_history_old_program.end_time, max(readings_by_meter_location_history_old_program.service_point_latitude) AS service_point_latitude, max(readings_by_meter_location_history_old_program.service_point_longitude) AS service_point_longitude, max((readings_by_meter_location_history_old_program.location)::text) AS "location_ID", max((readings_by_meter_location_history_old_program.address)::text) AS address, max(readings_by_meter_location_history_old_program.latitude) AS location_latitude, max(readings_by_meter_location_history_old_program.longitude) AS location_longitude FROM readings_by_meter_location_history_old_program GROUP BY readings_by_meter_location_history_old_program.service_point_id, readings_by_meter_location_history_old_program.end_time;


ALTER TABLE public.readings_channel_as_columns_by_old_program OWNER TO dave;

--
-- Name: readings_not_referenced_by_mlh; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW readings_not_referenced_by_mlh AS
    SELECT readings_by_meter_location_history_new_spid_2.meter_name AS mlh_meter_name, readings_with_meter_data_id_unfiltered.meter_name AS full_meter_name, readings_by_meter_location_history_new_spid_2.channel AS mlh_channel, readings_by_meter_location_history_new_spid_2.value AS mlh_value, readings_with_meter_data_id_unfiltered.channel AS full_channel, readings_with_meter_data_id_unfiltered.value AS full_value, readings_by_meter_location_history_new_spid_2.end_time AS mlh_end_time, readings_with_meter_data_id_unfiltered.end_time AS full_end_time, readings_with_meter_data_id_unfiltered.meter_data_id AS full_meter_data_id FROM (readings_unfiltered readings_with_meter_data_id_unfiltered LEFT JOIN readings_by_meter_location_history readings_by_meter_location_history_new_spid_2 ON ((readings_with_meter_data_id_unfiltered.meter_data_id = readings_by_meter_location_history_new_spid_2.meter_data_id))) WHERE (readings_by_meter_location_history_new_spid_2.meter_data_id IS NULL);


ALTER TABLE public.readings_not_referenced_by_mlh OWNER TO dave;

--
-- Name: readings_with_pv_service_point_id_new_program; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW readings_with_pv_service_point_id_new_program AS
    SELECT readings_by_meter_location_history_new_program.meter_name, readings_by_meter_location_history_new_program.end_time, max((readings_by_meter_location_history_new_program.location)::text) AS location_id, max(("PVServicePointIDs".old_pv_service_point_id)::text) AS pv_service_point_id, max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (1)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS pv_channel_1, max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (2)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS pv_channel_2, max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (3)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END) AS pv_channel_3, zero_to_null(max(CASE WHEN (readings_by_meter_location_history_new_program.channel = (4)::smallint) THEN readings_by_meter_location_history_new_program.value ELSE NULL::real END)) AS pv_channel_4_voltage FROM ("PVServicePointIDs" JOIN readings_by_meter_location_history readings_by_meter_location_history_new_program ON ((("PVServicePointIDs".old_pv_service_point_id)::text = (readings_by_meter_location_history_new_program.service_point_id)::text))) GROUP BY readings_by_meter_location_history_new_program.meter_name, readings_by_meter_location_history_new_program.end_time;


ALTER TABLE public.readings_with_pv_service_point_id_new_program OWNER TO dave;

--
-- Name: readings_with_pv_service_point_id_old_program; Type: VIEW; Schema: public; Owner: dave
--

CREATE VIEW readings_with_pv_service_point_id_old_program AS
    SELECT readings_by_meter_location_history_old_program.meter_name, readings_by_meter_location_history_old_program.end_time, max((readings_by_meter_location_history_old_program.location)::text) AS location_id, max(("PVServicePointIDs".old_pv_service_point_id)::text) AS pv_service_point_id, max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (1)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END) AS pv_channel_1, max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (2)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END) AS pv_channel_2, max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (3)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END) AS pv_channel_3, zero_to_null(max(CASE WHEN (readings_by_meter_location_history_old_program.channel = (4)::smallint) THEN readings_by_meter_location_history_old_program.value ELSE NULL::real END)) AS pv_channel_4_voltage FROM ("PVServicePointIDs" JOIN readings_by_meter_location_history readings_by_meter_location_history_old_program ON ((("PVServicePointIDs".old_pv_service_point_id)::text = (readings_by_meter_location_history_old_program.service_point_id)::text))) GROUP BY readings_by_meter_location_history_old_program.meter_name, readings_by_meter_location_history_old_program.end_time;


ALTER TABLE public.readings_with_pv_service_point_id_old_program OWNER TO dave;

--
-- Name: register_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE register_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_id_seq OWNER TO sepgroup;

--
-- Name: register_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE register_id_seq OWNED BY "Register".register_id;


--
-- Name: registerdata_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE registerdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.registerdata_id_seq OWNER TO sepgroup;

--
-- Name: registerdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE registerdata_id_seq OWNED BY "RegisterData".register_data_id;


--
-- Name: registerread_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE registerread_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.registerread_id_seq OWNER TO sepgroup;

--
-- Name: registerread_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE registerread_id_seq OWNED BY "RegisterRead".register_read_id;


--
-- Name: registers; Type: VIEW; Schema: public; Owner: daniel
--

CREATE VIEW registers AS
    SELECT "Register".number, "MeterData".meter_name, "RegisterRead".read_time FROM (((("MeterData" JOIN "RegisterData" ON (("MeterData".meter_data_id = "RegisterData".meter_data_id))) JOIN "RegisterRead" ON (("RegisterData".register_data_id = "RegisterRead".register_data_id))) JOIN "Tier" ON (("RegisterRead".register_read_id = "Tier".register_read_id))) JOIN "Register" ON (("Tier".tier_id = "Register".tier_id)));


ALTER TABLE public.registers OWNER TO daniel;

--
-- Name: VIEW registers; Type: COMMENT; Schema: public; Owner: daniel
--

COMMENT ON VIEW registers IS 'This is being used for development. @author Daniel Zhang (張道博)';


--
-- Name: tier_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE tier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tier_id_seq OWNER TO sepgroup;

--
-- Name: tier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE tier_id_seq OWNED BY "Tier".tier_id;


--
-- Name: transformer_view_test; Type: VIEW; Schema: public; Owner: sepgroup
--

CREATE VIEW transformer_view_test AS
    SELECT "TransformerDataNREL"."timestamp", "TransformerDataNREL".device_name, "TransformerDataNREL".frequency, "TransformerDataNREL".apparent_power_magnitude_s, "TransformerDataNREL".real_power_p, "TransformerDataNREL".reactive_power_q, "TransformerDataNREL".power_factor, "IrradianceData".sensor_id AS irradiance_sensor_id, "IrradianceData".irradiance_w_per_m2 FROM ("TransformerDataNREL" JOIN "IrradianceData" ON (("IrradianceData"."timestamp" = "TransformerDataNREL"."timestamp"))) WHERE ((("TransformerDataNREL".device_name)::text = '13976'::text) OR ("IrradianceData".irradiance_w_per_m2 = ANY (ARRAY[(2)::double precision, (3)::double precision, (4)::double precision])));


ALTER TABLE public.transformer_view_test OWNER TO sepgroup;

--
-- Name: view_meter_program_changes; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW view_meter_program_changes AS
    SELECT "MeterProgramChanges".meter_name, "MeterProgramChanges".date_changed, "MeterProgramChanges".program_id, raw_meter_readings.end_time, raw_meter_readings.channel, raw_meter_readings.value, raw_meter_readings.uom FROM ("MeterProgramChanges" JOIN raw_meter_readings ON ((("MeterProgramChanges".meter_name)::bpchar = raw_meter_readings.meter_name))) WHERE (raw_meter_readings.end_time > '2014-02-01 00:00:00'::timestamp without time zone);


ALTER TABLE public.view_meter_program_changes OWNER TO eileen;

--
-- Name: event_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Event" ALTER COLUMN event_id SET DEFAULT nextval('event_id_seq'::regclass);


--
-- Name: event_data_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "EventData" ALTER COLUMN event_data_id SET DEFAULT nextval('event_data_id_seq'::regclass);


--
-- Name: interval_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Interval" ALTER COLUMN interval_id SET DEFAULT nextval('interval_id_seq'::regclass);


--
-- Name: interval_read_data_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "IntervalReadData" ALTER COLUMN interval_read_data_id SET DEFAULT nextval('intervalreaddata_id_seq'::regclass);


--
-- Name: meter_data_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "MeterData" ALTER COLUMN meter_data_id SET DEFAULT nextval('meterdata_id_seq'::regclass);


--
-- Name: reading_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Reading" ALTER COLUMN reading_id SET DEFAULT nextval('reading_id_seq'::regclass);


--
-- Name: register_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Register" ALTER COLUMN register_id SET DEFAULT nextval('register_id_seq'::regclass);


--
-- Name: register_data_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "RegisterData" ALTER COLUMN register_data_id SET DEFAULT nextval('registerdata_id_seq'::regclass);


--
-- Name: register_read_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "RegisterRead" ALTER COLUMN register_read_id SET DEFAULT nextval('registerread_id_seq'::regclass);


--
-- Name: tier_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Tier" ALTER COLUMN tier_id SET DEFAULT nextval('tier_id_seq'::regclass);


--
-- Name: CircuitData_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "AverageFifteenMinCircuitData"
    ADD CONSTRAINT "CircuitData_copy_pkey" PRIMARY KEY (circuit, "timestamp");


--
-- Name: CircuitData_pkey1; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "CircuitData"
    ADD CONSTRAINT "CircuitData_pkey1" PRIMARY KEY (circuit, "timestamp");


--
-- Name: EgaugeEnergyAutoload_copy_pkey1; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "AverageFifteenMinEgaugeEnergyAutoload"
    ADD CONSTRAINT "EgaugeEnergyAutoload_copy_pkey1" PRIMARY KEY (egauge_id, datetime);


--
-- Name: EgaugeEnergyAutoload_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "EgaugeEnergyAutoload"
    ADD CONSTRAINT "EgaugeEnergyAutoload_pkey" PRIMARY KEY (egauge_id, datetime);


--
-- Name: EventData_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "EventData"
    ADD CONSTRAINT "EventData_pkey" PRIMARY KEY (event_data_id);


--
-- Name: Event_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (event_id);


--
-- Name: ExportHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "ExportHistory"
    ADD CONSTRAINT "ExportHistory_pkey" PRIMARY KEY ("timestamp");


--
-- Name: IntervalReadData_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "IntervalReadData"
    ADD CONSTRAINT "IntervalReadData_pkey" PRIMARY KEY (interval_read_data_id);


--
-- Name: Interval_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Interval"
    ADD CONSTRAINT "Interval_pkey" PRIMARY KEY (interval_id);


--
-- Name: IrradianceData_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "AverageFifteenMinIrradianceData"
    ADD CONSTRAINT "IrradianceData_copy_pkey" PRIMARY KEY (sensor_id, "timestamp");


--
-- Name: KiheiSCADATemperatureHumidity_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "AverageFifteenMinKiheiSCADATemperatureHumidity"
    ADD CONSTRAINT "KiheiSCADATemperatureHumidity_copy_pkey" PRIMARY KEY ("timestamp");


--
-- Name: KiheiSCADATemperatureHumidity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "KiheiSCADATemperatureHumidity"
    ADD CONSTRAINT "KiheiSCADATemperatureHumidity_pkey" PRIMARY KEY ("timestamp");


--
-- Name: LocationRecords_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "LocationRecords"
    ADD CONSTRAINT "LocationRecords_pkey" PRIMARY KEY (device_util_id);


--
-- Name: MeterLocationHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "MeterLocationHistory"
    ADD CONSTRAINT "MeterLocationHistory_pkey" PRIMARY KEY (meter_name, installed);


--
-- Name: MeterProgramChangesLookupTable_pkey; Type: CONSTRAINT; Schema: public; Owner: dave; Tablespace: 
--

ALTER TABLE ONLY "MeterProgramChanges"
    ADD CONSTRAINT "MeterProgramChangesLookupTable_pkey" PRIMARY KEY (meter_name, date_changed);


--
-- Name: MeterRecords_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "MeterRecords"
    ADD CONSTRAINT "MeterRecords_pkey" PRIMARY KEY (device_util_id);


--
-- Name: NotificationHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "NotificationHistory"
    ADD CONSTRAINT "NotificationHistory_pkey" PRIMARY KEY ("notificationType", "notificationTime");


--
-- Name: PowerMeterEvents_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "PowerMeterEvents"
    ADD CONSTRAINT "PowerMeterEvents_pkey" PRIMARY KEY (id, event_time);


--
-- Name: Reading_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Reading"
    ADD CONSTRAINT "Reading_pkey" PRIMARY KEY (reading_id);


--
-- Name: RegisterData_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "RegisterData"
    ADD CONSTRAINT "RegisterData_pkey" PRIMARY KEY (register_data_id);


--
-- Name: RegisterRead_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "RegisterRead"
    ADD CONSTRAINT "RegisterRead_pkey" PRIMARY KEY (register_read_id);


--
-- Name: Register_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Register"
    ADD CONSTRAINT "Register_pkey" PRIMARY KEY (register_id);


--
-- Name: Tier_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Tier"
    ADD CONSTRAINT "Tier_pkey" PRIMARY KEY (tier_id);


--
-- Name: TransformerDataNRELST_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "TransformerDataNRELST"
    ADD CONSTRAINT "TransformerDataNRELST_pkey" PRIMARY KEY ("timestamp", device_name);


--
-- Name: TransformerDataNREL_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "TransformerDataNREL"
    ADD CONSTRAINT "TransformerDataNREL_pkey" PRIMARY KEY ("timestamp", device_name);


--
-- Name: TransformerData_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "TransformerData"
    ADD CONSTRAINT "TransformerData_pkey" PRIMARY KEY (transformer, "timestamp");


--
-- Name: WeatherNOAA_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY "WeatherNOAA"
    ADD CONSTRAINT "WeatherNOAA_pkey" PRIMARY KEY (wban, datetime, record_type);


--
-- Name: firstkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "AsBuilt"
    ADD CONSTRAINT firstkey PRIMARY KEY (spid);


--
-- Name: irrad_sensor_info_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "IrradianceSensorInfo"
    ADD CONSTRAINT irrad_sensor_info_pkey PRIMARY KEY (sensor_id);


--
-- Name: irradiance_data_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "IrradianceData"
    ADD CONSTRAINT irradiance_data_pkey PRIMARY KEY (sensor_id, "timestamp");


--
-- Name: meter_data_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "MeterData"
    ADD CONSTRAINT meter_data_pkey PRIMARY KEY (meter_data_id);


--
-- Name: EventData_event_data_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "EventData_event_data_id_key" ON "EventData" USING btree (event_data_id);


--
-- Name: IntervalReadData_interval_read_data_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "IntervalReadData_interval_read_data_id_key" ON "IntervalReadData" USING btree (interval_read_data_id);


--
-- Name: Interval_end_time_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "Interval_end_time_idx" ON "Interval" USING btree (end_time);


--
-- Name: Interval_interval_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "Interval_interval_id_key" ON "Interval" USING btree (interval_id);


--
-- Name: MeterData_meter_data_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "MeterData_meter_data_id_key" ON "MeterData" USING btree (meter_data_id);


--
-- Name: MeterData_meter_name_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "MeterData_meter_name_idx" ON "MeterData" USING btree (meter_name);


--
-- Name: PVServicePointIDs_new_spid_new_spid_pv_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "PVServicePointIDs_new_spid_new_spid_pv_key" ON "PVServicePointIDs" USING btree (new_spid, new_spid_pv);


--
-- Name: RegisterData_meter_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "RegisterData_meter_data_id_idx" ON "RegisterData" USING btree (meter_data_id);


--
-- Name: RegisterData_register_data_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "RegisterData_register_data_id_key" ON "RegisterData" USING btree (register_data_id);


--
-- Name: RegisterRead_register_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "RegisterRead_register_data_id_idx" ON "RegisterRead" USING btree (register_data_id);


--
-- Name: RegisterRead_register_read_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "RegisterRead_register_read_id_key" ON "RegisterRead" USING btree (register_read_id);


--
-- Name: Register_register_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "Register_register_id_idx" ON "Register" USING btree (register_id);


--
-- Name: Register_tier_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "Register_tier_id_idx" ON "Register" USING btree (tier_id);


--
-- Name: Tier_register_read_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "Tier_register_read_id_idx" ON "Tier" USING btree (register_read_id);


--
-- Name: Tier_tier_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "Tier_tier_id_key" ON "Tier" USING btree (tier_id);


--
-- Name: device_util_id_index; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX device_util_id_index ON "LocationRecords" USING btree (device_util_id);


--
-- Name: idx_primary_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX idx_primary_key ON "EgaugeEnergyAutoload" USING btree (egauge_id, datetime);


--
-- Name: installed_uninstalled_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX installed_uninstalled_idx ON "MeterLocationHistory" USING btree (installed, uninstalled);


--
-- Name: interval_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX interval_id_idx ON "Reading" USING btree (interval_id);


--
-- Name: interval_read_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX interval_read_data_id_idx ON "Interval" USING btree (interval_read_data_id);


--
-- Name: mac_address_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX mac_address_idx ON "MeterLocationHistory" USING btree (mac_address);


--
-- Name: meter_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX meter_data_id_idx ON "IntervalReadData" USING btree (meter_data_id);


--
-- Name: old_service_point_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX old_service_point_id_idx ON "MeterLocationHistory" USING btree (old_service_point_id);


--
-- Name: reading_channel_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX reading_channel_idx ON "Reading" USING btree (channel);


--
-- Name: reading_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX reading_id_idx ON "Reading" USING btree (reading_id);


--
-- Name: service_point_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX service_point_id_idx ON "MeterLocationHistory" USING btree (service_point_id);


--
-- Name: _RETURN; Type: RULE; Schema: public; Owner: eileen
--

CREATE RULE "_RETURN" AS ON SELECT TO dates_irradiance_data DO INSTEAD SELECT "IrradianceSensorInfo".sensor_id, "IrradianceSensorInfo".latitude, "IrradianceSensorInfo".longitude, count("IrradianceData".irradiance_w_per_m2) AS count, min("IrradianceData"."timestamp") AS "Earliest Date", max("IrradianceData"."timestamp") AS "Latest Date", "IrradianceSensorInfo".name FROM ("IrradianceData" JOIN "IrradianceSensorInfo" ON (("IrradianceSensorInfo".sensor_id = "IrradianceData".sensor_id))) GROUP BY "IrradianceSensorInfo".sensor_id, "IrradianceSensorInfo".latitude, "IrradianceSensorInfo".longitude;


--
-- Name: EventData_meter_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "EventData"
    ADD CONSTRAINT "EventData_meter_data_id_fkey" FOREIGN KEY (meter_data_id) REFERENCES "MeterData"(meter_data_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Event_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Event"
    ADD CONSTRAINT "Event_event_id_fkey" FOREIGN KEY (event_data_id) REFERENCES "EventData"(event_data_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: IntervalReadData_meter_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "IntervalReadData"
    ADD CONSTRAINT "IntervalReadData_meter_data_id_fkey" FOREIGN KEY (meter_data_id) REFERENCES "MeterData"(meter_data_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Interval_interval_read_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Interval"
    ADD CONSTRAINT "Interval_interval_read_data_id_fkey" FOREIGN KEY (interval_read_data_id) REFERENCES "IntervalReadData"(interval_read_data_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Reading_interval_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Reading"
    ADD CONSTRAINT "Reading_interval_id_fkey" FOREIGN KEY (interval_id) REFERENCES "Interval"(interval_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: RegisterData_meter_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "RegisterData"
    ADD CONSTRAINT "RegisterData_meter_data_id_fkey" FOREIGN KEY (meter_data_id) REFERENCES "MeterData"(meter_data_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: RegisterRead_register_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "RegisterRead"
    ADD CONSTRAINT "RegisterRead_register_data_id_fkey" FOREIGN KEY (register_data_id) REFERENCES "RegisterData"(register_data_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Register_register_read_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Register"
    ADD CONSTRAINT "Register_register_read_id_fkey" FOREIGN KEY (tier_id) REFERENCES "Tier"(tier_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Tier_register_read_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Tier"
    ADD CONSTRAINT "Tier_register_read_id_fkey" FOREIGN KEY (register_read_id) REFERENCES "RegisterRead"(register_read_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: az; Type: ACL; Schema: -; Owner: ashkan
--

REVOKE ALL ON SCHEMA az FROM PUBLIC;
REVOKE ALL ON SCHEMA az FROM ashkan;
GRANT ALL ON SCHEMA az TO ashkan;


--
-- Name: dw; Type: ACL; Schema: -; Owner: dave
--

REVOKE ALL ON SCHEMA dw FROM PUBLIC;
REVOKE ALL ON SCHEMA dw FROM dave;
GRANT ALL ON SCHEMA dw TO dave;
GRANT ALL ON SCHEMA dw TO ashkan;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


SET search_path = dz, pg_catalog;

--
-- Name: meco_readings_dupe_count(); Type: ACL; Schema: dz; Owner: postgres
--

REVOKE ALL ON FUNCTION meco_readings_dupe_count() FROM PUBLIC;
REVOKE ALL ON FUNCTION meco_readings_dupe_count() FROM postgres;
GRANT ALL ON FUNCTION meco_readings_dupe_count() TO postgres;
GRANT ALL ON FUNCTION meco_readings_dupe_count() TO PUBLIC;
GRANT ALL ON FUNCTION meco_readings_dupe_count() TO sepgroup;
GRANT ALL ON FUNCTION meco_readings_dupe_count() TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: zero_to_null(real); Type: ACL; Schema: public; Owner: daniel
--

REVOKE ALL ON FUNCTION zero_to_null(real) FROM PUBLIC;
REVOKE ALL ON FUNCTION zero_to_null(real) FROM daniel;
GRANT ALL ON FUNCTION zero_to_null(real) TO daniel;
GRANT ALL ON FUNCTION zero_to_null(real) TO PUBLIC;
GRANT ALL ON FUNCTION zero_to_null(real) TO sepgroup;
GRANT ALL ON FUNCTION zero_to_null(real) TO sepgroupreadonly;


--
-- Name: zero_to_null(double precision); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON FUNCTION zero_to_null(double precision) FROM PUBLIC;
REVOKE ALL ON FUNCTION zero_to_null(double precision) FROM postgres;
GRANT ALL ON FUNCTION zero_to_null(double precision) TO postgres;
GRANT ALL ON FUNCTION zero_to_null(double precision) TO PUBLIC;
GRANT ALL ON FUNCTION zero_to_null(double precision) TO sepgroup;
GRANT ALL ON FUNCTION zero_to_null(double precision) TO sepgroup_nonmsg;
GRANT ALL ON FUNCTION zero_to_null(double precision) TO sepgroupreadonly;


SET search_path = dw, pg_catalog;

--
-- Name: MeterLocationHistory_deprecated; Type: ACL; Schema: dw; Owner: dave
--

REVOKE ALL ON TABLE "MeterLocationHistory_deprecated" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterLocationHistory_deprecated" FROM dave;
GRANT ALL ON TABLE "MeterLocationHistory_deprecated" TO dave;
GRANT ALL ON TABLE "MeterLocationHistory_deprecated" TO sepgroup;
GRANT SELECT ON TABLE "MeterLocationHistory_deprecated" TO sepgroupreadonly;
GRANT SELECT ON TABLE "MeterLocationHistory_deprecated" TO daniel;


SET search_path = public, pg_catalog;

--
-- Name: MeterProgramChanges; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE "MeterProgramChanges" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterProgramChanges" FROM dave;
GRANT ALL ON TABLE "MeterProgramChanges" TO dave;
GRANT ALL ON TABLE "MeterProgramChanges" TO sepgroup;
GRANT SELECT ON TABLE "MeterProgramChanges" TO sepgroupreadonly;


SET search_path = dw, pg_catalog;

--
-- Name: MeterProgramHistory_backup; Type: ACL; Schema: dw; Owner: dave
--

REVOKE ALL ON TABLE "MeterProgramHistory_backup" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterProgramHistory_backup" FROM dave;
GRANT ALL ON TABLE "MeterProgramHistory_backup" TO dave;
GRANT ALL ON TABLE "MeterProgramHistory_backup" TO sepgroup;
GRANT SELECT ON TABLE "MeterProgramHistory_backup" TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: Interval; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Interval" FROM PUBLIC;
REVOKE ALL ON TABLE "Interval" FROM sepgroup;
GRANT ALL ON TABLE "Interval" TO sepgroup;
GRANT SELECT ON TABLE "Interval" TO sepgroupreadonly;


--
-- Name: IntervalReadData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "IntervalReadData" FROM PUBLIC;
REVOKE ALL ON TABLE "IntervalReadData" FROM sepgroup;
GRANT ALL ON TABLE "IntervalReadData" TO sepgroup;
GRANT SELECT ON TABLE "IntervalReadData" TO sepgroupreadonly;


--
-- Name: MeterData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "MeterData" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterData" FROM sepgroup;
GRANT ALL ON TABLE "MeterData" TO sepgroup;
GRANT SELECT ON TABLE "MeterData" TO sepgroupreadonly;


--
-- Name: MeterLocationHistory; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "MeterLocationHistory" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterLocationHistory" FROM sepgroup;
GRANT ALL ON TABLE "MeterLocationHistory" TO sepgroup;
GRANT SELECT ON TABLE "MeterLocationHistory" TO sepgroupreadonly;


--
-- Name: PVServicePointIDs; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "PVServicePointIDs" FROM PUBLIC;
REVOKE ALL ON TABLE "PVServicePointIDs" FROM sepgroup;
GRANT ALL ON TABLE "PVServicePointIDs" TO sepgroup;
GRANT SELECT ON TABLE "PVServicePointIDs" TO sepgroupreadonly;


--
-- Name: Reading; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Reading" FROM PUBLIC;
REVOKE ALL ON TABLE "Reading" FROM sepgroup;
GRANT ALL ON TABLE "Reading" TO sepgroup;
GRANT SELECT ON TABLE "Reading" TO sepgroupreadonly;


--
-- Name: nonpv_service_point_ids; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE nonpv_service_point_ids FROM PUBLIC;
REVOKE ALL ON TABLE nonpv_service_point_ids FROM postgres;
GRANT ALL ON TABLE nonpv_service_point_ids TO postgres;
GRANT ALL ON TABLE nonpv_service_point_ids TO sepgroup;
GRANT SELECT ON TABLE nonpv_service_point_ids TO sepgroupreadonly;


--
-- Name: readings_by_meter_location_history; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE readings_by_meter_location_history FROM PUBLIC;
REVOKE ALL ON TABLE readings_by_meter_location_history FROM eileen;
GRANT ALL ON TABLE readings_by_meter_location_history TO eileen;
GRANT ALL ON TABLE readings_by_meter_location_history TO sepgroup;
GRANT SELECT ON TABLE readings_by_meter_location_history TO sepgroupreadonly;


SET search_path = dw, pg_catalog;

--
-- Name: test_monthly_energy_summary_for_nonpv_service_points; Type: ACL; Schema: dw; Owner: dave
--

REVOKE ALL ON TABLE test_monthly_energy_summary_for_nonpv_service_points FROM PUBLIC;
REVOKE ALL ON TABLE test_monthly_energy_summary_for_nonpv_service_points FROM dave;
GRANT ALL ON TABLE test_monthly_energy_summary_for_nonpv_service_points TO dave;
GRANT ALL ON TABLE test_monthly_energy_summary_for_nonpv_service_points TO sepgroup;
GRANT SELECT ON TABLE test_monthly_energy_summary_for_nonpv_service_points TO sepgroupreadonly;


SET search_path = dz, pg_catalog;

--
-- Name: _IrradianceFifteenMinIntervals; Type: ACL; Schema: dz; Owner: postgres
--

REVOKE ALL ON TABLE "_IrradianceFifteenMinIntervals" FROM PUBLIC;
REVOKE ALL ON TABLE "_IrradianceFifteenMinIntervals" FROM postgres;
GRANT ALL ON TABLE "_IrradianceFifteenMinIntervals" TO postgres;
GRANT ALL ON TABLE "_IrradianceFifteenMinIntervals" TO sepgroup;
GRANT SELECT ON TABLE "_IrradianceFifteenMinIntervals" TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: Event; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Event" FROM PUBLIC;
REVOKE ALL ON TABLE "Event" FROM sepgroup;
GRANT ALL ON TABLE "Event" TO sepgroup;
GRANT SELECT ON TABLE "Event" TO sepgroupreadonly;


--
-- Name: EventData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "EventData" FROM PUBLIC;
REVOKE ALL ON TABLE "EventData" FROM sepgroup;
GRANT ALL ON TABLE "EventData" TO sepgroup;
GRANT SELECT ON TABLE "EventData" TO sepgroupreadonly;


SET search_path = dz, pg_catalog;

--
-- Name: count_of_event_duplicates; Type: ACL; Schema: dz; Owner: daniel
--

REVOKE ALL ON TABLE count_of_event_duplicates FROM PUBLIC;
REVOKE ALL ON TABLE count_of_event_duplicates FROM daniel;
GRANT ALL ON TABLE count_of_event_duplicates TO daniel;
GRANT ALL ON TABLE count_of_event_duplicates TO sepgroup;
GRANT SELECT ON TABLE count_of_event_duplicates TO sepgroupreadonly;


--
-- Name: readings_by_meter_location_history; Type: ACL; Schema: dz; Owner: daniel
--

REVOKE ALL ON TABLE readings_by_meter_location_history FROM PUBLIC;
REVOKE ALL ON TABLE readings_by_meter_location_history FROM daniel;
GRANT ALL ON TABLE readings_by_meter_location_history TO daniel;
GRANT ALL ON TABLE readings_by_meter_location_history TO sepgroup;
GRANT SELECT ON TABLE readings_by_meter_location_history TO sepgroupreadonly;


--
-- Name: deprecated_readings_by_mlh_transposed_columns_opt1; Type: ACL; Schema: dz; Owner: daniel
--

REVOKE ALL ON TABLE deprecated_readings_by_mlh_transposed_columns_opt1 FROM PUBLIC;
REVOKE ALL ON TABLE deprecated_readings_by_mlh_transposed_columns_opt1 FROM daniel;
GRANT ALL ON TABLE deprecated_readings_by_mlh_transposed_columns_opt1 TO daniel;
GRANT ALL ON TABLE deprecated_readings_by_mlh_transposed_columns_opt1 TO sepgroup;
GRANT SELECT ON TABLE deprecated_readings_by_mlh_transposed_columns_opt1 TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: EgaugeEnergyAutoload; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "EgaugeEnergyAutoload" FROM PUBLIC;
REVOKE ALL ON TABLE "EgaugeEnergyAutoload" FROM sepgroup;
GRANT ALL ON TABLE "EgaugeEnergyAutoload" TO sepgroup;
GRANT SELECT ON TABLE "EgaugeEnergyAutoload" TO sepgroupreadonly;


SET search_path = dz, pg_catalog;

--
-- Name: outlier_test; Type: ACL; Schema: dz; Owner: postgres
--

REVOKE ALL ON TABLE outlier_test FROM PUBLIC;
REVOKE ALL ON TABLE outlier_test FROM postgres;
GRANT ALL ON TABLE outlier_test TO postgres;
GRANT ALL ON TABLE outlier_test TO sepgroup;
GRANT SELECT ON TABLE outlier_test TO sepgroupreadonly;


--
-- Name: reading_dupes; Type: ACL; Schema: dz; Owner: daniel
--

REVOKE ALL ON TABLE reading_dupes FROM PUBLIC;
REVOKE ALL ON TABLE reading_dupes FROM daniel;
GRANT ALL ON TABLE reading_dupes TO daniel;
GRANT ALL ON TABLE reading_dupes TO sepgroup;
GRANT SELECT ON TABLE reading_dupes TO sepgroupreadonly;


--
-- Name: readings_by_mlh_new_spid_for_ashkan_from_2013-07-01; Type: ACL; Schema: dz; Owner: daniel
--

REVOKE ALL ON TABLE "readings_by_mlh_new_spid_for_ashkan_from_2013-07-01" FROM PUBLIC;
REVOKE ALL ON TABLE "readings_by_mlh_new_spid_for_ashkan_from_2013-07-01" FROM daniel;
GRANT ALL ON TABLE "readings_by_mlh_new_spid_for_ashkan_from_2013-07-01" TO daniel;
GRANT ALL ON TABLE "readings_by_mlh_new_spid_for_ashkan_from_2013-07-01" TO sepgroup;
GRANT SELECT ON TABLE "readings_by_mlh_new_spid_for_ashkan_from_2013-07-01" TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: readings_unfiltered; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE readings_unfiltered FROM PUBLIC;
REVOKE ALL ON TABLE readings_unfiltered FROM postgres;
GRANT ALL ON TABLE readings_unfiltered TO postgres;
GRANT ALL ON TABLE readings_unfiltered TO sepgroup;
GRANT SELECT ON TABLE readings_unfiltered TO sepgroupreadonly;


SET search_path = dz, pg_catalog;

--
-- Name: readings_not_referenced_by_mlh_deprecated; Type: ACL; Schema: dz; Owner: postgres
--

REVOKE ALL ON TABLE readings_not_referenced_by_mlh_deprecated FROM PUBLIC;
REVOKE ALL ON TABLE readings_not_referenced_by_mlh_deprecated FROM postgres;
GRANT ALL ON TABLE readings_not_referenced_by_mlh_deprecated TO postgres;
GRANT ALL ON TABLE readings_not_referenced_by_mlh_deprecated TO sepgroup;
GRANT SELECT ON TABLE readings_not_referenced_by_mlh_deprecated TO sepgroupreadonly;


--
-- Name: readings_unfiltered; Type: ACL; Schema: dz; Owner: daniel
--

REVOKE ALL ON TABLE readings_unfiltered FROM PUBLIC;
REVOKE ALL ON TABLE readings_unfiltered FROM daniel;
GRANT ALL ON TABLE readings_unfiltered TO daniel;
GRANT ALL ON TABLE readings_unfiltered TO sepgroup;
GRANT SELECT ON TABLE readings_unfiltered TO sepgroupreadonly;


--
-- Name: readings_with_pv_service_point_id_deprecated; Type: ACL; Schema: dz; Owner: postgres
--

REVOKE ALL ON TABLE readings_with_pv_service_point_id_deprecated FROM PUBLIC;
REVOKE ALL ON TABLE readings_with_pv_service_point_id_deprecated FROM postgres;
GRANT ALL ON TABLE readings_with_pv_service_point_id_deprecated TO postgres;
GRANT ALL ON TABLE readings_with_pv_service_point_id_deprecated TO sepgroup;
GRANT SELECT ON TABLE readings_with_pv_service_point_id_deprecated TO sepgroupreadonly;


--
-- Name: test_readings_by_meter_location_history; Type: ACL; Schema: dz; Owner: daniel
--

REVOKE ALL ON TABLE test_readings_by_meter_location_history FROM PUBLIC;
REVOKE ALL ON TABLE test_readings_by_meter_location_history FROM daniel;
GRANT ALL ON TABLE test_readings_by_meter_location_history TO daniel;
GRANT ALL ON TABLE test_readings_by_meter_location_history TO sepgroup;
GRANT SELECT ON TABLE test_readings_by_meter_location_history TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: raw_meter_readings; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE raw_meter_readings FROM PUBLIC;
REVOKE ALL ON TABLE raw_meter_readings FROM postgres;
GRANT ALL ON TABLE raw_meter_readings TO postgres;
GRANT ALL ON TABLE raw_meter_readings TO sepgroup;
GRANT SELECT ON TABLE raw_meter_readings TO sepgroupreadonly;


SET search_path = ep, pg_catalog;

--
-- Name: dates_raw_meter_readings; Type: ACL; Schema: ep; Owner: eileen
--

REVOKE ALL ON TABLE dates_raw_meter_readings FROM PUBLIC;
REVOKE ALL ON TABLE dates_raw_meter_readings FROM eileen;
GRANT ALL ON TABLE dates_raw_meter_readings TO eileen;
GRANT ALL ON TABLE dates_raw_meter_readings TO sepgroup;
GRANT SELECT ON TABLE dates_raw_meter_readings TO sepgroupreadonly;


--
-- Name: egauge4913; Type: ACL; Schema: ep; Owner: eileen
--

REVOKE ALL ON TABLE egauge4913 FROM PUBLIC;
REVOKE ALL ON TABLE egauge4913 FROM eileen;
GRANT ALL ON TABLE egauge4913 TO eileen;
GRANT ALL ON TABLE egauge4913 TO sepgroup;
GRANT SELECT ON TABLE egauge4913 TO sepgroupreadonly;


--
-- Name: meter115651channel2; Type: ACL; Schema: ep; Owner: eileen
--

REVOKE ALL ON TABLE meter115651channel2 FROM PUBLIC;
REVOKE ALL ON TABLE meter115651channel2 FROM eileen;
GRANT ALL ON TABLE meter115651channel2 TO eileen;
GRANT ALL ON TABLE meter115651channel2 TO sepgroup;
GRANT SELECT ON TABLE meter115651channel2 TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: readings_unfiltered_columns; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE readings_unfiltered_columns FROM PUBLIC;
REVOKE ALL ON TABLE readings_unfiltered_columns FROM eileen;
GRANT ALL ON TABLE readings_unfiltered_columns TO eileen;
GRANT ALL ON TABLE readings_unfiltered_columns TO sepgroup;
GRANT SELECT ON TABLE readings_unfiltered_columns TO sepgroupreadonly;


SET search_path = ep, pg_catalog;

--
-- Name: readings_meter_changes; Type: ACL; Schema: ep; Owner: eileen
--

REVOKE ALL ON TABLE readings_meter_changes FROM PUBLIC;
REVOKE ALL ON TABLE readings_meter_changes FROM eileen;
GRANT ALL ON TABLE readings_meter_changes TO eileen;
GRANT ALL ON TABLE readings_meter_changes TO sepgroup;
GRANT SELECT ON TABLE readings_meter_changes TO sepgroupreadonly;


--
-- Name: voltage_data_for_lesson_Mel_3D; Type: ACL; Schema: ep; Owner: eileen
--

REVOKE ALL ON TABLE "voltage_data_for_lesson_Mel_3D" FROM PUBLIC;
REVOKE ALL ON TABLE "voltage_data_for_lesson_Mel_3D" FROM eileen;
GRANT ALL ON TABLE "voltage_data_for_lesson_Mel_3D" TO eileen;
GRANT ALL ON TABLE "voltage_data_for_lesson_Mel_3D" TO sepgroup;
GRANT SELECT ON TABLE "voltage_data_for_lesson_Mel_3D" TO sepgroupreadonly;


SET search_path = public, pg_catalog;

--
-- Name: AsBuilt; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "AsBuilt" FROM PUBLIC;
REVOKE ALL ON TABLE "AsBuilt" FROM sepgroup;
GRANT ALL ON TABLE "AsBuilt" TO sepgroup;
GRANT SELECT ON TABLE "AsBuilt" TO sepgroupreadonly;


--
-- Name: AverageFifteenMinCircuitData; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "AverageFifteenMinCircuitData" FROM PUBLIC;
REVOKE ALL ON TABLE "AverageFifteenMinCircuitData" FROM postgres;
GRANT ALL ON TABLE "AverageFifteenMinCircuitData" TO postgres;
GRANT ALL ON TABLE "AverageFifteenMinCircuitData" TO sepgroup;
GRANT SELECT ON TABLE "AverageFifteenMinCircuitData" TO sepgroupreadonly;


--
-- Name: AverageFifteenMinEgaugeEnergyAutoload; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "AverageFifteenMinEgaugeEnergyAutoload" FROM PUBLIC;
REVOKE ALL ON TABLE "AverageFifteenMinEgaugeEnergyAutoload" FROM postgres;
GRANT ALL ON TABLE "AverageFifteenMinEgaugeEnergyAutoload" TO postgres;
GRANT ALL ON TABLE "AverageFifteenMinEgaugeEnergyAutoload" TO sepgroup;
GRANT SELECT ON TABLE "AverageFifteenMinEgaugeEnergyAutoload" TO sepgroupreadonly;


--
-- Name: AverageFifteenMinIrradianceData; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "AverageFifteenMinIrradianceData" FROM PUBLIC;
REVOKE ALL ON TABLE "AverageFifteenMinIrradianceData" FROM postgres;
GRANT ALL ON TABLE "AverageFifteenMinIrradianceData" TO postgres;
GRANT ALL ON TABLE "AverageFifteenMinIrradianceData" TO sepgroup;
GRANT SELECT ON TABLE "AverageFifteenMinIrradianceData" TO sepgroupreadonly;


--
-- Name: AverageFifteenMinKiheiSCADATemperatureHumidity; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "AverageFifteenMinKiheiSCADATemperatureHumidity" FROM PUBLIC;
REVOKE ALL ON TABLE "AverageFifteenMinKiheiSCADATemperatureHumidity" FROM postgres;
GRANT ALL ON TABLE "AverageFifteenMinKiheiSCADATemperatureHumidity" TO postgres;
GRANT ALL ON TABLE "AverageFifteenMinKiheiSCADATemperatureHumidity" TO sepgroup;
GRANT SELECT ON TABLE "AverageFifteenMinKiheiSCADATemperatureHumidity" TO sepgroupreadonly;


--
-- Name: BatteryWailea; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "BatteryWailea" FROM PUBLIC;
REVOKE ALL ON TABLE "BatteryWailea" FROM sepgroup;
GRANT ALL ON TABLE "BatteryWailea" TO sepgroup;
GRANT SELECT ON TABLE "BatteryWailea" TO sepgroupreadonly;


--
-- Name: CircuitData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "CircuitData" FROM PUBLIC;
REVOKE ALL ON TABLE "CircuitData" FROM sepgroup;
GRANT ALL ON TABLE "CircuitData" TO sepgroup;
GRANT SELECT ON TABLE "CircuitData" TO sepgroupreadonly;


--
-- Name: EgaugeInfo; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE "EgaugeInfo" FROM PUBLIC;
REVOKE ALL ON TABLE "EgaugeInfo" FROM eileen;
GRANT ALL ON TABLE "EgaugeInfo" TO eileen;
GRANT ALL ON TABLE "EgaugeInfo" TO sepgroup;
GRANT SELECT ON TABLE "EgaugeInfo" TO sepgroupreadonly;


--
-- Name: ExportHistory; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "ExportHistory" FROM PUBLIC;
REVOKE ALL ON TABLE "ExportHistory" FROM postgres;
GRANT ALL ON TABLE "ExportHistory" TO postgres;
GRANT ALL ON TABLE "ExportHistory" TO sepgroup;
GRANT SELECT ON TABLE "ExportHistory" TO sepgroupreadonly;


--
-- Name: IrradianceData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "IrradianceData" FROM PUBLIC;
REVOKE ALL ON TABLE "IrradianceData" FROM sepgroup;
GRANT ALL ON TABLE "IrradianceData" TO sepgroup;
GRANT SELECT ON TABLE "IrradianceData" TO sepgroupreadonly;


--
-- Name: IrradianceSensorInfo; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "IrradianceSensorInfo" FROM PUBLIC;
REVOKE ALL ON TABLE "IrradianceSensorInfo" FROM sepgroup;
GRANT ALL ON TABLE "IrradianceSensorInfo" TO sepgroup;
GRANT SELECT ON TABLE "IrradianceSensorInfo" TO sepgroupreadonly;


--
-- Name: KiheiSCADATemperatureHumidity; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "KiheiSCADATemperatureHumidity" FROM PUBLIC;
REVOKE ALL ON TABLE "KiheiSCADATemperatureHumidity" FROM postgres;
GRANT ALL ON TABLE "KiheiSCADATemperatureHumidity" TO postgres;
GRANT ALL ON TABLE "KiheiSCADATemperatureHumidity" TO sepgroup;
GRANT SELECT ON TABLE "KiheiSCADATemperatureHumidity" TO sepgroupreadonly;


--
-- Name: LocationRecords; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "LocationRecords" FROM PUBLIC;
REVOKE ALL ON TABLE "LocationRecords" FROM sepgroup;
GRANT ALL ON TABLE "LocationRecords" TO sepgroup;
GRANT SELECT ON TABLE "LocationRecords" TO sepgroupreadonly;


--
-- Name: MSG_PV_Data; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE "MSG_PV_Data" FROM PUBLIC;
REVOKE ALL ON TABLE "MSG_PV_Data" FROM eileen;
GRANT ALL ON TABLE "MSG_PV_Data" TO eileen;
GRANT ALL ON TABLE "MSG_PV_Data" TO sepgroup;
GRANT SELECT ON TABLE "MSG_PV_Data" TO sepgroupreadonly;


--
-- Name: MeterRecords; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "MeterRecords" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterRecords" FROM sepgroup;
GRANT ALL ON TABLE "MeterRecords" TO sepgroup;
GRANT SELECT ON TABLE "MeterRecords" TO sepgroupreadonly;


--
-- Name: NotificationHistory; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "NotificationHistory" FROM PUBLIC;
REVOKE ALL ON TABLE "NotificationHistory" FROM postgres;
GRANT ALL ON TABLE "NotificationHistory" TO postgres;
GRANT ALL ON TABLE "NotificationHistory" TO sepgroup;
GRANT SELECT ON TABLE "NotificationHistory" TO sepgroupreadonly;


--
-- Name: PowerMeterEvents; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "PowerMeterEvents" FROM PUBLIC;
REVOKE ALL ON TABLE "PowerMeterEvents" FROM sepgroup;
GRANT ALL ON TABLE "PowerMeterEvents" TO sepgroup;
GRANT SELECT ON TABLE "PowerMeterEvents" TO sepgroupreadonly;


--
-- Name: Register; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Register" FROM PUBLIC;
REVOKE ALL ON TABLE "Register" FROM sepgroup;
GRANT ALL ON TABLE "Register" TO sepgroup;
GRANT SELECT ON TABLE "Register" TO sepgroupreadonly;


--
-- Name: RegisterData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "RegisterData" FROM PUBLIC;
REVOKE ALL ON TABLE "RegisterData" FROM sepgroup;
GRANT ALL ON TABLE "RegisterData" TO sepgroup;
GRANT SELECT ON TABLE "RegisterData" TO sepgroupreadonly;


--
-- Name: RegisterRead; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "RegisterRead" FROM PUBLIC;
REVOKE ALL ON TABLE "RegisterRead" FROM sepgroup;
GRANT ALL ON TABLE "RegisterRead" TO sepgroup;
GRANT SELECT ON TABLE "RegisterRead" TO sepgroupreadonly;


--
-- Name: TapData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "TapData" FROM PUBLIC;
REVOKE ALL ON TABLE "TapData" FROM sepgroup;
GRANT ALL ON TABLE "TapData" TO sepgroup;
GRANT SELECT ON TABLE "TapData" TO sepgroupreadonly;


--
-- Name: Tier; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Tier" FROM PUBLIC;
REVOKE ALL ON TABLE "Tier" FROM sepgroup;
GRANT ALL ON TABLE "Tier" TO sepgroup;
GRANT SELECT ON TABLE "Tier" TO sepgroupreadonly;


--
-- Name: TransformerData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "TransformerData" FROM PUBLIC;
REVOKE ALL ON TABLE "TransformerData" FROM sepgroup;
GRANT ALL ON TABLE "TransformerData" TO sepgroup;
GRANT SELECT ON TABLE "TransformerData" TO sepgroupreadonly;


--
-- Name: TransformerDataNREL; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "TransformerDataNREL" FROM PUBLIC;
REVOKE ALL ON TABLE "TransformerDataNREL" FROM sepgroup;
GRANT ALL ON TABLE "TransformerDataNREL" TO sepgroup;
GRANT SELECT ON TABLE "TransformerDataNREL" TO sepgroupreadonly;
GRANT ALL ON TABLE "TransformerDataNREL" TO ashkan;


--
-- Name: TransformerDataNRELST; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "TransformerDataNRELST" FROM PUBLIC;
REVOKE ALL ON TABLE "TransformerDataNRELST" FROM sepgroup;
GRANT ALL ON TABLE "TransformerDataNRELST" TO sepgroup;
GRANT SELECT ON TABLE "TransformerDataNRELST" TO sepgroupreadonly;
GRANT ALL ON TABLE "TransformerDataNRELST" TO ashkan;


--
-- Name: WeatherNOAA; Type: ACL; Schema: public; Owner: daniel
--

REVOKE ALL ON TABLE "WeatherNOAA" FROM PUBLIC;
REVOKE ALL ON TABLE "WeatherNOAA" FROM daniel;
GRANT ALL ON TABLE "WeatherNOAA" TO daniel;
GRANT ALL ON TABLE "WeatherNOAA" TO sepgroup;
GRANT SELECT ON TABLE "WeatherNOAA" TO sepgroupreadonly;


--
-- Name: _IrradianceFifteenMinIntervals; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "_IrradianceFifteenMinIntervals" FROM PUBLIC;
REVOKE ALL ON TABLE "_IrradianceFifteenMinIntervals" FROM postgres;
GRANT ALL ON TABLE "_IrradianceFifteenMinIntervals" TO postgres;
GRANT ALL ON TABLE "_IrradianceFifteenMinIntervals" TO sepgroup;
GRANT SELECT ON TABLE "_IrradianceFifteenMinIntervals" TO sepgroupreadonly;


--
-- Name: az_ashkan1; Type: ACL; Schema: public; Owner: christian
--

REVOKE ALL ON TABLE az_ashkan1 FROM PUBLIC;
REVOKE ALL ON TABLE az_ashkan1 FROM christian;
GRANT ALL ON TABLE az_ashkan1 TO christian;
GRANT ALL ON TABLE az_ashkan1 TO sepgroup;
GRANT SELECT ON TABLE az_ashkan1 TO sepgroupreadonly;


--
-- Name: az_houses_all_with_smart_meter; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE az_houses_all_with_smart_meter FROM PUBLIC;
REVOKE ALL ON TABLE az_houses_all_with_smart_meter FROM eileen;
GRANT ALL ON TABLE az_houses_all_with_smart_meter TO eileen;
GRANT ALL ON TABLE az_houses_all_with_smart_meter TO sepgroup;
GRANT SELECT ON TABLE az_houses_all_with_smart_meter TO sepgroupreadonly;


--
-- Name: az_houses_with_no_pv; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE az_houses_with_no_pv FROM PUBLIC;
REVOKE ALL ON TABLE az_houses_with_no_pv FROM eileen;
GRANT ALL ON TABLE az_houses_with_no_pv TO eileen;
GRANT ALL ON TABLE az_houses_with_no_pv TO sepgroup;
GRANT SELECT ON TABLE az_houses_with_no_pv TO sepgroupreadonly;


--
-- Name: az_houses_with_pv_and_pv_meter; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE az_houses_with_pv_and_pv_meter FROM PUBLIC;
REVOKE ALL ON TABLE az_houses_with_pv_and_pv_meter FROM eileen;
GRANT ALL ON TABLE az_houses_with_pv_and_pv_meter TO eileen;
GRANT ALL ON TABLE az_houses_with_pv_and_pv_meter TO sepgroup;
GRANT SELECT ON TABLE az_houses_with_pv_and_pv_meter TO sepgroupreadonly;


--
-- Name: az_houses_with_pv_no_extra_meter; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE az_houses_with_pv_no_extra_meter FROM PUBLIC;
REVOKE ALL ON TABLE az_houses_with_pv_no_extra_meter FROM eileen;
GRANT ALL ON TABLE az_houses_with_pv_no_extra_meter TO eileen;
GRANT ALL ON TABLE az_houses_with_pv_no_extra_meter TO sepgroup;
GRANT SELECT ON TABLE az_houses_with_pv_no_extra_meter TO sepgroupreadonly;


--
-- Name: az_noaa_weather_data; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE az_noaa_weather_data FROM PUBLIC;
REVOKE ALL ON TABLE az_noaa_weather_data FROM eileen;
GRANT ALL ON TABLE az_noaa_weather_data TO eileen;
GRANT ALL ON TABLE az_noaa_weather_data TO sepgroup;
GRANT SELECT ON TABLE az_noaa_weather_data TO sepgroupreadonly;


--
-- Name: cd_readings_channel_as_columns_by_service_point; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE cd_readings_channel_as_columns_by_service_point FROM PUBLIC;
REVOKE ALL ON TABLE cd_readings_channel_as_columns_by_service_point FROM eileen;
GRANT ALL ON TABLE cd_readings_channel_as_columns_by_service_point TO eileen;
GRANT ALL ON TABLE cd_readings_channel_as_columns_by_service_point TO sepgroup;
GRANT SELECT ON TABLE cd_readings_channel_as_columns_by_service_point TO sepgroupreadonly;


--
-- Name: az_readings_channel_as_columns_by_spid; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE az_readings_channel_as_columns_by_spid FROM PUBLIC;
REVOKE ALL ON TABLE az_readings_channel_as_columns_by_spid FROM eileen;
GRANT ALL ON TABLE az_readings_channel_as_columns_by_spid TO eileen;
GRANT ALL ON TABLE az_readings_channel_as_columns_by_spid TO sepgroup;
GRANT SELECT ON TABLE az_readings_channel_as_columns_by_spid TO sepgroupreadonly;


--
-- Name: readings_channel_as_columns_by_new_spid; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE readings_channel_as_columns_by_new_spid FROM PUBLIC;
REVOKE ALL ON TABLE readings_channel_as_columns_by_new_spid FROM eileen;
GRANT ALL ON TABLE readings_channel_as_columns_by_new_spid TO eileen;
GRANT ALL ON TABLE readings_channel_as_columns_by_new_spid TO sepgroup;
GRANT SELECT ON TABLE readings_channel_as_columns_by_new_spid TO sepgroupreadonly;


--
-- Name: az_readings_channels_as_columns_new_spid; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE az_readings_channels_as_columns_new_spid FROM PUBLIC;
REVOKE ALL ON TABLE az_readings_channels_as_columns_new_spid FROM eileen;
GRANT ALL ON TABLE az_readings_channels_as_columns_new_spid TO eileen;
GRANT ALL ON TABLE az_readings_channels_as_columns_new_spid TO sepgroup;
GRANT SELECT ON TABLE az_readings_channels_as_columns_new_spid TO sepgroupreadonly;


--
-- Name: az_transformer_and_pumping_station; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE az_transformer_and_pumping_station FROM PUBLIC;
REVOKE ALL ON TABLE az_transformer_and_pumping_station FROM dave;
GRANT ALL ON TABLE az_transformer_and_pumping_station TO dave;
GRANT ALL ON TABLE az_transformer_and_pumping_station TO sepgroup;
GRANT SELECT ON TABLE az_transformer_and_pumping_station TO sepgroupreadonly;


--
-- Name: az_transformer_only; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE az_transformer_only FROM PUBLIC;
REVOKE ALL ON TABLE az_transformer_only FROM dave;
GRANT ALL ON TABLE az_transformer_only TO dave;
GRANT ALL ON TABLE az_transformer_only TO sepgroup;
GRANT SELECT ON TABLE az_transformer_only TO sepgroupreadonly;


--
-- Name: cd_20130706-20130711; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE "cd_20130706-20130711" FROM PUBLIC;
REVOKE ALL ON TABLE "cd_20130706-20130711" FROM eileen;
GRANT ALL ON TABLE "cd_20130706-20130711" TO eileen;
GRANT ALL ON TABLE "cd_20130706-20130711" TO sepgroup;
GRANT SELECT ON TABLE "cd_20130706-20130711" TO sepgroupreadonly;


--
-- Name: cd_20130709-20130710; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE "cd_20130709-20130710" FROM PUBLIC;
REVOKE ALL ON TABLE "cd_20130709-20130710" FROM eileen;
GRANT ALL ON TABLE "cd_20130709-20130710" TO eileen;
GRANT ALL ON TABLE "cd_20130709-20130710" TO sepgroup;
GRANT SELECT ON TABLE "cd_20130709-20130710" TO sepgroupreadonly;


--
-- Name: cd_meter_ids_for_houses_with_pv_with_locations; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE cd_meter_ids_for_houses_with_pv_with_locations FROM PUBLIC;
REVOKE ALL ON TABLE cd_meter_ids_for_houses_with_pv_with_locations FROM eileen;
GRANT SELECT,INSERT,REFERENCES,TRIGGER,TRUNCATE ON TABLE cd_meter_ids_for_houses_with_pv_with_locations TO eileen;
GRANT ALL ON TABLE cd_meter_ids_for_houses_with_pv_with_locations TO sepgroup;
GRANT SELECT ON TABLE cd_meter_ids_for_houses_with_pv_with_locations TO sepgroupreadonly;


--
-- Name: cd_energy_voltages_for_houses_with_pv; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE cd_energy_voltages_for_houses_with_pv FROM PUBLIC;
REVOKE ALL ON TABLE cd_energy_voltages_for_houses_with_pv FROM postgres;
GRANT ALL ON TABLE cd_energy_voltages_for_houses_with_pv TO postgres;
GRANT ALL ON TABLE cd_energy_voltages_for_houses_with_pv TO sepgroup;
GRANT SELECT ON TABLE cd_energy_voltages_for_houses_with_pv TO sepgroupreadonly;


--
-- Name: cd_houses_with_pv_no_pv_meter; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE cd_houses_with_pv_no_pv_meter FROM PUBLIC;
REVOKE ALL ON TABLE cd_houses_with_pv_no_pv_meter FROM eileen;
GRANT ALL ON TABLE cd_houses_with_pv_no_pv_meter TO eileen;
GRANT ALL ON TABLE cd_houses_with_pv_no_pv_meter TO sepgroup;
GRANT SELECT ON TABLE cd_houses_with_pv_no_pv_meter TO sepgroupreadonly;


--
-- Name: cd_monthly_summary; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE cd_monthly_summary FROM PUBLIC;
REVOKE ALL ON TABLE cd_monthly_summary FROM eileen;
GRANT ALL ON TABLE cd_monthly_summary TO eileen;
GRANT ALL ON TABLE cd_monthly_summary TO sepgroup;
GRANT SELECT ON TABLE cd_monthly_summary TO sepgroupreadonly;


--
-- Name: count_of_meters_not_in_mlh; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE count_of_meters_not_in_mlh FROM PUBLIC;
REVOKE ALL ON TABLE count_of_meters_not_in_mlh FROM postgres;
GRANT ALL ON TABLE count_of_meters_not_in_mlh TO postgres;
GRANT ALL ON TABLE count_of_meters_not_in_mlh TO sepgroup;
GRANT SELECT ON TABLE count_of_meters_not_in_mlh TO sepgroupreadonly;


--
-- Name: readings_after_uninstall; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE readings_after_uninstall FROM PUBLIC;
REVOKE ALL ON TABLE readings_after_uninstall FROM postgres;
GRANT ALL ON TABLE readings_after_uninstall TO postgres;
GRANT ALL ON TABLE readings_after_uninstall TO sepgroup;
GRANT SELECT ON TABLE readings_after_uninstall TO sepgroupreadonly;


--
-- Name: readings_before_install; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE readings_before_install FROM PUBLIC;
REVOKE ALL ON TABLE readings_before_install FROM postgres;
GRANT ALL ON TABLE readings_before_install TO postgres;
GRANT ALL ON TABLE readings_before_install TO sepgroup;
GRANT SELECT ON TABLE readings_before_install TO sepgroupreadonly;


--
-- Name: count_of_non_mlh_readings; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE count_of_non_mlh_readings FROM PUBLIC;
REVOKE ALL ON TABLE count_of_non_mlh_readings FROM postgres;
GRANT ALL ON TABLE count_of_non_mlh_readings TO postgres;
GRANT ALL ON TABLE count_of_non_mlh_readings TO sepgroup;
GRANT SELECT ON TABLE count_of_non_mlh_readings TO sepgroupreadonly;


--
-- Name: count_of_readings_and_meters_by_day; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE count_of_readings_and_meters_by_day FROM PUBLIC;
REVOKE ALL ON TABLE count_of_readings_and_meters_by_day FROM postgres;
GRANT ALL ON TABLE count_of_readings_and_meters_by_day TO postgres;
GRANT ALL ON TABLE count_of_readings_and_meters_by_day TO sepgroup;
GRANT SELECT ON TABLE count_of_readings_and_meters_by_day TO sepgroupreadonly;


--
-- Name: count_of_register_duplicates; Type: ACL; Schema: public; Owner: daniel
--

REVOKE ALL ON TABLE count_of_register_duplicates FROM PUBLIC;
REVOKE ALL ON TABLE count_of_register_duplicates FROM daniel;
GRANT ALL ON TABLE count_of_register_duplicates TO daniel;
GRANT ALL ON TABLE count_of_register_duplicates TO sepgroup;
GRANT SELECT ON TABLE count_of_register_duplicates TO sepgroupreadonly;


--
-- Name: dates_az_readings_channels_as_columns_new_spid; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE dates_az_readings_channels_as_columns_new_spid FROM PUBLIC;
REVOKE ALL ON TABLE dates_az_readings_channels_as_columns_new_spid FROM eileen;
GRANT ALL ON TABLE dates_az_readings_channels_as_columns_new_spid TO eileen;
GRANT ALL ON TABLE dates_az_readings_channels_as_columns_new_spid TO sepgroup;
GRANT SELECT ON TABLE dates_az_readings_channels_as_columns_new_spid TO sepgroupreadonly;


--
-- Name: dates_egauge_energy_autoload; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE dates_egauge_energy_autoload FROM PUBLIC;
REVOKE ALL ON TABLE dates_egauge_energy_autoload FROM eileen;
GRANT ALL ON TABLE dates_egauge_energy_autoload TO eileen;
GRANT ALL ON TABLE dates_egauge_energy_autoload TO sepgroup;
GRANT SELECT ON TABLE dates_egauge_energy_autoload TO sepgroupreadonly;


--
-- Name: dates_irradiance_data; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE dates_irradiance_data FROM PUBLIC;
REVOKE ALL ON TABLE dates_irradiance_data FROM eileen;
GRANT ALL ON TABLE dates_irradiance_data TO eileen;
GRANT ALL ON TABLE dates_irradiance_data TO sepgroup;
GRANT SELECT ON TABLE dates_irradiance_data TO sepgroupreadonly;


--
-- Name: dates_kihei_scada_temp_hum; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE dates_kihei_scada_temp_hum FROM PUBLIC;
REVOKE ALL ON TABLE dates_kihei_scada_temp_hum FROM eileen;
GRANT ALL ON TABLE dates_kihei_scada_temp_hum TO eileen;
GRANT ALL ON TABLE dates_kihei_scada_temp_hum TO sepgroup;
GRANT SELECT ON TABLE dates_kihei_scada_temp_hum TO sepgroupreadonly;


--
-- Name: dates_meter_read_with_uninstall; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE dates_meter_read_with_uninstall FROM PUBLIC;
REVOKE ALL ON TABLE dates_meter_read_with_uninstall FROM dave;
GRANT ALL ON TABLE dates_meter_read_with_uninstall TO dave;
GRANT ALL ON TABLE dates_meter_read_with_uninstall TO sepgroup;
GRANT SELECT ON TABLE dates_meter_read_with_uninstall TO sepgroupreadonly;


--
-- Name: dates_powermeterevents; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE dates_powermeterevents FROM PUBLIC;
REVOKE ALL ON TABLE dates_powermeterevents FROM eileen;
GRANT ALL ON TABLE dates_powermeterevents TO eileen;
GRANT ALL ON TABLE dates_powermeterevents TO sepgroup;
GRANT SELECT ON TABLE dates_powermeterevents TO sepgroupreadonly;


--
-- Name: dates_tap_data; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE dates_tap_data FROM PUBLIC;
REVOKE ALL ON TABLE dates_tap_data FROM eileen;
GRANT ALL ON TABLE dates_tap_data TO eileen;
GRANT ALL ON TABLE dates_tap_data TO sepgroup;
GRANT SELECT ON TABLE dates_tap_data TO sepgroupreadonly;


--
-- Name: dates_transformer_data; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE dates_transformer_data FROM PUBLIC;
REVOKE ALL ON TABLE dates_transformer_data FROM eileen;
GRANT ALL ON TABLE dates_transformer_data TO eileen;
GRANT ALL ON TABLE dates_transformer_data TO sepgroup;
GRANT SELECT ON TABLE dates_transformer_data TO sepgroupreadonly;


--
-- Name: deprecated_meter_ids_for_houses_without_pv; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE deprecated_meter_ids_for_houses_without_pv FROM PUBLIC;
REVOKE ALL ON TABLE deprecated_meter_ids_for_houses_without_pv FROM postgres;
GRANT ALL ON TABLE deprecated_meter_ids_for_houses_without_pv TO postgres;
GRANT ALL ON TABLE deprecated_meter_ids_for_houses_without_pv TO sepgroup;
GRANT SELECT ON TABLE deprecated_meter_ids_for_houses_without_pv TO sepgroupreadonly;


--
-- Name: z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero FROM PUBLIC;
REVOKE ALL ON TABLE z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero FROM postgres;
GRANT ALL ON TABLE z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO postgres;
GRANT ALL ON TABLE z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO sepgroup;
GRANT SELECT ON TABLE z_dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO sepgroupreadonly;


--
-- Name: dz_count_of_fifteen_min_irradiance_intervals; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_count_of_fifteen_min_irradiance_intervals FROM PUBLIC;
REVOKE ALL ON TABLE dz_count_of_fifteen_min_irradiance_intervals FROM postgres;
GRANT ALL ON TABLE dz_count_of_fifteen_min_irradiance_intervals TO postgres;
GRANT ALL ON TABLE dz_count_of_fifteen_min_irradiance_intervals TO sepgroup;
GRANT SELECT ON TABLE dz_count_of_fifteen_min_irradiance_intervals TO sepgroupreadonly;


--
-- Name: dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero FROM PUBLIC;
REVOKE ALL ON TABLE dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero FROM postgres;
GRANT ALL ON TABLE dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO postgres;
GRANT ALL ON TABLE dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO sepgroup;
GRANT SELECT ON TABLE dz_avg_irradiance_uniform_fifteen_min_intervals_null_as_zero TO sepgroupreadonly;


--
-- Name: dz_energy_voltages_for_houses_without_pv; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_energy_voltages_for_houses_without_pv FROM PUBLIC;
REVOKE ALL ON TABLE dz_energy_voltages_for_houses_without_pv FROM postgres;
GRANT ALL ON TABLE dz_energy_voltages_for_houses_without_pv TO postgres;
GRANT ALL ON TABLE dz_energy_voltages_for_houses_without_pv TO sepgroup;
GRANT SELECT ON TABLE dz_energy_voltages_for_houses_without_pv TO sepgroupreadonly;


--
-- Name: dz_irradiance_fifteen_min_intervals_plus_one_year; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_irradiance_fifteen_min_intervals_plus_one_year FROM PUBLIC;
REVOKE ALL ON TABLE dz_irradiance_fifteen_min_intervals_plus_one_year FROM postgres;
GRANT ALL ON TABLE dz_irradiance_fifteen_min_intervals_plus_one_year TO postgres;
GRANT ALL ON TABLE dz_irradiance_fifteen_min_intervals_plus_one_year TO sepgroup;
GRANT SELECT ON TABLE dz_irradiance_fifteen_min_intervals_plus_one_year TO sepgroupreadonly;


--
-- Name: dz_monthly_energy_summary_double_pv_meter; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_monthly_energy_summary_double_pv_meter FROM PUBLIC;
REVOKE ALL ON TABLE dz_monthly_energy_summary_double_pv_meter FROM postgres;
GRANT ALL ON TABLE dz_monthly_energy_summary_double_pv_meter TO postgres;
GRANT ALL ON TABLE dz_monthly_energy_summary_double_pv_meter TO sepgroup;
GRANT SELECT ON TABLE dz_monthly_energy_summary_double_pv_meter TO sepgroupreadonly;


--
-- Name: dz_monthly_energy_summary_for_nonpv_service_points; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_monthly_energy_summary_for_nonpv_service_points FROM PUBLIC;
REVOKE ALL ON TABLE dz_monthly_energy_summary_for_nonpv_service_points FROM postgres;
GRANT ALL ON TABLE dz_monthly_energy_summary_for_nonpv_service_points TO postgres;
GRANT ALL ON TABLE dz_monthly_energy_summary_for_nonpv_service_points TO sepgroup;
GRANT SELECT ON TABLE dz_monthly_energy_summary_for_nonpv_service_points TO sepgroupreadonly;


--
-- Name: dz_monthly_energy_summary_single_pv_meter; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_monthly_energy_summary_single_pv_meter FROM PUBLIC;
REVOKE ALL ON TABLE dz_monthly_energy_summary_single_pv_meter FROM postgres;
GRANT ALL ON TABLE dz_monthly_energy_summary_single_pv_meter TO postgres;
GRANT ALL ON TABLE dz_monthly_energy_summary_single_pv_meter TO sepgroup;
GRANT SELECT ON TABLE dz_monthly_energy_summary_single_pv_meter TO sepgroupreadonly;


--
-- Name: dz_nonpv_addresses_service_points; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_nonpv_addresses_service_points FROM PUBLIC;
REVOKE ALL ON TABLE dz_nonpv_addresses_service_points FROM postgres;
GRANT ALL ON TABLE dz_nonpv_addresses_service_points TO postgres;
GRANT ALL ON TABLE dz_nonpv_addresses_service_points TO sepgroup;
GRANT SELECT ON TABLE dz_nonpv_addresses_service_points TO sepgroupreadonly;


--
-- Name: nonpv_mlh; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE nonpv_mlh FROM PUBLIC;
REVOKE ALL ON TABLE nonpv_mlh FROM postgres;
GRANT ALL ON TABLE nonpv_mlh TO postgres;
GRANT ALL ON TABLE nonpv_mlh TO sepgroup;
GRANT SELECT ON TABLE nonpv_mlh TO sepgroupreadonly;


--
-- Name: dz_pv_interval_ids; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_pv_interval_ids FROM PUBLIC;
REVOKE ALL ON TABLE dz_pv_interval_ids FROM postgres;
GRANT ALL ON TABLE dz_pv_interval_ids TO postgres;
GRANT ALL ON TABLE dz_pv_interval_ids TO sepgroup;
GRANT SELECT ON TABLE dz_pv_interval_ids TO sepgroupreadonly;


--
-- Name: dz_pv_readings_in_nonpv_mlh; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_pv_readings_in_nonpv_mlh FROM PUBLIC;
REVOKE ALL ON TABLE dz_pv_readings_in_nonpv_mlh FROM postgres;
GRANT ALL ON TABLE dz_pv_readings_in_nonpv_mlh TO postgres;
GRANT ALL ON TABLE dz_pv_readings_in_nonpv_mlh TO sepgroup;
GRANT SELECT ON TABLE dz_pv_readings_in_nonpv_mlh TO sepgroupreadonly;


--
-- Name: dz_summary_pv_readings_in_nonpv_mlh; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE dz_summary_pv_readings_in_nonpv_mlh FROM PUBLIC;
REVOKE ALL ON TABLE dz_summary_pv_readings_in_nonpv_mlh FROM postgres;
GRANT ALL ON TABLE dz_summary_pv_readings_in_nonpv_mlh TO postgres;
GRANT ALL ON TABLE dz_summary_pv_readings_in_nonpv_mlh TO sepgroup;
GRANT SELECT ON TABLE dz_summary_pv_readings_in_nonpv_mlh TO sepgroupreadonly;


--
-- Name: egauge_15min_find_outliers; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE egauge_15min_find_outliers FROM PUBLIC;
REVOKE ALL ON TABLE egauge_15min_find_outliers FROM eileen;
GRANT ALL ON TABLE egauge_15min_find_outliers TO eileen;
GRANT ALL ON TABLE egauge_15min_find_outliers TO sepgroup;
GRANT SELECT ON TABLE egauge_15min_find_outliers TO sepgroupreadonly;


--
-- Name: egauge_energy_15min_with_filter_for_outliers; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE egauge_energy_15min_with_filter_for_outliers FROM PUBLIC;
REVOKE ALL ON TABLE egauge_energy_15min_with_filter_for_outliers FROM sepgroup;
GRANT ALL ON TABLE egauge_energy_15min_with_filter_for_outliers TO sepgroup;
GRANT ALL ON TABLE egauge_energy_15min_with_filter_for_outliers TO eileen;
GRANT SELECT ON TABLE egauge_energy_15min_with_filter_for_outliers TO sepgroupreadonly;


--
-- Name: egauge_energy_autoload_dates; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE egauge_energy_autoload_dates FROM PUBLIC;
REVOKE ALL ON TABLE egauge_energy_autoload_dates FROM postgres;
GRANT ALL ON TABLE egauge_energy_autoload_dates TO postgres;
GRANT ALL ON TABLE egauge_energy_autoload_dates TO sepgroup;
GRANT SELECT ON TABLE egauge_energy_autoload_dates TO sepgroupreadonly;


--
-- Name: egauge_energy_autoload_with_outlier_filter; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE egauge_energy_autoload_with_outlier_filter FROM PUBLIC;
REVOKE ALL ON TABLE egauge_energy_autoload_with_outlier_filter FROM dave;
GRANT ALL ON TABLE egauge_energy_autoload_with_outlier_filter TO dave;
GRANT ALL ON TABLE egauge_energy_autoload_with_outlier_filter TO eileen;
GRANT ALL ON TABLE egauge_energy_autoload_with_outlier_filter TO sepgroup;
GRANT SELECT ON TABLE egauge_energy_autoload_with_outlier_filter TO sepgroupreadonly;


--
-- Name: egauge_view; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE egauge_view FROM PUBLIC;
REVOKE ALL ON TABLE egauge_view FROM sepgroup;
GRANT ALL ON TABLE egauge_view TO sepgroup;
GRANT SELECT ON TABLE egauge_view TO sepgroupreadonly;


--
-- Name: egauge_view_since_aug1; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE egauge_view_since_aug1 FROM PUBLIC;
REVOKE ALL ON TABLE egauge_view_since_aug1 FROM sepgroup;
GRANT ALL ON TABLE egauge_view_since_aug1 TO sepgroup;
GRANT SELECT ON TABLE egauge_view_since_aug1 TO sepgroupreadonly;


--
-- Name: event_data_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE event_data_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE event_data_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE event_data_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE event_data_id_seq TO sepgroupreadonly;


--
-- Name: event_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE event_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE event_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE event_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE event_id_seq TO sepgroupreadonly;


--
-- Name: event_table_view; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE event_table_view FROM PUBLIC;
REVOKE ALL ON TABLE event_table_view FROM eileen;
GRANT ALL ON TABLE event_table_view TO eileen;
GRANT ALL ON TABLE event_table_view TO sepgroup;
GRANT SELECT ON TABLE event_table_view TO sepgroupreadonly;


--
-- Name: interval_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE interval_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE interval_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE interval_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE interval_id_seq TO sepgroupreadonly;


--
-- Name: intervalreaddata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE intervalreaddata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE intervalreaddata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE intervalreaddata_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE intervalreaddata_id_seq TO sepgroupreadonly;


--
-- Name: irradiance_data; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE irradiance_data FROM PUBLIC;
REVOKE ALL ON TABLE irradiance_data FROM eileen;
GRANT ALL ON TABLE irradiance_data TO eileen;
GRANT ALL ON TABLE irradiance_data TO sepgroup;
GRANT SELECT ON TABLE irradiance_data TO sepgroupreadonly;


--
-- Name: locations_with_pv_service_points_ids; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE locations_with_pv_service_points_ids FROM PUBLIC;
REVOKE ALL ON TABLE locations_with_pv_service_points_ids FROM postgres;
GRANT ALL ON TABLE locations_with_pv_service_points_ids TO postgres;
GRANT ALL ON TABLE locations_with_pv_service_points_ids TO sepgroup;
GRANT SELECT ON TABLE locations_with_pv_service_points_ids TO sepgroupreadonly;


--
-- Name: nonpv_mlh_v2; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE nonpv_mlh_v2 FROM PUBLIC;
REVOKE ALL ON TABLE nonpv_mlh_v2 FROM postgres;
GRANT ALL ON TABLE nonpv_mlh_v2 TO postgres;
GRANT ALL ON TABLE nonpv_mlh_v2 TO sepgroup;
GRANT SELECT ON TABLE nonpv_mlh_v2 TO sepgroupreadonly;


--
-- Name: meter_ids_for_service_points_without_pv; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE meter_ids_for_service_points_without_pv FROM PUBLIC;
REVOKE ALL ON TABLE meter_ids_for_service_points_without_pv FROM postgres;
GRANT ALL ON TABLE meter_ids_for_service_points_without_pv TO postgres;
GRANT ALL ON TABLE meter_ids_for_service_points_without_pv TO sepgroup;
GRANT SELECT ON TABLE meter_ids_for_service_points_without_pv TO sepgroupreadonly;


--
-- Name: meterdata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE meterdata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE meterdata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE meterdata_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE meterdata_id_seq TO sepgroupreadonly;


--
-- Name: monthly_energy_summary_all_meters; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE monthly_energy_summary_all_meters FROM PUBLIC;
REVOKE ALL ON TABLE monthly_energy_summary_all_meters FROM eileen;
GRANT ALL ON TABLE monthly_energy_summary_all_meters TO eileen;
GRANT ALL ON TABLE monthly_energy_summary_all_meters TO sepgroup;
GRANT SELECT ON TABLE monthly_energy_summary_all_meters TO sepgroupreadonly;


--
-- Name: readings_by_meter_location_history_old_program; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE readings_by_meter_location_history_old_program FROM PUBLIC;
REVOKE ALL ON TABLE readings_by_meter_location_history_old_program FROM dave;
GRANT ALL ON TABLE readings_by_meter_location_history_old_program TO dave;
GRANT ALL ON TABLE readings_by_meter_location_history_old_program TO sepgroup;
GRANT SELECT ON TABLE readings_by_meter_location_history_old_program TO sepgroupreadonly;


--
-- Name: monthly_energy_summary_double_pv_meter; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE monthly_energy_summary_double_pv_meter FROM PUBLIC;
REVOKE ALL ON TABLE monthly_energy_summary_double_pv_meter FROM dave;
GRANT ALL ON TABLE monthly_energy_summary_double_pv_meter TO dave;
GRANT ALL ON TABLE monthly_energy_summary_double_pv_meter TO sepgroup;
GRANT SELECT ON TABLE monthly_energy_summary_double_pv_meter TO sepgroupreadonly;


--
-- Name: readings_by_meter_location_history_new_program; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE readings_by_meter_location_history_new_program FROM PUBLIC;
REVOKE ALL ON TABLE readings_by_meter_location_history_new_program FROM dave;
GRANT ALL ON TABLE readings_by_meter_location_history_new_program TO dave;
GRANT ALL ON TABLE readings_by_meter_location_history_new_program TO sepgroup;
GRANT SELECT ON TABLE readings_by_meter_location_history_new_program TO sepgroupreadonly;


--
-- Name: monthly_energy_summary_double_pv_meter_program_2; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE monthly_energy_summary_double_pv_meter_program_2 FROM PUBLIC;
REVOKE ALL ON TABLE monthly_energy_summary_double_pv_meter_program_2 FROM dave;
GRANT ALL ON TABLE monthly_energy_summary_double_pv_meter_program_2 TO dave;
GRANT ALL ON TABLE monthly_energy_summary_double_pv_meter_program_2 TO sepgroup;
GRANT SELECT ON TABLE monthly_energy_summary_double_pv_meter_program_2 TO sepgroupreadonly;


--
-- Name: monthly_energy_summary_houses_with_pv; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE monthly_energy_summary_houses_with_pv FROM PUBLIC;
REVOKE ALL ON TABLE monthly_energy_summary_houses_with_pv FROM eileen;
GRANT ALL ON TABLE monthly_energy_summary_houses_with_pv TO eileen;
GRANT ALL ON TABLE monthly_energy_summary_houses_with_pv TO sepgroup;
GRANT SELECT ON TABLE monthly_energy_summary_houses_with_pv TO sepgroupreadonly;


--
-- Name: monthly_energy_summary_single_pv_meter; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE monthly_energy_summary_single_pv_meter FROM PUBLIC;
REVOKE ALL ON TABLE monthly_energy_summary_single_pv_meter FROM dave;
GRANT ALL ON TABLE monthly_energy_summary_single_pv_meter TO dave;
GRANT ALL ON TABLE monthly_energy_summary_single_pv_meter TO sepgroup;
GRANT SELECT ON TABLE monthly_energy_summary_single_pv_meter TO sepgroupreadonly;


--
-- Name: name_address_service_point_id; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE name_address_service_point_id FROM PUBLIC;
REVOKE ALL ON TABLE name_address_service_point_id FROM eileen;
GRANT ALL ON TABLE name_address_service_point_id TO eileen;
GRANT ALL ON TABLE name_address_service_point_id TO sepgroup;
GRANT SELECT ON TABLE name_address_service_point_id TO sepgroupreadonly;


--
-- Name: power_meter_events_with_spid; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE power_meter_events_with_spid FROM PUBLIC;
REVOKE ALL ON TABLE power_meter_events_with_spid FROM dave;
GRANT ALL ON TABLE power_meter_events_with_spid TO dave;
GRANT ALL ON TABLE power_meter_events_with_spid TO sepgroup;
GRANT SELECT ON TABLE power_meter_events_with_spid TO sepgroupreadonly;


--
-- Name: pv_service_points_specifications_view; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE pv_service_points_specifications_view FROM PUBLIC;
REVOKE ALL ON TABLE pv_service_points_specifications_view FROM eileen;
GRANT ALL ON TABLE pv_service_points_specifications_view TO eileen;
GRANT ALL ON TABLE pv_service_points_specifications_view TO sepgroup;
GRANT SELECT ON TABLE pv_service_points_specifications_view TO sepgroupreadonly;


--
-- Name: reading_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE reading_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE reading_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE reading_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE reading_id_seq TO sepgroupreadonly;


--
-- Name: readings_channel_as_columns_by_new_program; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE readings_channel_as_columns_by_new_program FROM PUBLIC;
REVOKE ALL ON TABLE readings_channel_as_columns_by_new_program FROM dave;
GRANT ALL ON TABLE readings_channel_as_columns_by_new_program TO dave;
GRANT ALL ON TABLE readings_channel_as_columns_by_new_program TO sepgroup;
GRANT SELECT ON TABLE readings_channel_as_columns_by_new_program TO sepgroupreadonly;


--
-- Name: readings_channel_as_columns_by_old_program; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE readings_channel_as_columns_by_old_program FROM PUBLIC;
REVOKE ALL ON TABLE readings_channel_as_columns_by_old_program FROM dave;
GRANT ALL ON TABLE readings_channel_as_columns_by_old_program TO dave;
GRANT ALL ON TABLE readings_channel_as_columns_by_old_program TO sepgroup;
GRANT SELECT ON TABLE readings_channel_as_columns_by_old_program TO sepgroupreadonly;


--
-- Name: readings_not_referenced_by_mlh; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE readings_not_referenced_by_mlh FROM PUBLIC;
REVOKE ALL ON TABLE readings_not_referenced_by_mlh FROM dave;
GRANT ALL ON TABLE readings_not_referenced_by_mlh TO dave;
GRANT ALL ON TABLE readings_not_referenced_by_mlh TO sepgroup;
GRANT SELECT ON TABLE readings_not_referenced_by_mlh TO sepgroupreadonly;


--
-- Name: readings_with_pv_service_point_id_new_program; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE readings_with_pv_service_point_id_new_program FROM PUBLIC;
REVOKE ALL ON TABLE readings_with_pv_service_point_id_new_program FROM dave;
GRANT ALL ON TABLE readings_with_pv_service_point_id_new_program TO dave;
GRANT ALL ON TABLE readings_with_pv_service_point_id_new_program TO sepgroup;
GRANT SELECT ON TABLE readings_with_pv_service_point_id_new_program TO sepgroupreadonly;


--
-- Name: readings_with_pv_service_point_id_old_program; Type: ACL; Schema: public; Owner: dave
--

REVOKE ALL ON TABLE readings_with_pv_service_point_id_old_program FROM PUBLIC;
REVOKE ALL ON TABLE readings_with_pv_service_point_id_old_program FROM dave;
GRANT ALL ON TABLE readings_with_pv_service_point_id_old_program TO dave;
GRANT ALL ON TABLE readings_with_pv_service_point_id_old_program TO sepgroup;
GRANT SELECT ON TABLE readings_with_pv_service_point_id_old_program TO sepgroupreadonly;


--
-- Name: register_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE register_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE register_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE register_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE register_id_seq TO sepgroupreadonly;


--
-- Name: registerdata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE registerdata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE registerdata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE registerdata_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE registerdata_id_seq TO sepgroupreadonly;


--
-- Name: registerread_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE registerread_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE registerread_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE registerread_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE registerread_id_seq TO sepgroupreadonly;


--
-- Name: registers; Type: ACL; Schema: public; Owner: daniel
--

REVOKE ALL ON TABLE registers FROM PUBLIC;
REVOKE ALL ON TABLE registers FROM daniel;
GRANT ALL ON TABLE registers TO daniel;
GRANT ALL ON TABLE registers TO sepgroup;
GRANT SELECT ON TABLE registers TO sepgroupreadonly;


--
-- Name: tier_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE tier_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE tier_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE tier_id_seq TO sepgroup;
GRANT SELECT ON SEQUENCE tier_id_seq TO sepgroupreadonly;


--
-- Name: transformer_view_test; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE transformer_view_test FROM PUBLIC;
REVOKE ALL ON TABLE transformer_view_test FROM sepgroup;
GRANT ALL ON TABLE transformer_view_test TO sepgroup;
GRANT SELECT ON TABLE transformer_view_test TO sepgroupreadonly;
GRANT ALL ON TABLE transformer_view_test TO ashkan;


--
-- Name: view_meter_program_changes; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE view_meter_program_changes FROM PUBLIC;
REVOKE ALL ON TABLE view_meter_program_changes FROM eileen;
GRANT ALL ON TABLE view_meter_program_changes TO eileen;
GRANT ALL ON TABLE view_meter_program_changes TO sepgroup;
GRANT SELECT ON TABLE view_meter_program_changes TO sepgroupreadonly;


--
-- PostgreSQL database dump complete
--

