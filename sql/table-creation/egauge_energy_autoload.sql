-- Create table for the MSG Egauge Service.
--
-- @author Daniel Zhang (張道博)

-- ----------------------------
--  Table structure for EgaugeEnergyAutoload
-- ----------------------------
DROP TABLE IF EXISTS "EgaugeEnergyAutoload";
CREATE TABLE "EgaugeEnergyAutoload" (
	"house_id" int4 NOT NULL,
	"datetime" timestamp(6) NOT NULL,
	"use_kw" float8,
	"gen_kw" float8,
	"grid_kw" float8,
	"ac_kw" float8,
	"fan_kw" float8,
	"dhw_kw" float8,
	"stove_kw" float8,
	"dryer_kw" float8,
	"clotheswasher_kw" float8,
	"dishwasher_kw" float8,
	"solarpump_kw" float8,
	"upload_date" timestamp(6) NULL,
	"microwave_kw" float8,
	"acplus_kw" float8
)
WITH (OIDS=FALSE);
ALTER TABLE "EgaugeEnergyAutoload" OWNER TO "sepgroup";

-- ----------------------------
--  Primary key structure for table EgaugeEnergyAutoload
-- ----------------------------
ALTER TABLE "EgaugeEnergyAutoload" ADD CONSTRAINT "EgaugeEnergyAutoload_pkey" PRIMARY KEY ("house_id", "datetime") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Indexes structure for table EgaugeEnergyAutoload
-- ----------------------------
CREATE INDEX  "idx_primary_key" ON "EgaugeEnergyAutoload" USING btree(house_id ASC NULLS LAST, datetime ASC NULLS LAST);

