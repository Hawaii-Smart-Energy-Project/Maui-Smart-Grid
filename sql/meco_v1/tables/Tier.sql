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
-- Name: Tier; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "Tier" (
    register_read_id bigint NOT NULL,
    tier_id bigint NOT NULL,
    number smallint NOT NULL
);


ALTER TABLE public."Tier" OWNER TO sepgroup;

--
-- Name: tier_id_seq; Type: SEQUENCE; Schema: public; Owner: sepgroup
--

CREATE SEQUENCE tier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tier_id_seq OWNER TO sepgroup;

--
-- Name: tier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sepgroup
--

ALTER SEQUENCE tier_id_seq OWNED BY "Tier".tier_id;


--
-- Name: tier_id; Type: DEFAULT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Tier" ALTER COLUMN tier_id SET DEFAULT nextval('tier_id_seq'::regclass);


--
-- Name: Tier_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "Tier"
    ADD CONSTRAINT "Tier_pkey" PRIMARY KEY (tier_id);


--
-- Name: Tier_register_read_id_idx; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE INDEX "Tier_register_read_id_idx" ON "Tier" USING btree (register_read_id);


--
-- Name: Tier_tier_id_key; Type: INDEX; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE UNIQUE INDEX "Tier_tier_id_key" ON "Tier" USING btree (tier_id);


--
-- Name: Tier_register_read_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sepgroup
--

ALTER TABLE ONLY "Tier"
    ADD CONSTRAINT "Tier_register_read_id_fkey" FOREIGN KEY (register_read_id) REFERENCES "RegisterRead"(register_read_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Tier; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "Tier" FROM PUBLIC;
REVOKE ALL ON TABLE "Tier" FROM sepgroup;
GRANT ALL ON TABLE "Tier" TO sepgroup;


--
-- Name: tier_id_seq; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON SEQUENCE tier_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE tier_id_seq FROM sepgroup;
GRANT ALL ON SEQUENCE tier_id_seq TO sepgroup;


--
-- PostgreSQL database dump complete
--

