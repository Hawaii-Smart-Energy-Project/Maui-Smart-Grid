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
-- Name: get_voltage_with_meter_id; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW get_voltage_with_meter_id AS
    SELECT get_voltage_with_interval.channel, get_voltage_with_interval.value, get_voltage_with_interval.end_time, "IntervalReadData".start_time, "MeterData".meter_data_id, "MeterData".meter_name, "MeterData".util_device_id, "MeterData".mac_id FROM ((get_voltage_with_interval JOIN "IntervalReadData" ON ((get_voltage_with_interval.interval_read_data_id = "IntervalReadData".interval_read_data_id))) JOIN "MeterData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id)));


ALTER TABLE public.get_voltage_with_meter_id OWNER TO eileen;

--
-- Name: get_voltage_with_meter_id; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE get_voltage_with_meter_id FROM PUBLIC;
REVOKE ALL ON TABLE get_voltage_with_meter_id FROM eileen;
GRANT ALL ON TABLE get_voltage_with_meter_id TO eileen;
GRANT ALL ON TABLE get_voltage_with_meter_id TO sepgroup;


--
-- PostgreSQL database dump complete
--

