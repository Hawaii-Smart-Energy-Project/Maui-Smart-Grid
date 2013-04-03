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
-- Name: meter_locations; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW meter_locations AS
    SELECT "LocationRecords".service_pt_longitude, "LocationRecords".service_pt_latitude, "LocationRecords".device_util_id, "LocationRecords".device_serial_no, "LocationRecords".device_status, "LocationRecords".load_device_type FROM "LocationRecords";


ALTER TABLE public.meter_locations OWNER TO eileen;

--
-- Name: meter_locations; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE meter_locations FROM PUBLIC;
REVOKE ALL ON TABLE meter_locations FROM eileen;
GRANT ALL ON TABLE meter_locations TO eileen;
GRANT ALL ON TABLE meter_locations TO sepgroup;


--
-- PostgreSQL database dump complete
--

