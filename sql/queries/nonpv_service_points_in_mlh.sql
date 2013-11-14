-- This is the Meter Location History for nonPV service points.
-- It is the MLH minus those service points that have either a PV meter or
-- a PV meter along with a secondary PV meter.
--
-- @author Daniel Zhang (張道博)

SELECT
    mlh.service_point_id,
    mlh.service_point_height,
    mlh.service_point_latitude,
    mlh.service_point_longitude,
    mlh.notes,
    mlh.longitude,
    mlh.latitude,
    mlh.city,
    mlh.address,
    mlh."location",
    mlh.uninstalled,
    mlh.installed,
    mlh.mac_address,
    mlh.meter_name
FROM
    "MeterLocationHistory" mlh
WHERE
    (
        NOT (
            EXISTS(
                SELECT
                    "PVServicePointIDs".pv_service_point_id
                FROM
                    "PVServicePointIDs"
                WHERE
                    (
                        (
                            (
                                "PVServicePointIDs".pv_service_point_id
                            ) :: TEXT = (
                                            mlh.service_point_id
                                        ) :: TEXT
                        )
                        OR (
                            (
                                "PVServicePointIDs".house_service_point_id
                            ) :: TEXT = (
                                            mlh.service_point_id
                                        ) :: TEXT
                        )
                    )
            )
        )
    )
