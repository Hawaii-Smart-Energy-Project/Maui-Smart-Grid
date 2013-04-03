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
-- Name: get_voltage_with_interval; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW get_voltage_with_interval AS
    SELECT get_voltages.channel, get_voltages.value, get_voltages.interval_id, get_voltages.reading_id, "Interval".end_time, "Interval".interval_read_data_id FROM (get_voltages JOIN "Interval" ON (("Interval".interval_id = get_voltages.interval_id)));


ALTER TABLE public.get_voltage_with_interval OWNER TO eileen;

--
-- Name: get_voltage_with_interval; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE get_voltage_with_interval FROM PUBLIC;
REVOKE ALL ON TABLE get_voltage_with_interval FROM eileen;
GRANT ALL ON TABLE get_voltage_with_interval TO eileen;
GRANT ALL ON TABLE get_voltage_with_interval TO sepgroup;


--
-- PostgreSQL database dump complete
--

