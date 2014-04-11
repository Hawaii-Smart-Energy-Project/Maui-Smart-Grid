#!/bin/bash

# Grant permissions, to sepgroup and sepgroupreadonly, for multiple databases using the superuser role.
#
# Usage: grantAllPermissionsToDatabases.sh
#
# @author Daniel Zhang (張道博)

##
# Used for maintenance.
#
function performRevoke {
    sudo -u postgres psql -U postgres -c "REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA $1 FROM sepgroupreadonly;" $2
    sudo -u postgres psql -U postgres -c "REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA $1 FROM sepgroupreadonly;" $2
    sudo -u postgres psql -U postgres -c "REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA $1 FROM sepgroupreadonly;" $2
}

##
# Grant permissions for databases used by sepgroup and sepgroupreadonly.
#
function performGrant {
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA $1 TO sepgroup;" $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA $1 TO sepgroup;" $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA $1 TO sepgroup;" $2
    # performRevoke $1 $2
    sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA $1 TO sepgroupreadonly;" $2
    sudo -u postgres psql -U postgres -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA $1 TO sepgroupreadonly;" $2
    sudo -u postgres psql -U postgres -c "GRANT SELECT ON ALL SEQUENCES IN SCHEMA $1 TO sepgroupreadonly;" $2
}

##
# Grant permissions for databases used by sepgroup_nonmsg.
#
function performGrantNonMSG {
    performRevoke $1 $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA $1 TO sepgroup;" $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA $1 TO sepgroup;" $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA $1 TO sepgroup;" $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL TABLES IN SCHEMA $1 TO sepgroup_nonmsg;" $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA $1 TO sepgroup_nonmsg;" $2
    sudo -u postgres psql -U postgres -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA $1 TO sepgroup_nonmsg;" $2
}

function grant {
    echo "Granting all permissions on database $1...";
    echo "Role $role."
    echo "Granting to scheme $scheme."
    performGrant public $1
}

function grantNonMSG {
    performGrantNonMSG public $1
}

##
# Provide permissions granting for databases with schemes.
#
function grantWithSchemes {
    echo "Granting all permissions on database $1...";
    SCHEMES=(public ep dz cd dw az)
    for scheme in ${SCHEMES[@]}; do
        echo "Granting to scheme $scheme."
        performGrant $scheme $1
    done
}

DATABASES=(natural_ventilation biahouse fcphase3 sinclair uhmcampus kuykendall)

for db in ${DATABASES[@]}; do
    grant $db
done

grantNonMSG weather

grantWithSchemes meco_v3
