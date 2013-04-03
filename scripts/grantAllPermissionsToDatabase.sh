#!/bin/bash

# Grant permissions on a given database using the superuser role.
#
# Usage: grantAllPermissionsToDatabase.sh ${DATABASE_NAME}
#
# @author Daniel Zhang (張道博)

if [ $# -eq 0 ]
  then
    echo "Usage: grantAllPermissionsToDatabase.sh \${DATABASE_NAME}";
    exit;
fi

echo "Granting all permissions on database $1...";

# All tables here includes views:
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO sepgroup;" $1

sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO sepgroup;" $1
sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sepgroup;" $1
