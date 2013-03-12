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
-- Name: LocationRecords; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "LocationRecords" (
    load_device_type character varying,
    load_action character varying,
    device_util_id character varying NOT NULL,
    device_serial_no character varying,
    device_status character varying,
    device_operational_status character varying,
    install_date timestamp without time zone,
    remove_date timestamp without time zone,
    cust_account_no character varying,
    cust_name character varying,
    service_point_util_id character varying,
    service_type character varying,
    meter_phase character varying,
    cust_billing_cycle character varying,
    location_code character varying,
    voltage_level character varying,
    voltage_phase character varying,
    service_pt_height character varying,
    service_pt_longitude real,
    service_pt_latitude real,
    device_pt_ratio character varying,
    device_ct_ratio character varying,
    premise_util_id character varying,
    premise_type character varying,
    premise_description character varying,
    address1 character varying,
    address2 character varying,
    city character varying,
    cross_street character varying,
    state character(2),
    post_code character varying,
    country character varying,
    timezone character varying,
    region_code character varying,
    map_page_no character varying,
    map_coord character varying,
    longitude real,
    latitude real
);


ALTER TABLE public."LocationRecords" OWNER TO sepgroup;

--
-- Name: LocationRecords_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "LocationRecords"
    ADD CONSTRAINT "LocationRecords_pkey" PRIMARY KEY (device_util_id);


--
-- Name: LocationRecords; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "LocationRecords" FROM PUBLIC;
REVOKE ALL ON TABLE "LocationRecords" FROM sepgroup;
GRANT ALL ON TABLE "LocationRecords" TO sepgroup;


--
-- PostgreSQL database dump complete
--

