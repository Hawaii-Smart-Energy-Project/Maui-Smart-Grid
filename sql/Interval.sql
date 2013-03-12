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
-- Name: Interval; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Interval" (
    interval_read_data_id bigint NOT NULL,
    interval_id bigint NOT NULL,
    block_sequence_number smallint NOT NULL,
    end_time timestamp without time zone NOT NULL,
    gateway_collected_time timestamp without time zone NOT NULL,
    interval_sequence_number smallint NOT NULL
);


ALTER TABLE public."Interval" OWNER TO sepgroup;

--
-- Name: interval_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE interval_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.interval_id_seq OWNER TO sepgroup;

--
-- Name: interval_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE interval_id_seq OWNED BY "Interval".interval_id;


--
-- Name: interval_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Interval" ALTER COLUMN interval_id SET DEFAULT nextval('interval_id_seq'::regclass);


--
-- Name: Interval_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Interval"
    ADD CONSTRAINT "Interval_pkey" PRIMARY KEY (interval_id);


--
-- Name: Interval_interval_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "Interval_interval_id_key" ON "Interval" USING btree (interval_id);


--
-- Name: interval_read_data_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX interval_read_data_id_idx ON "Interval" USING btree (interval_read_data_id);


--
-- Name: Interval_interval_read_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Interval"
    ADD CONSTRAINT "Interval_interval_read_data_id_fkey" FOREIGN KEY (interval_read_data_id) REFERENCES "IntervalReadData"(interval_read_data_id);


--
-- Name: Interval; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Interval" FROM PUBLIC;
REVOKE ALL ON TABLE "Interval" FROM sepgroup;
GRANT ALL ON TABLE "Interval" TO sepgroup;


--
-- Name: interval_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE interval_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE interval_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE interval_id_seq TO sepgroup;


--
-- PostgreSQL database dump complete
--

