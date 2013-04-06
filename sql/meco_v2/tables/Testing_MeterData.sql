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
-- Name: Testing_MeterData; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE "Testing_MeterData" (
    meter_data_id bigint NOT NULL,
    mac_id character(23) NOT NULL,
    meter_name character(8) NOT NULL,
    util_device_id character(8) NOT NULL,
    created timestamp without time zone
);


ALTER TABLE public."Testing_MeterData" OWNER TO daniel;

--
-- Name: MeterData_copy_pkey1; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY "Testing_MeterData"
    ADD CONSTRAINT "MeterData_copy_pkey1" PRIMARY KEY (meter_data_id);


--
-- Name: Testing_MeterData; Type: ACL; Schema: public; Owner: daniel
--

REVOKE ALL ON TABLE "Testing_MeterData" FROM PUBLIC;
REVOKE ALL ON TABLE "Testing_MeterData" FROM daniel;
GRANT ALL ON TABLE "Testing_MeterData" TO daniel;
GRANT ALL ON TABLE "Testing_MeterData" TO sepgroup;


--
-- PostgreSQL database dump complete
--

