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
-- Name: Distinct_Voltage_and_Location; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW "Distinct_Voltage_and_Location" AS
    SELECT DISTINCT "Interval".end_time, "Reading".channel, "MeterData".meter_name, "Reading".value, "Reading".uom, "LocationRecords".service_pt_latitude, "LocationRecords".service_pt_longitude FROM (((("MeterData" JOIN "IntervalReadData" ON (("MeterData".meter_data_id = "IntervalReadData".meter_data_id))) JOIN "Interval" ON (("IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id))) JOIN "Reading" ON (("Interval".interval_id = "Reading".interval_id))) JOIN "LocationRecords" ON (("MeterData".util_device_id = ("LocationRecords".device_util_id)::bpchar))) WHERE ("Reading".channel = 4) ORDER BY "Interval".end_time, "MeterData".meter_name, "Reading".channel;


ALTER TABLE public."Distinct_Voltage_and_Location" OWNER TO eileen;

--
-- Name: Distinct_Voltage_and_Location; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE "Distinct_Voltage_and_Location" FROM PUBLIC;
REVOKE ALL ON TABLE "Distinct_Voltage_and_Location" FROM eileen;
GRANT ALL ON TABLE "Distinct_Voltage_and_Location" TO eileen;
GRANT ALL ON TABLE "Distinct_Voltage_and_Location" TO sepgroup;


--
-- PostgreSQL database dump complete
--

