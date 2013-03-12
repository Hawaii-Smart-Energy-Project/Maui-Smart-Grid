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
-- Name: TestMeterData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "TestMeterData" (
    meter_data_id bigint NOT NULL,
    mac_id character(23) NOT NULL,
    meter_name character(8) NOT NULL,
    util_device_id character(8) NOT NULL
);


ALTER TABLE public."TestMeterData" OWNER TO sepgroup;

--
-- Name: testmeterdata_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE testmeterdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.testmeterdata_id_seq OWNER TO sepgroup;

--
-- Name: testmeterdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE testmeterdata_id_seq OWNED BY "TestMeterData".meter_data_id;


--
-- Name: meter_data_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "TestMeterData" ALTER COLUMN meter_data_id SET DEFAULT nextval('testmeterdata_id_seq'::regclass);


--
-- Name: MeterData_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "TestMeterData"
    ADD CONSTRAINT "MeterData_copy_pkey" PRIMARY KEY (meter_data_id);


--
-- Name: TestMeterData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "TestMeterData" FROM PUBLIC;
REVOKE ALL ON TABLE "TestMeterData" FROM sepgroup;
GRANT ALL ON TABLE "TestMeterData" TO sepgroup;


--
-- Name: testmeterdata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE testmeterdata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE testmeterdata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE testmeterdata_id_seq TO sepgroup;


--
-- PostgreSQL database dump complete
--

