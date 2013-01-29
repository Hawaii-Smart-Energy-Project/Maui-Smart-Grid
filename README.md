# Maui Smart Grid Project

Daniel Zhang, Software Developer

## Overview

Provides data operations for the Maui Smart Grid energy sustainability project. Source data is downloaded in multiple formats including XML, tab-separated values, and comma-separated values.

### Software Features
* Parsing of source data.
* Insertion of data to a data store (PostgreSQL 9.1).

## Implementation

Code is written using Python 2.7. It has a testing suite implemented through unittest.

The database schema is illustrated in `docs/meco-direct-derived-schema.pdf`.

Data parsing is performed by the ElementTree XML parser. Data store operations are implemented through the psycopg2 PostgreSQL library.

Data processing involves inserting nested sets of data linked by the primary keys, generated as sequential integer values, of the preceding table. Foreign keys are determined by a separate class that holds the last primary key used for each table. The design for this feature is illustrated in `docs/fk-value-determiner.pdf`.

### Database Schema
A SQL dump, produced by pg_dump, of the database schema is provided for reference only.

## Configuration

The software is configured through a text configuration file contained in the user's home directory. The file is named `~/meco-data-operations.cfg`. It is read by the ConfigParser module.

### Example Configuration

    [Database]
    db_password=password
    db_host=msg.hawaii.edu
    db_name=msg
    db_port=5432
    db_username=username

## Software Operation

### Inserting Data from Source XML

Data insertion is performed by running

    .\insertData.py



