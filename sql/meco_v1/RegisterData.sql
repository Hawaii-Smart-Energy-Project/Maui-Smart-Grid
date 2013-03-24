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
-- Name: RegisterData; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "RegisterData" (
    meter_data_id bigint NOT NULL,
    register_data_id bigint NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    number_reads smallint NOT NULL
);


ALTER TABLE public."RegisterData" OWNER TO sepgroup;

--
-- Name: registerdata_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE registerdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.registerdata_id_seq OWNER TO sepgroup;

--
-- Name: registerdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE registerdata_id_seq OWNED BY "RegisterData".register_data_id;


--
-- Name: register_data_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "RegisterData" ALTER COLUMN register_data_id SET DEFAULT nextval('registerdata_id_seq'::regclass);


--
-- Name: RegisterData_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "RegisterData"
    ADD CONSTRAINT "RegisterData_pkey" PRIMARY KEY (register_data_id);


--
-- Name: RegisterData_meter_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "RegisterData_meter_data_id_idx" ON "RegisterData" USING btree (meter_data_id);


--
-- Name: RegisterData_register_data_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "RegisterData_register_data_id_key" ON "RegisterData" USING btree (register_data_id);


--
-- Name: RegisterData_meter_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "RegisterData"
    ADD CONSTRAINT "RegisterData_meter_data_id_fkey" FOREIGN KEY (meter_data_id) REFERENCES "MeterData"(meter_data_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: RegisterData; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "RegisterData" FROM PUBLIC;
REVOKE ALL ON TABLE "RegisterData" FROM sepgroup;
GRANT ALL ON TABLE "RegisterData" TO sepgroup;


--
-- Name: registerdata_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE registerdata_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE registerdata_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE registerdata_id_seq TO sepgroup;


--
-- PostgreSQL database dump complete
--

