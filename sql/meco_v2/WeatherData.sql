--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: WeatherData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "WeatherData" (
    wban character varying,
    datetime timestamp(6) without time zone,
    station_type smallint,
    sky_condition character varying,
    sky_condition_flag character varying,
    visibility smallint,
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


ALTER TABLE public."WeatherData" OWNER TO sepgroup;

--
-- Name: WeatherData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "WeatherData" FROM PUBLIC;
REVOKE ALL ON TABLE "WeatherData" FROM sepgroup;
GRANT ALL ON TABLE "WeatherData" TO sepgroup;


--
-- PostgreSQL database dump complete
--

