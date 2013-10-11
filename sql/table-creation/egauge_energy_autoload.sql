-- Create a table for the MSG Egauge Service used for storing autoloaded
-- values.
--
-- @author Daniel Zhang (張道博)

-- ----------------------------
--  Table structure for EgaugeEnergyAutoload
-- ----------------------------
DROP TABLE IF EXISTS "EgaugeEnergyAutoload";
CREATE TABLE "EgaugeEnergyAutoload" (
	"egauge_id" int4 NOT NULL,
	"datetime" timestamp(6) NOT NULL,
	"use_kw" float8,
	"gen_kw" float8,
	"grid_kw" float8,
	"ac_kw" float8,
	"acplus_kw" float8,
	"clotheswasher_kw" float8,
	"clotheswasher_usage_kw" float8,
	"dhw_kw" float8,
	"dishwasher_kw" float8,
	"dryer_kw" float8,
	"dryer_usage_kw" float8,
	"fan_kw" float8,
	"garage_ac_kw" float8,
	"garage_ac_usage_kw" float8,
	"large_ac_kw" float8,
	"large_ac_usage_kw" float8,
	"microwave_kw" float8,
	"oven_kw" float8,
	"oven_usage_kw" float8,
	"range_kw" float8,
	"range_usage_kw" float8,
	"refrigerator_kw" float8,
	"refrigerator_usage_kw" float8,
	"rest_of_house_usage_kw" float8,
	"solarpump_kw" float8,
	"stove_kw" float8,
	"upload_date" timestamp(6) NULL,
	"oven_and_microwave_kw" float8,
	"oven_and_microwave_plus_kw" float8
)
WITH (OIDS=FALSE);
ALTER TABLE "EgaugeEnergyAutoload" OWNER TO "sepgroup";

COMMENT ON TABLE "EgaugeEnergyAutoload" IS 'Data that is autoload by the MSG eGauge Service. @author Daniel Zhang (張道博)';

-- ----------------------------
--  Primary key structure for table EgaugeEnergyAutoload
-- ----------------------------
ALTER TABLE "EgaugeEnergyAutoload" ADD CONSTRAINT "EgaugeEnergyAutoload_pkey" PRIMARY KEY ("egauge_id", "datetime") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Indexes structure for table EgaugeEnergyAutoload
-- ----------------------------
CREATE INDEX  "idx_primary_key" ON "EgaugeEnergyAutoload" USING btree(egauge_id ASC NULLS LAST, datetime ASC NULLS LAST);

