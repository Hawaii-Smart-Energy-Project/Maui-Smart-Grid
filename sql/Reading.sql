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
-- Name: Reading; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Reading" (
    interval_id bigint NOT NULL,
    reading_id bigint NOT NULL,
    block_end_value real,
    channel smallint NOT NULL,
    raw_value smallint NOT NULL,
    uom character varying,
    value real
);


ALTER TABLE public."Reading" OWNER TO sepgroup;

--
-- Name: reading_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE reading_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reading_id_seq OWNER TO sepgroup;

--
-- Name: reading_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE reading_id_seq OWNED BY "Reading".reading_id;


--
-- Name: reading_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Reading" ALTER COLUMN reading_id SET DEFAULT nextval('reading_id_seq'::regclass);


--
-- Name: Reading_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Reading"
    ADD CONSTRAINT "Reading_pkey" PRIMARY KEY (reading_id);


--
-- Name: interval_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX interval_id_idx ON "Reading" USING btree (interval_id);


--
-- Name: reading_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX reading_id_idx ON "Reading" USING btree (reading_id);


--
-- Name: Reading_interval_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Reading"
    ADD CONSTRAINT "Reading_interval_id_fkey" FOREIGN KEY (interval_id) REFERENCES "Interval"(interval_id);


--
-- Name: Reading; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Reading" FROM PUBLIC;
REVOKE ALL ON TABLE "Reading" FROM sepgroup;
GRANT ALL ON TABLE "Reading" TO sepgroup;


--
-- Name: reading_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE reading_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE reading_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE reading_id_seq TO sepgroup;


--
-- PostgreSQL database dump complete
--

