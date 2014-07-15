#!/bin/bash

# @DEPRECATED in favor of grantAllPermissionsToDatabases.sh
#
# Grant permissions, to sepgroup and sepgroupreadonly, on a given database using the superuser role.
#
# Usage: grantAllPermissionsToDatabase.sh ${DATABASE_NAME}
#
# @author Daniel Zhang (張道博)

if [ $# -eq 0 ]
  then
    echo "Usage: grantAllPermissionsToDatabase.sh \$DATABASE_NAME";
    exit;
fi

echo "Granting all permissions on database $1...";

sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO sepgroupreadonly;" $1

sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA ep TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA ep TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA ep TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA ep TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA ep TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL SEQUENCES IN SCHEMA ep TO sepgroupreadonly;" $1

sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA dz TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA dz TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA dz TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA dz TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA dz TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL SEQUENCES IN SCHEMA dz TO sepgroupreadonly;" $1

sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA cd TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA cd TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA cd TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA cd TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA cd TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL SEQUENCES IN SCHEMA cd TO sepgroupreadonly;" $1

sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA dw TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA dw TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA dw TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA dw TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA dw TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL SEQUENCES IN SCHEMA dw TO sepgroupreadonly;" $1

sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA az TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA az TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA az TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA az TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA az TO sepgroupreadonly;" $1
sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL SEQUENCES IN SCHEMA az TO sepgroupreadonly;" $1
