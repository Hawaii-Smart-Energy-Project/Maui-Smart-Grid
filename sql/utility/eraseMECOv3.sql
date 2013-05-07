-- Erase everything in a MECO database using the cascading rules.
--
-- @author Daniel Zhang (張道博) 

delete from "Reading";
delete from "Interval";
delete from "IntervalReadData";
delete from "Event";
delete from "EventData";
delete from "MeterData";
ALTER SEQUENCE interval_id_seq RESTART WITH 1;
ALTER SEQUENCE intervalreaddata_id_seq RESTART WITH 1;
ALTER SEQUENCE meterdata_id_seq RESTART WITH 1;
ALTER SEQUENCE reading_id_seq RESTART WITH 1;
ALTER SEQUENCE register_id_seq RESTART WITH 1;
ALTER SEQUENCE registerdata_id_seq RESTART WITH 1;
ALTER SEQUENCE registerread_id_seq RESTART WITH 1;
ALTER SEQUENCE tier_id_seq RESTART WITH 1;
ALTER SEQUENCE event_data_id_seq RESTART WITH 1;
ALTER SEQUENCE event_id_seq RESTART WITH 1;
