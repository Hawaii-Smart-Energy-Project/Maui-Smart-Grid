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
-- Name: MeterData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "MeterData" (
    meter_data_id bigint DEFAULT nextval('testing_meterdata_id_seq'::regclass) NOT NULL,
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
-- Name: meter_data_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "MeterData"
    ADD CONSTRAINT meter_data_pkey PRIMARY KEY (meter_data_id);


--
-- Name: MeterData_meter_data_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "MeterData_meter_data_id_key" ON "MeterData" USING btree (meter_data_id);


--
-- Name: MeterData_meter_name_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "MeterData_meter_name_idx" ON "MeterData" USING btree (meter_name);


--
-- Name: MeterData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "MeterData" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterData" FROM sepgroup;
GRANT ALL ON TABLE "MeterData" TO sepgroup;


--
-- Name: meterdata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE meterdata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE meterdata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE meterdata_id_seq TO sepgroup;


--
-- PostgreSQL database dump complete
--

