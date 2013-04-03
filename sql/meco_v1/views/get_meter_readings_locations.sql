--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Name: get_meter_readings_locations; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW get_meter_readings_locations AS
    SELECT "MeterData".meter_name, "MeterData".util_device_id, "MeterData".mac_id, "MeterData".meter_data_id, "Reading".value, "Reading".uom, "Reading".channel, "LocationRecords".service_pt_longitude, "LocationRecords".service_pt_latitude, "Interval".end_time FROM (((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) JOIN "LocationRecords" ON (((("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id) AND (("LocationRecords".device_util_id)::bpchar = "MeterData".util_device_id)))) WHERE ("Reading".channel < 4);


ALTER TABLE public.get_meter_readings_locations OWNER TO eileen;

--
-- Name: get_meter_readings_locations; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE get_meter_readings_locations FROM PUBLIC;
REVOKE ALL ON TABLE get_meter_readings_locations FROM eileen;
GRANT ALL ON TABLE get_meter_readings_locations TO eileen;
GRANT ALL ON TABLE get_meter_readings_locations TO sepgroup;


--
-- PostgreSQL database dump complete
--

