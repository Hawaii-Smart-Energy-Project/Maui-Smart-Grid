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
-- Name: MeterRecords; Type: TABLE; Schema: public; Owner: sepgroup; Tablespace: 
--

CREATE TABLE "MeterRecords" (
    type character varying,
    action character varying,
    did_sub_type character varying,
    device_util_id character varying NOT NULL,
    device_serial_no character varying,
    device_status character varying,
    device_operational_status character varying,
    device_name character varying,
    device_description character varying,
    device_mfg character varying,
    device_mfg_date timestamp(6) without time zone,
    device_mfg_model character varying,
    device_sw_ver_no character varying,
    device_sw_rev_no character varying,
    device_sw_patch_no character varying,
    device_sw_config character varying,
    device_hw_ver_no character varying,
    device_hw_rev_no character varying,
    device_hw_patch_no character varying,
    device_hw_config character varying,
    meter_form_type character varying,
    meter_base_type character varying,
    max_amp_class character varying,
    rollover_point character varying,
    volt_type character varying,
    nic_mac_address character varying,
    nic_serial_no character varying,
    nic_rf_channel character varying,
    nic_network_identifier character varying,
    nic_model character varying,
    nic_sw_ver_no character varying,
    nic_sw_rev_no character varying,
    nic_sw_patch_no character varying,
    nic_released_date character varying,
    nic_sw_config character varying,
    nic_hw_ver_no character varying,
    nic_hw_rev_no character varying,
    nic_hw_patch_no character varying,
    nic_hw_config character varying,
    master_password character varying,
    reader_password character varying,
    cust_password character varying,
    meter_mode character varying,
    timezone_region character varying,
    battery_mfg_name character varying,
    battery_model_no character varying,
    battery_serial_no character varying,
    battery_mfg_date character varying,
    battery_exp_date character varying,
    battery_installed_date character varying,
    battery_lot_no character varying,
    battery_last_tested_date character varying,
    price_program character varying,
    catalog_number character varying,
    program_seal character varying,
    meter_program_id character varying,
    device_attribute_1 character varying,
    device_attribute_2 character varying,
    device_attribute_3 character varying,
    device_attribute_4 character varying,
    device_attribute_5 character varying,
    nic_attribute_1 character varying,
    nic_attribute_2 character varying,
    nic_attribute_3 character varying,
    nic_attribute_4 character varying,
    nic_attribute_5 character varying
);


ALTER TABLE public."MeterRecords" OWNER TO sepgroup;

--
-- Name: MeterRecords_pkey; Type: CONSTRAINT; Schema: public; Owner: sepgroup; Tablespace: 
--

ALTER TABLE ONLY "MeterRecords"
    ADD CONSTRAINT "MeterRecords_pkey" PRIMARY KEY (device_util_id);


--
-- Name: MeterRecords; Type: ACL; Schema: public; Owner: sepgroup
--

REVOKE ALL ON TABLE "MeterRecords" FROM PUBLIC;
REVOKE ALL ON TABLE "MeterRecords" FROM sepgroup;
GRANT ALL ON TABLE "MeterRecords" TO sepgroup;


--
-- PostgreSQL database dump complete
--

