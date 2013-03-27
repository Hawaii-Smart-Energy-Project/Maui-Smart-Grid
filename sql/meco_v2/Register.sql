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
-- Name: Register; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Register" (
    tier_id bigint NOT NULL,
    register_id bigint NOT NULL,
    cumulative_demand real,
    demand_uom character varying,
    number smallint NOT NULL,
    summation real,
    summation_uom character varying
);


ALTER TABLE public."Register" OWNER TO sepgroup;

--
-- Name: register_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE register_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.register_id_seq OWNER TO sepgroup;

--
-- Name: register_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE register_id_seq OWNED BY "Register".register_id;


--
-- Name: register_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Register" ALTER COLUMN register_id SET DEFAULT nextval('register_id_seq'::regclass);


--
-- Name: Register_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Register"
    ADD CONSTRAINT "Register_pkey" PRIMARY KEY (register_id);


--
-- Name: Register_register_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "Register_register_id_idx" ON "Register" USING btree (register_id);


--
-- Name: Register_tier_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "Register_tier_id_idx" ON "Register" USING btree (tier_id);


--
-- Name: Register_register_read_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Register"
    ADD CONSTRAINT "Register_register_read_id_fkey" FOREIGN KEY (tier_id) REFERENCES "Tier"(tier_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Register; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Register" FROM PUBLIC;
REVOKE ALL ON TABLE "Register" FROM sepgroup;
GRANT ALL ON TABLE "Register" TO sepgroup;


--
-- Name: register_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE register_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE register_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE register_id_seq TO sepgroup;


--
-- PostgreSQL database dump complete
--

