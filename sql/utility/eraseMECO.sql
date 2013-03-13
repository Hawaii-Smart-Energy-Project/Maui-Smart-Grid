-- Erase everything in a MECO database using the cascading rules.
-- @author Daniel Zhang (張道博) 

explain analyze delete from "Reading";
explain analyze delete from "Interval";
explain analyze delete from "IntervalReadData";
explain analyze delete from "MeterData";
SELECT setval('interval_id_seq', 1);
SELECT setval('intervalreaddata_id_seq', 1);
SELECT setval('meterdata_id_seq', 1);
SELECT setval('reading_id_seq', 1);
SELECT setval('register_id_seq', 1);
SELECT setval('registerdata_id_seq', 1);
SELECT setval('registerread_id_seq', 1);
SELECT setval('tier_id_seq', 1);
