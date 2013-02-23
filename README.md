# Maui Smart Grid Project

Daniel Zhang, Software Developer

## Overview

Provides data operations for the [Maui Smart Grid](http://www.mauismartgrid.com) energy sustainability project for the [Hawaii Natural Energy Institute](http://www.hnei.hawaii.edu). Source data is downloaded in multiple formats including XML, tab-separated values, and comma-separated values.


### Software Features
* Parsing of source data.
* Insertion of data to a data store (PostgreSQL 9.1).

### Open Source Status

This software is being held in a private repository until it is approved for open source release at which time it will be made available under a BSD license.


## Implementation

Code is written using Python 2.7. It has a testing suite implemented through unittest.

The database schema is illustrated in `docs/meco-direct-derived-schema.pdf`.

Data parsing is performed by the ElementTree XML parser. Data store operations are implemented through the psycopg2 PostgreSQL library.

Data processing involves inserting nested sets of data linked by the primary keys, generated as sequential integer values, of the preceding table. Foreign keys are determined by a separate class that holds the last primary key used for each table. The design for this feature is illustrated in `docs/fk-value-determiner.pdf`.

### Database Schema
A SQL dump, produced by pg_dump, of the database schema is provided for reference only.

The schema consists of the following components.

1. Energy data
2. Location Records
3. Meter Records
4. Weather Data (Kahalui Station)

## Configuration

The software is configured through a text configuration file contained in the user's home directory. The file is named `~/meco-data-operations.cfg`. It is read by the ConfigParser module.

### Example Configuration

    [Database]
    db_password=password
    db_host=msg.hawaii.edu
    db_name=msg
    db_port=5432
    db_username=username

## Database Configuration

The database schema can be installed using the following command form where `$DATABASE_NAME` is a valid database.

    $ psql $DATABASE_NAME < meco-data-schema.sql

## Software Operation

### Inserting Data from Source XML

The exported XML data files contain the energy data. Insertion to the database is performed by running

    .\insertData.py
    
in the directory the data files are contained.
    
### Inserting Location and Meter Records

Location and meter records are stored in separate tab-separated files and are inserted using separate scripts.

    insertLocationRecords.py $FILENAME

    insertMeterRecords.py $FILENAME

### Inserting Weather Data (Kahalui Station)

    insertWeatherData.py $FILENAME

### Utility Scripts

`grantAllPermissionsToDatabase.sh $DATABASE`
: Set appropriate permissions to databases.