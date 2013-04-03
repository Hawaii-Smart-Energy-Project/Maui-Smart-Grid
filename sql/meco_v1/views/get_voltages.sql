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
-- Name: get_voltages; Type: VIEW; Schema: public; Owner: eileen
--

CREATE VIEW get_voltages AS
    SELECT "Reading".channel, "Reading".value, "Reading".interval_id, "Reading".reading_id FROM "Reading" WHERE ("Reading".channel = 4);


ALTER TABLE public.get_voltages OWNER TO eileen;

--
-- Name: get_voltages; Type: ACL; Schema: public; Owner: eileen
--

REVOKE ALL ON TABLE get_voltages FROM PUBLIC;
REVOKE ALL ON TABLE get_voltages FROM eileen;
GRANT ALL ON TABLE get_voltages TO eileen;
GRANT ALL ON TABLE get_voltages TO sepgroup;


--
-- PostgreSQL database dump complete
--

