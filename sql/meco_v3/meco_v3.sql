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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

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
-- Name: COLUMN "MeterData".created; Type: COMMENT; Schema: public; Owner: sepgroup
--

COMMENT ON COLUMN "MeterData".created IS 'timestamp for when data is inserted';


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
-- Name: Tier; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Tier" (
    register_read_id bigint NOT NULL,
    tier_id bigint NOT NULL,
    number smallint NOT NULL
);


ALTER TABLE public."Tier" OWNER TO sepgroup;

--
-- Name: WeatherKahaluiAirport; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "WeatherKahaluiAirport" (
    wban character varying,
    datetime timestamp(6) without time zone,
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
    record_type character varying,
    record_type_flag character varying,
    hourly_precip character varying,
    hourly_precip_flag character varying,
    altimeter character varying,
    altimeter_flag character varying
);


ALTER TABLE public."WeatherKahaluiAirport" OWNER TO sepgroup;

--
-- Name: view_readings; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW view_readings AS
    SELECT "Interval".end_time, "MeterData".meter_name, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "IntervalReadData".start_time, "IntervalReadData".end_time AS ird_end_time FROM ((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) ORDER BY "Interval".end_time, "MeterData".meter_name, "Reading".channel;


ALTER TABLE public.view_readings OWNER TO postgres;

--
-- Name: VIEW view_readings; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW view_readings IS 'View readings along with their end times.

@author Daniel Zhang (張道博)';


--
-- Name: count_of_readings_and_meters_by_day; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW count_of_readings_and_meters_by_day AS
    SELECT date_trunc('day'::text, view_readings.end_time) AS "Day", count(view_readings.value) AS "Reading Count", count(DISTINCT view_readings.meter_name) AS "Meter Count" FROM view_readings WHERE (view_readings.channel = 1) GROUP BY date_trunc('day'::text, view_readings.end_time) ORDER BY date_trunc('day'::text, view_readings.end_time);


ALTER TABLE public.count_of_readings_and_meters_by_day OWNER TO postgres;

--
-- Name: VIEW count_of_readings_and_meters_by_day; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW count_of_readings_and_meters_by_day IS 'Get counts of readings and meters per day.

@author Daniel Zhang (張道博)';


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
-- Name: get_kwh_meter_locations; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW get_kwh_meter_locations AS
    SELECT "MeterData".meter_name, "MeterData".util_device_id, "MeterData".mac_id, "MeterData".meter_data_id, "Reading".value, "Reading".uom, "Reading".channel, "IntervalReadData".start_time, "IntervalReadData".end_time, "LocationRecords".service_pt_longitude, "LocationRecords".service_pt_latitude, "LocationRecords".service_pt_height, "LocationRecords".device_status FROM (((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) JOIN "LocationRecords" ON ((("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id))) WHERE ("Reading".channel < 4);


ALTER TABLE public.get_kwh_meter_locations OWNER TO postgres;

--
-- Name: get_meter_readings_locations; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW get_meter_readings_locations AS
    SELECT "MeterData".meter_name, "MeterData".util_device_id, "MeterData".mac_id, "MeterData".meter_data_id, "Reading".value, "Reading".uom, "Reading".channel, "LocationRecords".service_pt_longitude, "LocationRecords".service_pt_latitude, "Interval".end_time FROM (((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) JOIN "LocationRecords" ON (((("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id) AND (("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id)))) WHERE ("Reading".channel < 4);


ALTER TABLE public.get_meter_readings_locations OWNER TO postgres;

--
-- Name: get_voltages; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW get_voltages AS
    SELECT "Reading".channel, "Reading".value, "Reading".interval_id, "Reading".reading_id FROM "Reading" WHERE ("Reading".channel = 4);


ALTER TABLE public.get_voltages OWNER TO postgres;

--
-- Name: get_voltage_with_interval; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW get_voltage_with_interval AS
    SELECT get_voltages.channel, get_voltages.value, get_voltages.interval_id, get_voltages.reading_id, "Interval".end_time, "Interval".interval_read_data_id FROM (get_voltages JOIN "Interval" ON (("Interval".interval_id = get_voltages.interval_id)));


ALTER TABLE public.get_voltage_with_interval OWNER TO postgres;

--
-- Name: get_voltage_with_meter_id; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW get_voltage_with_meter_id AS
    SELECT get_voltage_with_interval.channel, get_voltage_with_interval.value, get_voltage_with_interval.end_time, "IntervalReadData".start_time, "MeterData".meter_data_id, "MeterData".meter_name, "MeterData".util_device_id, "MeterData".mac_id FROM ((get_voltage_with_interval JOIN "IntervalReadData" ON ((get_voltage_with_interval.interval_read_data_id = "IntervalReadData".interval_read_data_id))) JOIN "MeterData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id)));


ALTER TABLE public.get_voltage_with_meter_id OWNER TO postgres;

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
-- Name: meter_read_dates; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW meter_read_dates AS
    SELECT "MeterData".util_device_id, min("Interval".end_time) AS earliest_date, max("IntervalReadData".end_time) AS latest_date FROM (("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) GROUP BY "MeterData".util_device_id;


ALTER TABLE public.meter_read_dates OWNER TO eileen;

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
-- Name: new_energy_readings_with_location_address; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW new_energy_readings_with_location_address AS
    SELECT "LocationRecords".service_pt_latitude, "LocationRecords".service_pt_longitude, "LocationRecords".service_pt_height, "LocationRecords".device_util_id, "LocationRecords".device_serial_no, "LocationRecords".device_status, "MeterData".util_device_id, "MeterData".meter_name, "IntervalReadData".end_time, "Reading".channel, "Reading".uom, "Reading".value, "LocationRecords".address1 FROM (((("LocationRecords" JOIN "MeterData" ON (((("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id) AND (("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id)))) JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) WHERE ("Reading".channel < 4);


ALTER TABLE public.new_energy_readings_with_location_address OWNER TO postgres;

--
-- Name: raw_meter_readings; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW raw_meter_readings AS
    SELECT "Interval".end_time, "MeterData".meter_name, "Reading".channel, "Reading".raw_value, "Reading".value, "Reading".uom, "MeterData".util_device_id FROM ((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) ORDER BY "Interval".end_time, "MeterData".meter_name, "Reading".channel;


ALTER TABLE public.raw_meter_readings OWNER TO postgres;

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
-- Name: test_cast_channel; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW test_cast_channel AS
    SELECT "Interval".end_time, "MeterData".meter_name, "Reading".channel, (CASE WHEN ("Reading".channel = (1)::smallint) THEN "Reading".value ELSE NULL::real END)::numeric AS energy_out, (CASE WHEN ("Reading".channel = (2)::smallint) THEN "Reading".value ELSE NULL::real END)::numeric AS energy_from, "Reading".raw_value, "Reading".value, "Reading".uom, "IntervalReadData".start_time, "IntervalReadData".end_time AS ird_end_time FROM ((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) ORDER BY "Interval".end_time, "MeterData".meter_name, "Reading".channel;


ALTER TABLE public.test_cast_channel OWNER TO postgres;

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
-- Name: voltage_locations_highlow_events; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW voltage_locations_highlow_events AS
    SELECT "LocationRecords".service_pt_latitude, "LocationRecords".service_pt_longitude, "LocationRecords".service_pt_height, "LocationRecords".device_serial_no, "LocationRecords".device_status, "MeterData".util_device_id, "MeterData".meter_name, "Reading".channel, "Reading".uom, "Reading".value AS voltage, "LocationRecords".address1, CASE WHEN ("Reading".value > (252)::double precision) THEN 1 ELSE 0 END AS high_event, CASE WHEN ("Reading".value < (228)::double precision) THEN 1 ELSE 0 END AS low_event, "LocationRecords".service_point_util_id, "Interval".end_time FROM (((("LocationRecords" JOIN "MeterData" ON (((("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id) AND (("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id)))) JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) WHERE (("Reading".channel = 4) AND ("Reading".value > (0)::double precision));


ALTER TABLE public.voltage_locations_highlow_events OWNER TO postgres;

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
-- Name: LocationRecords_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "LocationRecords"
    ADD CONSTRAINT "LocationRecords_pkey" PRIMARY KEY (device_util_id);


--
-- Name: MeterRecords_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "MeterRecords"
    ADD CONSTRAINT "MeterRecords_pkey" PRIMARY KEY (device_util_id);


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
-- Name: Reading_channel_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "Reading_channel_idx" ON "Reading" USING btree (channel);


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
-- Name: interval_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX interval_id_idx ON "Reading" USING btree (interval_id);


--
-- Name: interval_read_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX interval_read_data_id_idx ON "Interval" USING btree (interval_read_data_id);


--
-- Name: meter_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX meter_data_id_idx ON "IntervalReadData" USING btree (meter_data_id);


--
-- Name: reading_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX reading_id_idx ON "Reading" USING btree (reading_id);


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
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: Event; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Event" FROM PUBLIC;
REVOKE ALL ON TABLE "Event" FROM sepgroup;
GRANT ALL ON TABLE "Event" TO sepgroup;


--
-- Name: EventData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "EventData" FROM PUBLIC;
REVOKE ALL ON TABLE "EventData" FROM sepgroup;
GRANT ALL ON TABLE "EventData" TO sepgroup;


--
-- Name: Interval; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Interval" FROM PUBLIC;
REVOKE ALL ON TABLE "Interval" FROM sepgroup;
GRANT ALL ON TABLE "Interval" TO sepgroup;


--
-- Name: IntervalReadData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "IntervalReadData" FROM PUBLIC;
REVOKE ALL ON TABLE "IntervalReadData" FROM sepgroup;
GRANT ALL ON TABLE "IntervalReadData" TO sepgroup;


--
-- Name: LocationRecords; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "LocationRecords" FROM PUBLIC;
REVOKE ALL ON TABLE "LocationRecords" FROM sepgroup;
GRANT ALL ON TABLE "LocationRecords" TO sepgroup;


--
-- Name: MeterData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "MeterData" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterData" FROM sepgroup;
GRANT ALL ON TABLE "MeterData" TO sepgroup;


--
-- Name: MeterRecords; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "MeterRecords" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterRecords" FROM sepgroup;
GRANT ALL ON TABLE "MeterRecords" TO sepgroup;


--
-- Name: Reading; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Reading" FROM PUBLIC;
REVOKE ALL ON TABLE "Reading" FROM sepgroup;
GRANT ALL ON TABLE "Reading" TO sepgroup;


--
-- Name: Register; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Register" FROM PUBLIC;
REVOKE ALL ON TABLE "Register" FROM sepgroup;
GRANT ALL ON TABLE "Register" TO sepgroup;


--
-- Name: RegisterData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "RegisterData" FROM PUBLIC;
REVOKE ALL ON TABLE "RegisterData" FROM sepgroup;
GRANT ALL ON TABLE "RegisterData" TO sepgroup;


--
-- Name: RegisterRead; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "RegisterRead" FROM PUBLIC;
REVOKE ALL ON TABLE "RegisterRead" FROM sepgroup;
GRANT ALL ON TABLE "RegisterRead" TO sepgroup;


--
-- Name: Tier; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Tier" FROM PUBLIC;
REVOKE ALL ON TABLE "Tier" FROM sepgroup;
GRANT ALL ON TABLE "Tier" TO sepgroup;


--
-- Name: WeatherKahaluiAirport; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "WeatherKahaluiAirport" FROM PUBLIC;
REVOKE ALL ON TABLE "WeatherKahaluiAirport" FROM sepgroup;
GRANT ALL ON TABLE "WeatherKahaluiAirport" TO sepgroup;


--
-- Name: view_readings; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE view_readings FROM PUBLIC;
REVOKE ALL ON TABLE view_readings FROM postgres;
GRANT ALL ON TABLE view_readings TO postgres;
GRANT ALL ON TABLE view_readings TO sepgroup;


--
-- Name: count_of_readings_and_meters_by_day; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE count_of_readings_and_meters_by_day FROM PUBLIC;
REVOKE ALL ON TABLE count_of_readings_and_meters_by_day FROM postgres;
GRANT ALL ON TABLE count_of_readings_and_meters_by_day TO postgres;
GRANT ALL ON TABLE count_of_readings_and_meters_by_day TO sepgroup;


--
-- Name: event_data_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE event_data_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE event_data_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE event_data_id_seq TO sepgroup;


--
-- Name: event_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE event_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE event_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE event_id_seq TO sepgroup;


--
-- Name: get_kwh_meter_locations; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE get_kwh_meter_locations FROM PUBLIC;
REVOKE ALL ON TABLE get_kwh_meter_locations FROM postgres;
GRANT ALL ON TABLE get_kwh_meter_locations TO postgres;
GRANT ALL ON TABLE get_kwh_meter_locations TO sepgroup;


--
-- Name: get_meter_readings_locations; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE get_meter_readings_locations FROM PUBLIC;
REVOKE ALL ON TABLE get_meter_readings_locations FROM postgres;
GRANT ALL ON TABLE get_meter_readings_locations TO postgres;
GRANT ALL ON TABLE get_meter_readings_locations TO sepgroup;


--
-- Name: get_voltages; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE get_voltages FROM PUBLIC;
REVOKE ALL ON TABLE get_voltages FROM postgres;
GRANT ALL ON TABLE get_voltages TO postgres;
GRANT ALL ON TABLE get_voltages TO sepgroup;


--
-- Name: get_voltage_with_interval; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE get_voltage_with_interval FROM PUBLIC;
REVOKE ALL ON TABLE get_voltage_with_interval FROM postgres;
GRANT ALL ON TABLE get_voltage_with_interval TO postgres;
GRANT ALL ON TABLE get_voltage_with_interval TO sepgroup;


--
-- Name: get_voltage_with_meter_id; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE get_voltage_with_meter_id FROM PUBLIC;
REVOKE ALL ON TABLE get_voltage_with_meter_id FROM postgres;
GRANT ALL ON TABLE get_voltage_with_meter_id TO postgres;
GRANT ALL ON TABLE get_voltage_with_meter_id TO sepgroup;


--
-- Name: interval_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE interval_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE interval_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE interval_id_seq TO sepgroup;


--
-- Name: intervalreaddata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE intervalreaddata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE intervalreaddata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE intervalreaddata_id_seq TO sepgroup;


--
-- Name: meter_read_dates; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE meter_read_dates FROM PUBLIC;
REVOKE ALL ON TABLE meter_read_dates FROM eileen;
GRANT ALL ON TABLE meter_read_dates TO eileen;
GRANT ALL ON TABLE meter_read_dates TO sepgroup;


--
-- Name: meterdata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE meterdata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE meterdata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE meterdata_id_seq TO sepgroup;


--
-- Name: new_energy_readings_with_location_address; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE new_energy_readings_with_location_address FROM PUBLIC;
REVOKE ALL ON TABLE new_energy_readings_with_location_address FROM postgres;
GRANT ALL ON TABLE new_energy_readings_with_location_address TO postgres;
GRANT ALL ON TABLE new_energy_readings_with_location_address TO sepgroup;


--
-- Name: raw_meter_readings; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE raw_meter_readings FROM PUBLIC;
REVOKE ALL ON TABLE raw_meter_readings FROM postgres;
GRANT ALL ON TABLE raw_meter_readings TO postgres;
GRANT ALL ON TABLE raw_meter_readings TO sepgroup;


--
-- Name: reading_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE reading_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE reading_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE reading_id_seq TO sepgroup;


--
-- Name: register_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE register_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE register_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE register_id_seq TO sepgroup;


--
-- Name: registerdata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE registerdata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE registerdata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE registerdata_id_seq TO sepgroup;


--
-- Name: registerread_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE registerread_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE registerread_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE registerread_id_seq TO sepgroup;


--
-- Name: test_cast_channel; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_cast_channel FROM PUBLIC;
REVOKE ALL ON TABLE test_cast_channel FROM postgres;
GRANT ALL ON TABLE test_cast_channel TO postgres;
GRANT ALL ON TABLE test_cast_channel TO sepgroup;


--
-- Name: tier_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE tier_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE tier_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE tier_id_seq TO sepgroup;


--
-- Name: voltage_locations_highlow_events; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE voltage_locations_highlow_events FROM PUBLIC;
REVOKE ALL ON TABLE voltage_locations_highlow_events FROM postgres;
GRANT ALL ON TABLE voltage_locations_highlow_events TO postgres;
GRANT ALL ON TABLE voltage_locations_highlow_events TO sepgroup;


--
-- PostgreSQL database dump complete
--

