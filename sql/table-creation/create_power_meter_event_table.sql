-- Create Power Meter Events table.
--
-- @author Daniel Zhang (張道博)

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE "PowerMeterEvents" (
    dtype text,
    id bigint NOT NULL,
    event_category integer,
    el_epoch_num text,
    el_seq_num text,
    event_ack_status text,
    event_text text,
    event_time timestamp without time zone,
    generic_col_1 text,
    generic_col_2 text,
    generic_col_3 text,
    generic_col_4 text,
    generic_col_5 text,
    generic_col_6 text,
    generic_col_7 text,
    generic_col_8 text,
    generic_col_9 text,
    generic_col_10 text,
    insert_ts timestamp without time zone,
    job_id text,
    event_key integer,
    nic_reboot_count text,
    seconds_since_reboot text,
    event_severity text,
    source_id integer,
    update_ts timestamp without time zone,
    updated_by_user text,
    event_ack_note text
);


ALTER TABLE public."PowerMeterEvents" OWNER TO sepgroup;

--
-- Name: PowerMeterEvents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "PowerMeterEvents"
    ADD CONSTRAINT "PowerMeterEvents_pkey" PRIMARY KEY (id);


--
-- Name: PowerMeterEvents; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE "PowerMeterEvents" FROM PUBLIC;
REVOKE ALL ON TABLE "PowerMeterEvents" FROM sepgroup;
GRANT ALL ON TABLE "PowerMeterEvents" TO sepgroup;
GRANT SELECT ON TABLE "PowerMeterEvents" TO sepgroupreadonly;
